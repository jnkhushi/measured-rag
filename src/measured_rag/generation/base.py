"""LLM provider interfaces (M1)."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class GenerationResult:
    text: str
    model: str | None = None
    provider: str | None = None
    usage: dict[str, Any] | None = None  # N/A if unavailable; never estimated
    latency_ms: float | None = None
    raw: dict[str, Any] = field(default_factory=dict)


class LLMProvider(ABC):
    @abstractmethod
    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        raise NotImplementedError
