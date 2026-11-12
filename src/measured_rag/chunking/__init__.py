"""Chunking package (M1)."""

from .base import Chunker
from .fixed import FixedSizeChunker

__all__ = ["Chunker", "FixedSizeChunker"]
