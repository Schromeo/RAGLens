# Local Retrieval Baseline (v0)

## Purpose
Document the current local retrieval implementation used by `examples/local_rag_demo`.

This baseline prioritizes transparency and deterministic behavior over semantic expressiveness.

## Current Implementation

### Document loading
- Markdown files are loaded from `sdk/python/examples/local_rag_demo/docs`.

### Chunking
- Implementation: `sdk/python/examples/local_rag_demo/local_rag/chunker.py`
- Strategy: fixed-size character chunks with overlap.
- Defaults:
  - `chunk_size = 500`
  - `overlap = 80`
- Chunk ID format: `{doc_id}::chunk_{index}`

### Retrieval
- Implementation: `sdk/python/examples/local_rag_demo/local_rag/tfidf_retriever.py`
- Vectorizer: `sklearn.feature_extraction.text.TfidfVectorizer`
- Similarity: cosine similarity (`sklearn.metrics.pairwise.cosine_similarity`)
- Ranking: descending similarity, return top-k

## Retrieval Flow

1. Build corpus matrix with `fit_transform(chunks)`.
2. Encode query with `transform([query])`.
3. Compute cosine similarity to all chunk vectors.
4. Sort by score descending.
5. Return ranked `RetrievedChunk` objects.

## Score Semantics

- Scores are lexical similarity signals from TF-IDF vectors.
- High score means stronger weighted token overlap with the query.
- This is not embedding-based semantic similarity.

## Known Limits

- Synonyms/paraphrases may score low without shared keywords.
- Chunk boundary effects may hide a fact split across chunks.
- Stop-word and tokenization defaults can affect ranking behavior.

## Why This Baseline Is Acceptable Now

- Fully local, no external model service.
- Easy to inspect and debug.
- Stable foundation for validating trace schema and warning behavior.

## Next Candidate Baseline

After Real Local RAG Demo is validated:

- sentence-transformers embeddings + cosine similarity

This should be introduced without breaking existing trace and warning contracts.
