# Measured RAG — Windows 11 Setup

This guide targets **Windows 11**, **Python 3.11+**, and **CPU-friendly** local development. It reflects the repository’s **current** state and clearly marks deferred/runtime-unverified components. Commands documented here are limited to those supported by the current project structure; **no installations or system configuration were executed** as part of this documentation update.

## 1. Prerequisites

| Requirement | Purpose | Status |
|---|---|---|
| Windows 11 | Documented environment | Supported (target) |
| Python 3.11+ on `PATH` | Runtime/tooling (`pyproject.toml` requires `>=3.11`) | Required |
| PowerShell | Shell for commands below | Recommended |
| Git (optional) | Source control | Optional (no Git ops performed here) |
| VS Code + Python extension (optional) | Editing/debugging | Optional |
| Docker Desktop (WSL2 backend) | PostgreSQL + pgvector for DB-backed indexing/query | **Deferred / not required for current ingest demo** |
| Ollama | Local LLM generation runtime | **Deferred / not required for current ingest demo** |

## 2. Repository location

Project root (workspace): `D:\docsss\AI-ML\projects\measured-rag`

Run commands from the project root unless noted.

## 3. Virtual environment creation

```powershell
cd D:\docsss\AI-ML\projects\measured-rag
python -m venv .venv
```

## 4. Activation

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution (common on Windows), you may allow scripts for the current user (one-time, if appropriate for your environment):

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then re-run activation. **This document does not change your system policy.**

## 5. Dependency installation

Dependencies are declared in `pyproject.toml` (read-only in this phase). Install only when you intend to work locally:

- **Runtime/base dependencies** (includes config/DB libs and currently declared `httpx`, `numpy`, `sentence-transformers`, `torch`, etc.):
  ```powershell
  pip install -e .
  ```
- **Development dependencies** (pytest, pytest-cov, ruff) plus runtime:
  ```powershell
  pip install -e ".[dev]"
  ```

### CPU-friendly notes
- A **GPU is not required**. Prefer CPU-compatible package builds.
- `torch` and `sentence-transformers` can be large and may require network access/time; if installation fails, consult the official PyTorch CPU install instructions for your Python version and retry.
- Model downloads (HuggingFace embeddings, Ollama models) occur only when those components are actually used/pulled; they are **not** required for the current `scripts/ingest.py` flow or mocked unit tests.

## 6. Environment configuration

1. Copy the example environment file:
   ```powershell
   Copy-Item .env.example .env
   ```
2. Edit `.env` as needed. **Never commit secrets or real API keys.** (`.env` is gitignored.)

**Key variables (see `.env.example`):**
- **Database:** `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, optional `DATABASE_URL`
- **Embeddings:** `EMBEDDING_MODEL`, `EMBEDDING_DEVICE` (default `cpu`), `EMBEDDING_BATCH_SIZE`, `EMBEDDING_NORMALIZE`, `EMBEDDING_CACHE_ENABLED`
- **Chunking:** `CHUNK_SIZE`, `CHUNK_OVERLAP`
- **Retrieval:** `TOP_K`
- **Generation:** `GENERATION_TIMEOUT_S`, `LLM_PROVIDER`, `OLLAMA_BASE_URL`, `OLLAMA_MODEL`, optional `OPENAI_COMPAT_*`
- **Paths/resources:** `DATA_DIR`, `CONFIG_DIR`, `CACHE_DIR`, `SEED`, `MAX_TOP_N_RERANK`, `RRF_K`

YAML files in `configs/` are examples/alignment references; **automatic YAML runtime loading is not implemented**.

## 7. PostgreSQL and pgvector prerequisites (deferred)

Required for **future** DB-backed indexing/query and end-to-end baseline execution. **Not required** for the current ingest CLI or existing mocked tests.

- Install and run **Docker Desktop** with WSL2 backend (recommended on Windows 11).
- Start a PostgreSQL image that includes **pgvector** (e.g. a `pgvector/pgvector` image) with a persistent volume and port mapping to localhost.
- Configure `.env` `POSTGRES_*` values to match the container.
- Schema/migrations must be created/applied before DB-backed operations work. **Current repository status:** no applied M1 migrations/schema; `src/measured_rag/db/migrations/README.md` is a placeholder. Do **not** assume `scripts/index.py`/`scripts/query.py` exist (they do not).

## 8. Ollama setup (deferred)

Required for **live LLM generation** through the implemented `OllamaProvider`. **Deferred for current runnable subset.**

- Install Ollama for Windows and ensure the service is running.
- Pull a model compatible with your settings (default example: `llama3.2:3b`).
- Verify `OLLAMA_BASE_URL` and `OLLAMA_MODEL` in `.env`.
- Generation is **not** exercised by `scripts/ingest.py` and is **not verified** here.

## 9. Available commands (current project)

Run from project root with the virtual environment activated and required dependencies installed as appropriate.

| Command | Purpose | Requirements / notes |
|---|---|---|
| `python scripts/ingest.py --manifest data/raw/source_manifest.yaml` | Load manifest, chunk with settings-driven fixed chunker, print deterministic summary | No DB, no embedding model download, no LLM service required. Optional: `--base-dir` to resolve `local_path` entries. |
| `pytest` | Run unit tests | Dev dependencies installed (e.g. `pip install -e ".[dev]"`). Tests are designed to avoid DB/services/model downloads where mocked. |
| `ruff check .` | Lint checks | Dev dependencies installed. |

**Not available (deferred):** `scripts/index.py`, `scripts/query.py`, evaluation runners, API/UI entrypoints.

## 10. Common Windows errors and troubleshooting

| Symptom | Likely cause | Suggested fix |
|---|---|---|
| `python` / `pip` not recognized | Python not on `PATH` | Reinstall Python with “Add python.exe to PATH” or use full interpreter path; reopen terminal. |
| `Activate.ps1` cannot be loaded | Execution policy restriction | Use `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (if acceptable) then re-activate `.venv`. |
| `ModuleNotFoundError: measured_rag` | Project not installed in active venv or wrong working directory | Activate `.venv`, run `pip install -e .` (or `.[dev]`) from project root, run scripts from root. |
| Ingest fails with manifest/file path errors | Wrong CWD, missing files, or base-dir resolution | Run from project root; confirm `data/raw/source_manifest.yaml` and referenced `local_path` files exist; pass `--base-dir` if needed. |
| `pip install` fails building/installing `torch` or ML deps | Platform/Python wheel mismatch or network issues | Upgrade `pip`, select a CPU-compatible wheel per official PyTorch guidance, ensure network access; retry. |
| Slow install or high disk usage | Large scientific/ML packages | Expected for CPU ML stacks; ensure sufficient disk space and time. |
| PostgreSQL/`psycopg` connection errors | DB not running or wrong credentials/port | Relevant only for deferred DB work; verify container/service status and `.env` settings. |
| Ollama connection refused/timeouts | Service not running or wrong URL/model | Relevant only for deferred generation; start Ollama, pull model, verify `OLLAMA_BASE_URL`/`OLLAMA_MODEL`. |
| Out-of-memory or slow embedding/generation | Resource limits on CPU | Use smaller models/batch sizes (e.g. `EMBEDDING_BATCH_SIZE`) when runtime components are enabled; prefer CPU defaults. |

## 11. Verification notes (unverified in this phase)

- Dependency installation, test/lint execution, database connectivity, Ollama connectivity, and end-to-end RAG runs were **not executed** during this documentation task. Prior project context indicates `pytest`, `ruff`, and `scripts/ingest.py` succeeded in earlier phases; treat as **previously reported, not re-verified now** unless you run them locally.
