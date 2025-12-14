import sqlite3
from unittest.mock import MagicMock, patch

import pytest
from genomicranges import SeqInfo

from txdb import TxDb, TxDbRegistry

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@pytest.fixture
def mock_db_file(tmp_path):
    """Create a temporary SQLite file with minimal schema."""
    db_path = tmp_path / "mock.sqlite"
    conn = sqlite3.connect(db_path)

    conn.execute("CREATE TABLE chrominfo (chrom TEXT, length INTEGER, is_circular INTEGER)")
    conn.execute("INSERT INTO chrominfo VALUES ('chr1', 1000, 0)")

    conn.execute(
        "CREATE TABLE transcript (tx_id INTEGER, tx_name TEXT, tx_chrom TEXT, tx_strand TEXT, tx_start INTEGER, tx_end INTEGER, _tx_id INTEGER)"
    )
    conn.execute("INSERT INTO transcript VALUES (1, 't1', 'chr1', '+', 100, 200, 1)")

    conn.commit()
    conn.close()
    return str(db_path)


@pytest.fixture
def registry(tmp_path):
    """Initialize registry with a temp cache dir."""
    return TxDbRegistry(cache_dir=tmp_path / "cache")


def test_registry_init(registry):
    assert isinstance(registry, TxDbRegistry)
    assert "TxDb.Mmusculus.UCSC.mm10.knownGene" in registry.list_txdb()


# @patch("txdb.txdbregistry.BiocFileCache")
# def test_load_db(mock_bfc_cls, registry, mock_db_file):
#     # Setup Mock BiocFileCache instance
#     mock_bfc = MagicMock()
#     # When .add() is called (simulating download), return a resource with the mock path
#     mock_resource = MagicMock()
#     mock_resource.rpath = mock_db_file
#     mock_resource.get.return_value = mock_db_file
#     mock_bfc.add.return_value = mock_resource

#     # Inject mock into registry
#     registry._bfc = mock_bfc

#     # Test load_db
#     txdb = registry.load_db("TxDb.Mmusculus.UCSC.mm10.knownGene")

#     assert isinstance(txdb, TxDb)
#     assert txdb.dbpath == mock_db_file
#     print(txdb.seqinfo)
#     assert (
#         txdb.seqinfo.__repr__()
#         == SeqInfo(seqnames=["chr1"], seqlengths=[1000], is_circular=[False], genome=[None]).__repr__()
#     )

#     txdb.close()
