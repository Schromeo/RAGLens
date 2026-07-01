# AI Handoff

## Project Name
RAGLens

## One-liner
RAGLens is a local-first visual debugger for RAG pipelines.

## Core Problem
RAG developers often do not know why their system answered incorrectly.

A wrong answer may come from:

- Bad retrieval
- Bad chunking
- Stale context
- Conflicting chunks
- Weak grounding
- LLM ignoring retrieved evidence

RAGLens helps developers inspect the full RAG pipeline locally.

## Target Users

- AI application developers
- RAG builders
- Backend engineers adding LLM/RAG to their systems
- Indie hackers building AI apps
- Developers debugging retrieval pipelines

## MVP Scope
v0.1 should support:

- Python SDK
- Trace context manager
- Retrieval span logging
- LLM call logging
- Local collector
- Local storage
- Trace list UI
- Trace detail UI
- Retrieved chunks viewer
- Basic warning rules
- Refund policy demo

## Long-term Vision
RAGLens starts as a local-first RAG debugger.

v0.1 is complete and validated end-to-end.

The long-term direction is TraceForge: local-first observability and debugging for AI application harnesses.

In this framing, RAG is the first vertical slice because retrieval quality, context quality, conflicting evidence, and grounding are common failure points.

Potential future modules:

- tool spans
- memory spans
- verification spans
- human feedback / intervention spans
- agent workflow visibility
- Prompt/model regression testing
- Eval dataset generation
- Semantic cache analysis
- AI gateway integration
- OpenTelemetry export
- Langfuse/Promptfoo/Ragas interoperability

Important scope note: these are future possible directions, not v0.1 features.

## Current Strategy
Start narrow.

Do not build a full AI infra platform first.

Build a polished, useful, easy-to-run RAG debugging tool first.

## Current Implementation Status
RAGLens v0.1 MVP is complete and validated end-to-end.

The full production path has been implemented and tested:

```text
Python SDK
  ↓
t.flush()
  ↓
POST /api/traces
  ↓
Go Collector (:4319)
  ↓
SQLite (traces, spans, warnings)
  ↓
GET /api/traces
  ↓
GET /api/traces/{trace_id}
  ↓
React Dashboard
  ↓
Real warning cards, trace detail, chunk viewer
```

**v0.1 Status: COMPLETE AND RELEASED**

### Completed Implementation

- Python SDK
  - `trace()` context manager
  - retrieval span logging
  - LLM span logging
  - trace payload generation
  - `flush()` to local collector
- Go Collector
  - `GET /health`
  - `POST /api/traces`
  - `GET /api/traces`
  - `GET /api/traces/{trace_id}`
  - SQLite persistence for traces and spans
  - Warning Engine runs after trace persistence
  - Implemented diagnosis rules:
    - `no_retrieved_chunks`
    - `low_retrieval_score` (default threshold `0.5`, overridable via span metadata)
    - `duplicate_chunks`
    - `conflicting_chunks`
    - simplified `answer_not_grounded`
  - Warning persistence in SQLite
- React Dashboard
  - trace list page
  - trace detail page
  - span timeline
  - retrieved chunk viewer
  - LLM prompt/response viewer
  - real warning cards on trace detail

- Warning smoke tests
  - `sdk/python/examples/warning_rules_demo.py`
  - one demo function per warning rule
  - supports running all demos or a single demo case
  - expected result per case: `warnings_generated: 1`

The local inspection loop is complete and validated end-to-end:

```text
Python SDK
  ↓
t.flush()
  ↓
POST /api/traces
  ↓
Go Collector (:4319)
  ↓
SQLite (traces, spans, warnings)
  ↓
GET /api/traces/{trace_id}
  ↓
React Dashboard warning cards
```

Important implementation detail:

- In `warning_rules_demo.py`, `t.flush()` is called after exiting the `with trace(...)` block so `ended_at` and `duration_ms` are finalized before payload submission.

### Recent Dashboard UI Polish (2026-06-22)

- Sidebar trace list: text truncation for query (2 lines) and answer (3 lines) to keep card heights uniform
- Trace detail: Final answer moved from floating window to grid layout with Query/Duration/Warnings
- Final answer card: inline vertical resizing with scrollable content area
- All styling consolidated, no nested border redundancy

### Known Limitations (By Design)

- Local-first v0.1: no cloud sync, no auth, no multi-user workspaces
- Retrieval baseline: TF-IDF + cosine similarity (transparent and local-first, not semantic)
- Warning rules: simple heuristic deterministic rules, not ML-based
- Framework support: Python SDK only in v0.1; LangChain/LlamaIndex adapters deferred to v0.2+

### Current Known Issues / Notes

- Trace duration may show `0ms` in the mock demo because the demo executes instantly.
- Local artifacts such as `node_modules`, SQLite database files, and sample trace files should stay ignored by git.

### Real Local RAG Demo Milestone

Status: Completed

Completed:

- Added local markdown policy documents.
- Implemented local document loader.
- Implemented deterministic chunking.
- Implemented TF-IDF + cosine similarity retriever.
- Added simple local answerer.
- Added demo case matrix.
- Integrated real local retrieval output with existing Python SDK trace schema.
- Sent traces to Go Collector on port `4319`.
- Verified traces in Dashboard.
- Verified existing warning rules trigger on real retrieval output.

Demo commands:

```powershell
# terminal 1
cd collector/go
go run ./cmd/raglens-collector

# terminal 2
cd sdk/python
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo inspect
python -m examples.local_rag_demo.run_demo retrieve "How can I reset my password?"
python -m examples.local_rag_demo.run_demo trace duplicate
python -m examples.local_rag_demo.run_demo trace-all
```

### Milestone Update: Real Local RAG Demo (Completed)

Milestone status: Completed

Completed components:

- local markdown policy document set
- local document loader
- deterministic chunker
- TF-IDF plus cosine similarity retriever
- simple local answerer with optional hallucinated mode
- real retrieved chunk mapping to existing SDK trace schema
- trace submission through existing SDK flow: `trace()`, `t.retrieval()`, `t.llm()`, `t.flush()`
- collector ingestion and SQLite persistence reuse
- dashboard validation for real retrieval traces and warning cards

Verified commands (from `sdk/python`):

```powershell
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo inspect
python -m examples.local_rag_demo.run_demo retrieve "How long does standard shipping take?"
python -m examples.local_rag_demo.run_demo all
python -m examples.local_rag_demo.run_demo trace conflict
python -m examples.local_rag_demo.run_demo trace-all
```

Verified warning cases:

- no_match -> no_retrieved_chunks
- low_score -> low_retrieval_score
- duplicate -> duplicate_chunks
- conflict -> conflicting_chunks
- hallucinated -> answer_not_grounded

Current project state:

- Warning Engine / Diagnosis Layer MVP: Completed
- Real Local RAG Demo milestone: Completed
- End-to-end path is validated with real retrieval output:

```text
Python SDK -> Collector (:4319) -> SQLite -> Dashboard
```

Recommended next step:

- Developer Experience and Demo Packaging
- Improve README quickstart and demo runbook polish
- Add screenshots or GIF walkthrough
- Make local startup simpler for first-time users
- Polish dashboard demonstration flow
- Keep LangChain and LlamaIndex adapters deferred until DX and test hardening are stable

### Next Major Step

Plan v0.2 Developer Integration / User Onboarding.

The immediate next step is to help developers instrument their own RAG pipelines with the Python SDK. Harness-level features remain a long-term TraceForge direction, not current implementation scope.