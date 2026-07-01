# Roadmap

This roadmap is ordered by delivery sequence.

Each version includes clear scope boundaries so RAGLens stays local-first, lightweight, and useful as a developer tool.

## Current Snapshot

**Current version:** v0.1 — Local RAG Debugger MVP  
**Status:** Completed

RAGLens now has a working local inspection loop:

```text
Python SDK
  ↓
Go Collector
  ↓
SQLite
  ↓
React Dashboard
````

Completed in v0.1:

* Python SDK tracing foundation
* Go collector ingestion APIs
* SQLite persistence for traces, spans, and warnings
* React Dashboard MVP
* Warning Engine / Diagnosis Layer MVP
* Real Local RAG Demo
* Demo Packaging / Developer Experience
* README screenshots and release presentation polish
* Final smoke test validation

### Current focus

Planning v0.2 Developer Integration / User Onboarding.

The next milestone is to make it clear how developers can use RAGLens with their own RAG pipelines instead of modifying the built-in demo.

---

## v0.1 — Local RAG Debugger MVP

**Status:** Completed

### Goal

Let a developer trace a RAG pipeline, store traces locally, and inspect the pipeline in a browser UI.

### Scope

#### Core tracing and ingestion

* [x] Python SDK
* [x] Trace context manager
* [x] Retrieval span logging
* [x] LLM call span logging
* [x] Trace payload generation
* [x] SDK `flush()` to local collector
* [x] Refund policy demo
* [x] Real local RAG demo using local documents, deterministic chunking, and TF-IDF retrieval

#### Collector and local storage

* [x] Go collector
* [x] `GET /health`
* [x] `POST /api/traces`
* [x] `GET /api/traces`
* [x] `GET /api/traces/{trace_id}`
* [x] SQLite storage
* [x] Trace persistence
* [x] Span persistence
* [x] Warning persistence

#### Dashboard

* [x] Trace list page
* [x] Trace detail page
* [x] Retrieved chunks viewer
* [x] LLM prompt / response viewer
* [x] Warning cards in trace detail
* [x] Demo-friendly trace list labels
* [x] Improved warning card readability
* [x] Responsive trace detail layout polish

#### Warning engine

* [x] `no_retrieved_chunks`
* [x] `low_retrieval_score`
* [x] `duplicate_chunks`
* [x] `conflicting_chunks`
* [x] simplified `answer_not_grounded`

### Completed Milestone: Real Local RAG Demo

Completed and verified in v0.1:

* local markdown policy documents for retrieval
* simple deterministic chunking pipeline
* TF-IDF plus cosine similarity retriever baseline
* real retrieved chunks with rank and score
* SDK trace integration without schema changes
* traces sent to the local Go collector
* dashboard verification of real retrieval traces
* warning rule verification on real retrieval output

Verified warning-target cases:

| Case           | Expected warning      |
| -------------- | --------------------- |
| `no_match`     | `no_retrieved_chunks` |
| `low_score`    | `low_retrieval_score` |
| `duplicate`    | `duplicate_chunks`    |
| `conflict`     | `conflicting_chunks`  |
| `hallucinated` | `answer_not_grounded` |

### Validation

v0.1 smoke test passed.

Verified:

* collector starts successfully
* dashboard starts successfully
* local RAG `trace-all` runs successfully
* demo traces appear in dashboard
* warning cards render in trace detail
* retrieved chunks, scores, prompt, response, and warnings are inspectable
* expected warning-focused demo cases generate warnings

---

## v0.1 Demo Packaging / Developer Experience

**Status:** Completed

### Goal

Make RAGLens easy to run, understand, demo, and show as a polished local-first RAG debugging MVP.

### Completed Scope

* [x] Root README quickstart
* [x] Local RAG demo documentation
* [x] Warning rules documentation
* [x] Smoke test guide
* [x] Dashboard demo polish checklist
* [x] Windows PowerShell startup scripts
* [x] Windows PowerShell demo scripts
* [x] Deterministic `trace-all` demo flow
* [x] CLI output polish for local demo
* [x] Stabilized warning-focused demo cases
* [x] Dashboard demo readability improvements
* [x] README screenshots
* [x] Repo hygiene pass
* [x] Final smoke test pass

### Completed scripts

PowerShell scripts from repository root:

```powershell
.\scripts\start-collector.ps1
.\scripts\start-dashboard.ps1
.\scripts\demo-trace-all.ps1
.\scripts\smoke.ps1
```

### Exit Criteria

Completed:

* warning records are generated
* warning records are persisted in SQLite
* warning records are returned by the trace detail API
* dashboard trace detail renders real warnings
* a developer can run the local demo and understand the value of RAGLens without reading raw JSON
* README includes screenshots and a clear local-first quickstart
* smoke test passes

---

## v0.2 — Developer Integration / User Onboarding

**Status:** Not Started

### Goal

Make it clear how a developer can use RAGLens with their own RAG pipeline instead of modifying the built-in local demo.

The built-in `local_rag_demo` is a proof demo and smoke-test fixture. Real users should instrument their own retrieval and LLM calls with the RAGLens SDK.

### Product Questions

v0.2 should answer:

* How does a developer start RAGLens locally?
* How does RAGLens fit into an existing RAG application?
* What code does the user add to their own pipeline?
* What trace data should the user send?
* What does a valid retrieved chunk look like?
* What does RAGLens analyze?
* What does RAGLens not do?
* What is the difference between the built-in demo and real user integration?

### Planned Scope

#### User onboarding docs

* [ ] `docs/product/USER_ONBOARDING.md`
* [ ] Explain RAGLens as an observability/debugging tool, not a training framework
* [ ] Explain that users do not modify the built-in demo for real usage
* [ ] Explain how users instrument their own RAG pipeline
* [ ] Explain what data RAGLens needs:

  * query
  * retrieved chunks
  * retrieval scores
  * sources
  * prompt
  * response
  * metadata

#### Python SDK integration guide

* [ ] `docs/integrations/PYTHON_SDK_GUIDE.md`
* [ ] Minimal install/setup instructions
* [ ] `RAGLENS_COLLECTOR_URL` configuration
* [ ] Basic `trace()` usage
* [ ] Retrieval span example
* [ ] LLM span example
* [ ] `flush()` behavior
* [ ] Common mistakes and troubleshooting

#### Stable trace/chunk schema documentation

* [ ] Document expected retrieved chunk shape
* [ ] Document recommended fields:

  * `id`
  * `text`
  * `score`
  * `source`
  * `document_id`
  * `rank`
  * `metadata`
* [ ] Document how warning rules use chunk fields
* [ ] Document current limitations of v0.1/v0.2 warning rules

#### Custom pipeline example

* [ ] Add `sdk/python/examples/custom_pipeline_demo.py`
* [ ] Show how to instrument a user-owned retrieval pipeline
* [ ] Keep example local and deterministic
* [ ] Avoid requiring LangChain, LlamaIndex, OpenAI, Anthropic, or other external APIs
* [ ] Focus on SDK instrumentation rather than demo documents

#### Unified local startup path

* [ ] Decide between:

  * Docker Compose local run path
  * `raglens ui`
  * `raglens up`
  * improved scripts
* [ ] Define expected user startup flow
* [ ] Keep existing PowerShell scripts working
* [ ] Add Bash equivalents if needed
* [ ] Consider a local reset command for demo data

#### Optional raw LLM example

* [ ] Add a raw OpenAI-style example only after the SDK onboarding path is clear
* [ ] Keep it optional
* [ ] Do not make real LLM integration required for the default demo

### Out of Scope

Not part of v0.2 initial scope:

* LangChain adapter
* LlamaIndex adapter
* full grounding evaluator
* LLM-as-judge evaluation
* cloud sync
* auth
* team workspaces
* production deployment
* hosted collector

### Exit Criteria

v0.2 is complete when:

* a developer can understand how to use RAGLens with their own RAG pipeline
* documentation clearly distinguishes built-in demo usage from real integration usage
* Python SDK integration guide exists
* stable retrieved chunk schema is documented
* custom pipeline instrumentation example exists
* local startup path is documented and easy to follow
* no external LLM API is required for the default onboarding path

---

## v0.3 — RAG Quality Analysis

**Status:** Not Started

### Goal

Improve the diagnosis layer beyond deterministic v0.1 warning rules.

v0.1 introduced simple warnings to make common RAG failure modes visible. v0.3 should make those diagnostics more useful, configurable, and closer to real debugging workflows.

### Planned Scope

* Configurable warning thresholds
* Better weak retrieval analysis
* Missing context detection
* Stale or legacy context warning
* Improved duplicate chunk detection
* Improved conflicting context detection
* Stronger answer grounding checks
* Claim-level grounding analysis
* Better source attribution view
* Warning evidence display
* Save failing trace as eval case seed

### Possible warning improvements

* distinguish no retrieval vs filtered retrieval
* distinguish low top score vs low average score
* identify chunks that caused conflict warnings
* identify unsupported answer claims
* expose warning evidence in dashboard
* support rule configuration through local config file

### Out of Scope

* full automated factuality scoring
* hosted eval service
* multi-run benchmark dashboard
* CI regression runner

---

## v0.4 — Evaluation and Regression

**Status:** Not Started

### Goal

Turn debugging outcomes into repeatable quality checks.

Once users can inspect failing traces, RAGLens should help turn those failures into regression cases.

### Planned Scope

* Eval dataset export
* Save failing trace as regression case
* Basic regression test runner
* Prompt/model comparison runs
* Retrieval configuration comparison
* Warning diff across runs
* CI-friendly report output
* Local HTML or markdown report generation

### Example workflow

```text
Find bad trace
  ↓
Save as eval case
  ↓
Change retriever/chunker/prompt
  ↓
Re-run eval
  ↓
Compare warnings and outputs
```

---

## Future — TraceForge Direction

**Status:** Future

RAGLens starts as a local-first RAG debugger.

The following items are possible future directions after the core local debugger experience is useful and stable. They are not part of the immediate MVP commitment.

Potential expansion:

* AI application harness observability
* agent span
* tool span
* memory span
* verification span
* human feedback / intervention span
* context engineering diagnostics
* failure attribution
* harness-level timeline
* tool call debugging
* memory/context drift detection
* verification result tracking
* Semantic cache analysis
* AI gateway integration
* OpenTelemetry export
* Langfuse export
* Promptfoo/Ragas interoperability
* Cloud sync
* Team workspace
* Hosted collector
* Multi-user projects
* Dataset and eval management
* Production observability mode

### Long-term direction

RAGLens can evolve from a local-first RAG debugger into a broader tracing and debugging platform for AI application harnesses.

The long-term project direction is TraceForge: a developer-first, local-first observability and debugging layer for AI application harnesses.

This future direction is intentionally separate from v0.2, which remains focused on Developer Integration / User Onboarding.

