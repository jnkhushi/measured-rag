"""Generation package (M1)."""

from .base import GenerationResult, LLMProvider
from .ollama import OllamaProvider

__all__ = ["GenerationResult", "LLMProvider", "OllamaProvider"]
