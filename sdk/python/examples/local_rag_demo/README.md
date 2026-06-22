# Real Local RAG Demo

## What This Demo Is

This demo is a real, local retrieval pipeline wired into the existing RAGLens trace path.

It replaces synthetic retrieval chunks with actual retrieval output while preserving the same SDK trace schema, collector ingestion flow, SQLite persistence, dashboard visualization, and warning engine behavior.

## Why This Demo Exists

The goal is to prove that RAGLens can diagnose real retrieval behavior, not only handcrafted warning examples.

This milestone keeps the implementation intentionally simple and local-first:

- local markdown policy documents
- deterministic chunking
- TF-IDF plus cosine similarity retrieval
- simple local answer generation without external LLM calls

## Directory Structure

```text
local_rag_demo/
	README.md
	__init__.py
	run_demo.py
	docs/
		refund_policy.md
		legacy_refund_policy.md
		shipping_policy.md
		account_policy.md
		warranty_policy.md
	local_rag/
		__init__.py
		document_loader.py
		chunker.py
		tfidf_retriever.py
		answerer.py
```

## How The Local RAG Pipeline Works

1. Load markdown policy files from local disk.
2. Split each document into deterministic chunks.
3. Build TF-IDF vectors and score chunks with cosine similarity.
4. Return ranked chunks with chunk id, document id, source path, rank, text, and score.
5. Generate a local answer from retrieved chunks.
6. Map retrieved chunks into existing SDK retrieval span schema.
7. Send trace via trace(), t.retrieval(), t.llm(), and t.flush().
8. Collector stores trace, spans, warnings in SQLite.
9. Dashboard shows real retrieval traces and warning cards.

End-to-end flow:

```text
Python SDK
	-> t.flush()
	-> POST /api/traces
	-> Go Collector (:4319)
	-> SQLite (traces, spans, warnings)
	-> GET /api/traces/{trace_id}
	-> Dashboard warning cards
```

## Prerequisites

Run these commands from sdk/python.

Collector should already be running on port 4319.

```powershell
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
```

## Run Inspect

Inspect loaded docs and generated chunks.

```powershell
python -m examples.local_rag_demo.run_demo inspect
```

## Run Retrieve

Run one retrieval query locally, without sending traces.

```powershell
python -m examples.local_rag_demo.run_demo retrieve "How long does standard shipping take?"
```

## Run One Traced Case

Run a single traced case and send it to the collector.

```powershell
python -m examples.local_rag_demo.run_demo trace conflict
```

## Run All Traced Cases

```powershell
python -m examples.local_rag_demo.run_demo trace-all
```

## Expected Warning Cases

- no_match -> no_retrieved_chunks
- low_score -> low_retrieval_score
- duplicate -> duplicate_chunks
- conflict -> conflicting_chunks
- hallucinated -> answer_not_grounded

Notes:

- duplicate is intentionally forced by adding one synthetic exact-duplicate chunk in traced mode.
- trace-all does not imply one warning per case.
- some cases can produce zero warnings and some can produce multiple warnings.

## Available Cases

- refund
- shipping
- warranty
- account
- no_match
- low_score
- duplicate
- conflict
- hallucinated

## Dashboard Verification

After running trace or trace-all, open the dashboard and inspect trace detail pages.

You should see:

- real retrieved chunks and similarity scores
- warning cards generated from real retrieval output

## Non-Goals In This Milestone

- No LangChain integration yet.
- No LlamaIndex integration yet.
- No vector database yet.
- No external embeddings service.

These are intentionally deferred to keep v0.1 local-first, transparent, and simple.