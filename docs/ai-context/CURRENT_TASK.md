# Current Task

## Current Focus
Final smoke test and screenshot pass for demo packaging.

The Python SDK, Go collector, SQLite persistence, and initial React Dashboard are now working.

RAGLens can generate a trace from the Python SDK, send it to the local collector, persist it in SQLite, and display it in the browser dashboard.

The Warning Engine / Diagnosis Layer MVP is complete.
The Real Local RAG Demo milestone is complete.

## Current Goal
Lock down a reproducible demo runbook and complete final validation before screenshot capture.
Ensure docs, scripts, and collector/dashboard startup paths are consistent.

## Current System Status
Completed so far:

- Product direction defined
- Product spec created
- Trace/span data model created
- Python SDK created
- `trace()` context manager implemented
- Retrieval span logging implemented
- LLM span logging implemented
- SDK `flush()` implemented
- Refund policy demo created
- Go collector created
- SQLite persistence implemented
- Collector trace ingestion implemented
- Collector trace list/detail APIs implemented
- React Dashboard MVP created
- Trace list page implemented
- Trace detail page implemented
- Retrieved chunk viewer implemented
- LLM prompt/response viewer implemented
- Warning Engine implemented in collector
- Warning rules implemented:
  - `no_retrieved_chunks`
  - `low_retrieval_score`
  - `duplicate_chunks`
  - `conflicting_chunks`
  - simplified `answer_not_grounded`
- Warning persistence after trace ingestion implemented
- Dashboard real warning cards implemented
- Dashboard null-warning crash fixed
- `.gitignore` updated for local artifacts
- Warning smoke test implemented: `sdk/python/examples/warning_rules_demo.py`
- Real Local RAG Demo completed:
  - local markdown policy docs
  - local document loader
  - deterministic chunking
  - TF-IDF + cosine retriever
  - simple local answerer
  - demo case matrix
  - traced cases verified against collector on `:4319`

## Current Working Path

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
React Dashboard
```

## Current Milestone

Real Local RAG Demo (Completed).

Current active work is documentation and demo cleanup.
Current active work is final smoke validation and screenshot preparation.

## Files Likely To Change Next

Documentation:

- `README.md`
- `sdk/python/examples/local_rag_demo/README.md`
- `docs/demo/LOCAL_RAG_DEMO.md`
- `docs/demo/WARNING_RULES.md`
- `docs/demo/SMOKE_TEST.md`
- `docs/ai-context/ROADMAP.md`
- `docs/ai-context/DEVLOG.md`
- `docs/ai-context/AI_HANDOFF.md`

## Initial Warning Rules

Warning rules implemented in v0.1:

- [x] `no_retrieved_chunks`
- [x] `low_retrieval_score`
- [x] `duplicate_chunks`
- [x] `conflicting_chunks`
- [x] simplified `answer_not_grounded`

Smoke test entrypoint:

- `python -m examples.warning_rules_demo all`
- expected result: each case returns `warnings_generated: 1`

## Key Decision

Warning generation should live in the Go collector for v0.1.

Reason:

The collector already receives the full trace payload, owns local persistence, and can generate warnings immediately after storing traces and spans.

The Python SDK should remain lightweight and focused on instrumentation.

## Next Step

Final smoke test / screenshot pass:

- run scripts from clean root invocation and record pass/fail
- validate expected warning mapping for five local RAG demo traces
- capture dashboard screenshots for conflict/hallucinated/no_match traces
- freeze demo docs for handoff
- then start warning/test hardening in a focused quality pass

Keep LangChain/LlamaIndex integration deferred until this milestone is complete.

The next successful validation should be:

1. Run real local retrieval demo.
2. Send trace via SDK `flush()` to collector on `:4319`.
3. Collector persists traces, spans, and warnings.
4. Dashboard trace detail displays real chunks, scores, and warnings.