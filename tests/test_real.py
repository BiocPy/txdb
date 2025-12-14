import pytest

from txdb import TxDb, TxDbRegistry

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


def test_real_txdb_workflow(tmp_path):
    registry = TxDbRegistry(cache_dir=tmp_path / "cache")
    txdb_id = "TxDb.Celegans.UCSC.ce11.ensGene"

    assert txdb_id in registry.list_txdb()

    txdb = registry.load_db(txdb_id, force=True)
    assert isinstance(txdb, TxDb)

    si = txdb.seqinfo
    assert "chrI" in si.get_seqnames()

    tx = txdb.transcripts(filter={"tx_chrom": "chrI"})
    assert len(tx) > 0

    txdb.close()
