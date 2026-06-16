# Real Local RAG Demo Milestone

## Status
Active

## Goal
Replace mock retrieval chunks with real local retrieval output while keeping the existing RAGLens trace schema and warning pipeline unchanged.

## Why This Milestone
The Warning Engine / Diagnosis Layer MVP is complete and validated end-to-end.

This milestone validates that warnings remain useful on real retrieval data, not only synthetic demo chunks.

## Current Baseline (Already Working)

```text
Python SDK
  -> t.flush()
  -> POST /api/traces
  -> Go Collector (:4319)
  -> SQLite (traces/spans/warnings)
  -> GET /api/traces/{trace_id}
  -> React Dashboard warning cards
```

Implemented warning rules:

- `no_retrieved_chunks`
- `low_retrieval_score`
- `duplicate_chunks`
- `conflicting_chunks`
- simplified `answer_not_grounded`

Primary smoke test:

- `python -m examples.warning_rules_demo all`
- Expected: each case returns `warnings_generated: 1`.

## Scope

1. Local documents in `sdk/python/examples/local_rag_demo/docs`.
2. Deterministic local chunking.
3. Transparent local retriever first (TF-IDF + cosine similarity).
4. Real top-k chunks and relevance scores.
5. Trace emission through current Python SDK API.
6. Collector persistence and warning generation unchanged.

## Non-Goals

- Do not introduce LangChain adapters in this milestone.
- Do not introduce LlamaIndex adapters in this milestone.
- Do not change trace/warning schema unless a blocker appears.

## Exit Criteria

1. A real query retrieves real local chunks with scores.
2. Trace payload includes retrieval chunks and LLM output in existing schema.
3. Collector stores traces/spans/warnings successfully.
4. Dashboard displays real warnings on trace detail.
5. Existing warning smoke test still passes.

## Runbook

```powershell
# terminal 1
cd collector/go
go run ./cmd/raglens-collector

# terminal 2
cd sdk/python
python -m examples.local_rag_demo.run_demo inspect
python -m examples.local_rag_demo.run_demo retrieve "How can I reset my password?"
python -m examples.warning_rules_demo all
```

## Risks

- Keyword-based retrieval may miss semantically similar phrasing.
- Character chunking can split facts at boundaries.
- Low-score thresholds may need tuning for real corpora.

## Follow-up After Completion

- Improve warning explanation and details rendering.
- Add unit tests for warning rules.
- Evaluate semantic retrieval baseline (sentence-transformers + cosine).
- Consider framework adapters after schema and warning behavior remain stable.
