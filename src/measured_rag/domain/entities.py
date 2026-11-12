"""Core domain entities (M0 minimal)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SourceProvenance:
    source_url: str
    title: str
    publication_date: str | None = None
    version: str | None = None
    license_or_terms: str | None = None


@dataclass
class Document:
    id: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    provenance: SourceProvenance | None = None


@dataclass
class Chunk:
    id: str
    document_id: str
    text: str
    metadata: dict[str, Any] = field(default_factory=dict)
    # Index-time contextual enrichment (M7): preserved original text always available
    enriched_text: str | None = None


@dataclass
class RankedResult:
    chunk_id: str
    score: float
    rank: int
    source: str = "unknown"
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class Citation:
    chunk_id: str
    valid: bool | None = None
    detail: str | None = None


@dataclass
class Answer:
    text: str
    citations: list[Citation] = field(default_factory=list)
    refused: bool = False
    refusal_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
