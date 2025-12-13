import pytest
from biocframe import BiocFrame
from genomicranges import GenomicRanges
from iranges import IRanges

from txdb import TxDb

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_txdb_init(mock_txdb):
    assert isinstance(mock_txdb, TxDb)
    assert mock_txdb.conn is not None


def test_seqinfo(mock_txdb):
    si = mock_txdb.seqinfo
    assert si.get_seqnames() == ["chr1", "chr2"]
    assert si.get_seqlengths() == [2000, 2000]
    assert si.get_is_circular() == [False, False]


def test_transcripts(mock_txdb):
    tx = mock_txdb.transcripts()
    assert isinstance(tx, GenomicRanges)
    assert len(tx) == 3
    assert tx.start[0] == 100
    assert tx.mcols.get_column("tx_name")[0] == "tx1"

    tx_chr2 = mock_txdb.transcripts(filter={"tx_chrom": "chr2"})
    assert len(tx_chr2) == 1
    assert tx_chr2.mcols.get_column("tx_name")[0] == "tx3"


def test_exons(mock_txdb):
    ex = mock_txdb.exons()
    assert len(ex) == 3
    widths = sorted(ex.width)
    assert widths == [51, 51, 101]


def test_cds(mock_txdb):
    cds = mock_txdb.cds()
    assert len(cds) == 2
    assert cds.mcols.get_column("cds_name") == ["cds1", "cds2"]


def test_genes(mock_txdb):
    genes = mock_txdb.genes()
    assert len(genes) == 2

    gene_names = list(genes.names)
    g1_idx = gene_names.index("gene1")

    assert genes.start[g1_idx] == 100
    assert genes.end[g1_idx] == 600
    assert genes.mcols.get_column("gene_id")[g1_idx] == "gene1"


def test_promoters(mock_txdb):
    proms = mock_txdb.promoters(upstream=100, downstream=50)
    assert len(proms) == 3
    assert isinstance(proms, GenomicRanges)


def test_transcript_lengths(mock_txdb):
    lens = mock_txdb.transcript_lengths()
    assert isinstance(lens, BiocFrame)
    assert len(lens) == 3

    colnames = list(lens.column_names)
    assert "tx_len" in colnames
    assert "nexon" in colnames

    row_tx1 = None
    tx_names = lens.get_column("tx_name")
    for i, tname in enumerate(tx_names):
        if tname == "tx1":
            row_tx1 = i
            break

    assert lens.get_column("tx_len")[row_tx1] == 152
    assert lens.get_column("nexon")[row_tx1] == 2

    lens_cds = mock_txdb.transcript_lengths(with_cds_len=True)
    assert "cds_len" in list(lens_cds.column_names)
    assert lens_cds.get_column("cds_len")[row_tx1] == 82


def test_overlaps(mock_txdb):
    query = GenomicRanges(seqnames=["chr1"], ranges=IRanges([120], [11]))

    tx_ov = mock_txdb.transcripts_by_overlaps(query)
    assert len(tx_ov) == 1
    assert tx_ov.mcols.get_column("tx_name")[0] == "tx1"
