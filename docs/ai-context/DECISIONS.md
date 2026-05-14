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