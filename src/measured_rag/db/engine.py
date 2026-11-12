"""Database engine and session helpers (M0 skeleton)."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from measured_rag.config.settings import AppSettings, get_settings


def get_engine(settings: AppSettings | None = None) -> Engine:
    s = settings or get_settings()
    return create_engine(s.sqlalchemy_database_url, pool_pre_ping=True, future=True)


def get_session_factory(engine: Engine | None = None) -> sessionmaker[Session]:
    eng = engine or get_engine()
    return sessionmaker(bind=eng, autoflush=False, autocommit=False, future=True)


@contextmanager
def session_scope(settings: AppSettings | None = None) -> Iterator[Session]:
    factory = get_session_factory(get_engine(settings))
    session = factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def check_database_connection(settings: AppSettings | None = None) -> bool:
    """Lightweight connectivity check for M0 (requires reachable Postgres)."""
    engine = get_engine(settings)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return True
