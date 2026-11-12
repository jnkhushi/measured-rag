"""Application settings loaded from environment variables.

M0: minimal, validated settings with CPU-friendly defaults and no secrets in code.
Later milestones may extend with experiment/config-file loading.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    # Environment
    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # Paths
    data_dir: Path = Field(default=Path("./data"), alias="DATA_DIR")
    config_dir: Path = Field(default=Path("./configs"), alias="CONFIG_DIR")
    cache_dir: Path = Field(default=Path("./.cache"), alias="CACHE_DIR")

    # Database
    postgres_host: str = Field(default="localhost", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")
    postgres_db: str = Field(default="measured_rag", alias="POSTGRES_DB")
    postgres_user: str = Field(default="measured_rag", alias="POSTGRES_USER")
    postgres_password: str = Field(default="change_me", alias="POSTGRES_PASSWORD")
    database_url: str | None = Field(default=None, alias="DATABASE_URL")

    # Embeddings (local, CPU-friendly defaults)
    embedding_model: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2", alias="EMBEDDING_MODEL"
    )
    embedding_device: str = Field(default="cpu", alias="EMBEDDING_DEVICE")
    embedding_batch_size: int = Field(default=16, alias="EMBEDDING_BATCH_SIZE", ge=1)
    embedding_normalize: bool = Field(default=True, alias="EMBEDDING_NORMALIZE")
    embedding_cache_enabled: bool = Field(default=True, alias="EMBEDDING_CACHE_ENABLED")

    # LLM provider
    llm_provider: Literal["ollama", "openai_compat"] = Field(
        default="ollama", alias="LLM_PROVIDER"
    )
    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="llama3.2:3b", alias="OLLAMA_MODEL")
    openai_compat_base_url: str | None = Field(default=None, alias="OPENAI_COMPAT_BASE_URL")
    openai_compat_api_key: str | None = Field(default=None, alias="OPENAI_COMPAT_API_KEY")
    openai_compat_model: str | None = Field(default=None, alias="OPENAI_COMPAT_MODEL")

    # Chunking (baseline fixed)
    chunk_size: int = Field(default=500, alias="CHUNK_SIZE", ge=1)
    chunk_overlap: int = Field(default=50, alias="CHUNK_OVERLAP", ge=0)

    # Retrieval
    top_k: int = Field(default=5, alias="TOP_K", ge=1)

    # Generation
    generation_timeout_s: int = Field(default=60, alias="GENERATION_TIMEOUT_S", ge=1)

    # Reproducibility and resource controls
    seed: int = Field(default=42, alias="SEED")
    max_top_n_rerank: int = Field(default=20, alias="MAX_TOP_N_RERANK", ge=1)
    rrf_k: int = Field(default=60, alias="RRF_K", ge=1)

    @property
    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    return AppSettings()
