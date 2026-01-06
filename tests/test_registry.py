import pytest

from txdb import TxDbRegistry

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@pytest.fixture
def registry(tmp_path):
    """Initialize registry with a temp cache dir."""
    return TxDbRegistry(cache_dir=tmp_path / "cache")


def test_registry_init(registry):
    assert isinstance(registry, TxDbRegistry)
    assert "TxDb.Mmusculus.UCSC.mm10.knownGene" in registry.list_txdb()
