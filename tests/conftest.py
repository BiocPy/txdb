"""
Dummy conftest.py for txdb.

If you don't know what this is for, just leave it empty.
Read more about conftest.py under:
- https://docs.pytest.org/en/stable/fixture.html
- https://docs.pytest.org/en/stable/writing_plugins.html
"""

import os
import sqlite3

import pytest

from txdb import TxDb

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@pytest.fixture
def mock_db_path(tmp_path):
    """Create a temporary SQLite file with a standard TxDb schema and sample data."""
    db_path = tmp_path / "mock_txdb.sqlite"
    conn = sqlite3.connect(db_path)

    # 1. chrominfo table
    conn.execute("CREATE TABLE chrominfo (chrom TEXT, length INTEGER, is_circular INTEGER)")
    conn.execute("INSERT INTO chrominfo VALUES ('chr1', 2000, 0)")
    conn.execute("INSERT INTO chrominfo VALUES ('chr2', 2000, 0)")

    # 2. transcript table
    # _tx_id is internal PK, tx_id is user ID (often integer or string)
    conn.execute("""
        CREATE TABLE transcript (
            _tx_id INTEGER PRIMARY KEY,
            tx_id INTEGER,
            tx_name TEXT,
            tx_chrom TEXT,
            tx_strand TEXT,
            tx_start INTEGER,
            tx_end INTEGER
        )
    """)

    # Sample Data:
    # Tx1: gene1, chr1:100-500, +
    # Tx2: gene1, chr1:200-600, + (isoform)
    # Tx3: gene2, chr2:100-200, -
    conn.execute("INSERT INTO transcript VALUES (1, 101, 'tx1', 'chr1', '+', 100, 500)")
    conn.execute("INSERT INTO transcript VALUES (2, 102, 'tx2', 'chr1', '+', 200, 600)")
    conn.execute("INSERT INTO transcript VALUES (3, 201, 'tx3', 'chr2', '-', 100, 200)")

    # 3. exon table
    conn.execute("""
        CREATE TABLE exon (
            _exon_id INTEGER PRIMARY KEY,
            exon_id INTEGER,
            exon_name TEXT,
            exon_chrom TEXT,
            exon_strand TEXT,
            exon_start INTEGER,
            exon_end INTEGER
        )
    """)
    # Exons for Tx1: (100-150), (400-500)
    conn.execute("INSERT INTO exon VALUES (1, 1001, 'ex1', 'chr1', '+', 100, 150)")
    conn.execute("INSERT INTO exon VALUES (2, 1002, 'ex2', 'chr1', '+', 400, 500)")
    # Exons for Tx2: (200-250), (400-500) (shares ex2 roughly) -> distinct exon entry in DB usually?
    # Let's say it shares the physical exon ID 2, but we need mapping in splicing.
    conn.execute("INSERT INTO exon VALUES (3, 1003, 'ex3', 'chr1', '+', 200, 250)")

    # 4. cds table
    conn.execute("""
        CREATE TABLE cds (
            _cds_id INTEGER PRIMARY KEY,
            cds_id INTEGER,
            cds_name TEXT,
            cds_chrom TEXT,
            cds_strand TEXT,
            cds_start INTEGER,
            cds_end INTEGER
        )
    """)
    # CDS for Tx1: (120-150), (400-450)
    conn.execute("INSERT INTO cds VALUES (1, 501, 'cds1', 'chr1', '+', 120, 150)")
    conn.execute("INSERT INTO cds VALUES (2, 502, 'cds2', 'chr1', '+', 400, 450)")

    # 5. splicing table (maps tx to exon and cds)
    conn.execute("""
        CREATE TABLE splicing (
            _tx_id INTEGER,
            exon_rank INTEGER,
            _exon_id INTEGER,
            _cds_id INTEGER
        )
    """)
    # Tx1: Exon 1 (rank 1), CDS 1
    conn.execute("INSERT INTO splicing VALUES (1, 1, 1, 1)")
    # Tx1: Exon 2 (rank 2), CDS 2
    conn.execute("INSERT INTO splicing VALUES (1, 2, 2, 2)")

    # Tx2: Exon 3 (rank 1), No CDS
    conn.execute("INSERT INTO splicing VALUES (2, 1, 3, NULL)")
    # Tx2: Exon 2 (rank 2), No CDS (non-coding isoform example)
    conn.execute("INSERT INTO splicing VALUES (2, 2, 2, NULL)")

    # 6. gene table
    conn.execute("CREATE TABLE gene (gene_id TEXT, _tx_id INTEGER)")
    conn.execute("INSERT INTO gene VALUES ('gene1', 1)")
    conn.execute("INSERT INTO gene VALUES ('gene1', 2)")
    conn.execute("INSERT INTO gene VALUES ('gene2', 3)")

    conn.commit()
    conn.close()
    return str(db_path)


@pytest.fixture
def mock_txdb(mock_db_path):
    """Return an open TxDb instance using the mock database."""
    db = TxDb(mock_db_path)
    yield db
    db.close()
