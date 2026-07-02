# AI Handoff

## Project Name

RAGLens

## One-liner

RAGLens is a local-first visual debugger for RAG pipelines.

## Current Project Status

### v0.1 Status

**v0.1 Local RAG Debugger MVP is complete and smoke-tested.**

Completed v0.1 foundation:

* Python SDK tracing foundation
* Go collector ingestion APIs
* SQLite trace/span/warning persistence
* React dashboard MVP
* Warning Engine / Diagnosis Layer MVP
* Real Local RAG Demo
* Demo packaging / developer experience

### v0.2 Status

**v0.2 Developer Integration / Local SDK Onboarding is complete and smoke-tested.**

Current completed v0.2 work:

* `docs/product/USER_ONBOARDING.md`
* `docs/integrations/PYTHON_SDK_GUIDE.md`
* `sdk/python/examples/custom_pipeline_demo.py`
* `scripts/start-raglens.py`
* `README.md` two-path quickstart
* root README documentation map
* SDK packaging hygiene (`sdk/python` version `0.2.0`, local SDK README, local editable install path)

## Current Implemented Flow

```text
Python SDK
  ↓
trace()
  ↓
retrieval span + LLM span
  ↓
t.flush()
  ↓
POST /api/traces
  ↓
Go Collector (:4319)
  ↓
SQLite
  ↓
React Dashboard
```

## Exact Commands That Passed

Validated commands:

```bash
python scripts/start-raglens.py
cd sdk/python
python -m examples.custom_pipeline_demo
python -m examples.local_rag_demo.run_demo trace-all
```

Verified results:

* dashboard showed `custom-rag-pipeline`
* dashboard showed built-in local RAG demo traces
* dashboard showed warning-focused demo traces and warning cards

## Files Added or Updated

Core v0.2 onboarding artifacts:

* `docs/product/USER_ONBOARDING.md`
* `docs/integrations/PYTHON_SDK_GUIDE.md`
* `sdk/python/examples/custom_pipeline_demo.py`
* `scripts/start-raglens.py`
* `README.md`
* `sdk/python/pyproject.toml`
* `sdk/python/README.md`

Status docs refreshed:

* `docs/ai-context/ROADMAP.md`
* `docs/ai-context/CURRENT_TASK.md`
* `docs/ai-context/DEVLOG.md`
* `docs/ai-context/AI_HANDOFF.md`

## Current Implemented Span Types

Only these span types are implemented today:

* `retrieval`
* `llm`

Do not claim tool spans, memory spans, verification spans, human feedback spans, or agent tracing as implemented.

## Current Warning Rules

Implemented rules:

* `no_retrieved_chunks`
* `low_retrieval_score`
* `duplicate_chunks`
* `conflicting_chunks`
* simplified `answer_not_grounded`

Important limitation:

* `answer_not_grounded` is still a simplified deterministic rule, not a full grounding evaluator.

## Current Limitations

Current scope limits:

* only `retrieval` and `llm` spans are implemented
* onboarding path is local-first and repo-based
* editable install from local checkout is the supported SDK path today
* no agent/tool/memory spans
* no Docker Compose local setup yet
* no packaged CLI yet
* no PyPI publishing yet
* no LangChain or LlamaIndex adapters yet
* no raw OpenAI or Anthropic integration guides in current scope
* no cloud sync, auth, hosted collector, or hosted features
* no full LLM-as-judge grounding evaluator

## Current Positioning

RAGLens is:

* a local-first visual debugger for RAG pipelines
* a local trace and debugging layer for existing RAG apps
* useful both with the built-in demo and with user-owned Python RAG pipelines instrumented through the SDK

RAGLens is not:

* a chatbot framework
* a vector database
* a training framework
* a hosted AI platform
* a replacement for the user's RAG app

## Recommended Next Milestone

### v0.3 — RAG Quality Analysis / Diagnostic Intelligence

Recommended direction:

* warning schema v2
* evidence-backed warning details
* improved `answer_not_grounded` heuristics
* numeric/date/entity grounding checks
* retrieval quality diagnostics
* conflict detection v2
* dashboard warning detail improvements
* optional future LLM-assisted diagnostics later, not default local path

## Important Guardrails

Still future direction only, not current implementation:

* tool spans
* memory spans
* verification spans
* human feedback spans
* agent tracing
* cloud sync
* hosted collector
* auth
* full harness-level TraceForge behavior
