# AI Handoff

## Project Name

RAGLens

## One-liner

RAGLens is a local-first visual debugger for RAG pipelines.

## Core Problem

RAG developers often do not know why their system answered incorrectly.

A wrong answer may come from:

- Bad retrieval
- Bad chunking
- Stale context
- Conflicting chunks
- Weak grounding
- LLM ignoring retrieved evidence

RAGLens helps developers inspect the full RAG pipeline locally.

## Target Users

- AI application developers
- RAG builders
- Backend engineers adding LLM/RAG to their systems
- Indie hackers building AI apps
- Developers debugging retrieval pipelines

## MVP Scope

v0.1 should support:

- Python SDK
- Trace context manager
- Retrieval span logging
- LLM call logging
- Local collector
- Local storage
- Trace list UI
- Trace detail UI
- Retrieved chunks viewer
- Basic warning rules
- Refund policy demo

## Long-term Vision

RAGLens starts as a local-first RAG debugger.

Over time, it can evolve into a broader LLM/Agent observability and evaluation platform, internally referred to as TraceForge.

Potential future modules:

- Agent/tool call tracing
- Prompt/model regression testing
- Eval dataset generation
- Semantic cache analysis
- AI gateway integration
- OpenTelemetry export
- Langfuse/Promptfoo/Ragas interoperability

## Current Strategy

Start narrow.

Do not build a full AI infra platform first.

Build a polished, useful, easy-to-run RAG debugging tool first.