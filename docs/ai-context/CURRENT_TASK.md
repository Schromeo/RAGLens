# Current Task

## Current Focus
Post-Real Local RAG Demo hardening and quality improvements.

The Python SDK, Go collector, SQLite persistence, and initial React Dashboard are now working.

RAGLens can generate a trace from the Python SDK, send it to the local collector, persist it in SQLite, and display it in the browser dashboard.

The Warning Engine / Diagnosis Layer MVP is complete.
The Real Local RAG Demo milestone is complete.

## Current Goal
Improve warning explainability, add tests, and stabilize the real local retrieval path for iteration.

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

Current active work is follow-up hardening.

## Files Likely To Change Next

Python demo / retrieval prototype:

- `sdk/python/examples/`
- `examples/refund-policy-demo/docs/`

Go Collector:

- `collector/go/internal/warnings/engine.go`

Optional collector updates only if needed for real retrieval metadata compatibility.

Dashboard:

- `dashboard/web/src/pages/TraceDetailPage.tsx`

Mostly validation; no major UI changes required for this milestone.

Documentation:

- `README.md`
- `docs/ai-context/ROADMAP.md`
- `docs/ai-context/DEVLOG.md`
- `docs/ai-context/DECISIONS.md`

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

Implement post-milestone hardening tasks:

- Improve warning detail display and wording.
- Add unit tests for warning rules.
- Add retrieval demo assertions for expected warning targets.
- Evaluate semantic retrieval baseline while preserving existing trace schema.

Keep LangChain/LlamaIndex integration deferred until this milestone is complete.

The next successful validation should be:

1. Run real local retrieval demo.
2. Send trace via SDK `flush()` to collector on `:4319`.
3. Collector persists traces, spans, and warnings.
4. Dashboard trace detail displays real chunks, scores, and warnings.