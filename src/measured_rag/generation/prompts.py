"""Prompt templates for grounded generation (M1 baseline)."""

from __future__ import annotations

from collections.abc import Iterable

from measured_rag.domain.entities import RankedResult


def format_context(results: Iterable[RankedResult], chunk_texts: dict[str, str]) -> str:
    blocks: list[str] = []
    for r in results:
        text = chunk_texts.get(r.chunk_id, "")
        meta = r.metadata or {}
        src = meta.get("source_title") or meta.get("source_url") or r.chunk_id
        blocks.append(
            f"[chunk_id={r.chunk_id} rank={r.rank} score={r.score:.4f} source={src}]\n{text}"
        )
    return "\n\n".join(blocks)


def build_grounded_prompt(question: str, context: str) -> str:
    return (
        "You are a cybersecurity assistant. Answer the question using ONLY the provided context. "
        "If the context is insufficient, say that the answer is not supported by the provided context. "
        "Cite chunk_ids you used in your answer.\n\n"
        f"Question:\n{question}\n\n"
        f"Context:\n{context}\n\n"
        "Answer:"
    )
