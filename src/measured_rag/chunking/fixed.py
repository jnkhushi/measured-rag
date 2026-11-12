"""Fixed-size baseline chunker (M1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from measured_rag.domain.entities import Chunk, Document

from .base import Chunker

if TYPE_CHECKING:
    from measured_rag.config.settings import AppSettings


@dataclass
class FixedSizeChunker(Chunker):
    chunk_size: int = 500
    chunk_overlap: int = 50

    @classmethod
    def from_settings(cls, settings: AppSettings) -> FixedSizeChunker:
        return cls(chunk_size=settings.chunk_size, chunk_overlap=settings.chunk_overlap)

    def __post_init__(self) -> None:
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be > 0")
        if self.chunk_overlap < 0:
            raise ValueError("chunk_overlap must be >= 0")
        if self.chunk_overlap >= self.chunk_size:
            raise ValueError("chunk_overlap must be < chunk_size")

    def chunk(self, document: Document) -> list[Chunk]:
        text = document.content or ""
        if not text:
            return []
        step = self.chunk_size - self.chunk_overlap
        chunks: list[Chunk] = []
        start = 0
        index = 0
        n = len(text)
        while start < n:
            end = min(start + self.chunk_size, n)
            chunk_text = text[start:end]
            chunk_id = f"{document.id}::chunk-{index}"
            metadata = {
                **(document.metadata or {}),
                "chunk_index": index,
                "start_char": start,
                "end_char": end,
                "chunk_strategy": "fixed",
                "chunk_size": self.chunk_size,
                "chunk_overlap": self.chunk_overlap,
            }
            if document.provenance:
                metadata.update(
                    {
                        "source_url": document.provenance.source_url,
                        "source_title": document.provenance.title,
                        "publication_date": document.provenance.publication_date,
                        "version": document.provenance.version,
                        "license_or_terms": document.provenance.license_or_terms,
                    }
                )
            chunks.append(
                Chunk(id=chunk_id, document_id=document.id, text=chunk_text, metadata=metadata)
            )
            if end == n:
                break
            start += step
            index += 1
        return chunks
