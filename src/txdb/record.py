from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

__author__ = "Jayaram Kancherla"
__copyright__ = "Jayaram Kancherla"
__license__ = "MIT"


@dataclass(frozen=True)
class TxDbRecord:
    """Container for a single TxDb entry."""

    txdb_id: str
    release_date: Optional[date]
    url: str

    organism: Optional[str] = None  # e.g. "Hsapiens"
    source: Optional[str] = None  # e.g. "UCSC", "BioMart"
    build: Optional[str] = None  # e.g. "hg38.knownGene"

    # Parsed from URL path (e.g. .../3.22/TxDb...)
    bioc_version: Optional[str] = None

    @classmethod
    def from_config_entry(cls, txdb_id: str, entry: dict) -> "TxDbRecord":
        """Build a record from a TXDB_CONFIG entry:
        {
            "release_date": "YYYY-MM-DD",  # optional
            "url": "https://..."
        }
        """
        url = entry["url"]

        date_str = entry.get("release_date")
        rel_date: Optional[date]
        if date_str:
            rel_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            rel_date = None

        organism, source, build = _parse_txdb_id(txdb_id)
        bioc_version = _parse_bioc_version(url)

        return cls(
            txdb_id=txdb_id,
            release_date=rel_date,
            url=url,
            organism=organism,
            source=source,
            build=build,
            bioc_version=bioc_version,
        )


def _parse_txdb_id(txdb_id: str):
    """Parse IDs like:
      TxDb.Hsapiens.UCSC.hg38.knownGene.sqlite
      TxDb.Hsapiens.BioMart.igis.sqlite
    into (organism, source, build).
    """
    name = txdb_id
    if name.startswith("TxDb."):
        name = name[len("TxDb.") :]
    if name.endswith(".sqlite"):
        name = name[: -len(".sqlite")]

    parts = name.split(".")
    if len(parts) < 2:
        return None, None, None

    organism = parts[0]
    source = parts[1] if len(parts) >= 2 else None
    build = ".".join(parts[2:]) if len(parts) >= 3 else None
    return organism, source, build


def _parse_bioc_version(url: str) -> Optional[str]:
    """Extract the Bioconductor/AnnotationHub-like version from URL.

    Example:
        .../standard/3.22/TxDb....sqlite -> "3.22"
    """
    parts = url.rstrip("/").split("/")
    if len(parts) < 2:
        return None
    candidate = parts[-2]
    # crude but works for "3.22", "3.4", etc.
    if candidate.replace(".", "").isdigit():
        return candidate
    return None
