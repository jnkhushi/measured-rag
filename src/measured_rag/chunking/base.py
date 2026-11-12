"""Chunker interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod

from measured_rag.domain.entities import Chunk, Document


class Chunker(ABC):
    @abstractmethod
    def chunk(self, document: Document) -> list[Chunk]:
        """Split a document into chunks while preserving original text in chunk.text."""
        raise NotImplementedError
