import os
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pybiocfilecache import BiocFileCache

from ._ahub import TXDB_CONFIG
from .record import TxDbRecord
from .txdb import TxDb

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class TxDbRegistry:
    """Registry for TxDb resources backed by TXDB_CONFIG and a BiocFileCache."""

    def __init__(
        self,
        config: Dict[str, Dict[str, Any]] = TXDB_CONFIG,
        cache_dir: Optional[Union[str, Path]] = None,
    ) -> None:
        """Initialize the TxDB registry.

        Args:
            config:
                TXDB_CONFIG-style mapping:
                    txdb_id -> {"release_date": "YYYY-MM-DD", "url": "..."}

            cache_dir:
                Directory for the BiocFileCache database and cached files.
                If None, defaults to "~/.cache/txdb_bfc".
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "txdb_bfc"

        cache_dir = Path(cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)

        self._bfc = BiocFileCache(cache_dir)
        self._config = config

    def list_txdb(self) -> list[str]:
        """List all available TxDb IDs.

        Returns:
            A list of valid TxDb ID strings.
        """
        return list(self._config.keys())

    def get_record(self, txdb_id: str) -> TxDbRecord:
        """Get the metadata record for a given TxDb ID.

        Args:
            txdb_id:
                The TxDb ID to look up.

        Returns:
            A TxDbRecord object containing metadata.

        Raises:
            KeyError: If the ID is not found in the configuration.
        """
        if txdb_id not in self._config:
            raise KeyError(f"TxDb ID '{txdb_id}' not found in registry.")

        entry = self._config[txdb_id]
        return TxDbRecord.from_config_entry(txdb_id, entry)

    def _get_absolute_path(self, x: str):
        return f"{self._bfc.config.cache_dir}/{x}"

    def download(self, txdb_id: str, force: bool = False) -> str:
        """Download and cache the TxDb file.

        Args:
            txdb_id:
                The TxDb ID to fetch.

            force:
                If True, forces re-download even if already cached.
                Defaults to False.

        Returns:
            Local filesystem path to the cached file.
        """
        record = self.get_record(txdb_id)
        url = record.url
        key = txdb_id

        if force:
            try:
                self._bfc.remove(key)
            except Exception:
                pass

        resource = self._bfc.add(
            key,
            url,
            rtype="web",
            download=True,
        )

        path = self._resource_path(resource)
        if path is None:
            raise RuntimeError(f"Could not resolve local path for resource {key!r}")

        abs_path = self._get_absolute_path(path)

        # Validation: Check if file exists and is not empty
        if not os.path.exists(abs_path) or os.path.getsize(abs_path) == 0:
            try:
                self._bfc.remove(key)
            except Exception:
                pass
            raise RuntimeError(
                f"Download failed for {txdb_id}: File at {abs_path} is empty or missing. "
                "Please check your internet connection or the resource URL."
            )

        return str(abs_path)

    def load_db(self, txdb_id: str, force: bool = False) -> TxDb:
        """Load a TxDb object for the given ID.

        This will download the file if it is not already cached.

        Args:
            txdb_id:
                The ID of the TxDb to load.

            force:
                If True, forces re-download of the database file.

        Returns:
            An initialized TxDb object connected to the cached database.
        """
        path = self.download(txdb_id, force=force)
        return TxDb(path)

    def exists_locally(self, txdb_id: str) -> bool:
        """Check if the file for a given TxDb ID is already present in the cache."""
        try:
            resource = self._bfc.get(txdb_id)
        except Exception:
            return False

        path = self._resource_path(resource)
        return bool(path and os.path.exists(path) and os.path.getsize(path) > 0)

    def local_path(self, txdb_id: str) -> Optional[str]:
        """Return local path if cached, else None."""
        try:
            resource = self._bfc.get(txdb_id)
        except Exception:
            return None

        path = self._resource_path(resource)
        if not path or not os.path.exists(path) or os.path.getsize(path) == 0:
            return None

        return str(path)

    def _resource_path(self, resource: Any) -> Optional[str]:
        """Helper to extract path from a BiocFileCache resource object."""
        if hasattr(resource, "rpath"):
            return str(resource.rpath)

        return str(resource.get("rpath")) if hasattr(resource, "get") else None
