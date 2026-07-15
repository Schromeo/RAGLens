
# AGENTS.md

## Project

SledTrace is a local-first visual debugger for RAG pipelines.

## Product Goal

Help developers inspect retrieved chunks, trace LLM calls, and understand why a RAG application answered incorrectly.

## Current MVP

- Python SDK
- Local collector
- Local trace storage
- React dashboard
- Retrieval chunk visualization
- Basic RAG warning rules
- Refund policy demo

## Engineering Rules

- Keep the MVP local-first and simple.
- Prefer small, focused changes.
- Do not add auth, billing, multi-tenancy, or cloud features in v0.1.
- Do not introduce Kafka, Kubernetes, ClickHouse, or complex infrastructure in v0.1.
- Do not log private chain-of-thought.
- Do not store secrets in traces.
- Public APIs must be easy to understand and documented.
- Update docs/ai-context/DEVLOG.md after completing meaningful work.
- Update docs/ai-context/DECISIONS.md when making architecture decisions.

## Tech Stack

Planned stack:

- Python SDK for developer integration
- Go collector for trace ingestion
- SQLite for local-first storage in MVP
- React + TypeScript dashboard
- Docker Compose later for easy deployment

## Design Philosophy

SledTrace is not a full hosted LLMOps platform.

It should feel like a lightweight developer tool:

- Fast to install
- Easy to run locally
- Clear visual debugging
- Useful without a cloud account
- Compatible with existing RAG stacks

## Do Not

- Do not build a generic chatbot.
- Do not build a full Langfuse replacement.
- Do not build a generic AI gateway in v0.1.
- Do not over-engineer the MVP.


