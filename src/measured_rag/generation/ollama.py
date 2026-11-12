"""Ollama LLM provider (M1, local-first).

Network calls occur only when generate() is invoked. Not used in unit tests.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

from .base import GenerationResult, LLMProvider

if TYPE_CHECKING:
    from measured_rag.config.settings import AppSettings


@dataclass
class OllamaProvider(LLMProvider):
    base_url: str = "http://localhost:11434"
    model: str = "llama3.2:3b"
    timeout_s: float = 60.0

    @classmethod
    def from_settings(cls, settings: AppSettings) -> OllamaProvider:
        return cls(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            timeout_s=float(settings.generation_timeout_s),
        )

    def generate(self, prompt: str, **kwargs: Any) -> GenerationResult:
        import httpx

        url = self.base_url.rstrip("/") + "/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": kwargs.get("temperature", 0.0)},
        }
        start = time.perf_counter()
        with httpx.Client(timeout=self.timeout_s) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
        latency_ms = (time.perf_counter() - start) * 1000.0
        usage = None
        # Ollama may report token counts; record only if present (never estimated)
        prompt_eval = data.get("prompt_eval_count")
        eval_count = data.get("eval_count")
        if prompt_eval is not None or eval_count is not None:
            usage = {
                "prompt_tokens": prompt_eval,
                "completion_tokens": eval_count,
                "total_tokens": (prompt_eval or 0) + (eval_count or 0)
                if prompt_eval is not None and eval_count is not None
                else None,
            }
        return GenerationResult(
            text=data.get("response", ""),
            model=data.get("model", self.model),
            provider="ollama",
            usage=usage,
            latency_ms=latency_ms,
            raw=data if isinstance(data, dict) else {},
        )
