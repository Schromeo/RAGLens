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

Over time, it can evolve into a broader LLM/Agent observability and evaluation platform, internally referred to as TraceForge.

Potential future modules:

- Agent/tool call tracing
- Prompt/model regression testing
- Eval dataset generation
- Semantic cache analysis
- AI gateway integration
- OpenTelemetry export
- Langfuse/Promptfoo/Ragas interoperability

## Current Strategy
Start narrow.

Do not build a full AI infra platform first.

Build a polished, useful, easy-to-run RAG debugging tool first.

## Current Implementation Status
RAGLens now has a working local MVP skeleton.

The following path has been implemented and validated:

```text
Python SDK
  ↓
t.flush()
  ↓
POST /api/traces
  ↓
Go Collector
  ↓
SQLite
  ↓
GET /api/traces
  ↓
GET /api/traces/{trace_id}
  ↓
React Dashboard
```

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
  - First diagnosis rule: `conflicting_chunks`
  - Warning persistence in SQLite
- React Dashboard
  - trace list page
  - trace detail page
  - span timeline
  - retrieved chunk viewer
  - LLM prompt/response viewer
  - real warning cards on trace detail

The refund policy demo successfully sends traces from the Python SDK to the local collector and displays them in the dashboard.

### Current Known Issues / Notes

- Warning coverage is still partial in v0.1.
- Only `conflicting_chunks` is implemented so far.
- Trace duration may show `0ms` in the mock demo because the demo executes instantly.
- Local artifacts such as `node_modules`, SQLite database files, and sample trace files should stay ignored by git.

### Next Major Step

Expand warning coverage in the existing warning engine.

Initial warning rules should include:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- `conflicting_chunks` (completed)
- simplified `answer_not_grounded`