# Current Task

## Current Focus

Initialize the RAGLens repository from scratch.

## Current Goal

Create the project skeleton and initial documentation files that define the product direction, engineering rules, roadmap, and collaboration context.

## Files Being Created

- README.md
- AGENTS.md
- docs/ai-context/AI_HANDOFF.md
- docs/ai-context/DECISIONS.md
- docs/ai-context/ROADMAP.md
- docs/ai-context/DEVLOG.md
- docs/ai-context/CURRENT_TASK.md
- docs/product/PRODUCT_SPEC.md

## Next Step

After the documentation skeleton is created, design the v0.1 product specification and the initial trace/span data model.

# Current Task

## Current Focus

Design the initial RAGLens v0.1 architecture and trace/span data model.

## Current Goal

Define the shared data contract used by:

- Python SDK
- Go Collector
- SQLite storage
- React Dashboard

The product spec already exists and should be treated as the v0.1 product source of truth.

## Files Being Created

- docs/architecture/TRACE_DATA_MODEL.md
- docs/architecture/SYSTEM_ARCHITECTURE.md

## Key Decision

RAGLens will expose a simple Python API for developers, while internally representing RAG pipeline events using a trace/span model.

This keeps the MVP easy to use while preserving a path toward future AgentOps-style tracing.

## Next Step

Create `docs/architecture/TRACE_DATA_MODEL.md`.