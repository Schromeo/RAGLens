# Roadmap

## v0.1 — Local RAG Debugger MVP

Status: In Progress

Goal: Allow a developer to trace a RAG pipeline and inspect it locally.

### Features

- Done: Python SDK
- Done: Trace context manager
- Done: Retrieval span
- Done: LLM call span
- Done: Local collector
- Done: SQLite storage
- Done: Refund policy demo
- Done: SDK flush() to collector
- Next: Trace list page
- Next: Trace detail page
- Next: Retrieved chunks viewer
- Later in v0.1: Basic warnings

## v0.2 — Developer Experience

Status: Not Started

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

Status: Not Started

Goal: Help developers understand why retrieval failed.

### Features

- Weak retrieval warning
- Missing context warning
- Duplicate chunk warning
- Conflicting context warning
- Stale context warning
- Save failing trace as eval case

## v0.4 — Evaluation and Regression

Status: Not Started

Goal: Turn debugging sessions into repeatable tests.

### Features

- Eval dataset export
- Basic regression test runner
- Prompt/model comparison
- CI-friendly report

## Future — TraceForge Direction

Status: Future

- Agent/tool call tracing
- Semantic cache analysis
- AI gateway integration
- OpenTelemetry export
- Langfuse export
- Promptfoo/Ragas integration