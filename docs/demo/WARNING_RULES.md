# Warning Rules

This document describes the current v0.1 warning rules used by the RAGLens local demo.

The warning engine is intentionally simple in v0.1.
The goal is to make common RAG failure modes visible during local development, not to provide a complete factuality or evaluation system.

Related docs:

- [Local demo runbook](LOCAL_RAG_DEMO.md)
- [Smoke test checklist](SMOKE_TEST.md)

## Rule Summary

| Warning | What it detects | Demo case |
| --- | --- | --- |
| `no_retrieved_chunks` | The retriever returned no usable chunks | `no_match` |
| `low_retrieval_score` | Retrieved chunks have weak relevance scores | `low_score` |
| `duplicate_chunks` | Retrieved chunks contain duplicated text | `duplicate` |
| `conflicting_chunks` | Retrieved chunks contain conflicting policy signals | `conflict` |
| `answer_not_grounded` | The answer contains an unsupported numeric day-count claim | `hallucinated` |

## `no_retrieved_chunks`

This warning fires when the retrieval span contains no retrieved chunks.

It represents a retrieval miss: the RAG pipeline has no evidence to use.

Demo case:

```txt
no_match
```

## `low_retrieval_score`

This warning fires when retrieved chunks have low relevance scores.

It represents weak retrieval confidence. The system found chunks, but they may not be good enough to support an answer.

Demo case:

```txt
low_score
```

## `duplicate_chunks`

This warning fires when retrieved chunks contain duplicated text.

It represents redundant context. Duplicate chunks can waste context window space and over-weight repeated evidence.

Demo case:

```txt
duplicate
```

## `conflicting_chunks`

This warning fires when retrieved chunks contain conflicting policy information.

In the local demo, this is shown with refund policy chunks that mention different return windows.

Demo case:

```txt
conflict
```

## `answer_not_grounded`

This is a simplified v0.1 grounding rule.

It currently detects unsupported numeric day-count claims. For example, if the retrieved context says shipping usually takes 5 to 7 business days, but the generated answer says 45 days, the warning can fire.

Demo case:

```txt
hallucinated
```

## Current Limitation

This is not a full grounding evaluator.

It does not yet perform:

- claim extraction
- semantic entailment
- full factuality checking
- LLM-as-judge evaluation
- general unsupported statement detection

For v0.1, the goal is to demonstrate the shape of grounding diagnostics with a deterministic local rule.

Future versions can expand this into richer grounding analysis.