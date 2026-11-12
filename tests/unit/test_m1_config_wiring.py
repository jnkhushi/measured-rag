"""Configuration wiring tests for M1 (mocked; no DB/services/models/downloads)."""

from __future__ import annotations

from typing import Any

from measured_rag.chunking.fixed import FixedSizeChunker
from measured_rag.config.settings import AppSettings, get_settings
from measured_rag.domain.entities import Document, RankedResult
from measured_rag.generation.base import GenerationResult, LLMProvider
from measured_rag.pipeline.query import BaselineRAGPipeline
from measured_rag.retrieval.base import Retriever


class _MockRetriever(Retriever):
    def __init__(self) -> None:
        self.last_query: str | None = None
        self.last_top_k: int | None = None

    def retrieve(self, query: str, top_k: int = 5, **kwargs: Any) -> list[RankedResult]:
        self.last_query = query
        self.last_top_k = top_k
        return [
            RankedResult(chunk_id=f"c{i}", score=1.0 - i * 0.1, rank=i + 1, source="mock")
            for i in range(top_k)
        ]


class _MockGenerator(LLMProvider):
    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        return GenerationResult(
            text="mock answer",
            model="mock-model",
            provider="mock",
            usage=None,
            latency_ms=1.0,
            raw={},
        )


def test_chunker_from_settings_and_validation() -> None:
    get_settings.cache_clear()
    settings = AppSettings(_env_file=None, CHUNK_SIZE="700", CHUNK_OVERLAP="70")
    chunker = FixedSizeChunker.from_settings(settings)
    assert chunker.chunk_size == 700
    assert chunker.chunk_overlap == 70

    doc = Document(id="d1", content="x" * 1500, metadata={})
    chunks = chunker.chunk(doc)
    assert chunks
    assert chunks[0].metadata["chunk_size"] == 700
    assert chunks[0].metadata["chunk_overlap"] == 70

    import pytest

    with pytest.raises(ValueError):
        FixedSizeChunker(chunk_size=100, chunk_overlap=100)


def test_pipeline_uses_default_top_k_and_passes_explicit() -> None:
    retriever = _MockRetriever()
    generator = _MockGenerator()
    pipeline = BaselineRAGPipeline(
        retriever=retriever,
        generator=generator,
        chunk_text_lookup={"c0": "ctx0", "c1": "ctx1", "c2": "ctx2"},
        default_top_k=3,
    )
    artifact = pipeline.run("question?")
    assert retriever.last_top_k == 3
    assert len(artifact.retrieved) == 3
    assert artifact.measurements["top_k"] == 3

    artifact2 = pipeline.run("question?", top_k=2)
    assert retriever.last_top_k == 2
    assert len(artifact2.retrieved) == 2
    assert artifact2.measurements["top_k"] == 2


def test_ollama_provider_from_settings_timeout_without_httpx() -> None:
    # Must not require httpx/network; from_settings should only copy config values.
    import measured_rag.generation.ollama as ollama_mod

    assert "httpx" not in ollama_mod.__dict__
    get_settings.cache_clear()
    settings = AppSettings(
        _env_file=None,
        OLLAMA_BASE_URL="http://example:11434",
        OLLAMA_MODEL="test-model",
        GENERATION_TIMEOUT_S="45",
    )
    provider = ollama_mod.OllamaProvider.from_settings(settings)
    assert provider.base_url == "http://example:11434"
    assert provider.model == "test-model"
    assert provider.timeout_s == 45.0
