# Roadmap

This roadmap is ordered by delivery sequence.

Each version includes clear scope boundaries so RAGLens stays local-first, lightweight, and useful as a developer tool.

## Current Snapshot

**Current version:** v0.1 — Local RAG Debugger MVP
**Status:** In Progress

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
  * warning placeholder
* Refund policy demo end-to-end flow

### Active focus

The current milestone is to implement the first warning engine.

Immediate goals:

* Generate warning records in the Go collector
* Persist warning records in SQLite
* Return warnings from the trace detail API
* Render real warnings in the dashboard trace detail page

---

## v0.1 — Local RAG Debugger MVP

**Status:** In Progress

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
* [x] Warning panel placeholder

#### Warning engine

* [ ] `no_retrieved_chunks`
* [ ] `low_retrieval_score`
* [ ] `duplicate_chunks`
* [ ] `conflicting_chunks`
* [ ] simplified `answer_not_grounded`

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
* LangChain example
* LlamaIndex example

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
