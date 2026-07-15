# Reference RAG App Runbook

## Purpose

The reference app is a thin, realistic integration sample for validating RAGLens diagnostics without turning RAGLens into a RAG framework.

It demonstrates:

- local markdown policy corpus
- local lexical retrieval
- mixed retrieval output shapes
- normalization through `normalize_chunks()`
- retrieval + llm span tracing
- deterministic default behavior

## How It Differs from local_rag_demo

`local_rag_demo` is a simpler warning-focused demo fixture.

`reference_rag_app` is closer to a real integration path and intentionally includes mixed raw retrieval result formats to validate chunk normalization and warning stability.

## Default Mode: Deterministic

By default, the reference app uses deterministic answer paths and does not require API keys.

Run all deterministic cases:

```bash
cd sdk/python
python -m examples.reference_rag_app.run all
```

Run one case:

```bash
python -m examples.reference_rag_app.run conflict
```

## Optional Real LLM Mode

If already configured, you can run with `--llm`.

OpenAI-compatible example:

```bash
export OPENAI_API_KEY="your_key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
export OPENAI_MODEL="gpt-4o-mini"
python -m examples.reference_rag_app.run conflict --llm
```

Ollama-compatible example:

```bash
export OPENAI_API_KEY="ollama"
export OPENAI_BASE_URL="http://localhost:11434/v1"
export OPENAI_MODEL="llama3.1:8b"
python -m examples.reference_rag_app.run refund --llm
```

## Cases

- refund
- conflict
- wrong-window
- processing-range
- wrong-processing-range
- damaged
- digital
- subscription
- weak

## Expected High-Level Warning Behavior

- `refund`: no false positive numeric mismatch for elapsed-time phrasing
- `conflict`: relevant conflicting chunk diagnostics
- `wrong-window`: numeric_mismatch for incorrect return window claim
- `processing-range`: relevant refund-processing conflict can appear
- `wrong-processing-range`: numeric_mismatch should appear
- `damaged`: should not show unrelated refund-processing conflict
- `digital`: should avoid unrelated physical return-window conflict
- `subscription`: low-noise trace, usually no warning
- `weak`: low retrieval quality plus answer_not_grounded behavior

## Expected Trace Names in Dashboard

- reference-rag-app-refund
- reference-rag-app-conflict
- reference-rag-app-wrong-window
- reference-rag-app-processing-range
- reference-rag-app-wrong-processing-range
- reference-rag-app-damaged
- reference-rag-app-digital
- reference-rag-app-subscription
- reference-rag-app-weak
