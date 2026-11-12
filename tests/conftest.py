"""Pytest configuration and fixtures (M0)."""

from __future__ import annotations

import pytest


@pytest.fixture
def sample_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("POSTGRES_PASSWORD", "test_password")
    monkeypatch.setenv("SEED", "123")
    monkeypatch.setenv("EMBEDDING_BATCH_SIZE", "8")
