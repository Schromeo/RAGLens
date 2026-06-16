# Current Task

## Current Focus
Expand the RAGLens diagnosis layer beyond the first shipped rule.

The Python SDK, Go collector, SQLite persistence, and initial React Dashboard are now working.

RAGLens can generate a trace from the Python SDK, send it to the local collector, persist it in SQLite, and display it in the browser dashboard.

## Current Goal
Add the next set of lightweight warning rules on top of the working warning pipeline.

The goal is not to build a perfect evaluator.

The goal is to surface obvious RAG debugging signals in the dashboard.

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
- `conflicting_chunks` rule implemented
- Warning persistence after trace ingestion implemented
- Dashboard real warning cards implemented
- Dashboard null-warning crash fixed
- `.gitignore` updated for local artifacts

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

Ship additional warning rules on top of the first end-to-end warning flow.

The warning engine already inspects trace payloads after ingestion and inserts warning records into SQLite.

## Files Likely To Change Next

Go Collector:

- `collector/go/internal/warnings/engine.go`
- `collector/go/internal/storage/sqlite.go`
- `collector/go/internal/api/handlers.go`
- `collector/go/internal/models/models.go`

Dashboard:

- `dashboard/web/src/pages/TraceDetailPage.tsx`
- `dashboard/web/src/components/WarningCard.tsx`

Demo / SDK:

- `sdk/python/examples/refund_policy_demo.py`

Documentation:

- `docs/ai-context/DEVLOG.md`
- `docs/ai-context/DECISIONS.md`
- `docs/architecture/SYSTEM_ARCHITECTURE.md`

## Initial Warning Rules

Start with simple heuristic rules:

- [ ] `no_retrieved_chunks`
- [ ] `low_retrieval_score`
- [ ] `duplicate_chunks`
- [x] `conflicting_chunks`
- [ ] simplified `answer_not_grounded`

The refund policy demo now triggers `conflicting_chunks` because retrieved chunks contain both 30 days and 14 days refund windows.

## Key Decision

Warning generation should live in the Go collector for v0.1.

Reason:

The collector already receives the full trace payload, owns local persistence, and can generate warnings immediately after storing traces and spans.

The Python SDK should remain lightweight and focused on instrumentation.

## Next Step

Add the next warning rules under:

- `collector/go/internal/warnings`

The warning engine is already called from `POST /api/traces` after saving the trace payload.

The next successful validation should be:

1. Run the refund policy demo.
2. Send the trace to the collector.
3. Collector generates warnings for additional rule types when conditions match.
4. Dashboard continues to display warning cards in the trace detail page.