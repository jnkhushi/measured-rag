"""Retrieval package (M1)."""

from .base import Retriever
from .vector import DenseVectorRetriever

__all__ = ["Retriever", "DenseVectorRetriever"]
