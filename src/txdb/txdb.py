import sqlite3
from typing import List, Optional

from biocframe import BiocFrame
from genomicranges import GenomicRanges, SeqInfo
from iranges import IRanges

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class TxDb:
    """Interface for accessing TxDb SQLite databases in Python."""

    def __init__(self, dbpath: str):
        """Initialize the TxDb object.

        Args:
            dbpath:
                Path to the SQLite database file.
        """
        self.dbpath = dbpath
        self.conn = sqlite3.connect(dbpath)
        self.conn.row_factory = sqlite3.Row
        self._seqinfo = None
        self._validate_db()

    def _validate_db(self):
        """Check if the database has the expected schema."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='chrominfo'")
            if cursor.fetchone()[0] == 0:
                raise ValueError(
                    f"Invalid TxDb database at '{self.dbpath}': 'chrominfo' table is missing. "
                    "The file might be corrupted or not a valid TxDb."
                )
        except sqlite3.DatabaseError as e:
            raise ValueError(f"Failed to open database at '{self.dbpath}': {e}") from e

    @property
    def seqinfo(self) -> SeqInfo:
        """Get the sequence information from the database.

        Returns:
            A SeqInfo object representing the chrominfo table.
        """
        if self._seqinfo is None:
            query = "SELECT chrom, length, is_circular FROM chrominfo"
            bf = self._query_as_biocframe(query)

            # TxDb stores is_circular as INTEGER (1/0) or NULL.
            is_circular_col = bf.get_column("is_circular")
            is_circular = [bool(x) if x is not None else False for x in is_circular_col]

            self._seqinfo = SeqInfo(
                seqnames=[str(x) for x in bf.get_column("chrom")],
                seqlengths=[int(x) if x is not None else None for x in bf.get_column("length")],
                is_circular=is_circular,
            )
        return self._seqinfo

    def _query_as_biocframe(self, query: str, params: tuple = ()) -> BiocFrame:
        """Execute a SQL query and return the result as a BiocFrame.

        Args:
            query:
                SQL query string.

            params:
                Parameters for the SQL query.

        Returns:
            BiocFrame containing the query results.
        """
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()

        if not results:
            col_names = [desc[0] for desc in cursor.description]
            return BiocFrame({}, column_names=col_names)

        col_names = [desc[0] for desc in cursor.description]
        columns_data = list(zip(*results))

        data_dict = {}
        for i, name in enumerate(col_names):
            data_dict[name] = list(columns_data[i])

        return BiocFrame(data_dict)

    def _fetch_as_gr(
        self,
        table: str,
        prefix: str,
        columns: Optional[List[str]] = None,
        filter: Optional[dict] = None,
    ) -> GenomicRanges:
        """Internal helper to fetch a table and convert to GenomicRanges.

        Args:
            table:
                Table name (e.g., 'transcript').

            prefix:
                Column prefix (e.g., 'tx' implies 'tx_chrom', 'tx_start').

            columns:
                Specific columns to fetch. If None, fetches all.

            filter:
                Dictionary of filters (e.g. {'tx_chrom': 'chr1'}).

        Returns:
            GenomicRanges object.
        """
        if columns is None:
            cols_str = "*"
        else:
            cols_str = ", ".join(columns)

        query = f"SELECT {cols_str} FROM {table}"

        params = []
        if filter:
            clauses = []
            for k, v in filter.items():
                clauses.append(f"{k} = ?")
                params.append(v)
            query += " WHERE " + " AND ".join(clauses)

        bf = self._query_as_biocframe(query, tuple(params))

        if bf.shape[0] == 0:
            return GenomicRanges.empty()

        chrom_col = f"{prefix}_chrom"
        strand_col = f"{prefix}_strand"
        start_col = f"{prefix}_start"
        end_col = f"{prefix}_end"

        starts = bf.get_column(start_col)
        ends = bf.get_column(end_col)

        # Calculate widths (end - start + 1)
        widths = [e - s + 1 for s, e in zip(starts, ends)]
        ranges = IRanges(start=starts, width=widths)

        raw_strand = bf.get_column(strand_col)
        strand = [s if s is not None else "*" for s in raw_strand]

        seqnames = [str(x) for x in bf.get_column(chrom_col)]

        core_cols = {chrom_col, strand_col, start_col, end_col}
        keep_cols = [c for c in bf.column_names if c not in core_cols]
        mcols = bf[keep_cols]

        return GenomicRanges(
            seqnames=seqnames,
            ranges=ranges,
            strand=strand,
            mcols=mcols,
            seqinfo=self.seqinfo,
        )

    def transcripts(self, filter: Optional[dict] = None) -> GenomicRanges:
        """Retrieve transcripts as a GenomicRanges object.

        Args:
            filter:
                Dictionary of filters (e.g. {'tx_chrom': 'chr1'}).

        Returns:
            GenomicRanges object containing transcripts.
        """
        return self._fetch_as_gr("transcript", "tx", filter=filter)

    def exons(self, filter: Optional[dict] = None) -> GenomicRanges:
        """Retrieve exons as a GenomicRanges object.

        Args:
            filter:
                Dictionary of filters.

        Returns:
            GenomicRanges object containing exons.
        """
        return self._fetch_as_gr("exon", "exon", filter=filter)

    def cds(self, filter: Optional[dict] = None) -> GenomicRanges:
        """Retrieve coding sequences (CDS) as a GenomicRanges object.

        Args:
            filter:
                Dictionary of filters.

        Returns:
            GenomicRanges object containing CDS regions.
        """
        return self._fetch_as_gr("cds", "cds", filter=filter)

    def promoters(self, upstream: int = 2000, downstream: int = 200) -> GenomicRanges:
        """Retrieve promoter regions for transcripts.

        Args:
            upstream:
                Number of bases upstream of TSS. Defaults to 2000.

            downstream:
                Number of bases downstream of TSS. Defaults to 200.

        Returns:
            GenomicRanges object containing promoters.
        """
        tx_gr = self.transcripts()
        return tx_gr.promoters(upstream=upstream, downstream=downstream)

    def genes(self, single_strand_only: bool = True) -> GenomicRanges:
        """Retrieve genes as a GenomicRanges object.

        Aggregates transcripts by gene_id and calculates the genomic range
        (min start to max end) for each gene.

        Args:
            single_strand_only:
                If True, genes spanning multiple chromosomes or strands are dropped.
                Defaults to True.

        Returns:
            GenomicRanges object containing gene extents.
        """
        # join gene and transcript tables.
        base_query = """
        SELECT
            g.gene_id,
            MIN(t.tx_chrom) as chrom,
            MIN(t.tx_strand) as strand,
            MIN(t.tx_start) as start,
            MAX(t.tx_end) as end
        FROM gene g
        JOIN transcript t ON g._tx_id = t._tx_id
        GROUP BY g.gene_id
        """

        if single_strand_only:
            query = base_query + " HAVING COUNT(DISTINCT t.tx_chrom) = 1 AND COUNT(DISTINCT t.tx_strand) = 1"
        else:
            query = base_query

        bf = self._query_as_biocframe(query)

        if bf.shape[0] == 0:
            return GenomicRanges.empty()

        names = [str(x) for x in bf.get_column("gene_id")]
        starts = bf.get_column("start")
        ends = bf.get_column("end")

        widths = [e - s + 1 for s, e in zip(starts, ends)]

        seqnames = [str(x) for x in bf.get_column("chrom")]
        strand = bf.get_column("strand")

        mcols = BiocFrame({"gene_id": names}, row_names=names)

        return GenomicRanges(
            seqnames=seqnames,
            ranges=IRanges(start=starts, width=widths),
            strand=strand,
            names=names,
            mcols=mcols,
            seqinfo=self.seqinfo,
        )

    def transcripts_by_overlaps(self, query: GenomicRanges) -> GenomicRanges:
        """Retrieve transcripts that overlap with the query ranges.

        Args:
            query:
                Query genomic ranges.

        Returns:
            GenomicRanges object of overlapping transcripts.
        """
        tx = self.transcripts()
        return tx.subset_by_overlaps(query)

    def exons_by_overlaps(self, query: GenomicRanges) -> GenomicRanges:
        """Retrieve exons that overlap with the query ranges.

        Args:
            query:
                Query genomic ranges.

        Returns:
            GenomicRanges object of overlapping exons.
        """
        ex = self.exons()
        return ex.subset_by_overlaps(query)

    def cds_by_overlaps(self, query: GenomicRanges) -> GenomicRanges:
        """Retrieve cds that overlap with the query ranges.

        Args:
            query:
                Query genomic ranges.

        Returns:
            GenomicRanges object of overlapping cds.
        """
        c = self.cds()
        return c.subset_by_overlaps(query)

    def transcript_lengths(
        self,
        with_cds_len: bool = False,
        with_utr5_len: bool = False,
        with_utr3_len: bool = False,
    ) -> BiocFrame:
        """Calculate lengths of transcripts, and optionally CDS and UTRs.

        Args:
            with_cds_len:
                Include CDS length.

            with_utr5_len:
                Include 5' UTR length (Not yet implemented).

            with_utr3_len:
                Include 3' UTR length (Not yet implemented).

        Returns:
            BiocFrame with columns: tx_id, tx_name, gene_id, nexon, tx_len.
        """
        if with_utr5_len or with_utr3_len:
            raise NotImplementedError("UTR length calculation not yet implemented.")

        # Fetch base info (tx_id, tx_name, gene_id) using _tx_id for joining
        base_query = """
        SELECT t._tx_id, t.tx_id, t.tx_name, g.gene_id
        FROM transcript t
        LEFT JOIN gene g ON t._tx_id = g._tx_id
        """
        bf = self._query_as_biocframe(base_query)

        # Calculate transcript length (sum of exon widths)
        len_query = """
        SELECT t._tx_id, SUM(e.exon_end - e.exon_start + 1) as tx_len, COUNT(e.exon_id) as nexon
        FROM transcript t
        JOIN splicing s ON t._tx_id = s._tx_id
        JOIN exon e ON s._exon_id = e._exon_id
        GROUP BY t._tx_id
        """
        len_bf = self._query_as_biocframe(len_query)

        tx_map = {
            row[0]: (row[1], row[2])
            for row in zip(
                len_bf.get_column("_tx_id"),
                len_bf.get_column("tx_len"),
                len_bf.get_column("nexon"),
            )
        }

        internal_ids = bf.get_column("_tx_id")
        tx_lens = []
        nexons = []

        for tid in internal_ids:
            val = tx_map.get(tid, (0, 0))
            tx_lens.append(val[0])
            nexons.append(val[1])

        bf["tx_len"] = tx_lens
        bf["nexon"] = nexons

        if with_cds_len:
            cds_query = """
            SELECT t._tx_id, SUM(c.cds_end - c.cds_start + 1) as cds_len
            FROM transcript t
            JOIN splicing s ON t._tx_id = s._tx_id
            JOIN cds c ON s._cds_id = c._cds_id
            GROUP BY t._tx_id
            """
            cds_bf = self._query_as_biocframe(cds_query)
            cds_map = {row[0]: row[1] for row in zip(cds_bf.get_column("_tx_id"), cds_bf.get_column("cds_len"))}

            cds_lens = [cds_map.get(tid, 0) for tid in internal_ids]
            bf["cds_len"] = cds_lens

        cols_to_keep = [c for c in bf.column_names if c != "_tx_id"]
        return bf[cols_to_keep]

    def close(self):
        """Close the database connection."""
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
