# Current Task

## Current Focus
v0.1 Release MVP Complete and Demo Polish.

The Python SDK, Go collector, SQLite persistence, React Dashboard MVP, and Real Local RAG Demo are all working and validated.

RAGLens can generate a trace from the Python SDK, send it to the local collector, persist it in SQLite, and display it in the browser dashboard with real warnings.

## Current Goal
Finalize v0.1 release presentation and prepare for v0.2 developer integration work.
Complete dashboard UI polish and ensure all documentation is aligned.

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
Current active work is final smoke validation and screenshot preparation.

## Files Recently Updated

Documentation (synchronized with v0.1 completion):

- `README.md` - added Screenshots section with trace overview, conflict, and grounding examples
- `docs/ai-context/ROADMAP.md` - marked v0.1 complete, outlined v0.2 developer integration
- `docs/ai-context/DEVLOG.md` - latest entries document final smoke validation and UI polish
- `docs/ai-context/AI_HANDOFF.md` - updated with v0.1 completion status
- `sdk/python/examples/local_rag_demo/README.md` - demo runbook complete
- `docs/demo/LOCAL_RAG_DEMO.md` - demo documentation complete
- `docs/demo/WARNING_RULES.md` - warning rule documentation complete
- `docs/demo/SMOKE_TEST.md` - smoke test guide complete

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

## v0.1 Validation Complete

All validation gates passed:

- [x] run scripts from clean root invocation and record pass/fail
- [x] validate expected warning mapping for five local RAG demo traces
- [x] capture dashboard screenshots for conflict/hallucinated/no_match traces
- [x] freeze demo docs for handoff
- [x] dashboard UI polish (sidebar text truncation, Final answer card resizing)
- [x] README aligned with screenshots and current feature set
- [x] ROADMAP and docs synchronized

## Next Milestone

Preparing for v0.2 Developer Integration / User Onboarding:

- User onboarding documentation
- Python SDK integration guide
- Custom pipeline example
- Stable trace/chunk schema documentation
- Local startup command consolidation (Docker Compose / improved scripts)

LangChain/LlamaIndex adapters remain deferred until v0.2 schema and warning behavior stabilize.