# AI Handoff

## Project Name

RAGLens

## One-liner

RAGLens is a local-first visual debugger for RAG pipelines.

## Updated Long-term Direction

RAGLens starts as a local-first RAG pipeline debugger and is designed to evolve toward TraceForge: local-first observability and debugging for AI application harnesses.

Current positioning:

> RAGLens helps developers inspect and debug RAG pipelines locally.

Long-term positioning:

> RAGLens can grow into an observability layer for AI application harnesses: systems that manage context, retrieval, tools, memory, model calls, verification, and human feedback around foundation models.

Important distinction:

* Current implemented product: RAG pipeline debugger.
* Long-term direction: AI application harness observability.
* Do not claim tool spans, memory spans, verification spans, human feedback spans, or agent workflow tracing are implemented yet.

## Core Problem

RAG and AI application developers often do not know why their system answered incorrectly.

A wrong answer may come from:

* no retrieved context
* bad retrieval
* weak retrieval scores
* bad chunking
* duplicated chunks
* stale or legacy context
* conflicting chunks
* weak grounding
* answer claims not supported by retrieved context
* LLM ignoring useful retrieved evidence

RAGLens helps developers inspect the full RAG pipeline locally instead of guessing where the failure happened.

## Target Users

* AI application developers
* RAG builders
* Backend engineers adding LLM/RAG to their systems
* Indie hackers building AI apps
* Developers debugging retrieval pipelines
* Future: developers building tool-using agents or AI harnesses who need trace visibility

## Current Strategy

Start narrow.

Do not build a full AI infra platform first.

v0.1 focused on a polished, useful, local-first RAG debugging tool.

v0.2 should focus on helping real developers integrate RAGLens into their own RAG pipelines, instead of modifying the built-in demo.

Harness-level / TraceForge features remain long-term direction, not immediate implementation scope.

---

# Current Project Status

## v0.1 Status

**v0.1 is complete and smoke-tested.**

RAGLens now has a working local inspection loop:

```text
Python SDK
  ↓
Go Collector
  ↓
SQLite
  ↓
React Dashboard
```

Full validated path:

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
SQLite (traces, spans, warnings)
  ↓
GET /api/traces
  ↓
GET /api/traces/{trace_id}
  ↓
React Dashboard
  ↓
