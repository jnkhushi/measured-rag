"""M1 ingestion CLI (functional, no DB/services/models/downloads).

Loads manifest, chunks documents with settings-driven FixedSizeChunker, and prints
a deterministic summary. Does not write to the database or external services.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Ingest and chunk corpus from a source manifest.")
    parser.add_argument(
        "--manifest",
        default="data/raw/source_manifest.yaml",
        help="Path to source manifest YAML (default: data/raw/source_manifest.yaml)",
    )
    parser.add_argument(
        "--base-dir",
        default=None,
        help="Base directory for resolving manifest local_path entries (default: project root inferred from manifest)",
    )
    args = parser.parse_args(argv)

    # Lazy/local imports to keep CLI lightweight and avoid unnecessary runtime deps.
    from measured_rag.chunking.fixed import FixedSizeChunker
    from measured_rag.config.settings import get_settings
    from measured_rag.ingestion.loader import load_manifest_documents

    settings = get_settings()
    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found: {manifest_path}", file=sys.stderr)
        return 2

    documents = load_manifest_documents(manifest_path, base_dir=args.base_dir)
    chunker = FixedSizeChunker.from_settings(settings)

    total_chunks = 0
    print(f"manifest: {manifest_path}")
    print(f"documents: {len(documents)}")
    print(f"chunking: fixed chunk_size={chunker.chunk_size} chunk_overlap={chunker.chunk_overlap}")
    for doc in documents:
        chunks = chunker.chunk(doc)
        total_chunks += len(chunks)
        prov = doc.provenance
        src = prov.source_url if prov else "N/A"
        lic = prov.license_or_terms if prov else "N/A"
        title = prov.title if prov else doc.id
        print(
            f"- id={doc.id} title={title!r} chunks={len(chunks)} source_url={src} license_or_terms={lic!r}"
        )
    print(f"total_chunks: {total_chunks}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
