# System Architecture

## Current v0.1 Architecture

RAGLens currently runs as local-first components:

```text
Python SDK
  -> Go Collector
  -> SQLite

React Dashboard
  <- Go Collector API
```

## Components

### Python SDK

The Python SDK instruments a RAG pipeline.

It records:

- trace metadata
- retrieval spans
- retrieved chunks
- LLM calls
- final answer

It sends trace payloads to the collector using:

- `POST /api/traces`

### Go Collector

The collector is a local HTTP service, running by default at:

- `http://localhost:4319`

Implemented endpoints:

- `GET /health`
- `POST /api/traces`
- `GET /api/traces`
- `GET /api/traces/{trace_id}`

The collector validates incoming trace payloads and persists data to SQLite.

### SQLite

SQLite is the local storage backend.

Current tables:

- `traces`
- `spans`
- `warnings`

Note:

- Warning generation is implemented in the Go collector.
- The first live diagnosis rule is `conflicting_chunks`.

### React Dashboard

The dashboard runs locally with Vite.

It reads collector APIs and displays:

- trace list
- trace detail
- span timeline
- retrieval chunks
- LLM prompt and response
- metadata
- warning cards

## Current Data Flow

1. Developer runs a RAG app instrumented with the Python SDK.
2. SDK records retrieval and LLM spans.
3. SDK calls `t.flush()`.
4. Collector receives the trace payload.
5. Collector stores trace and spans in SQLite.
6. Collector runs the warning engine.
7. Collector stores generated warnings in SQLite.
8. Dashboard fetches traces from the collector.
9. Developer inspects spans and warnings in the browser.

## Warning Engine Flow

The warning engine runs inside the Go collector after trace ingestion and before the response is returned from `POST /api/traces`.

Current flow:

```text
POST /api/traces
  -> save trace/spans
  -> run warning engine
  -> save warnings
  -> return stored response with warnings_generated
```