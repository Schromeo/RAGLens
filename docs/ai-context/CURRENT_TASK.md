# Current Task

## Current Focus
Implement the first RAGLens diagnosis layer.

The Python SDK, Go collector, SQLite persistence, and initial React Dashboard are now working.

RAGLens can generate a trace from the Python SDK, send it to the local collector, persist it in SQLite, and display it in the browser dashboard.

## Current Goal
Add a basic warning engine that generates lightweight diagnostic warnings from stored trace/span data.

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
- Warning placeholder implemented
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

Build the first warning engine.

The initial warning engine should inspect trace payloads after ingestion and insert warning records into SQLite.

## Files Likely To Change Next

Go Collector:

- `collector/go/internal/warnings/engine.go`
- `collector/go/internal/storage/sqlite.go`
- `collector/go/internal/api/handlers.go`
- `collector/go/internal/models/models.go`

Dashboard:

- `dashboard/web/src/pages/TraceDetailPage.tsx`
- `dashboard/web/src/components/WarningCard.tsx`

Documentation:

- `docs/ai-context/DEVLOG.md`
- `docs/ai-context/DECISIONS.md`
- `docs/architecture/SYSTEM_ARCHITECTURE.md`

## Initial Warning Rules

Start with simple heuristic rules:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- `conflicting_chunks`
- simplified `answer_not_grounded`

The refund policy demo should trigger a conflicting_chunks warning because retrieved chunks contain both 30 days and 14 days refund windows.

## Key Decision

Warning generation should live in the Go collector for v0.1.

Reason:

The collector already receives the full trace payload, owns local persistence, and can generate warnings immediately after storing traces and spans.

The Python SDK should remain lightweight and focused on instrumentation.

## Next Step

Create the initial warning engine under:

- `collector/go/internal/warnings`

Then call it from POST /api/traces after saving the trace payload.

The first successful validation should be:

1. Run the refund policy demo.
2. Send the trace to the collector.
3. Collector generates a warning.
4. Dashboard displays the warning in the trace detail page.