"""Corpus loading from manifest (M1)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from measured_rag.domain.entities import Document, SourceProvenance


def load_manifest(path: str | Path) -> dict[str, Any]:
    manifest_path = Path(path)
    data = yaml.safe_load(manifest_path.read_text(encoding="utf-8")) or {}
    if "sources" not in data or not isinstance(data["sources"], list):
        raise ValueError("Manifest must contain a 'sources' list")
    return data


def _require_provenance_fields(source: dict[str, Any]) -> None:
    required = ["id", "title", "source_url", "publication_date", "license_or_terms", "local_path"]
    missing = [k for k in required if not source.get(k)]
    if missing:
        raise ValueError(f"Source {source.get('id', '<unknown>')} missing fields: {missing}")


def load_manifest_documents(
    manifest_path: str | Path, base_dir: str | Path | None = None
) -> list[Document]:
    manifest_path = Path(manifest_path)
    base = Path(base_dir) if base_dir else manifest_path.parent.parent.parent
    data = load_manifest(manifest_path)
    documents: list[Document] = []
    for source in data["sources"]:
        _require_provenance_fields(source)
        local_path = Path(source["local_path"])
        if not local_path.is_absolute():
            local_path = base / local_path
        content = local_path.read_text(encoding="utf-8")
        provenance = SourceProvenance(
            source_url=source["source_url"],
            title=source["title"],
            publication_date=str(source.get("publication_date")) if source.get("publication_date") else None,
            version=str(source.get("version")) if source.get("version") else None,
            license_or_terms=source.get("license_or_terms"),
        )
        metadata = {
            "source_id": source["id"],
            "local_path": str(local_path),
            "format": source.get("format", "text"),
            "notes": source.get("notes"),
        }
        documents.append(
            Document(id=source["id"], content=content, metadata=metadata, provenance=provenance)
        )
    return documents
