# Devlog

## 2026-06-30 (Platform-Specific Script Folders)

### Completed

- Split repository startup scripts into platform-specific folders:
  - `scripts/windows` for PowerShell entry points
  - `scripts/mac` for Bash entry points
- Added macOS shell wrappers for collector, dashboard, demo trace generation, and smoke testing.
- Added one-click `start-all` launchers for macOS and Windows to start collector and dashboard together.
- Updated README quickstart and shortcut commands to point at the new platform-specific script paths.

### Notes

- macOS scripts are executable Bash entry points and can be run with `bash ./scripts/mac/...`.
- Windows scripts remain PowerShell-based and now live under `scripts/windows`.

## 2026-06-22 (Dashboard UI Polish + Final v0.1 Release Prep)

### Completed

- Dashboard sidebar trace list: added text truncation for query and answer fields
  - Query: max 2 lines, ellipsis overflow
  - Answer: max 3 lines, ellipsis overflow
  - Ensures uniform card heights regardless of content length
- Final answer card in trace detail:
  - Repositioned from floating window to grid layout with Query/Duration/Warnings
  - Added inline vertical resizing with `resize: vertical` CSS
  - Scrollable content area for long answers
  - Removed nested border structure (single outer card border)
  - Initial height: 92px min, 320px max, user-adjustable
- README aligned with current screenshots and feature set
- All dashboard, SDK, collector, and documentation paths verified and consistent

### Notes

- Sidebar truncation prevents layout explosion when some traces have very long final answers
- Final answer card resizing allows users to expand/collapse inline without moving page flow
- UI changes improve dashboard readability for both quick scanning (list view) and detailed inspection (detail view)

## 2026-06-22 (Demo Packaging Progress + Final Smoke Validation)

### Completed

- Ran startup and demo scripts from repository root:
  - `scripts/start-collector.ps1`
  - `scripts/start-dashboard.ps1`
  - `scripts/demo-trace-all.ps1`
  - `scripts/smoke.ps1`
- Verified `trace-all` completed with `Generated traces: 5` and `Failed traces: 0`.
- Verified expected warning mapping via collector API for generated trace IDs.
- Aligned README and demo docs command paths with actual directories:
  - collector path -> `collector/go`
  - dashboard path -> `dashboard/web`
- Added cross-links across demo docs:
  - `LOCAL_RAG_DEMO.md` <-> `WARNING_RULES.md` <-> `SMOKE_TEST.md`

### Acceptance Snapshot

- Collector health: pass
- Dashboard starts: pass
- trace-all runs: pass
- no_match warning: pass
- low_score warning: pass
- duplicate warning: pass
- conflict warning: pass
- hallucinated warning: pass
- Trace detail readable: pass
- README commands accurate: pass

### Notes

- Conflict trace can include an additional warning alongside `conflicting_chunks` in some runs.
- For acceptance, conflict case validation checks that `conflicting_chunks` is present.

## 2026-06-21 (Real Local RAG Demo Documentation and Milestone Closeout)

### Completed

- Finalized documentation for the Real Local RAG Demo milestone.
- Updated local demo runbook in `sdk/python/examples/local_rag_demo/README.md` for new developers.
- Synced milestone-complete status across AI handoff, roadmap, and current task docs.
- Documented verified command set and expected warning-target case mapping.

### What Was Built (Milestone Summary)

- local markdown policy corpus
- local loader
- deterministic chunker
- TF-IDF plus cosine retriever
- simple local answerer
- SDK trace integration to collector on `:4319`
- dashboard verification of real retrieval traces and warning cards

### Why TF-IDF Was Chosen

- Fully local-first and easy to run in v0.1.
- Transparent scoring behavior for debugging and explanation.
- Minimal dependency and infrastructure complexity.
- Good baseline before semantic retriever comparison.

### What Was Verified

- End-to-end flow from SDK flush to collector to SQLite to dashboard.
- Real retrieved chunks include ids, source, rank, text, and scores.
- Warning cards render from real retrieval output, not only synthetic fixtures.

