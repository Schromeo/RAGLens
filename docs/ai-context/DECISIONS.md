# Architecture Decisions

## 2026-05-14 — Start with RAGLens instead of full TraceForge

### Decision

Start with RAGLens, a local-first visual debugger for RAG pipelines.

### Reason

A full AI observability platform is too broad for the first version. A focused RAG debugging tool has a clearer user pain point and a better chance of being useful to developers.

### Alternatives Considered

- Full AgentOps platform
- AI Gateway with semantic cache
- Multi-agent PR reviewer
- Generic LLM evaluation framework

### Outcome

RAGLens will be the first product cut.

The long-term platform vision remains TraceForge.

---

## 2026-05-14 — Use local-first development as the MVP principle

### Decision

RAGLens v0.1 should run locally with minimal setup.

### Reason

Community adoption is more likely if users can try the tool quickly without signing up for a cloud service or deploying complex infrastructure.

### Outcome

The MVP should prioritize:

- Simple install
- Local collector
- Local storage
- Local dashboard
- Example app

# Decisions

## 2026-05-14

### RAGLens starts as a local-first RAG debugger

RAGLens v0.1 will focus on helping developers understand why a RAG pipeline produced a bad answer.

It will not start as a full LLM observability platform.

### Trace/span model will be designed with future AgentOps support

The initial data model will use traces and spans.

A trace represents one complete RAG request.

A span represents one step inside the pipeline, such as retrieval, prompt construction, or LLM generation.

This keeps v0.1 narrow while preserving a path toward broader agent tracing later.

### Local storage will use SQLite

RAGLens v0.1 will use SQLite for local-first storage.

This keeps setup simple and avoids requiring developers to run external infrastructure.

### v0.1 span types

The initial supported span types are:

- retrieval
- prompt
- llm
- custom

Additional span types such as tool_call, agent_step, memory_read, rerank, and eval may be added later.