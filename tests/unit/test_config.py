from measured_rag.config.settings import AppSettings, get_settings


def test_settings_defaults_cpu_friendly(sample_env: None) -> None:
    get_settings.cache_clear()
    settings = AppSettings()
    assert settings.embedding_device == "cpu"
    assert settings.embedding_batch_size == 8  # from fixture
    assert settings.seed == 123
    assert settings.llm_provider == "ollama"


def test_sqlalchemy_database_url_builds_from_parts(sample_env: None) -> None:
    get_settings.cache_clear()
    settings = AppSettings()
    url = settings.sqlalchemy_database_url
    assert url.startswith("postgresql+psycopg://")
    assert "measured_rag" in url
    assert "5432" in url


def test_database_url_override(sample_env: None, monkeypatch) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://u:p@db:5432/other")
    get_settings.cache_clear()
    settings = AppSettings()
    assert settings.sqlalchemy_database_url == "postgresql+psycopg://u:p@db:5432/other"
