# Roadmap

This roadmap is ordered by delivery sequence.

Each version includes clear scope boundaries so RAGLens stays local-first, lightweight, and useful as a developer tool.

## Current Snapshot

**Current version:** v0.2 — Developer Integration / Local SDK Onboarding  
**Status:** Completed

RAGLens now has a working local inspection loop for both the built-in demo and user-owned Python RAG pipelines:

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
* `conflicting_chunks`
* simplified `answer_not_grounded`

v0.2 completion highlights:

* `docs/product/USER_ONBOARDING.md`
* `docs/integrations/PYTHON_SDK_GUIDE.md`
* `sdk/python/examples/custom_pipeline_demo.py`
* `scripts/start-raglens.py`
* README two-path quickstart for demo usage and real integration
* README documentation map for users and maintainers
* SDK packaging hygiene (`sdk/python` version `0.2.0`, local SDK README, local editable install path)
* integration smoke test validation through the dashboard

---

## v0.1 — Local RAG Debugger MVP

**Status:** Completed

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

**Status:** Completed

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

**Status:** Not Started

### Goal

RAG Quality Analysis / Diagnostic Intelligence.

### Candidate Scope

* warning schema v2
* evidence-backed warning details
* improved `answer_not_grounded` heuristics
* numeric/date/entity grounding checks
* retrieval quality diagnostics
* conflict detection v2
* dashboard warning detail improvements
* optional future LLM-assisted diagnostics (later, not default local path)

### Out of Scope

Still not part of this milestone by default:

* cloud sync
* auth
* hosted collector
* tool/memory/verification/human feedback spans

These remain future direction only and are intentionally separate from current v0.2 scope.

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
* this direction is not part of current v0.2 completion scope
