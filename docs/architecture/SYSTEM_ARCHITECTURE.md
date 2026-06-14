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

- The `warnings` table exists, but warning generation is not implemented yet.

### React Dashboard

The dashboard runs locally with Vite.

It reads collector APIs and displays:

- trace list
- trace detail
- span timeline
- retrieval chunks
- LLM prompt and response
- metadata
- warning placeholder

## Current Data Flow

1. Developer runs a RAG app instrumented with the Python SDK.
2. SDK records retrieval and LLM spans.
3. SDK calls `t.flush()`.
4. Collector receives the trace payload.
5. Collector stores trace and spans in SQLite.
6. Dashboard fetches traces from the collector.
7. Developer inspects the RAG pipeline in the browser.

## Next Architecture Addition

The next component is the warning engine.

It will run inside the Go collector after trace ingestion and before the response is returned from `POST /api/traces`.

Future flow:

```text
POST /api/traces
  -> save trace/spans
  -> run warning engine
  -> save warnings
  -> return stored response with warnings_generated
```