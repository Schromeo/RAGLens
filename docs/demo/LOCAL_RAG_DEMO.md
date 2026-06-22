
# Local RAG Demo

This demo shows RAGLens debugging a fully local, deterministic RAG pipeline.

It uses:

- local markdown policy documents
- simple document loading
- simple chunking
- TF-IDF retrieval
- cosine similarity scores
- a local template-based answerer
- the RAGLens Python SDK
- the local Go collector
- the React dashboard

No external LLM API is required.  
No API key is required.

## Why this demo exists

RAG applications can fail for different reasons.

A bad answer may come from:

- no useful retrieved context
- weak retrieval confidence
- duplicated chunks
- conflicting retrieved evidence
- an answer that is not grounded in the retrieved chunks

This demo generates representative traces for those failure modes so they can be inspected in the RAGLens dashboard.

## Prerequisites

Start the RAGLens collector:

```bash
cd collector/go
go run ./cmd/raglens-collector
```

The collector should run on:

```txt
http://localhost:4319
```

Start the dashboard in another terminal:

```bash
cd dashboard/web
npm install
npm run dev
```

Related docs:

- [Warning rules and limitations](WARNING_RULES.md)
- [Smoke test checklist](SMOKE_TEST.md)

Then run the demo from the Python SDK directory:

```bash
cd sdk/python
```

For PowerShell:

```powershell
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
```

For Bash:

```bash
export RAGLENS_COLLECTOR_URL="http://localhost:4319"
```

## Commands

Inspect local documents and generated chunks:

```bash
python -m examples.local_rag_demo.run_demo inspect
```

Run retrieval for a custom query:

```bash
python -m examples.local_rag_demo.run_demo retrieve "How long does standard shipping take?"
```

Run all non-traced local demo cases in the terminal:

```bash
python -m examples.local_rag_demo.run_demo all
```

Generate one traced case:

```bash
python -m examples.local_rag_demo.run_demo trace conflict
```

Generate all warning-focused traced demo cases:

```bash
python -m examples.local_rag_demo.run_demo trace-all
```

## Demo cases

| Case           | What it simulates                                           | Expected warning      |
| -------------- | ----------------------------------------------------------- | --------------------- |
| `no_match`     | The retriever finds no useful chunks for the query          | `no_retrieved_chunks` |
| `low_score`    | The retriever returns weakly relevant chunks                | `low_retrieval_score` |
| `duplicate`    | The retrieved context contains duplicated evidence          | `duplicate_chunks`    |
| `conflict`     | The retrieved chunks contain conflicting policy information | `conflicting_chunks`  |
| `hallucinated` | The answer is not supported by the retrieved chunks         | `answer_not_grounded` |

For details about the current warning rules and their limitations, see [WARNING_RULES.md](WARNING_RULES.md).

## Recommended demo flow

1. Start the collector.
2. Start the dashboard.
3. Run:

```bash
python -m examples.local_rag_demo.run_demo trace-all
```

4. Open the dashboard.
5. Inspect the generated traces.

Recommended traces to inspect first:

* `real-local-rag-conflict`
* `real-local-rag-hallucinated`
* `real-local-rag-no_match`

## What to look for in the dashboard

For each trace, check:

1. The original query.
2. The retrieved chunks.
3. The retrieval scores.
4. The generated answer.
5. The warning cards.

The goal is not just to see that a warning was generated.

The goal is to understand where the RAG pipeline failed:

```txt
Query
  ↓
Retrieval
  ↓
Retrieved chunks
  ↓
Prompt
  ↓
Answer
  ↓
Warnings
```

## Notes

The demo intentionally uses a local deterministic answerer instead of a real LLM.

This keeps the default demo:

* local-first
* deterministic
* free to run
* easy to debug
* suitable for smoke tests and screenshots

Real LLM integrations can be added later, but they should not be required for the default v0.1 demo path.

