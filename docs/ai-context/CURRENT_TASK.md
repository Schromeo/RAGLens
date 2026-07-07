# Current Task

## Current Focus

RAGLens v0.1 is complete and smoke-tested.

RAGLens v0.2 Developer Integration / Local SDK Onboarding is complete, documented, and smoke-tested.

RAGLens v0.3 Diagnostic Intelligence core is now implemented and smoke-tested.

The project now has:

* user onboarding documentation
* a Python SDK integration guide
* a custom pipeline integration example
* a cross-platform repo-local startup helper
* a README that explains both the built-in demo path and the real SDK integration path
* SDK packaging hygiene for the local editable install path
* a root README documentation map to separate user docs from maintainer docs

## Current Goal

Document the completed v0.3 diagnostic intelligence core and prepare the next follow-up slice.

Current focus:

- finalize v0.3 implementation documentation
- capture smoke-tested validation status
- identify the next narrow follow-up after the core milestone

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
  - `weak_query_chunk_overlap`
  - `conflicting_chunks` with evidence-backed v2 details
  - `answer_not_grounded` with evidence-backed v2 details
  - `numeric_mismatch`
- Real Local RAG Demo completed and verified
- `docs/product/USER_ONBOARDING.md` completed
- `docs/integrations/PYTHON_SDK_GUIDE.md` completed
- `sdk/python/examples/custom_pipeline_demo.py` added
- `scripts/start-raglens.py` added and polished
- `README.md` updated with two Quickstart paths
- `sdk/python/examples/diagnostic_quality_demo.py` covers all current v0.3 core warning cases
- dashboard warning detail cards show evidence previews, numeric value diffs, and recommended actions

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

v0.3 RAG Quality Analysis / Diagnostic Intelligence.

Status: core implemented and smoke-tested.

## Smoke-Tested Validation

The following commands passed:

```bash
cd collector/go
go test ./...

cd dashboard/web
npm run build

python scripts/start-raglens.py
cd sdk/python
python -m examples.custom_pipeline_demo
python -m examples.local_rag_demo.run_demo trace-all
python -m examples.diagnostic_quality_demo all
```

Additional backend test coverage added:

```bash
cd collector/go
go test ./... -count=1
```

Covered:

- warning engine unit tests for v0.3 rules
- SQLite Warning Schema v2 round-trip persistence
- legacy warning table migration for v2 columns
- API handler coverage for v0.3 warning generation and trace-detail response fields

Verified in dashboard:

- `custom-rag-pipeline`
- built-in local RAG demo traces
- warning-focused demo traces and warning cards
- evidence-backed warning detail sections
- numeric mismatch value-diff block
- recommended action label in warning detail cards

Milestone status:

- v0.1 completed and smoke-tested
- v0.2 completed and smoke-tested
- v0.3 diagnostic intelligence core completed and smoke-tested

## Files Recently Updated

- `collector/go/internal/warnings/engine.go` - v0.3 evidence-backed diagnostics and rule logic
- `dashboard/web/src/pages/TraceDetailPage.tsx` - evidence-backed warning rendering and recommended action label
- `dashboard/web/src/style.css` - warning detail and responsive layout polish
- `sdk/python/examples/diagnostic_quality_demo.py` - deterministic v0.3 diagnostic demo cases
- `docs/product/V0_3_DIAGNOSTIC_INTELLIGENCE.md` - v0.3 scope and diagnostic intelligence design spec
- `README.md` - two-path v0.2 quickstart for built-in demo and real SDK integration
- `docs/product/USER_ONBOARDING.md` - developer onboarding flow for existing RAG apps
- `docs/integrations/PYTHON_SDK_GUIDE.md` - current Python SDK API guide
- `sdk/python/examples/custom_pipeline_demo.py` - minimal local integration example
- `scripts/start-raglens.py` - cross-platform repo-local startup helper
- `sdk/python/pyproject.toml` - SDK package version and README path aligned for v0.2
- `sdk/python/README.md` - concise SDK package README for local install and API usage
- `docs/ai-context/ROADMAP.md` - v0.2 status updated
- `docs/ai-context/DEVLOG.md` - v0.2 completion notes
- `docs/ai-context/AI_HANDOFF.md` - refreshed handoff and next milestone options

## Current Guardrails

- Do not start LangChain adapters.
- Do not start LlamaIndex adapters.
- Do not start PyPI work.
- Do not start Docker work.
- Do not start CLI work.
- Do not start packaging work beyond the current local editable SDK path.
- Do not add agent spans.
- Do not add tool spans.
- Do not add memory spans.
- Do not make LLM-as-judge the default path.
- Continue local-first.
- Continue deterministic-first.

## Current Implementation Limits

Current implemented span types:

- `retrieval`
- `llm`

Current warning rules:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- `weak_query_chunk_overlap`
- `numeric_mismatch`
- `conflicting_chunks` with evidence-backed v2 details
- `answer_not_grounded` with evidence-backed v2 details

Still not implemented:

- tool spans
- memory spans
- verification spans
- human feedback spans
- agent tracing
- running traces for multi-step agent harness executions
- partial span ingestion
- retry spans
- diagnostics for agent loops, oscillation, retry storms, and no-progress execution
- cloud sync
- hosted collector
- auth
- full LLM-as-judge grounding evaluation

## Next Task

Choose the next narrow follow-up after the completed v0.3 diagnostic intelligence core.

Recommended next options:

1. v0.3 polish: improve warning grouping / suppression when multiple related diagnostics fire on one trace.
2. v0.3 polish: improve dashboard diagnostic detail views for signals, evidence, and compared values.
3. v0.3 hardening: add focused Go tests for warning rules.
4. v0.3 hardening: add more diagnostic demo cases and acceptance snapshots.
5. Future milestone planning: decide whether v0.4 should focus on tests/hardening, local packaging, or integration adapters.

Guardrail:

Do not start LangChain, LlamaIndex, PyPI, Docker, CLI, agent/tool/memory spans, cloud, auth, or LLM-as-judge work unless explicitly selected as a future milestone.
