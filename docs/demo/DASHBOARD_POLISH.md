# Dashboard Demo Polish Checklist

This checklist defines the minimum dashboard polish needed for the SledTrace v0.1 local demo.

The goal is not to make the UI visually fancy.

The goal is to make RAG debugging understandable at a glance.

## Product goal

When a developer opens a demo trace, they should quickly understand:

- what the user asked
- what chunks were retrieved
- how confident retrieval was
- what answer was produced
- what warnings were generated
- why the warning matters

SledTrace should make the RAG pipeline visible:

```txt
Query
  ->
Retrieval
  ->
Retrieved chunks
  ->
Prompt
  ->
Answer
  ->
Warnings
````

## Trace list

The trace list should help users find interesting demo traces quickly.

Checklist:

* [ ] Show trace name clearly
* [ ] Show trace status
* [ ] Show created time
* [ ] Show warning count if available
* [ ] Make demo traces easy to recognize
* [ ] Show enough metadata to distinguish demo cases
* [ ] Avoid requiring users to click every trace blindly

Useful demo traces:

* `real-local-rag-conflict`
* `real-local-rag-hallucinated`
* `real-local-rag-no_match`
* `real-local-rag-low_score`
* `real-local-rag-duplicate`

## Trace detail header

The top of the trace detail page should summarize the trace before showing raw spans.

Checklist:

* [ ] Show trace name
* [ ] Show user query
* [ ] Show final answer if available
* [ ] Show status
* [ ] Show warning count
* [ ] Show duration if available
* [ ] Show demo case metadata if available

The user should not need to scroll deeply to understand what the trace is about.

## Warning cards

Warning cards are the main product value in the v0.1 demo.

Checklist:

* [ ] Show warning cards near the top of the trace detail page
* [ ] Show warning type clearly
* [ ] Show short human-readable warning message
* [ ] Show severity if available
* [ ] Show evidence or reason if available
* [ ] Make multiple warnings easy to scan
* [ ] Avoid hiding warnings below raw JSON or low-level span data

Expected warning types:

* `no_retrieved_chunks`
* `low_retrieval_score`
* `duplicate_chunks`
* `conflicting_chunks`
* `answer_not_grounded`

## Retrieved chunks viewer

The retrieved chunks viewer should help users inspect evidence quality.

Checklist:

* [ ] Show chunk rank
* [ ] Show chunk score
* [ ] Show chunk source / document id
* [ ] Show chunk text preview
* [ ] Preserve enough text to understand evidence
* [ ] Make low scores noticeable
* [ ] Make duplicate chunks easy to notice
* [ ] Make conflicting chunks easy to compare

For the `conflict` trace, users should be able to see conflicting policy information from retrieved chunks.

For the `duplicate` trace, users should be able to see repeated chunk text.

## LLM prompt / response viewer

The prompt / response section should make grounding issues debuggable.

Checklist:

* [ ] Show prompt
* [ ] Show generated answer
* [ ] Keep prompt readable
* [ ] Keep answer readable
* [ ] Make it possible to compare answer against retrieved chunks

For the `hallucinated` trace, users should be able to see that the answer is not supported by retrieved chunks.

## Empty, loading, and error states

The dashboard should fail clearly during local development.

Checklist:

* [ ] Show clear empty state when no traces exist
* [ ] Show loading state while fetching traces
* [ ] Show error state if collector is unavailable
* [ ] Show helpful message if a trace cannot be found

Possible empty state copy:

```txt
No traces yet.

Run the local RAG demo to generate traces:
python -m examples.local_rag_demo.run_demo trace-all
```

## Demo screenshot targets

These are the screenshots or GIF frames that should eventually appear in the README.

Checklist:

* [ ] Trace list with multiple local RAG demo traces
* [ ] Trace detail for `real-local-rag-conflict`
* [ ] Warning cards section
* [ ] Retrieved chunks viewer
* [ ] LLM prompt / response viewer
* [ ] Trace detail for `real-local-rag-hallucinated`

## Out of scope for v0.1 polish

Do not prioritize these yet:

* full design system
* authentication
* cloud sync
* team workspaces
* advanced filtering
* complex charts
* timeline animations
* dark mode
* real-time streaming
* LangChain-specific UI
* LlamaIndex-specific UI

These can come later.

For v0.1, the dashboard only needs to make the local RAG debugging story clear.

## Definition of done

Dashboard demo polish is good enough for v0.1 when:

* a new user can find generated demo traces
* a new user can open a trace and understand the query
* warning cards are visible without hunting
* retrieved chunks and scores are visible
* prompt and answer are visible
* the `conflict` case clearly shows conflicting evidence
* the `hallucinated` case clearly shows an unsupported answer
* the dashboard is good enough for README screenshots



