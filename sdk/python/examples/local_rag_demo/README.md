# Real Local RAG Demo

This demo validates the real local retrieval path using the current RAGLens trace schema:

`local docs -> chunking -> TF-IDF retrieval -> trace flush -> collector warnings -> dashboard`

## Setup

Run from the repository root:

```powershell
cd sdk/python
$env:RAGLENS_COLLECTOR_URL="http://localhost:4319"
```

Make sure the collector is running on `:4319` before `trace` commands.

## Commands

Inspect loaded docs and generated chunks:

```powershell
python -m examples.local_rag_demo.run_demo inspect
```

Run one retrieval-only query (no trace flush):

```powershell
python -m examples.local_rag_demo.run_demo retrieve "How long does standard shipping take?"
```

Run one traced case and send to collector:

```powershell
python -m examples.local_rag_demo.run_demo trace conflict
```

Run all traced cases:

```powershell
python -m examples.local_rag_demo.run_demo trace-all
```

## Available Cases

- `refund`
- `shipping`
- `warranty`
- `account`
- `no_match`
- `low_score`
- `duplicate`
- `conflict`
- `hallucinated`

## Expected Warning Mapping

Deterministic warning-target cases:

- `no_match` -> `no_retrieved_chunks`
- `low_score` -> `low_retrieval_score`
- `duplicate` -> `duplicate_chunks`
- `conflict` -> `conflicting_chunks`
- `hallucinated` -> `answer_not_grounded`

Notes:

- `duplicate` is intentionally forced to trigger by appending one synthetic exact duplicate chunk in the traced path.
- `trace-all` does not mean each case returns exactly one warning.
- Some cases can return zero warnings (for example `warranty`), and some can return multiple warnings depending on retrieved context and answer content.

## Quick Verification

If you want a compact warning summary per case:

```powershell
$cases = @('refund','shipping','warranty','account','no_match','low_score','duplicate','conflict','hallucinated')
foreach($c in $cases){
	Write-Output "CASE $c"
	$out = python -m examples.local_rag_demo.run_demo trace $c 2>&1
	($out | Select-String "warnings_generated").Line
}
```