# Roadmap

This roadmap is ordered by delivery sequence.

Each version includes clear scope boundaries so RAGLens stays local-first, lightweight, and useful as a developer tool.

## Current Snapshot

**Current version:** v0.3.5 — Diagnostic Quality Hardening  
**Status:** Completed and smoke-tested

RAGLens has completed the local inspection loop for both the built-in demo and user-owned Python RAG pipelines, and is now upgrading the warning layer into evidence-backed diagnostics:

```text
Python SDK
  ↓
Go Collector
  ↓
SQLite
  ↓
React Dashboard
```

Current implemented span types:

* `retrieval`
* `llm`

Current warning rules:

* `no_retrieved_chunks`
* `low_retrieval_score`
* `duplicate_chunks`
* `weak_query_chunk_overlap`
* `conflicting_chunks`
* `answer_not_grounded`
* `numeric_mismatch`

Current v0.3.5 hardening highlights:

* numeric expression range handling supports both hyphen and natural-language ranges
* conflicting chunk selection is query/answer relevance-aware and deterministic
* conflicting chunk topic gating reduces cross-topic numeric noise
* thin reference integration app validates mixed raw retrieval output normalization
* deterministic-first behavior retained, with optional real LLM validation path

Completed foundation highlights:

* `docs/product/USER_ONBOARDING.md`
* `docs/integrations/PYTHON_SDK_GUIDE.md`
* `sdk/python/examples/custom_pipeline_demo.py`
* `scripts/start-raglens.py`
* README two-path quickstart for demo usage and real integration
* README documentation map for users and maintainers
* SDK packaging hygiene (`sdk/python` version `0.2.0`, local SDK README, local editable install path)
* integration smoke test validation through the dashboard
* v0.3 diagnostic intelligence design spec in `docs/product/V0_3_DIAGNOSTIC_INTELLIGENCE.md`
* v0.3 diagnostic quality demo cases for numeric mismatch, weak overlap, unsupported claim, and conflicting chunks
* evidence-backed warning detail UI with compared-value and recommended-action blocks
* v0.3.5 reference integration app and policy corpus under `sdk/python/examples/reference_rag_app/`

---

## v0.1 — Local RAG Debugger MVP

**Status:** Done

### Goal

Let a developer trace a RAG pipeline, store traces locally, and inspect the pipeline in a browser UI.

### Scope

#### Core tracing and ingestion

* [x] Python SDK
* [x] Trace context manager
* [x] Retrieval span logging
* [x] LLM call span logging
* [x] Trace payload generation
* [x] SDK `flush()` to local collector
* [x] Refund policy demo
* [x] Real local RAG demo using local documents, deterministic chunking, and TF-IDF retrieval

#### Collector and local storage

* [x] Go collector
* [x] `GET /health`
* [x] `POST /api/traces`
* [x] `GET /api/traces`
* [x] `GET /api/traces/{trace_id}`
* [x] SQLite storage
* [x] Trace persistence
* [x] Span persistence
* [x] Warning persistence

#### Dashboard

* [x] Trace list page
* [x] Trace detail page
* [x] Retrieved chunks viewer
* [x] LLM prompt / response viewer
* [x] Warning cards in trace detail
* [x] Demo-friendly trace list labels
* [x] Improved warning card readability
* [x] Responsive trace detail layout polish

#### Warning engine

* [x] `no_retrieved_chunks`
* [x] `low_retrieval_score`
* [x] `duplicate_chunks`
* [x] `conflicting_chunks`
* [x] simplified `answer_not_grounded`

### Validation

v0.1 smoke test passed.

Verified:

* collector starts successfully
* dashboard starts successfully
* local RAG `trace-all` runs successfully
* demo traces appear in dashboard
* warning cards render in trace detail
* retrieved chunks, scores, prompt, response, and warnings are inspectable
* expected warning-focused demo cases generate warnings

---

## v0.2 — Developer Integration / Local SDK Onboarding

**Status:** Done

### Goal

Make it clear how a developer can use RAGLens with their own RAG pipeline instead of modifying the built-in local demo.

The built-in `local_rag_demo` is a deterministic proof demo and smoke-test fixture. Real users should instrument their own retrieval and LLM calls with the RAGLens Python SDK.

### Completed Core Scope

#### User onboarding docs

* [x] `docs/product/USER_ONBOARDING.md`
* [x] Explain RAGLens as a local-first debugging/observability layer for RAG pipelines
* [x] Explain that real users do not modify the built-in demo for production usage
* [x] Explain how users instrument their own RAG pipeline
* [x] Explain what data RAGLens expects today

#### Python SDK integration guide

