# Measured RAG

**Measured RAG** is a cybersecurity question-answering (RAG) project focused on experimentally comparing retrieval strategies with **measurable, reproducible evidence**. It is being developed as an evaluation-first, local-first (CPU-friendly) system: no performance claims are made without measured artifacts.

> **Integrity:** this repository reports **no benchmark results, experiments, or performance improvements**. Metrics and run artifacts are only meaningful when produced by measured executions (evaluation and end-to-end baseline runs are not yet complete).

## Project overview

- **Domain:** cybersecurity Q&A over a documented corpus with per-source provenance and licensing metadata.
- **Goal:** compare retrieval strategies (baseline first, then controlled upgrades) on fixed/versioned datasets with transparent measurements (retrieval quality, grounding/citation/refusal behavior, latency/resource usage).
- **Current focus:** M0 foundation and M1 baseline components in partial implementation; documentation and reproducibility scaffolding.

## Current milestone status

| Milestone | Status | Notes |
|---|---|---|
| **M0 — Foundation** | **Completed** (scaffold/verification reported previously) | Project layout, typed env settings, domain entities, DB engine/session helpers and placeholder models/migrations notes, configs/templates, tooling. Prior project context reported unit/lint/ingest checks passed; **not re-executed in this documentation phase**. Live DB connectivity not demonstrated. |
| **M1 — Baseline Vector RAG** | **Partially implemented** | Manifest ingestion, fixed chunking, embedding/indexing/retrieval/generation/pipeline code paths, `scripts/ingest.py`, and mocked unit tests exist. **Not complete/verified end-to-end:** applied DB schema/migrations, `scripts/index.py`/`scripts/query.py`, live embedding/indexing/generation runs, persisted real query artifacts. |
| **M2+** | **Planned / deferred** | Evaluation harness & fixed datasets (M2), chunking/retrieval/reranking/contextual upgrades (M3–M7), programmatic citation/refusal validation & metrics (M8), reporting/API/UI/hardening (M9–M11). |

## Actual implemented components

**Implemented (runnable/verifiable subset):**
- `src/measured_rag/config/settings.py`: `AppSettings` (pydantic-settings, env/`.env`), defaults/validation, cached `get_settings()`.
- `src/measured_rag/ingestion/loader.py` + `data/raw/source_manifest.yaml`: manifest-driven loading with required provenance/licensing fields.
- `src/measured_rag/chunking/fixed.py`: `FixedSizeChunker` (settings-aware, validated, provenance/offset metadata).
- `scripts/ingest.py`: ingest + chunk summary CLI (no DB/services/model downloads).
- `tests/unit/*`: config/domain and mocked M1 wiring tests.

**Implemented in code but not runtime-verified end-to-end:**
- `src/measured_rag/embeddings/huggingface.py`: lazy `sentence-transformers` embedder (CPU/batch/normalize/cache).
- `src/measured_rag/indexing/vector_store.py`: pgvector-oriented upsert/search helper (requires running Postgres+pgvector and compatible schema/migrations).
- `src/measured_rag/retrieval/vector.py` (+ registry): dense vector retriever.
- `src/measured_rag/generation/ollama.py`, `prompts.py`: grounded prompt helpers and Ollama provider (lazy `httpx`).
- `src/measured_rag/pipeline/query.py`: baseline orchestration and JSON run-artifact persistence (usage `N/A` if unavailable; indexing cost separate).

**Partially implemented/skeleton:** `src/measured_rag/db/engine.py`, `src/measured_rag/db/models.py` (M0 placeholder), `src/measured_rag/db/migrations/README.md` (no applied schema/migrations).

**Not implemented:** DB migrations/applied schema, `scripts/index.py`, `scripts/query.py`, evaluation framework/datasets/metrics/reports, YAML runtime config loading, BM25/hybrid/RRF/reranking/contextual retrieval, programmatic citation/refusal validation and metrics, API/UI.

## Documentation

- [Architecture](docs/architecture.md) — components, data flow, implemented vs planned.
- [Evaluation](docs/evaluation.md) — research objectives, proposed metrics/protocol (no results; not implemented).
- [Windows 11 setup](docs/setup_windows.md) — prerequisites, venv, config, available commands, troubleshooting.
- [Corpus sources & licensing](docs/corpus_sources.md) — provenance, recorded terms, attribution/redistribution notes.

## Working commands

Run from the project root (PowerShell examples in [docs/setup_windows.md](docs/setup_windows.md)):

```powershell
# Ingest + chunk summary (functional; no DB/services/model downloads)
python scripts/ingest.py --manifest data/raw/source_manifest.yaml

# Unit tests (requires dev dependencies installed)
pytest

# Lint (requires dev dependencies installed)
ruff check .
```

## Corpus attribution and licensing caveats

- Starter corpus provenance and recorded usage terms are documented in [docs/corpus_sources.md](docs/corpus_sources.md) and `data/raw/source_manifest.yaml`.
- Local files in `data/raw/` are **project-authored starter excerpts/summaries** for development, **not** substitutes for official NIST/CISA publications. Verify current terms at official source URLs before reuse or redistribution.
- **Unresolved:** redistribution of derived local summaries (especially CISA-derived, and NIST-derived beyond recorded statements) in a public repository has **not been legally cleared/independently verified** in this project. Confirm terms/attribution requirements before public distribution.
- The project software license ([LICENSE](LICENSE), MIT for original code) does **not** automatically cover third-party/NIST/CISA materials, datasets, model weights, or dependencies.

## Limitations

- No verified end-to-end baseline run or persisted measured query artifacts.
- No DB schema/migrations; no indexing/query CLIs; DB and LLM runtime paths are unverified in this phase.
- Evaluation is not implemented and **incomplete by design at this stage**; placeholder config only (`configs/eval/default_eval.yaml`).
- Only fixed chunking and dense retrieval implemented; advanced strategies and programmatic citation/refusal enforcement are deferred.
- Runtime YAML config loading is not implemented.
- Some behaviors are environment-dependent (dependency installation, model downloads, external services) and **unverified** here.

## Roadmap

1. **Complete M1:** schema/migrations, `scripts/index.py`/`scripts/query.py`, approved runtime deps/services, verified end-to-end baseline with measured artifacts.
2. **M2 (evaluation-first):** fixed/versioned dataset and automated metrics/reporting before further upgrades.
3. **M3–M7:** structure-aware chunking, hybrid retrieval, RRF, reranking, contextual retrieval.
4. **M8:** programmatic citation validation and refusal handling with separate metrics.
5. **M9–M11:** dataset expansion/comparative reporting, API/UI, hardening.

## License

Original project code is licensed under the MIT License — see [LICENSE](LICENSE). Third-party materials and dependencies remain under their respective terms.
