"""Corpus ingestion: build a checksummed manifest of raw message files.

Raw email is untrusted text: files are read as bytes and hashed, never executed.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ManifestEntry:
    rel_path: str
    custodian: str
    folder: str
    size: int
    sha256: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def iter_manifest(root: Path) -> Iterator[ManifestEntry]:
    """Yield one entry per file under ``root/<custodian>/<folder...>/<file>``, sorted."""
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = path.relative_to(root)
        parts = rel.parts
        if len(parts) < 2:
            continue  # files directly under root have no custodian
        data = path.read_bytes()
        yield ManifestEntry(
            rel_path=rel.as_posix(),
            custodian=parts[0],
            folder="/".join(parts[1:-1]),
            size=len(data),
            sha256=sha256_bytes(data),
        )


def manifest_hash(entries: list[ManifestEntry]) -> str:
    """Single hash over the whole manifest, for recording the data version."""
    digest = hashlib.sha256()
    for e in sorted(entries, key=lambda e: e.rel_path):
        digest.update(f"{e.rel_path}\0{e.sha256}\n".encode())
    return digest.hexdigest()
