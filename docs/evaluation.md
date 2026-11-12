# Measured RAG — Evaluation Plan and Methodology

This document defines the **evaluation intent and proposed methodology** for Measured RAG. It is written for an evaluation-first, research-oriented RAG system where claims must be supported by measured evidence.

> **Status:** The evaluation framework, datasets, metric implementations, experiment runs, and comparative reports are **not implemented and no evaluation is complete**. `configs/eval/default_eval.yaml` is a placeholder only. **No benchmark results, datasets-as-executed, experiments, or performance improvements are reported or fabricated.**

## 1. Research objective

Experimentally compare retrieval (and downstream RAG) strategies for cybersecurity question answering to determine, with reproducible measurements, how design choices affect retrieval quality, answer grounding/citation behavior, refusal correctness, and efficiency (latency/resource/cost) under a fixed evaluation protocol.

## 2. Experimental questions (proposed)

Examples of questions the evaluation is intended to answer (to be refined when M2 is implemented):
- How does dense vector baseline retrieval perform on a fixed, versioned cybersecurity QA set?
- What measurable gains/trade-offs do structure-aware chunking, hybrid (BM25+dense), RRF fusion, reranking, and contextual retrieval provide over the baseline?
- How often are answers grounded in retrieved evidence, with **valid** citations and correct refusals on unanswerable/insufficient-evidence cases?
- What are the retrieval/end-to-end latency and resource/token-usage costs per strategy?

**Status:** proposed research questions; no experiments executed.

## 3. Baseline retrieval strategy

- **Baseline (intended):** dense vector retrieval over fixed-size chunks using local embeddings and pgvector-backed search, feeding a grounded prompt to a local LLM (Ollama default) as implemented partially in M1 code.
- **Current reality:** baseline pipeline components exist in code but a verified end-to-end baseline run and measured baseline results are **not available**.

## 4. Future retrieval strategies (planned comparisons)

To be evaluated against the same fixed dataset/version once implemented: structure-aware chunking, sparse/BM25, hybrid retrieval, RRF fusion, cross-encoder reranking, and contextual retrieval (index-time enrichment primary; query-time expansion treated separately/optionally). **Not implemented.**

## 5. Dataset and query-set requirements

**Proposed requirements:**
- **Fixed, versioned** datasets with documented provenance and change history; all compared strategies run on identical dataset versions.
- **Manually verified** cybersecurity Q&A items with relevance judgments (e.g. relevant chunk/document identifiers) and answerability labels where applicable.
- **Coverage targets (planned):** progressive expansion toward ~60–100 questions including **exact CVE lookups**, **multi-hop** questions, and **unanswerable** questions (to test refusal).
- **Storage/config:** `data/eval/datasets/` (currently placeholders) and dataset/version identifiers recorded per run.

**Current state:** no verified evaluation dataset published; dataset creation and labeling are **deferred (M2+)**.

## 6. Retrieval metrics (proposed)

Computed against labeled relevance judgments per query/strategy (definitions standard; implementations **not present**):

| Metric | Definition (intent) | Implementation status |
|---|---|---|
| **Recall@K** | Proportion of relevant items retrieved in top-K | **Proposed / not implemented** |
| **Precision@K** | Proportion of top-K items that are relevant | **Proposed / not implemented** |
| **MRR** | Mean reciprocal rank of first relevant result | **Proposed / not implemented** |
| **nDCG@K** | Rank-aware gain normalized by ideal ranking | **Proposed / not implemented** |
| (Diagnostic) **Hit@K** | Whether any relevant item appears in top-K | **Proposed / not implemented** |

## 7. Answer and grounding metrics (proposed)

