"""Retriever interfaces and registry (M1)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from measured_rag.domain.entities import RankedResult


class Retriever(ABC):
    strategy_name: str = "base"

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5, **kwargs: Any) -> list[RankedResult]:
        raise NotImplementedError


_REGISTRY: dict[str, type[Retriever]] = {}


def register_retriever(name: str, cls: type[Retriever]) -> None:
    _REGISTRY[name] = cls


def get_retriever_class(name: str) -> type[Retriever] | None:
    return _REGISTRY.get(name)
