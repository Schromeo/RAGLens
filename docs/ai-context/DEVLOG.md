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

## 2026-05-19

### Completed

- Audited task documentation against implemented code and roadmap.
- Reconciled `CURRENT_TASK.md` to remove stale/duplicated initialization-phase content.
- Confirmed current milestone as dashboard implementation on top of the verified local ingestion path.

### Validation

- Verified collector endpoints remain aligned with docs:
  - `GET /health`
  - `POST /api/traces`
  - `GET /api/traces`
  - `GET /api/traces/{trace_id}`
- Verified SDK still supports posting traces through `flush()`.
- Verified dashboard source files exist but are not implemented yet (placeholders/whitespace).

### Notes

Documentation now matches actual project state:

- Infrastructure path is working end-to-end locally.
- Current data values in the demo are mock/sample values.
- The immediate workstream is building the first usable dashboard views.

### Documentation Sync

- Updated `docs/ai-context/ROADMAP.md` to include explicit phase status.
- Marked v0.1 as in progress, with SDK/collector/storage path done and dashboard work next.
- Left v0.2, v0.3, and v0.4 as not started.

## 2026-06-13

### Completed

- Reformatted `docs/ai-context/AI_HANDOFF.md` for readability and consistency.
- Normalized heading hierarchy and section spacing.
- Converted free-form completion/status blocks into structured bullet lists.
- Added clear subsection boundaries for implementation status, known issues, and next step.

### Notes

- This change is documentation-only and does not affect runtime behavior.

## 2026-06-13

### Completed

- Reformatted `docs/ai-context/CURRENT_TASK.md` for consistent Markdown structure.
- Fixed broken section boundaries and unclosed code block in the working path section.
- Standardized file lists and warning rules into clear bullet formatting.
- Converted final validation flow to a numbered checklist.

### Notes

- This change is documentation-only and does not affect runtime behavior.

## 2026-05-19

### Completed

- Added the initial React Dashboard MVP.
- Added trace list UI.
- Added trace detail UI.
- Added span timeline UI.
- Added retrieved chunk cards.
- Added LLM prompt and response viewer.
- Added JSON metadata viewer.
- Added warning placeholder UI.
- Connected the dashboard to the Go collector APIs:
  - `GET /api/traces`
  - `GET /api/traces/{trace_id}`
- Verified that traces generated by the Python SDK can be inspected in the browser.
- Fixed a dashboard blank-screen issue caused by `warnings` being returned as `null`.
- Updated backend/ frontend handling so empty warnings and spans are treated as empty arrays.
- Updated `.gitignore` to exclude local artifacts such as `node_modules`, SQLite databases, Python caches, and sample trace files.

### Validation

Started the collector:

```bash
cd collector/go
go run ./cmd/raglens-collector
```

Generated and flushed a demo trace:

```bash
cd sdk/python
python -m examples.refund_policy_demo
```

Started the dashboard:

```bash
cd dashboard/web
npm install
npm run dev
```

Opened:

- http://localhost:5173

Verified that the dashboard can display:

- local trace list
- selected trace detail
- retrieval span
- retrieved chunks
- LLM prompt
- LLM response
- metadata JSON

### Notes

RAGLens now has a complete local inspection loop:

- Python SDK -> Go Collector -> SQLite -> React Dashboard

The project is ready for the first diagnosis layer.

### Next Step

Implement the warning engine.

The first target warning is conflicting_chunks for the refund policy demo.

## 2026-06-13

### Completed

- Reformatted `docs/ai-context/ROADMAP.md` and removed duplicated v0.1 sections.
- Reorganized roadmap into a single logical sequence: current snapshot -> v0.1 -> v0.2 -> v0.3 -> v0.4 -> future direction.
- Added explicit v0.1 exit criteria to make completion conditions measurable.
- Aligned warning-engine scope language with `CURRENT_TASK.md` and `AI_HANDOFF.md`.

### Notes

- This update is documentation-only and does not change runtime behavior.

## 2026-06-13

### Completed

- Updated `docs/ai-context/ROADMAP.md` to keep a dedicated "Latest Progress (v0.1 Execution Status)" section at the end.
- Preserved roadmap phase order while making newest implementation status easy to find in the final section.

### Notes

- This is a documentation structure decision to separate long-horizon plan from rolling execution status.

## 2026-06-13

### Completed

- Reformatted `docs/architecture/SYSTEM_ARCHITECTURE.md` for consistent heading hierarchy and readable section flow.
- Fixed malformed Markdown structure, including unclosed code block and collapsed plain-text lists.
- Reorganized architecture description into clear sections: components, data flow, and next architecture addition.

### Notes

- This is a documentation-only change and does not affect runtime behavior.