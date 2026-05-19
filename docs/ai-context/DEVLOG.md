# Devlog

## 2026-05-14

### Completed

- Chose RAGLens as the first product cut.
- Defined the long-term path: RAGLens -> AgentOps Lite -> TraceForge.
- Decided to start with a local-first visual debugger for RAG pipelines.
- Created the initial repository documentation plan.

### Key Decisions

- Start narrow with RAG debugging instead of building a full LLMOps platform.
- Keep v0.1 local-first.
- Prioritize usability, visual clarity, and easy setup.
- Use project docs as long-term memory for AI collaboration.

### Next

- Create the initial repo structure.
- Write PRODUCT_SPEC.md.
- Design the trace/span data model.
- Decide the first implementation order.

## 2026-05-15

### Completed

- Defined the v0.1 product direction for RAGLens.
- Confirmed that RAGLens starts as a local-first visual debugger for RAG pipelines.
- Established the long-term architecture direction: start with RAG debugging, while keeping the internal model compatible with future AgentOps/TraceForge-style tracing.
- Created the initial product specification in `docs/product/PRODUCT_SPEC.md`.
- Defined the initial trace/span data model in `docs/architecture/TRACE_DATA_MODEL.md`.
- Decided that the developer-facing Python API should stay simple, while the internal representation uses traces and spans.
- Defined the core v0.1 entities:
  - Trace
  - Span
  - Retrieval chunk
  - LLM span
  - Warning
- Defined the initial SQLite schema for:
  - `traces`
  - `spans`
  - `warnings`
- Implemented the first minimal Python SDK.
- Added a `trace()` context manager.
- Added support for recording retrieval spans.
- Added support for recording LLM spans.
- Created the refund policy demo.
- Verified that the SDK can generate a complete trace payload locally.
- Pushed the initial documentation and SDK code to GitHub.

### Key Decisions

- RAGLens v0.1 will use a local-first architecture.
- SQLite will be the default local storage backend.
- The Python SDK will expose a simple API:
  - `trace(name)`
  - `t.retrieval(...)`
  - `t.llm(...)`
- Internally, RAGLens will represent RAG pipeline activity using a trace/span model.
- A trace represents one complete RAG request.
- A span represents one step inside the pipeline, such as retrieval or LLM generation.
- The initial span types are:
  - `retrieval`
  - `prompt`
  - `llm`
  - `custom`
- Warning rules will start as lightweight heuristics, not ML-based evaluation.

### Validation

Ran the refund policy demo locally:

```bash
cd sdk/python
python -m examples.refund_policy_demo
```

The SDK successfully generated a trace payload containing:

- One trace named refund-policy-qa
- One retrieval span named search_refund_docs
- Two retrieved chunks:
  - refund_policy_new.md, version 2026, refund window 30 days
  - refund_policy_old.md, version 2024, refund window 14 days
- One LLM span named generate_answer
- A final answer using the outdated 14 days refund window

### Notes

This is the first runnable milestone for RAGLens.

The project now has both:

- A documented product and architecture direction
- A working Python SDK prototype that can generate structured trace payloads

The current SDK only prints trace JSON locally.

The next step is to build the Go collector so the SDK can send traces to a local HTTP endpoint and persist them in SQLite.

### Next Step

Build the local Go collector.

Initial collector scope:

- GET /health
- POST /api/traces
- SQLite persistence
- GET /api/traces
- GET /api/traces/{trace_id}

## 2026-05-15

### Completed

- Implemented the initial Go collector.
- Added `GET /health`.
- Added `POST /api/traces`.
- Added SQLite-backed local persistence.
- Added storage for traces and spans.
- Verified that the collector can receive a Python SDK-generated trace payload.
- Verified that the collector stores trace data in local SQLite.

### Validation

Started the collector locally:

```bash
cd collector/go
go run ./cmd/raglens-collector
```

Checked collector health:

```powershell
Invoke-RestMethod http://localhost:4319/health
```

Posted a sample trace payload:

```powershell
Invoke-RestMethod `
  -Uri http://localhost:4319/api/traces `
  -Method POST `
  -ContentType "application/json" `
  -InFile sample_trace.json
```

The collector returned:

```json
{
  "status": "stored",
  "warnings_generated": 0
}
```

### Notes

The local collector can now receive and persist trace payloads.

The next step is to add a flush() method to the Python SDK so demo traces can be sent directly to the collector without manually copying JSON into a file.

### Commit

```bash
git add .
git commit -m "feat(collector): add Go collector with SQLite persistence"
git push
```

## 2026-05-18

### Completed

- Added `flush()` support to the Python SDK.
- Added `collector_url` support to the trace context manager.
- Updated the refund policy demo to send traces directly to the local collector.
- Verified that the Python SDK can POST trace payloads to `POST /api/traces`.
- Verified that the Go collector returns a successful stored response.

### Validation

Started the collector:

```bash
cd collector/go
go run ./cmd/raglens-collector
```

Ran the Python demo:

```bash
cd sdk/python
python -m examples.refund_policy_demo
```

The SDK generated a trace payload and sent it to the collector.

Collector response:

```json
{
  "trace_id": "trace_af404e92216b4f7f97fb415208dc5992",
  "status": "stored",
  "warnings_generated": 0
}
```

### Notes

RAGLens now has a working local trace ingestion path from Python SDK to Go collector to SQLite.

The next step is to build the initial React Dashboard so traces can be inspected visually instead of through raw JSON.