trace list, trace detail, chunks, prompt/response, warning cards
```

## Completed v0.1 Components

### Python SDK

Completed:

* `trace()` context manager
* retrieval span logging
* LLM span logging
* trace payload generation
* `flush()` to local collector
* local demo integration
* warning rules demo integration

Important implementation detail:

* In warning/demo scripts, `t.flush()` should be called after exiting the `with trace(...)` block so `ended_at` and `duration_ms` are finalized before payload submission.

### Go Collector

Completed:

* runs on port `4319`
* `GET /health`
* `POST /api/traces`
* `GET /api/traces`
* `GET /api/traces/{trace_id}`
* SQLite persistence for traces
* SQLite persistence for spans
* SQLite persistence for warnings
* Warning Engine runs after trace persistence

Implemented diagnosis rules:

* `no_retrieved_chunks`
* `low_retrieval_score`
* `duplicate_chunks`
* `conflicting_chunks`
* simplified `answer_not_grounded`

Important warning rule limitation:

* `answer_not_grounded` is currently a simplified deterministic rule, not a full grounding evaluator.
* It currently detects unsupported numeric day-count claims, such as an answer claiming `45 days` when retrieved evidence only supports another day range.
* It does not yet perform claim extraction, semantic entailment, LLM-as-judge evaluation, or full factuality checking.

### SQLite Storage

Completed:

* traces table
* spans table
* warnings table
* trace detail API returns persisted warnings
* dashboard renders real warnings from storage

### React Dashboard

Completed:

* trace list page
* trace detail page
* span timeline
* retrieved chunk viewer
* retrieval score display
* LLM prompt / response viewer
* real warning cards
* demo case labels in trace list
* warning count display
* collapsible trace sidebar
* improved topbar layout
* collector status display
* warning card readability polish
* summary card visual hierarchy
* responsive layout fixes for browser / VSCode-sized windows

Recent dashboard polish included:

* fixed TraceDetailPage JSX structure issues
* replaced `replaceAll` with `split/join` for TypeScript lib compatibility
* fixed narrow timeline/warnings layout issues
* restored stable large-screen detail layout
* improved medium/small-screen responsive behavior
* added trace sidebar show/hide behavior
* adjusted topbar to left toggle / centered title / right Collector status
* improved warning card structure
* semantic summary card coloring:

  * query emphasis
  * duration emphasis
  * warning count dynamic coloring

---

# Real Local RAG Demo

## Status

Completed and verified.

## Location

```text
sdk/python/examples/local_rag_demo/
```

## Implemented

* local markdown policy documents
* `document_loader.py`
* deterministic `chunker.py`
* `tfidf_retriever.py` using TF-IDF + cosine similarity
* `answerer.py` using local deterministic answer generation
* `run_demo.py` with commands:

  * `inspect`
  * `retrieve`
  * `all`
  * `trace <case>`
  * `trace-all`
* real retrieved chunks and scores
* integration with existing Python SDK trace schema
* traces sent to Go Collector on port `4319`
* dashboard verified with real retrieval traces and warning cards

## Demo Commands

From `sdk/python`:

PowerShell:

```powershell
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo inspect
python -m examples.local_rag_demo.run_demo retrieve "How long does standard shipping take?"
python -m examples.local_rag_demo.run_demo all
python -m examples.local_rag_demo.run_demo trace conflict
python -m examples.local_rag_demo.run_demo trace-all
```

Bash / Mac:

```bash
export RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo inspect
python -m examples.local_rag_demo.run_demo retrieve "How long does standard shipping take?"
python -m examples.local_rag_demo.run_demo all
python -m examples.local_rag_demo.run_demo trace conflict
python -m examples.local_rag_demo.run_demo trace-all
```

## Verified Demo Warning Cases

| Case           | Expected warning      | Status   |
| -------------- | --------------------- | -------- |
| `no_match`     | `no_retrieved_chunks` | verified |
| `low_score`    | `low_retrieval_score` | verified |
| `duplicate`    | `duplicate_chunks`    | verified |
| `conflict`     | `conflicting_chunks`  | verified |
| `hallucinated` | `answer_not_grounded` | verified |

## Hallucinated Case Stabilization

The `hallucinated` case was stabilized to isolate `answer_not_grounded`.

Current behavior:

* query is close to shipping policy wording
* `top_k = 1`
* retrieves `shipping_policy`
* score around `0.68`
* answer includes unsupported `45 days` claim
* collector returns `warnings_generated: 1`
* target warning: `answer_not_grounded`

Reason:

* Earlier hallucinated case mixed with `low_retrieval_score` and `conflicting_chunks`.
* Current case cleanly demonstrates: retrieval is relevant, but answer introduces an unsupported claim.

---

# Demo Packaging / Developer Experience

## Status

Completed.

## Completed

* root README quickstart
* README screenshots
* local RAG demo documentation
* warning rules documentation
* smoke test guide
* dashboard polish checklist
* Windows PowerShell scripts
* Mac/manual run path verified
* repo hygiene pass
* final smoke test pass

## Important Docs

Expected docs include:

```text
README.md
ROADMAP.md
DEVLOG.md
CURRENT_TASK.md
docs/ai-context/AI_HANDOFF.md
docs/demo/LOCAL_RAG_DEMO.md
docs/demo/SMOKE_TEST.md
docs/demo/WARNING_RULES.md
docs/demo/DASHBOARD_POLISH.md
docs/assets/screenshots/*.png
```

## PowerShell Scripts

From repository root:

```powershell
.\scripts\start-collector.ps1
.\scripts\start-dashboard.ps1
.\scripts\demo-trace-all.ps1
.\scripts\smoke.ps1
```

Important path notes:

* collector script should run from `collector/go`
* dashboard script should run from `dashboard/web`
* Python demo runs from `sdk/python`

## Mac Setup Note

On Mac, `pip install -e .` previously failed because `sdk/python/pyproject.toml` referenced root README outside the Python package root:

```text
readme = "../../README.md"
```

Correct fix:

```toml
readme = "README.md"
```

and ensure:

```text
sdk/python/README.md
```

exists.

This is a Python packaging hygiene issue and should remain fixed so future users can install the SDK in editable mode.

---

# Current Roadmap State

## v0.1 — Local RAG Debugger MVP

Status: Completed.

Completed:

* Python SDK tracing foundation
* Go collector ingestion APIs
* SQLite persistence
* React dashboard MVP
* Warning Engine / Diagnosis Layer MVP
* Real Local RAG Demo
* Demo Packaging / Developer Experience
* README screenshots and release presentation polish
* smoke test validation

## v0.2 — Developer Integration / User Onboarding

Status: Ready to start.

Goal:

Make it clear how a developer can use RAGLens with their own RAG pipeline instead of modifying the built-in local demo.

The built-in `local_rag_demo` is a proof demo and smoke-test fixture. Real users should instrument their own retrieval and LLM calls with the RAGLens SDK.

---

# Recommended Next Milestone

## v0.2 Developer Integration / User Onboarding

The immediate next task is not LangChain, LlamaIndex, real LLM integration, or harness features.

The immediate task is to define and implement the user onboarding path.

## Key Product Question

How does a developer use RAGLens with their own RAG pipeline?

Answer should become:

```text
Start RAGLens locally.
Import the Python SDK.
Wrap your RAG pipeline in trace().
Log retrieval results.
Log LLM prompt/response.
Flush trace to collector.
Open dashboard.
Inspect pipeline and warnings.
```

## First Recommended File

Create:

```text
docs/product/USER_ONBOARDING.md
```

This document should answer:

* What is RAGLens?
* What is RAGLens not?
* Who is the user?
* How does RAGLens fit into an existing RAG app?
* What does the user start locally?
* What code does the user add?
* What data does RAGLens need?
* What does a retrieved chunk look like?
* What does RAGLens analyze?
* What does RAGLens not analyze yet?
* What is the difference between the built-in local demo and real user integration?

## Suggested USER_ONBOARDING.md Positioning

RAGLens is:

* a local-first trace and debugging layer for RAG pipelines
* an observability/debugging tool
* a way to inspect retrieval, context, prompts, responses, and warnings

RAGLens is not:

* a chatbot framework
* a training framework
* a vector database
* an eval benchmark suite yet
* a hosted AI platform
* a replacement for the user’s RAG app

Important message:

Users should not modify `local_rag_demo` for real usage.

Instead, users should instrument their own RAG pipeline with the Python SDK.

---

# v0.2 Planned Scope

## 1. User onboarding docs

Create:

```text
docs/product/USER_ONBOARDING.md
```

Explain:

* local-first startup
* SDK instrumentation model
* difference between demo and real integration
* RAGLens role in user systems
* what data is captured
* what remains user-owned

## 2. Python SDK integration guide

Create:

```text
docs/integrations/PYTHON_SDK_GUIDE.md
```

Should include:

* setup
* `RAGLENS_COLLECTOR_URL`
* `trace()` basics
* retrieval span example
* LLM span example
* `flush()`
* common mistakes
* troubleshooting

## 3. Stable trace/chunk schema documentation

Document expected retrieved chunk shape:

```python
{
    "id": "chunk_123",
    "text": "...",
    "score": 0.82,
    "source": "docs/refund_policy.md",
    "document_id": "refund_policy",
    "rank": 1,
    "metadata": {
        "retriever": "my-vector-db",
        "embedding_model": "my-embedding-model"
    }
}
```

Explain how warning rules use:

* chunk text
* score
* source
* document id
* rank
* metadata

## 4. Custom pipeline example

Add:

```text
sdk/python/examples/custom_pipeline_demo.py
```

Purpose:

Show how a user instruments their own RAG pipeline.

Important:

* Keep it local and deterministic.
* Do not require OpenAI, Anthropic, LangChain, LlamaIndex, or external APIs.
* Focus on SDK instrumentation.
* Do not make users modify `local_rag_demo`.

Basic shape:

```python
from raglens import trace

with trace(name="custom-rag", query=user_query) as t:
    chunks = my_retriever(user_query)

    t.retrieval(
        name="my_retriever",
        query=user_query,
        chunks=sdk_chunks,
        top_k=len(sdk_chunks),
        metadata={
            "retriever": "custom",
        },
    )

    answer = my_answerer(user_query, chunks)

    t.llm(
        name="my_answerer",
        model="local-or-user-model",
        prompt=prompt,
        response=answer,
        metadata={
            "provider": "custom",
        },
    )

t.flush()
```

## 5. Unified local startup path

Consider:

* Bash scripts for Mac/Linux:

  * `scripts/start-collector.sh`
  * `scripts/start-dashboard.sh`
  * `scripts/demo-trace-all.sh`
  * `scripts/smoke.sh`
* Docker Compose local run path
* future CLI:

  * `raglens ui`
  * `raglens up`
* local reset command for demo data

Do not overbuild this first.

Recommended order:

1. Bash scripts for Mac/Linux.
2. Document current startup path.
3. Then design Docker Compose or CLI.

## 6. Optional raw LLM example

Defer until SDK onboarding is clear.

If added later:

* keep it optional
* do not make API keys required for default demo
* do not replace deterministic local demo

---

# Out of Scope for Immediate v0.2

Do not start with:

* LangChain adapter
* LlamaIndex adapter
* real LLM default path
* cloud sync
* auth
* hosted collector
* multi-user workspace
* full grounding evaluator
* LLM-as-judge
* multi-agent support
* tool/memory/verification spans

These belong later.

Harness-level observability is long-term TraceForge direction, not current v0.2 implementation.

---

# TraceForge / Harness Direction

Long-term direction:

RAGLens can evolve into TraceForge: local-first observability and debugging for AI application harnesses.

In this framing, a RAG pipeline is one type of AI harness:

```text
query
  ↓
context selection / retrieval
  ↓
model call
  ↓
answer
  ↓
diagnostics
```

Future AI harnesses may include:

```text
task
  ↓
planning
  ↓
context retrieval
  ↓
tool calls
  ↓
memory reads/writes
  ↓
model calls
  ↓
verification
  ↓
human feedback
  ↓
final result
```

Potential future span types:

* agent span
* tool span
* memory span
* verification span
* human feedback / intervention span
* planner span
* state transition span

Potential future diagnostics:

* failed tool call
* missing verification
* unsafe tool call
* memory conflict
* state drift
* context drift
* unsupported claim
* stale context
* conflicting evidence
* planner loop

Important:

Do not claim these are implemented yet.

Current implemented span types are retrieval and LLM spans.

---

# Current Development Guidance

Use ChatGPT for:

* product direction
* architecture decisions
* milestone planning
* implementation guidance
* AI infra / RAG / observability reasoning

Use Copilot for:

* local bug finding
* static code review
* mechanical code edits after direction is decided
* documentation updates after direction is decided
* checking compile/type errors

Important user preference:

The user wants to learn through the development process, not just outsource the project. Proceed step by step. Explain why each step matters for AI infra, RAG systems, observability, or developer tooling.

Avoid dropping huge task dumps unless explicitly asked.

Preferred collaboration style:

1. Explain the problem.
2. Explain why it matters.
3. Propose a small design.
4. Touch a small number of files.
5. Verify with a command.
6. Reflect on what was learned.

---

# Recommended First Step in Next Conversation

Start v0.2 with:

```text
docs/product/USER_ONBOARDING.md
```

Do not write code first.

First clarify the real user journey:

```text
A developer has their own RAG app.
They start RAGLens locally.
They install/import the Python SDK.
They instrument retrieval and LLM calls.
They send traces to collector.
They inspect traces and warnings in dashboard.
```

Then proceed to:

1. `USER_ONBOARDING.md`
2. `PYTHON_SDK_GUIDE.md`
3. chunk schema docs
4. `custom_pipeline_demo.py`
5. Mac/Linux Bash scripts or unified startup path
