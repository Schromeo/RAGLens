# Roadmap

## v0.1 — Local RAG Debugger MVP

Goal: Allow a developer to trace a RAG pipeline and inspect it locally.

### Features

- Python SDK
- Trace context manager
- Retrieval span
- LLM call span
- Local collector
- SQLite storage
- Trace list page
- Trace detail page
- Retrieved chunks viewer
- Basic warnings
- Refund policy demo

## v0.2 — Developer Experience

Goal: Make the project easy to try and pleasant to use.

### Features

- Better README
- GIF demo
- Docker Compose
- CLI command: raglens ui
- Raw OpenAI example
- LangChain example
- LlamaIndex example

## v0.3 — RAG Quality Analysis

Goal: Help developers understand why retrieval failed.

### Features

- Weak retrieval warning
- Missing context warning
- Duplicate chunk warning
- Conflicting context warning
- Stale context warning
- Save failing trace as eval case

## v0.4 — Evaluation and Regression

Goal: Turn debugging sessions into repeatable tests.

### Features

- Eval dataset export
- Basic regression test runner
- Prompt/model comparison
- CI-friendly report

## Future — TraceForge Direction

- Agent/tool call tracing
- Semantic cache analysis
- AI gateway integration
- OpenTelemetry export
- Langfuse export
- Promptfoo/Ragas integration