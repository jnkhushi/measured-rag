"""Baseline query pipeline and artifact persistence (M1)."""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from measured_rag.domain.entities import RankedResult
from measured_rag.generation.base import GenerationResult, LLMProvider
from measured_rag.generation.prompts import build_grounded_prompt, format_context
from measured_rag.retrieval.base import Retriever


@dataclass
class RunArtifact:
    run_id: str
    timestamp_utc: str
    experiment_id: str | None
    strategy: str
    question: str
    config: dict[str, Any]
    retrieved: list[dict[str, Any]]
    prompt: str
    answer: str
    answer_metadata: dict[str, Any] = field(default_factory=dict)
    measurements: dict[str, Any] = field(default_factory=dict)


def persist_run_artifact(artifact: RunArtifact, output_dir: str | Path) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{artifact.run_id}.json"
    path.write_text(json.dumps(asdict(artifact), indent=2, ensure_ascii=False), encoding="utf-8")
    return path


@dataclass
class BaselineRAGPipeline:
    retriever: Retriever
    generator: LLMProvider
    chunk_text_lookup: dict[str, str]
    strategy_name: str = "dense_vector"
    experiment_id: str | None = None
    default_top_k: int = 5

    def run(
        self, question: str, top_k: int | None = None, config: dict[str, Any] | None = None
    ) -> RunArtifact:
        run_config = config or {}
        effective_top_k = self.default_top_k if top_k is None else top_k
        t0 = time.perf_counter()
        retrieved = self.retriever.retrieve(question, top_k=effective_top_k)
        retrieval_ms = (time.perf_counter() - t0) * 1000.0

        context = format_context(retrieved, self.chunk_text_lookup)
        prompt = build_grounded_prompt(question, context)
        gen: GenerationResult = self.generator.generate(prompt)
        end_to_end_ms = (time.perf_counter() - t0) * 1000.0

        usage = gen.usage if gen.usage is not None else "N/A"
        artifact = RunArtifact(
            run_id=str(uuid.uuid4()),
            timestamp_utc=datetime.now(UTC).isoformat(),
            experiment_id=self.experiment_id,
            strategy=self.strategy_name,
            question=question,
            config=run_config,
            retrieved=[_ranked_to_dict(r) for r in retrieved],
            prompt=prompt,
            answer=gen.text,
            answer_metadata={
                "provider": gen.provider,
                "model": gen.model,
                "generation_latency_ms": gen.latency_ms,
                "raw_keys": list(gen.raw.keys()) if isinstance(gen.raw, dict) else [],
            },
            measurements={
            "retrieval_latency_ms": retrieval_ms,
            "end_to_end_latency_ms": end_to_end_ms,
            "model_token_usage": usage,  # recorded if available else N/A; never estimated
            "indexing_cost": "N/A (separate indexing run)",
            "top_k": effective_top_k,
        },
        )
        return artifact


def _ranked_to_dict(r: RankedResult) -> dict[str, Any]:
    return {"chunk_id": r.chunk_id, "score": r.score, "rank": r.rank, "source": r.source, "metadata": r.metadata}
