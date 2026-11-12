"""Embedder interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod


class Embedder(ABC):
    model_id: str
    dimension: int | None

    @abstractmethod
    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        raise NotImplementedError

    def embed_query(self, text: str) -> list[float]:
        vectors = self.embed_texts([text])
        return vectors[0] if vectors else []
