# RAGLens

RAGLens is a local-first visual debugger for RAG pipelines.

It helps developers inspect retrieved chunks, trace LLM calls, and understand why a RAG application answered incorrectly.

## Why RAGLens?

Debugging RAG systems is painful.

When a RAG app gives a wrong answer, it is often unclear whether the failure came from:

- Poor retrieval
- Bad chunking
- Stale or conflicting context
- Weak grounding
- The LLM ignoring the retrieved evidence

RAGLens makes the pipeline visible.

## MVP Goal

The first version focuses on one simple workflow:

```python
from raglens import trace

with trace("refund-policy-qa") as t:
    t.retrieval(query=query, chunks=chunks)
    t.llm(model=model, prompt=prompt, response=answer)
```

Then run:
```Bash
raglens ui
```
And inspect the full RAG trace locally.

## Current Status

v0.1 (Local RAG Debugger MVP) is active.

The Warning Engine / Diagnosis Layer MVP is complete.
The Real Local RAG Demo milestone is complete.

Implemented local inspection loop:

```text
Python SDK
    -> t.flush()
    -> POST /api/traces
    -> Go Collector (:4319)
    -> SQLite (traces, spans, warnings)
    -> GET /api/traces/{trace_id}
    -> React Dashboard warning cards
```

Implemented warning rules:

- `no_retrieved_chunks`
- `low_retrieval_score` (default threshold `0.5`, overridable by span metadata)
- `duplicate_chunks`
- `conflicting_chunks`
- simplified `answer_not_grounded`

Smoke test entrypoint:

```powershell
cd sdk/python
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.warning_rules_demo all
```

Expected smoke result: each demo returns `warnings_generated: 1`.

Implementation detail: `warning_rules_demo.py` flushes after exiting the `trace()` context manager so `ended_at` and `duration_ms` are finalized before sending.

Real local retrieval demo:

```powershell
# terminal 1
cd collector/go
go run ./cmd/raglens-collector

# terminal 2
cd sdk/python
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
python -m examples.local_rag_demo.run_demo inspect
python -m examples.local_rag_demo.run_demo retrieve "How can I reset my password?"
python -m examples.local_rag_demo.run_demo trace-all
```

Current focus after this milestone:

- Improve warning explanation quality and dashboard details.
- Add unit tests for warning rules and demo cases.
- Evaluate semantic retrieval baseline (sentence-transformers + cosine) without breaking current trace schema.

# Roadmap
- Python SDK
- Local collector
- Trace list page
- Trace detail page
- Retrieved chunk viewer
- Basic RAG warnings (MVP complete)
- Real Local RAG Demo (completed)
- Warning explanation and testing hardening (active)
- LangChain / LlamaIndex examples
- Eval dataset export
- Agent/tool call tracing