### Warning Rules Triggered In Verified Cases

- `no_retrieved_chunks` via `no_match`
- `low_retrieval_score` via `low_score`
- `duplicate_chunks` via `duplicate`
- `conflicting_chunks` via `conflict`
- simplified `answer_not_grounded` via `hallucinated`

### Deferred By Design

- LangChain adapter integration
- LlamaIndex adapter integration
- Vector database integration
- External embedding providers

These remain intentionally deferred until DX hardening and test coverage improve.

## 2026-06-15 (Real Local RAG Milestone Completed)

### Completed

- Marked Real Local RAG Demo milestone as completed across milestone, roadmap, task, and handoff docs.
- Captured completed implementation scope:
  - local markdown policy documents
  - local document loader
  - deterministic chunking
  - TF-IDF + cosine retriever
  - simple local answerer
  - demo case matrix
  - traced integration through existing SDK schema
  - collector ingestion on `:4319`
  - dashboard verification
  - warning trigger verification on real retrieval output

### Notes

- Added explicit demo command runbook to the milestone and handoff docs.
- Shifted active focus to post-milestone hardening (warning explanations, tests, semantic retriever evaluation).

## 2026-06-15 (Real Local RAG Docs)

### Completed

- Added `docs/ai-context/REAL_LOCAL_RAG_MILESTONE.md` to define active milestone scope, exit criteria, runbook, and non-goals.
- Added `docs/architecture/LOCAL_RETRIEVAL_BASELINE.md` to document current local retrieval implementation (chunking + TF-IDF + cosine).

### Notes

- Current retriever baseline is intentionally lexical and transparent.
- Framework adapters remain deferred until Real Local RAG Demo is validated.

## 2026-06-15 (Docs Sync)

### Completed

- Updated core docs to reflect that Warning Engine / Diagnosis Layer MVP is complete.
- Synced status across README, roadmap, handoff, current task, architecture, and product docs.
- Marked Real Local RAG Demo as the next active milestone.

### Notes

- Warning rules now documented as implemented: `no_retrieved_chunks`, `low_retrieval_score`, `duplicate_chunks`, `conflicting_chunks`, simplified `answer_not_grounded`.
- `sdk/python/examples/warning_rules_demo.py` documented as primary warning smoke test.

## 2026-06-15

### Completed

- Updated `sdk/python/examples/warning_rules_demo.py` to call `print_and_flush(t)` after exiting each `with trace(...)` block.
- Ensured all five warning-rule smoke demos finalize trace lifecycle before serialization and POST.

### Validation

Ran all warning demos:

```bash
cd sdk/python
python -m examples.warning_rules_demo all
```

Observed result:

- All five demos still return `warnings_generated: 1`.
- `trace.ended_at` is now populated (no longer `null`) across all demo payloads.
- `trace.duration_ms` is now populated as `0` for this fast local smoke run (no longer `null`).

### Notes

This keeps demo payload timing fields compatible with timeline rendering and future latency-oriented warning logic.

## 2026-06-13

### Completed

- Added Warning Engine in the Go collector.
- Implemented the first diagnosis rule: `conflicting_chunks`.
- Collector now generates and persists warnings after storing trace payloads.
- Dashboard trace detail now renders real warning cards.
- Refund policy demo now reliably triggers one warning for conflicting `30 days` vs `14 days` refund-policy chunks.

### Validation

Collector health check:

```powershell
Invoke-RestMethod http://localhost:4319/health
```

Demo execution:

```bash
cd sdk/python
python -m examples.refund_policy_demo
```

Observed result:

- Trace is ingested and persisted.
- `conflicting_chunks` warning is generated and stored.
- Warning appears on dashboard trace detail.

### Notes

RAGLens now has an end-to-end diagnosis path from ingestion to UI rendering.

The warning engine is intentionally incremental in v0.1: start with one high-signal rule, validate the full loop, then add additional rules.

### Next Step

Expand warning coverage with the next rules:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- simplified `answer_not_grounded`

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