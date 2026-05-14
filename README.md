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

RAGLens is currently in early development.

# Roadmap
- Python SDK
- Local collector
- Trace list page
- Trace detail page
- Retrieved chunk viewer
- Basic RAG warnings
- LangChain / LlamaIndex examples
- Eval dataset export
- Agent/tool call tracing