| Metric/aspect | Intent | Implementation status |
|---|---|---|
| **Context relevance** | Degree to which retrieved context is relevant to the question/answer needs (may use labels or documented proxies) | **Proposed / not implemented** |
| **Answer faithfulness / groundedness** | Whether claims are supported by retrieved/cited evidence; prefer deterministic checks where feasible, else documented proxies with limitations | **Proposed / not implemented** |
| **Citation correctness** | Programmatic validation that cited chunk IDs exist in retrieved context and support is attributable as defined by the protocol | **Proposed / not implemented** (prompting alone is insufficient) |
| **Refusal behaviour** | Correct refusal/abstention on unanswerable or insufficient-evidence cases; measure correct refusals, false refusals, and unsupported answers separately | **Proposed / not implemented** |

## 8. Latency and resource measurements (proposed, integrity-critical)

| Measurement | Requirement | Implementation status |
|---|---|---|
| **Retrieval latency** | Per-query and aggregated (e.g. mean/p50/p95) from measured runs | **Proposed / not implemented** as evaluation reporting; pipeline code can record retrieval latency in artifacts but **no verified runs** |
| **End-to-end latency** | Full query-path timing per query and aggregated | **Proposed / not implemented** as evaluation reporting; artifact field exists in code |
| **Token/model usage** | Record provider/model-reported tokens **only when available**; otherwise `N/A`. **Never estimate.** | **Partially represented in code** (usage recorded if reported else N/A) but **no verified runs** |
| **Indexing cost** | Record **separately** per indexing run (duration, doc/chunk counts, model/batch/index settings, measurable resource usage) | **Proposed / not implemented** |
| **Resource usage** | CPU/memory/runtime environment details as feasible and documented | **Proposed / not implemented** |

## 9. Reproducibility controls (proposed)

- Fixed dataset versions and documented query sets.
- Explicit experiment configurations (strategy, chunking, embedding, retrieval, reranking/contextual options, generation settings) with stored config identifiers/hashes.
- Recorded seeds and deterministic components where applicable (`SEED` exists in settings; end-to-end determinism **not verified**).
- Persisted run artifacts (inputs, retrieved IDs/scores/ranks, prompts/outputs, measurements, timestamps, model/index identifiers).
- Environment capture (Python/package versions, model IDs, index versions) for comparative runs.

**Current state:** partial artifact/config primitives exist in code; full reproducibility protocol and enforcement are **not implemented**.

## 10. Experimental configuration

- **Reference configs present:** `configs/eval/default_eval.yaml` (placeholder), `configs/experiments/01_baseline_vector.yaml`, `configs/app.example.yaml`, `.env.example`.
- **Runtime reality:** settings are env/`.env` driven via `AppSettings`; **YAML-driven experiment loading/execution is not implemented**. Any experiment definitions beyond code defaults are **proposed/alignment-only** until a loader/runner exists.

## 11. Statistical reporting requirements (proposed)

When results exist (future): report per-strategy aggregates and distributions with sample sizes (n queries), dataset version, confidence/variability measures as appropriate (e.g. intervals or bootstrap) and clearly labeled comparisons/deltas vs baseline; avoid claims unsupported by the measured data. **No statistical results exist.**

## 12. Limitations and threats to validity

- **Implementation gap:** evaluation tooling, datasets, and verified end-to-end runs do not yet exist; current conclusions about quality/performance are **not possible**.
- **Dataset validity:** small or unverified datasets, labeling errors, and limited coverage (CVE/multi-hop/unanswerable) can bias outcomes; dataset construction is pending.
- **Metric validity:** automated proxies for faithfulness/context relevance may misalign with human judgment; citation checks depend on precise protocol definitions.
- **Model/service variability:** LLM nondeterminism, model/version changes, and hardware differences can affect reproducibility.
- **Leakage/contamination:** must be controlled when constructing datasets and selecting sources (process **not yet implemented/documented as executed**).
- **Generalizability:** results on a cybersecurity corpus subset may not transfer to other domains or source distributions.
- **Unverified assumptions:** some planned metric choices, thresholds, and reporting formats are **proposed** and subject to change during M2+ implementation.

**Integrity statement:** this project must not report fabricated or estimated benchmark results. All future evaluation claims must be traceable to persisted, measured artifacts.
