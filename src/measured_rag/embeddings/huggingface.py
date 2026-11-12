"""Local HuggingFace/sentence-transformers embedder (M1).

Model loading is lazy and not performed during module import or unit tests unless
embed_texts/embed_query is called.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .base import Embedder


@dataclass
class HuggingFaceEmbedder(Embedder):
    model_id: str = "sentence-transformers/all-MiniLM-L6-v2"
    device: str = "cpu"
    batch_size: int = 16
    normalize: bool = True
    cache_enabled: bool = True
    dimension: int | None = None
    _model: Any = field(default=None, init=False, repr=False)
    _cache: dict[str, list[float]] = field(default_factory=dict, init=False, repr=False)

    def _load_model(self) -> Any:
        if self._model is None:
            try:
                from sentence_transformers import SentenceTransformer
            except Exception as exc:  # pragma: no cover - depends on optional install/runtime
                raise RuntimeError(
                    "sentence-transformers is required for HuggingFaceEmbedder. "
                    "Install declared M1 dependencies before running embeddings."
                ) from exc
            self._model = SentenceTransformer(self.model_id, device=self.device)
        return self._model

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        model = self._load_model()
        results: list[list[float] | None] = [None] * len(texts)
        to_encode: list[str] = []
        to_index: list[int] = []
        for i, text in enumerate(texts):
            if self.cache_enabled and text in self._cache:
                results[i] = list(self._cache[text])
            else:
                to_encode.append(text)
                to_index.append(i)
        if to_encode:
            embeddings = model.encode(
                to_encode,
                batch_size=self.batch_size,
                normalize_embeddings=self.normalize,
                show_progress_bar=False,
                convert_to_numpy=True,
            )
            for idx, vec in zip(to_index, embeddings, strict=True):
                arr = vec.tolist() if hasattr(vec, "tolist") else list(vec)
                results[idx] = arr
                if self.cache_enabled:
                    self._cache[to_encode[to_index.index(idx)]] = list(arr)
        final = [r for r in results if r is not None]
        if final and self.dimension is None:
            self.dimension = len(final[0])
        return [r if r is not None else [] for r in results]
