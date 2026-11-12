"""pgvector-backed storage and retrieval helpers (M1).

This module defines DB operations; it does not connect or run migrations during import.
Execution requires an approved, running PostgreSQL+pgvector instance.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from sqlalchemy import bindparam, text
from sqlalchemy.engine import Engine

from measured_rag.domain.entities import Chunk, RankedResult


@dataclass
class PgVectorStore:
    engine: Engine
    embedding_model_id: str
    embedding_dimension: int
    index_version: str = "v1"

    def ensure_extension_sql(self) -> str:
        return "CREATE EXTENSION IF NOT EXISTS vector"

    def upsert_source(self, conn: Any, document: Any) -> None:
        prov = document.provenance
        stmt = text(
            """
            INSERT INTO sources (id, title, source_url, publication_date, version, license_or_terms, metadata_json)
            VALUES (:id, :title, :source_url, :publication_date, :version, :license_or_terms, CAST(:metadata_json AS jsonb))
            ON CONFLICT (id) DO UPDATE SET
              title = EXCLUDED.title,
              source_url = EXCLUDED.source_url,
              publication_date = EXCLUDED.publication_date,
              version = EXCLUDED.version,
              license_or_terms = EXCLUDED.license_or_terms,
              metadata_json = EXCLUDED.metadata_json
            """
        )
        conn.execute(
            stmt,
            {
                "id": document.id,
                "title": prov.title if prov else document.metadata.get("title"),
                "source_url": prov.source_url if prov else document.metadata.get("source_url"),
                "publication_date": prov.publication_date if prov else None,
                "version": prov.version if prov else None,
                "license_or_terms": prov.license_or_terms if prov else None,
                "metadata_json": json.dumps(document.metadata or {}),
            },
        )

    def upsert_chunk(self, conn: Any, chunk: Chunk, source_id: str) -> None:
        stmt = text(
            """
            INSERT INTO chunks (id, source_id, document_id, chunk_index, text, enriched_text, metadata_json)
            VALUES (:id, :source_id, :document_id, :chunk_index, :text, :enriched_text, CAST(:metadata_json AS jsonb))
            ON CONFLICT (id) DO UPDATE SET
              source_id = EXCLUDED.source_id,
              document_id = EXCLUDED.document_id,
              chunk_index = EXCLUDED.chunk_index,
              text = EXCLUDED.text,
              enriched_text = EXCLUDED.enriched_text,
              metadata_json = EXCLUDED.metadata_json
            """
        )
        conn.execute(
            stmt,
            {
                "id": chunk.id,
                "source_id": source_id,
                "document_id": chunk.document_id,
                "chunk_index": int(chunk.metadata.get("chunk_index", 0)),
                "text": chunk.text,
                "enriched_text": chunk.enriched_text,
                "metadata_json": json.dumps(chunk.metadata or {}),
            },
        )

    def upsert_embedding(self, conn: Any, chunk_id: str, vector: list[float]) -> None:
        if self.embedding_dimension and len(vector) != self.embedding_dimension:
            raise ValueError(
                f"Embedding dimension mismatch: expected {self.embedding_dimension}, got {len(vector)}"
            )
        stmt = text(
            """
            INSERT INTO chunk_embeddings (chunk_id, embedding, embedding_model_id, embedding_dimension, index_version)
            VALUES (:chunk_id, :embedding, :embedding_model_id, :embedding_dimension, :index_version)
            ON CONFLICT (chunk_id) DO UPDATE SET
              embedding = EXCLUDED.embedding,
              embedding_model_id = EXCLUDED.embedding_model_id,
              embedding_dimension = EXCLUDED.embedding_dimension,
              index_version = EXCLUDED.index_version
            """
        )
        conn.execute(
            stmt,
            {
                "chunk_id": chunk_id,
                "embedding": vector,
                "embedding_model_id": self.embedding_model_id,
                "embedding_dimension": len(vector),
                "index_version": self.index_version,
            },
        )

    def search(self, query_vector: list[float], top_k: int = 5) -> list[RankedResult]:
        # Cosine distance via pgvector <=> operator; score reported as 1 - distance.
        sql = text(
            """
            SELECT c.id AS chunk_id,
                   c.metadata_json AS metadata_json,
                   (1 - (e.embedding <=> :query_embedding)) AS score
            FROM chunk_embeddings e
            JOIN chunks c ON c.id = e.chunk_id
            WHERE e.embedding_model_id = :model_id AND e.index_version = :index_version
            ORDER BY e.embedding <=> :query_embedding
            LIMIT :top_k
            """
        ).bindparams(bindparam("query_embedding"))
        with self.engine.connect() as conn:
            rows = conn.execute(
                sql,
                {
                    "query_embedding": query_vector,
                    "model_id": self.embedding_model_id,
                    "index_version": self.index_version,
                    "top_k": top_k,
                },
            ).mappings().all()
        results: list[RankedResult] = []
        for i, row in enumerate(rows, start=1):
            meta = row.get("metadata_json") or {}
            if isinstance(meta, str):
                meta = json.loads(meta)
            results.append(
                RankedResult(
                    chunk_id=row["chunk_id"],
                    score=float(row["score"]),
                    rank=i,
                    source="dense_vector",
                    metadata=meta,
                )
            )
        return results
