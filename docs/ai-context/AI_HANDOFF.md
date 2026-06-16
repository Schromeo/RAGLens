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

### Next Major Step

Improve warning explanation quality, add tests for warning rules and demo cases, then evaluate a semantic retriever baseline before adapter work.