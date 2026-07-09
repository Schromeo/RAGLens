# Smoke Test

This document describes the manual smoke test for the RAGLens local-first deterministic demo flows.

The goal is to verify that the core local tracing loop still works:

```txt
Python demo
  ↓
Python SDK trace
  ↓
Go collector
  ↓
SQLite persistence
  ↓
React dashboard
  ↓
Warning cards
```

This is not a full test suite.  
It is a quick end-to-end check before demos, screenshots, README updates, or larger refactors.

Related docs:

- [Local demo runbook](LOCAL_RAG_DEMO.md)
- [Warning rules and limitations](WARNING_RULES.md)

## Prerequisites

Make sure the following tools are installed:

- Go
- Node.js
- Python

The default local collector URL is:

```txt
http://localhost:4319
```

## Step 1: Start the collector

From the repository root:

```bash
cd collector/go
go run ./cmd/raglens-collector
```

PowerShell shortcut:

```powershell
.\scripts\start-collector.ps1
```

Expected result:

```txt
Collector starts successfully and listens on port 4319.
```

In another terminal, verify the health endpoint:

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

## Step 2: Start the dashboard

In another terminal:

```bash
cd dashboard/web
npm install
npm run dev
```

PowerShell shortcut:

```powershell
.\scripts\start-dashboard.ps1
```

Expected result:

```txt
Dashboard dev server starts successfully.
```

Open the local dashboard URL printed by the dev server.

## Step 3: Run the warning rules demo

In another terminal:

```bash
cd sdk/python
```

PowerShell:

```powershell
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.warning_rules_demo all
```

Bash:

```bash
export RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.warning_rules_demo all
```

Expected result:

```txt
Each warning rule demo case completes successfully.
```

Expected warning types:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- `conflicting_chunks`
- `answer_not_grounded`

## Step 3.5: Run the v0.3.5 reference integration demo

From `sdk/python`:

```bash
python -m examples.reference_rag_app.run all
python -m examples.reference_rag_app.run processing-range
python -m examples.reference_rag_app.run wrong-processing-range
```

Expected result:

```txt
Reference integration traces are generated and sent to the collector.
```

Expected traces include:

- `reference-rag-app-refund`
- `reference-rag-app-conflict`
- `reference-rag-app-wrong-window`
- `reference-rag-app-processing-range`
- `reference-rag-app-wrong-processing-range`
- `reference-rag-app-damaged`
- `reference-rag-app-digital`
- `reference-rag-app-subscription`
- `reference-rag-app-weak`

## Step 4: Run the local RAG trace demo

From `sdk/python`:

```bash
python -m examples.local_rag_demo.run_demo trace-all
```

PowerShell shortcut (from repository root):

```powershell
.\scripts\demo-trace-all.ps1
```

Expected result:

```txt
The demo generates warning-focused traces and sends them to the collector.
```

Expected traced cases:

- `real-local-rag-no_match`
- `real-local-rag-low_score`
- `real-local-rag-duplicate`
- `real-local-rag-conflict`
- `real-local-rag-hallucinated`

## Step 5: Verify traces in the dashboard

Open the dashboard and check that new traces appear.

Inspect these traces first:

- `real-local-rag-conflict`
- `real-local-rag-hallucinated`
- `real-local-rag-no_match`

For each trace, verify:

- query is visible
- retrieved chunks are visible
- retrieval scores are visible
- prompt / response are visible
- warning cards are visible

## Step 6: Verify expected warnings

Check that the following cases produce the expected warnings:

| Trace | Expected warning |
|---|---|
| `real-local-rag-no_match` | `no_retrieved_chunks` |
| `real-local-rag-low_score` | `low_retrieval_score` |
| `real-local-rag-duplicate` | `duplicate_chunks` |
| `real-local-rag-conflict` | `conflicting_chunks` |
| `real-local-rag-hallucinated` | `answer_not_grounded` |

## Pass criteria

The smoke test passes if:

- collector starts successfully
- `/health` returns ok
- dashboard starts successfully
- warning rules demo runs successfully
- local RAG `trace-all` runs successfully
- traces appear in the dashboard
- retrieved chunks are visible
- warning cards are visible
- expected warning types are generated
- reference integration traces are generated and inspectable

## Acceptance Table

```txt
Collector health: pass / fail
Dashboard starts: pass / fail
trace-all runs: pass / fail
reference-rag-app runs: pass / fail
no_match warning: pass / fail
low_score warning: pass / fail
duplicate warning: pass / fail
conflict warning: pass / fail
hallucinated warning: pass / fail
Trace detail readable: pass / fail
README commands accurate: pass / fail
```

## Latest Run Snapshot (2026-06-22)

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

Evidence summary:

- `scripts/demo-trace-all.ps1` completed with `Generated traces: 5` and `Failed traces: 0`.
- Collector API checks confirmed warning types for the five generated trace IDs:
  - `no_match` -> `no_retrieved_chunks`
  - `low_score` -> `low_retrieval_score`
  - `duplicate` -> `duplicate_chunks`
  - `conflict` -> includes `conflicting_chunks`
  - `hallucinated` -> `answer_not_grounded`

## Fail criteria

The smoke test fails if:

- collector cannot start
- `/health` fails
- dashboard cannot start
- Python demo cannot send traces
- traces do not appear in dashboard
- warning cards are missing
- expected warning types are not generated

## Notes

This smoke test is intentionally manual for now.

Later, parts of it can be automated with:

- a script for collector health checks
- a script for demo trace generation
- collector API assertions
- snapshot checks for expected warning types
- Playwright checks for dashboard rendering

For v0.1, the priority is to keep the local demo easy to verify by hand.