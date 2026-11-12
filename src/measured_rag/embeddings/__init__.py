"""Embeddings package (M1)."""

from .base import Embedder
from .huggingface import HuggingFaceEmbedder

__all__ = ["Embedder", "HuggingFaceEmbedder"]
