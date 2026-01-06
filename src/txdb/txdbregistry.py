import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pybiocfilecache import BiocFileCache

from ._ahub import AHUB_METADATA_URL
from .record import TxDbRecord
from .txdb import TxDb

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


class TxDbRegistry:
    """Registry for TxDb resources, populated from AnnotationHub."""

    def __init__(
        self,
        cache_dir: Optional[Union[str, Path]] = None,
        force: bool = False,
    ) -> None:
        """Initialize the TxDB registry.

        Args:
            cache_dir:
                Directory for the BiocFileCache database and cached files.
                If None, defaults to "~/.cache/txdb_bfc".

            force:
                If True, force re-download of the AnnotationHub metadata database.
        """
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "txdb_bfc"

        self._cache_dir = Path(cache_dir)
        self._cache_dir.mkdir(parents=True, exist_ok=True)
        self._bfc = BiocFileCache(self._cache_dir)

        self._registry_map: Dict[str, TxDbRecord] = {}

        self._initialize_registry(force=force)

    def _initialize_registry(self, force: bool = False):
        """Fetch the AnnotationHub metadata and populate the registry."""
        rname = "annotationhub_metadata"

        existing = None
        try:
            existing = self._bfc.get(rname)
        except Exception:
            pass

        if force and existing:
            try:
                self._bfc.remove(rname)
            except Exception:
                pass
            existing = None

        if existing:
            md_resource = existing
        else:
            md_resource = self._bfc.add(rname, AHUB_METADATA_URL, rtype="web")

        md_path = self._get_filepath(md_resource)

        if not md_path or not os.path.exists(md_path):
            if existing and not force:
                return self._initialize_registry(force=True)

            raise RuntimeError("Failed to retrieve AnnotationHub metadata database.")

        conn = sqlite3.connect(md_path)
        try:
            query = """
            SELECT
                r.title,
                r.rdatadateadded,
                lp.location_prefix || rp.rdatapath AS full_rdatapath
            FROM resources r
            LEFT JOIN location_prefixes lp
                ON r.location_prefix_id = lp.id
            LEFT JOIN rdatapaths rp
                ON rp.resource_id = r.id
            WHERE r.title LIKE 'TxDb%.sqlite'
            ORDER BY r.rdatadateadded DESC;
            """
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
        finally:
            conn.close()

        for title, date_added, url in rows:
            if title.endswith(".sqlite"):
                txdb_id = title[:-7]
            else:
                txdb_id = title

            if txdb_id in self._registry_map:
                continue

            entry = {"url": url, "release_date": str(date_added).split(" ")[0] if date_added else None}

            record = TxDbRecord.from_config_entry(txdb_id, entry)
            self._registry_map[txdb_id] = record

    def list_txdb(self) -> list[str]:
        """List all available TxDb IDs.

        Returns:
            A list of valid TxDb ID strings.
        """
        return sorted(list(self._registry_map.keys()))

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
        if txdb_id not in self._registry_map:
            raise KeyError(f"TxDb ID '{txdb_id}' not found in registry.")

        return self._registry_map[txdb_id]

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

        path = self._get_filepath(resource)

        if not path or not os.path.exists(path) or os.path.getsize(path) == 0:
            try:
                self._bfc.remove(key)
            except Exception:
                pass
            raise RuntimeError(f"Download failed for {txdb_id}. File is empty or missing.")

        return path

    def load_db(self, txdb_id: str, force: bool = False) -> TxDb:
        """Load a TxDb object for the given ID.

        If the resource is already downloaded and valid, it returns the local copy
        immediately (unless force=True).

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

    def _get_filepath(self, resource: Any) -> Optional[str]:
        """Helper to extract absolute path from a BiocFileCache resource."""
        if hasattr(resource, "rpath"):
            rel_path = str(resource.rpath)
        elif hasattr(resource, "get"):
            rel_path = str(resource.get("rpath"))
        else:
            return None

        return str(self._cache_dir / rel_path)
