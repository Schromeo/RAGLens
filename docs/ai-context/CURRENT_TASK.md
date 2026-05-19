# Current Task

## Current Focus

Build the initial React dashboard on top of the working local ingestion path.

The documentation baseline, trace/span data model, Python SDK, Go collector, and SQLite storage are already in place.

## Current Goal

Make stored traces inspectable in a browser with a minimal but useful dashboard.

The first dashboard slice should cover:

- Trace list
- Trace detail
- Span timeline/readout
- Retrieval chunk inspection
- Raw JSON fallback panel for debugging

## Current System Status

Completed and verified so far:

- Product direction and MVP scope docs
- Trace/span architecture and data model docs
- Python SDK trace context manager
- Retrieval span logging
- LLM span logging
- Python SDK `flush()` support
- Go collector HTTP APIs
  - `GET /health`
  - `POST /api/traces`
  - `GET /api/traces`
  - `GET /api/traces/{trace_id}`
- SQLite persistence for traces, spans, and warnings
- End-to-end local pipeline validation

Current validated path:

```text
Python demo -> SDK trace/span -> flush() -> POST /api/traces -> Go collector -> SQLite -> GET /api/traces -> GET /api/traces/{trace_id}
```

## Scope Clarification

Current trace content is demo-driven (mock retrieval/LLM payload values), but transport and persistence are real.

This means infrastructure is validated, while production data integrations are still pending.

## Primary Files Involved

- `sdk/python/raglens/trace.py`
- `sdk/python/examples/refund_policy_demo.py`
- `collector/go/internal/api/handlers.go`
- `collector/go/internal/storage/sqlite.go`
- `collector/go/internal/models/models.go`
- `dashboard/web/src/App.tsx`
- `dashboard/web/src/pages/HomePage.tsx`
- `dashboard/web/src/components/TraceViewer.tsx`
- `dashboard/web/src/api/client.ts`

## Immediate Next Steps

1. Implement dashboard API client for list/detail endpoints.
2. Build trace list page from `GET /api/traces`.
3. Build trace detail page from `GET /api/traces/{trace_id}`.
4. Render spans and retrieval chunks in a readable layout.
5. Add empty-state and error-state handling.
6. Keep warning UI as placeholder until warning rules are implemented.

## Out of Scope For This Step

- Cloud deployment or multi-tenant features
- Auth/billing
- Advanced warning engine logic
- Non-local infrastructure changes
