# Roadmap

This roadmap is ordered by delivery sequence.

Each version includes clear scope boundaries so RAGLens stays local-first, lightweight, and useful as a developer tool.

## Current Snapshot

**Current version:** v0.1 — Local RAG Debugger MVP
**Status:** In Progress (Warning Engine MVP + Real Local RAG Demo complete)

### Completed foundation

RAGLens currently has a working local inspection loop:

```text
Python SDK
  ↓
Go Collector
  ↓
SQLite
  ↓
React Dashboard
```

Completed so far:

* Python SDK instrumentation:

  * `trace()`
  * retrieval span logging
  * LLM span logging
  * trace payload generation
  * `flush()` to local collector
* Go collector ingestion APIs:

  * `GET /health`
  * `POST /api/traces`
  * `GET /api/traces`
  * `GET /api/traces/{trace_id}`
* SQLite persistence for traces and spans
* React Dashboard MVP:

  * trace list page
  * trace detail page
  * retrieved chunk viewer
  * LLM prompt/response viewer
  * warning cards
* Refund policy demo end-to-end flow

### Active focus

Real Local RAG Demo is complete.

Immediate goals:

* Improve warning explanation quality and details display in dashboard.
* Add unit tests for warning rules and local retrieval demo cases.
* Expand real local RAG instrumentation coverage.
* Evaluate semantic retriever baseline (sentence-transformers + cosine) without breaking trace schema.
* Keep LangChain/LlamaIndex adapters deferred until test coverage is stable.

---

## v0.1 — Local RAG Debugger MVP

**Status:** In Progress (Diagnosis Layer MVP + Real Local RAG Demo complete)

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
* [x] Real local RAG demo (local docs + deterministic chunking + TF-IDF retrieval)

#### Collector and local storage

* [x] Go collector
* [x] `GET /health`
* [x] `POST /api/traces`
* [x] `GET /api/traces`
* [x] `GET /api/traces/{trace_id}`
* [x] SQLite storage
* [x] Trace persistence
* [x] Span persistence

#### Dashboard

* [x] Trace list page
* [x] Trace detail page
* [x] Retrieved chunks viewer
* [x] LLM call viewer
* [x] Warning cards in trace detail

#### Warning engine

* [x] `no_retrieved_chunks`
* [x] `low_retrieval_score`
* [x] `duplicate_chunks`
* [x] `conflicting_chunks`
* [x] simplified `answer_not_grounded`

Validation smoke test:

* `sdk/python/examples/warning_rules_demo.py`
* supports `all` and per-rule runs
* expected result: each case returns `warnings_generated: 1`

### Completed Milestone: Real Local RAG Demo

Completed and verified in v0.1:

* local markdown policy documents for retrieval
* simple deterministic chunking pipeline
* TF-IDF plus cosine similarity retriever baseline
* real retrieved chunks with rank and score
* SDK trace integration without schema changes
* dashboard verification of real retrieval traces
* warning rule verification on real retrieval output

Verified warning-target cases:

* `no_match` -> `no_retrieved_chunks`
* `low_score` -> `low_retrieval_score`
* `duplicate` -> `duplicate_chunks`
* `conflict` -> `conflicting_chunks`
* `hallucinated` -> `answer_not_grounded`

### Exit Criteria

v0.1 is complete when:

* The refund policy demo produces at least one warning.
* Warning records are persisted in SQLite.
* Warning records are returned by the trace detail API.
* The dashboard trace detail page renders real warnings.
* A developer can run the local demo and understand the value of RAGLens without reading raw JSON.

---

## v0.2 — Developer Experience

**Status:** Not Started

### Goal

Make RAGLens fast to try, simple to run, and pleasant for first-time users.

### Planned Scope

* Better README quickstart
* GIF or short demo walkthrough
* One-command local startup path
* Docker Compose local run path
* CLI command: `raglens ui`
* Local reset command for demo data
* Raw OpenAI example

Note: LangChain and LlamaIndex adapters remain deferred until Real Local RAG Demo is complete and validated.

---

## v0.3 — RAG Quality Analysis

**Status:** Not Started

### Goal

Help developers identify why retrieval quality broke for a given answer.

### Planned Scope

* Weak retrieval warning
* Missing context warning
* Duplicate chunk warning
* Conflicting context warning
* Stale context warning
* Answer not grounded warning
* Source attribution view
* Save failing trace as eval case seed

---

## v0.4 — Evaluation and Regression

**Status:** Not Started

### Goal

Turn debugging outcomes into repeatable quality checks.

### Planned Scope

* Eval dataset export
* Basic regression test runner
* Prompt/model comparison runs
* Retrieval configuration comparison
* CI-friendly report output

---

## Future — TraceForge Direction

**Status:** Future

RAGLens starts as a local-first RAG debugger.

The following items are possible future directions after the core local debugger experience is useful and stable. They are not part of the immediate MVP commitment.

Potential expansion:

* Agent/tool call tracing
* Multi-step agent timeline
* Semantic cache analysis
* AI gateway integration
* OpenTelemetry export
* Langfuse export
* Promptfoo/Ragas interoperability
* Cloud sync
* Team workspace
