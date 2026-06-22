# Current Task

## Current Focus
Real Local RAG Demo documentation closeout and demo packaging prep.

The Python SDK, Go collector, SQLite persistence, and initial React Dashboard are now working.

RAGLens can generate a trace from the Python SDK, send it to the local collector, persist it in SQLite, and display it in the browser dashboard.

The Warning Engine / Diagnosis Layer MVP is complete.
The Real Local RAG Demo milestone is complete.

## Current Goal
Ensure milestone-complete docs are accurate and usable for first-time developers.
Set up the next iteration around Developer Experience and demo packaging.

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

## Files Likely To Change Next

Documentation:

- `README.md`
- `sdk/python/examples/local_rag_demo/README.md`
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

Developer Experience and Demo Packaging:

- improve top-level and demo README quickstart quality
- add screenshots or short GIF walkthrough for dashboard flow
- reduce local startup friction for first-time users
- polish end-to-end demo script and operator instructions
- then start warning/test hardening in a focused quality pass

Keep LangChain/LlamaIndex integration deferred until this milestone is complete.

The next successful validation should be:

1. Run real local retrieval demo.
2. Send trace via SDK `flush()` to collector on `:4319`.
3. Collector persists traces, spans, and warnings.
4. Dashboard trace detail displays real chunks, scores, and warnings.