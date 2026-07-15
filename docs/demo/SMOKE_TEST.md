# Smoke Test

This document defines the v0.4 local-first smoke test for first-run developer experience.

Goal:

```txt
Fresh clone
  -> start collector + dashboard
  -> run reference traces
  -> open dashboard
  -> inspect diagnostics
```

## Path A: Docker (recommended)

From repository root:

```bash
docker compose up --build
```

In another terminal:

```bash
curl http://localhost:4319/health
```

Expected health response:

```json
{
  "service": "sledtrace-collector",
  "status": "ok"
}
```

Generate reference traces:

```bash
cd sdk/python
pip install -e .
python -m examples.reference_rag_app.run all
```

Open dashboard:

```text
http://localhost:5173
```

## Path B: Non-Docker fallback

From repository root:

```bash
python scripts/start-sledtrace.py
```

Then:

```bash
cd sdk/python
python -m examples.reference_rag_app.run all
```

## Expected reference traces

- `reference-rag-app-refund`
- `reference-rag-app-conflict`
- `reference-rag-app-wrong-window`
- `reference-rag-app-processing-range`
- `reference-rag-app-wrong-processing-range`
- `reference-rag-app-damaged`
- `reference-rag-app-digital`
- `reference-rag-app-subscription`
- `reference-rag-app-weak`

## Expected high-level behavior checks

- `damaged` does not produce unrelated refund-processing conflict
- `processing-range` still shows relevant refund-processing conflict
- `wrong-processing-range` still shows `numeric_mismatch`
- `wrong-window` still shows `numeric_mismatch`
- `weak` still shows `answer_not_grounded`
- `subscription` remains low-noise and typically warning-free

## Stop and reset

Stop Docker stack:

```bash
docker compose down
```

Reset Docker data volume:

```bash
docker compose down -v
```

Reset non-Docker SQLite data:

- Collector defaults to `raglens.db` and `scripts/start-sledtrace.py` runs collector from `collector/go`.
- So the default local DB path is `collector/go/raglens.db`.

Bash:

```bash
rm -f collector/go/raglens.db
```

PowerShell:

```powershell
Remove-Item .\collector\go\raglens.db -ErrorAction SilentlyContinue
```

## Validation checklist

```txt
docker compose up --build: pass / fail
collector /health: pass / fail
reference-rag-app run all: pass / fail
dashboard loads: pass / fail
reference traces visible: pass / fail
```