* [x] `docs/integrations/PYTHON_SDK_GUIDE.md`
* [x] local editable install instructions
* [x] `RAGLENS_COLLECTOR_URL` configuration
* [x] `trace()` basics
* [x] Retrieval span example
* [x] LLM span examples
* [x] `flush()` behavior
* [x] Common mistakes and troubleshooting

#### Custom pipeline example

* [x] `sdk/python/examples/custom_pipeline_demo.py`
* [x] Show how to instrument a user-owned retrieval pipeline
* [x] Keep the example local and deterministic
* [x] Avoid LangChain, LlamaIndex, OpenAI, Anthropic, and other external APIs

#### Unified local startup path

* [x] `scripts/start-raglens.py`
* [x] Cross-platform repo-local startup helper
* [x] Recommended local startup flow documented in README and SDK guide
* [x] Existing PowerShell and macOS script paths preserved as shortcuts/fallbacks

#### README integration path

* [x] Two-path quickstart in `README.md`
* [x] Path A: built-in demo validation flow
* [x] Path B: integrate the SDK into your own Python RAG app

### Smoke-Tested Validation

The following commands passed during v0.2 integration validation:

```bash
python scripts/start-raglens.py
cd sdk/python
python -m examples.custom_pipeline_demo
python -m examples.local_rag_demo.run_demo trace-all
```

Validated results:

* dashboard confirmed `custom-rag-pipeline`
* dashboard confirmed built-in local RAG demo traces
* dashboard confirmed warning-focused demo cases
* custom pipeline demo flushed successfully through the local collector

### Explicitly Not Completed in v0.2

Future work, not current v0.2 completion:

* Docker Compose local setup
* packaged CLI
* PyPI publishing
* raw LLM provider examples
* LangChain adapter
* LlamaIndex adapter
* LLM-assisted diagnostics

### Out of Scope

Not part of current v0.2 implementation:

* tool spans
* memory spans
* verification spans
* human feedback spans
* agent tracing
* cloud sync
* auth
* hosted collector
* full LLM-as-judge grounding evaluator

---

## v0.3 — RAG Quality Analysis / Diagnostic Intelligence

**Status:** Core implemented and smoke-tested

### Goal

Upgrade warnings from simple flags into evidence-backed diagnostics.

### Scope

* [x] warning schema v2
* [x] evidence-backed warning details
* [x] diagnostic object design
* [x] improved `answer_not_grounded` heuristics
* [x] weak query/chunk overlap diagnostics
* [x] numeric mismatch diagnostics
* [x] conflict detection v2
* [x] dashboard warning detail improvements
* [x] diagnostic quality demo cases

### Validation

Validated with:

```bash
cd collector/go
go test ./...

cd dashboard/web
npm run build

cd sdk/python
python -m examples.diagnostic_quality_demo all
```

### Out of Scope

Not part of this milestone:

* LangChain / LlamaIndex
* PyPI / Docker / CLI
* agent/tool/memory spans
* LLM-as-judge default path
* cloud sync
* auth
* hosted collector

These remain intentionally outside the v0.3 local-first deterministic-first path.

---

## v0.3.5 — Diagnostic Quality Hardening

**Status:** Done

### Goal

Harden deterministic warning quality on realistic integration traces without introducing LLM-as-judge or changing core trace/storage contracts.

### Scope

* [x] natural-language numeric range extraction in warning engine
* [x] conservative numeric mismatch behavior preserved for elapsed-time and directly-supported values
* [x] relevance-aware conflicting chunk candidate selection
* [x] deterministic topic classifier for numeric conflict candidate gating
* [x] expanded warning-engine tests for range and relevance behavior
* [x] thin reference RAG integration app with mixed raw retrieval output normalization
* [x] deterministic answer cleanup for lower avoidable grounding-noise in demo traces

### Validation

```bash
cd collector/go
go test ./... -count=1

cd sdk/python
python -m examples.reference_rag_app.run all
python -m examples.reference_rag_app.run processing-range
python -m examples.reference_rag_app.run wrong-processing-range
python -m examples.real_llm_rag_demo all
```

### Out of Scope

* storage schema changes
* dashboard UI/schema changes
* SDK trace API changes
* LLM-as-judge or non-deterministic warning evaluation

---

## Future — Agent Harness Observability (TraceForge Direction)

**Status:** Future

Potential future direction after current milestones:

* running traces for multi-step agent/harness executions
* partial span ingestion for long-running or interrupted runs
* future span types such as `agent`, `tool`, and `retry`
* diagnostics for agent loops
* diagnostics for oscillation between states/actions
* diagnostics for retry storms
* diagnostics for no-progress execution

Important scope note:

* none of the above is implemented in current RAGLens
* this direction is not part of current v0.3 scope
