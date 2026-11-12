"""ORM models placeholder (M0).

Actual tables (documents, chunks, embeddings, runs, eval results, provenance)
will be introduced incrementally with Alembic migrations in later milestones.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
