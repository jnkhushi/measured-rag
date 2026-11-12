"""Dense vector retriever (M1)."""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any

from measured_rag.domain.entities import RankedResult
from measured_rag.embeddings.base import Embedder
from measured_rag.indexing.vector_store import PgVectorStore

from .base import Retriever, register_retriever


@dataclass
class DenseVectorRetriever(Retriever):
    embedder: Embedder
    store: PgVectorStore
    strategy_name: str = "dense_vector"

    def retrieve(self, query: str, top_k: int = 5, **kwargs: Any) -> list[RankedResult]:
        start = time.perf_counter()
        query_vector = self.embedder.embed_query(query)
        results = self.store.search(query_vector=query_vector, top_k=top_k)
        latency_ms = (time.perf_counter() - start) * 1000.0
        # attach measured latency to each result metadata for downstream artifact capture
        for r in results:
            r.metadata = {**(r.metadata or {}), "retrieval_latency_ms_total": latency_ms}
        return results


register_retriever("dense_vector", DenseVectorRetriever)
