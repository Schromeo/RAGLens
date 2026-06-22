# RAGLens

RAGLens is a local-first visual debugger for RAG pipelines.

It helps developers inspect what happened inside a RAG application: what was retrieved, what context was sent to the model, what answer was produced, and what warning signals were detected.

## Why RAGLens?

RAG applications often fail silently.

A wrong answer may come from:

- no retrieved context
- weak retrieval scores
- duplicated chunks
- conflicting retrieved evidence
- an answer that is not grounded in the retrieved chunks
- the model ignoring useful context

RAGLens makes these failure modes visible locally.

## What RAGLens shows

The current v0.1 MVP supports:

- Python SDK tracing
- retrieval span logging
- LLM span logging
- local Go collector
- SQLite persistence
- React dashboard
- trace list
- trace detail view
- retrieved chunks viewer
- LLM prompt / response viewer
- warning cards

Current warning rules:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- `conflicting_chunks`
- `answer_not_grounded`

The v0.1 warning rules are intentionally simple and deterministic. See `docs/demo/WARNING_RULES.md` for current rule definitions and limitations.

## Current status

RAGLens is currently a local-first v0.1 MVP.

Completed:

- Python SDK tracing foundation
- Go collector ingestion APIs
- SQLite trace/span/warning persistence
- React dashboard MVP
- Warning Engine / Diagnosis Layer MVP
- Real Local RAG Demo using local markdown docs, TF-IDF retrieval, cosine similarity, and a deterministic local answerer

The default demo requires no external LLM API and no API key.

## Quickstart

### 1. Start the collector

From the repository root:

```bash
cd collector/go
go run ./cmd/raglens-collector
```

The collector runs on:

```txt
http://localhost:4319
```

You can verify it with:

```bash
curl http://localhost:4319/health
```

Expected response:

```json
{
  "service": "raglens-collector",
  "status": "ok"
}
```

### 2. Start the dashboard

In another terminal:

```bash
cd dashboard/web
npm install
npm run dev
```

Then open the local dashboard URL printed by the dev server.

### 3. Run the local RAG demo

In another terminal:

```bash
cd sdk/python
```

PowerShell:

```powershell
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo trace-all
```

Bash:

```bash
export RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo trace-all
```

This generates representative RAG debugging traces and sends them to the local collector.

### Windows PowerShell shortcuts

Start the collector:

```powershell
.\scripts\start-collector.ps1
```

Start the dashboard in another terminal:

```powershell
.\scripts\start-dashboard.ps1
```

Generate demo traces in a third terminal:

```powershell
.\scripts\demo-trace-all.ps1
```

Run the smoke test:

```powershell
.\scripts\smoke.ps1
```

## Local RAG Demo

The local demo is deterministic and API-key free.

It uses:

* local markdown policy documents
* simple chunking
* TF-IDF retrieval
* cosine similarity scores
* a local template-based answerer
* the RAGLens Python SDK
* the local collector and dashboard

Demo guide:

```txt
docs/demo/LOCAL_RAG_DEMO.md
```

Dashboard demo polish checklist:

```txt
docs/demo/DASHBOARD_POLISH.md
```

Smoke test guide:

```txt
docs/demo/SMOKE_TEST.md
```

Warning rule guide:

```txt
docs/demo/WARNING_RULES.md
```

Warning-focused demo cases:

| Case           | What it simulates                        | Expected warning      |
| -------------- | ---------------------------------------- | --------------------- |
| `no_match`     | No useful retrieved chunks               | `no_retrieved_chunks` |
| `low_score`    | Weak retrieval confidence                | `low_retrieval_score` |
| `duplicate`    | Duplicated retrieved evidence            | `duplicate_chunks`    |
| `conflict`     | Conflicting retrieved policy chunks      | `conflicting_chunks`  |
| `hallucinated` | Answer not supported by retrieved chunks | `answer_not_grounded` |

Recommended command:

```bash
python -m examples.local_rag_demo.run_demo trace-all
```

On Windows PowerShell, you can also run:

```powershell
.\scripts\demo-trace-all.ps1
```

For a basic smoke test:

```powershell
.\scripts\smoke.ps1
```

Then open the dashboard and inspect:

* `real-local-rag-conflict`
* `real-local-rag-hallucinated`
* `real-local-rag-no_match`

## Project direction

RAGLens starts as a local-first visual debugger for RAG pipelines.

The long-term direction is to grow the tracing core into an AgentOps-lite observability foundation that can later evolve toward TraceForge.

Near-term focus:

* improve developer experience
* package the local demo
* polish README and demo docs
* add smoke test instructions
* improve dashboard demo presentation
* keep the default path local, deterministic, and API-key free

Future integrations such as LangChain, LlamaIndex, and real LLM providers can be added later, but they are not required for the default v0.1 demo.

