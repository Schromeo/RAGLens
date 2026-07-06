# Current Task

## Current Focus

RAGLens v0.1 is complete and smoke-tested.

RAGLens v0.2 Developer Integration / Local SDK Onboarding is complete, documented, and smoke-tested.

RAGLens is now starting v0.3 - RAG Quality Analysis / Diagnostic Intelligence.

The project now has:

* user onboarding documentation
* a Python SDK integration guide
* a custom pipeline integration example
* a cross-platform repo-local startup helper
* a README that explains both the built-in demo path and the real SDK integration path
* SDK packaging hygiene for the local editable install path
* a root README documentation map to separate user docs from maintainer docs

## Current Goal

Start and define v0.3 RAG Quality Analysis / Diagnostic Intelligence.

Current focus:

- design Warning Schema v2
- design DiagnosticObject structure
- define evidence-backed warning details
- define the first deterministic diagnostic rules
- define dashboard evidence-backed warning UX

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
  - `conflicting_chunks`
  - simplified `answer_not_grounded`
- Real Local RAG Demo completed and verified
- `docs/product/USER_ONBOARDING.md` completed
- `docs/integrations/PYTHON_SDK_GUIDE.md` completed
- `sdk/python/examples/custom_pipeline_demo.py` added
- `scripts/start-raglens.py` added and polished
- `README.md` updated with two Quickstart paths

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

Status: starting.

## Smoke-Tested Validation

The following commands passed:

```bash
python scripts/start-raglens.py
cd sdk/python
python -m examples.custom_pipeline_demo
python -m examples.local_rag_demo.run_demo trace-all
```

Verified in dashboard:

- `custom-rag-pipeline`
- built-in local RAG demo traces
- warning-focused demo traces and warning cards

Milestone status:

- v0.1 completed and smoke-tested
- v0.2 completed and smoke-tested

## Files Recently Updated

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
- `conflicting_chunks`
- simplified `answer_not_grounded`

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

Design and specify v0.3 RAG Quality Analysis / Diagnostic Intelligence.

Recommended next options:

1. Define warning schema v2 and evidence-backed warning detail payloads.
2. Define DiagnosticObject and EvidenceItem structures for deterministic warning analysis.
3. Design improved grounding/retrieval diagnostics and dashboard warning details.
4. Keep optional LLM-assisted diagnostics as later/future, not default local path.

Future TraceForge direction note:

- agent harness observability capabilities such as running traces, partial ingestion, agent/tool/retry spans, and no-progress diagnostics remain future-only and are not part of current v0.3 implementation scope.
