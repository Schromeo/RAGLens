# Rebranding: RAGLens -> SledTrace

SledTrace v0.4.1 renames the project from RAGLens to SledTrace.

The rename is to avoid confusion with an unrelated research project. Core functionality and architecture are unchanged in this release.

## What Stayed the Same

- Local-first architecture
- Python SDK trace API semantics
- Collector API routes (`/health`, `/api/traces`, `/api/traces/{trace_id}`)
- Warning generation logic and rule behavior
- SQLite schema and table names (`traces`, `spans`, `warnings`)
- Default collector port (`4319`)

## Environment Variable Migration

Preferred variable:

- `SLEDTRACE_COLLECTOR_URL`

Compatibility in v0.4.1:

- Legacy `RAGLENS_COLLECTOR_URL` is still supported temporarily
- Resolution order is:
  1. `SLEDTRACE_COLLECTOR_URL`
  2. `RAGLENS_COLLECTOR_URL` (deprecated)
  3. `http://localhost:4319`

## Startup Command Migration

Preferred command:

```bash
python scripts/start-sledtrace.py
```

Compatibility in v0.4.1:

- Legacy `python scripts/start-raglens.py` still works
- The old command is now a thin wrapper that delegates to the new launcher and prints a concise deprecation message

## Python Import Migration

Preferred import path:

```python
from sledtrace import trace
```

Compatibility in v0.4.1:

- Legacy import path remains available:

```python
from raglens import trace
```

- `raglens` remains as a compatibility shim and re-exports the same public API

## Notes on Historical Releases

- v0.4.0 was originally released under the RAGLens name
- Historical docs and release notes keep that context intentionally
