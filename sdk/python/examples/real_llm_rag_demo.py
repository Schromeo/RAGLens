"""
SledTrace v0.3.5 Real LLM RAG Demo

Goal:
- Keep retrieval local and deterministic.
- Use a real OpenAI-compatible LLM for answer generation.
- Trace both retrieval and LLM spans through the existing SledTrace SDK.
- Inspect the resulting trace and diagnostics in the SledTrace dashboard.

Expected usage:

  cd sdk/python

  # Required for a real LLM call:
  export OPENAI_API_KEY="your_api_key_here"

  # Optional:
  export OPENAI_MODEL="gpt-4o-mini"
  export OPENAI_BASE_URL="https://api.openai.com/v1"
    export SLEDTRACE_COLLECTOR_URL="http://localhost:4319"

  python -m examples.real_llm_rag_demo

You can also run specific cases:

  python -m examples.real_llm_rag_demo refund
  python -m examples.real_llm_rag_demo warranty
  python -m examples.real_llm_rag_demo shipping
  python -m examples.real_llm_rag_demo mismatch
  python -m examples.real_llm_rag_demo all

Ollama example:

  ollama pull llama3.1:8b
  ollama serve

  export OPENAI_API_KEY="ollama"
  export OPENAI_BASE_URL="http://localhost:11434/v1"
  export OPENAI_MODEL="llama3.1:8b"

  python -m examples.real_llm_rag_demo refund
"""

from __future__ import annotations

import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

from sledtrace import trace


DOCS_DIR = Path(__file__).parent / "local_rag_demo" / "docs"

DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_BASE_URL = "https://api.openai.com/v1"

CASE_QUERIES = {
    "refund": "What is the refund window for a customer purchase?",
    "warranty": "How long is the product warranty and what does it cover?",
    "shipping": "How long does standard shipping usually take?",
    "mismatch": (
        "A customer says they can return an item after 45 days. "
        "Is that allowed under the refund policy?"
    ),
}


@dataclass
class Document:
    source: str
    text: str


@dataclass
class RetrievedChunk:
    id: str
    source: str
    text: str
    score: float
    rank: int


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())


def now_ms() -> int:
    return int(time.time() * 1000)


def load_documents(docs_dir: Path = DOCS_DIR) -> List[Document]:
    if not docs_dir.exists():
        raise FileNotFoundError(
            f"Could not find docs directory: {docs_dir}\n"
            "Expected local demo docs at sdk/python/examples/local_rag_demo/docs."
        )

    docs: List[Document] = []

    for path in sorted(docs_dir.glob("*.md")):
        text = path.read_text(encoding="utf-8").strip()
        if text:
            docs.append(Document(source=path.name, text=text))

    if not docs:
        raise RuntimeError(f"No markdown documents found in {docs_dir}")

    return docs


def chunk_document(
    doc: Document,
    max_chars: int = 650,
    overlap_chars: int = 100,
) -> List[Tuple[str, str, str]]:
    """
    Small deterministic chunker.

    Returns:
      (chunk_id, source, chunk_text)
    """
    text = doc.text.strip()

    if len(text) <= max_chars:
        return [(f"{doc.source}::chunk_0", doc.source, text)]

    chunks: List[Tuple[str, str, str]] = []
    start = 0
    idx = 0

    while start < len(text):
        end = min(start + max_chars, len(text))
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append((f"{doc.source}::chunk_{idx}", doc.source, chunk_text))

        if end >= len(text):
            break

        start = max(0, end - overlap_chars)
        idx += 1

    return chunks


def build_chunks(documents: Sequence[Document]) -> List[Tuple[str, str, str]]:
    chunks: List[Tuple[str, str, str]] = []

    for doc in documents:
        chunks.extend(chunk_document(doc))

    return chunks


def compute_idf(chunks: Sequence[Tuple[str, str, str]]) -> Dict[str, float]:
    """
    Lightweight TF-IDF-style IDF calculation.

    This avoids adding sklearn as a dependency for the demo.
    """
    doc_count = len(chunks)
    df: Dict[str, int] = {}

    for _, _, text in chunks:
        terms = set(tokenize(text))

        for term in terms:
            df[term] = df.get(term, 0) + 1

    idf: Dict[str, float] = {}

    for term, count in df.items():
        idf[term] = math.log((doc_count + 1) / (count + 1)) + 1.0

    return idf


def retrieve(
    query: str,
    chunks: Sequence[Tuple[str, str, str]],
    top_k: int = 3,
) -> List[RetrievedChunk]:
    """
    Deterministic local retriever.

    Scores chunks by weighted lexical overlap with the query.
    This is intentionally simple so the demo focuses on SledTrace observability,
    not retrieval framework complexity.
    """
    idf = compute_idf(chunks)
    query_terms = tokenize(query)
    query_term_set = set(query_terms)

    scored: List[RetrievedChunk] = []

    for chunk_id, source, text in chunks:
        chunk_terms = tokenize(text)
        chunk_term_set = set(chunk_terms)
        overlap = query_term_set.intersection(chunk_term_set)

        if not overlap:
            score = 0.0
        else:
            weighted_overlap = sum(idf.get(term, 1.0) for term in overlap)
            query_weight = sum(idf.get(term, 1.0) for term in query_term_set) or 1.0
            score = weighted_overlap / query_weight

        scored.append(
            RetrievedChunk(
                id=chunk_id,
                source=source,
                text=text,
                score=round(score, 4),
                rank=0,
            )
        )

    scored.sort(key=lambda c: c.score, reverse=True)

    top = scored[:top_k]

    for idx, chunk in enumerate(top, start=1):
        chunk.rank = idx

    return top


def build_prompt(
    query: str,
    chunks: Sequence[RetrievedChunk],
    case_name: str,
) -> str:
    context_blocks = []

    for chunk in chunks:
        context_blocks.append(
            f"[Source: {chunk.source}, Chunk: {chunk.id}, Score: {chunk.score}]\n"
            f"{chunk.text}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    base_instruction = """
You are answering a user question using only the provided retrieved context.

Rules:
- Prefer the retrieved context over outside knowledge.
- If the context does not support the answer, say that the retrieved context is insufficient.
- Be concise.
- Include specific numeric policy values only when they appear in the context.
""".strip()

    if case_name == "mismatch":
        extra_instruction = """
The user may be asking about an incorrect numeric value. Carefully compare the user's number against the retrieved policy text.
""".strip()
    else:
        extra_instruction = ""

    return f"""
{base_instruction}

{extra_instruction}

Retrieved context:

{context}

User question:

{query}

Answer:
""".strip()


def call_openai_compatible_chat_completion(
    prompt: str,
    model: str,
    api_key: str,
    base_url: str,
    timeout_seconds: int = 60,
) -> str:
    """
    Calls an OpenAI-compatible /chat/completions endpoint using only stdlib.

    This avoids requiring the openai Python package for the demo.
    """
    normalized_base_url = base_url.rstrip("/")
    url = f"{normalized_base_url}/chat/completions"

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a careful assistant helping test a RAG debugging tool. "
                    "Answer only from the retrieved context when possible."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
    }

    request = urllib.request.Request(
        url=url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read().decode("utf-8")
    except urllib.error.HTTPError as exc:
        error_body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"LLM request failed with HTTP {exc.code}.\n"
            f"Response body:\n{error_body}"
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"LLM request failed: {exc}") from exc

    data = json.loads(raw)

    try:
        return data["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(
            f"Unexpected LLM response shape:\n{json.dumps(data, indent=2)}"
        ) from exc


def to_SledTrace_chunks(chunks: Sequence[RetrievedChunk]) -> List[Dict[str, Any]]:
    """
    Convert local chunk objects into the SDK-friendly chunk payload shape.

    Existing warning rules depend on fields such as id, text, source, score, and rank.
    """
    return [
        {
            "id": chunk.id,
            "text": chunk.text,
            "source": chunk.source,
            "score": chunk.score,
            "rank": chunk.rank,
            "metadata": {
                "demo": "real_llm_rag_demo",
                "demo_version": "v0.3.5",
                "retriever": "local_tfidf_style_retriever",
            },
        }
        for chunk in chunks
    ]


def record_retrieval_span(
    t: Any,
    query: str,
    chunks: Sequence[RetrievedChunk],
    elapsed_ms: Optional[int] = None,
) -> None:
    """
    Compatibility helper for the retrieval span API.

    The current SDK examples should have a retrieval-span method, but this helper
    makes the demo slightly more robust if method names changed during development.
    """
    metadata: Dict[str, Any] = {
        "retriever": "local_tfidf_style_retriever",
        "demo_version": "v0.3.5",
    }

    if elapsed_ms is not None:
        metadata["latency_ms"] = elapsed_ms
        metadata["duration_ms"] = elapsed_ms

    payload = {
        "name": "local_tfidf_style_retriever",
        "query": query,
        "chunks": to_SledTrace_chunks(chunks),
        "top_k": len(chunks),
        "metadata": metadata,
    }

    for method_name in (
        "retrieval",
        "retrieval_span",
        "log_retrieval",
        "add_retrieval_span",
    ):
        method = getattr(t, method_name, None)

        if callable(method):
            method(**payload)
            return

    raise AttributeError(
        "Could not find a retrieval span method on the SledTrace trace object. "
        "Expected one of: retrieval, retrieval_span, log_retrieval, add_retrieval_span."
    )


def record_llm_span(
    t: Any,
    model: str,
    prompt: str,
    response: str,
    elapsed_ms: int,
) -> None:
    """
    Compatibility helper for the LLM span API.
    """
    payload = {
        "name": "real_llm_answer_generation",
        "model": model,
        "prompt": prompt,
        "response": response,
        "metadata": {
            "provider": "openai_compatible",
            "temperature": 0.2,
            "latency_ms": elapsed_ms,
            "duration_ms": elapsed_ms,
            "demo_version": "v0.3.5",
        },
    }

    for method_name in (
        "llm",
        "llm_span",
        "log_llm",
        "add_llm_span",
    ):
        method = getattr(t, method_name, None)

        if callable(method):
            method(**payload)
            return

    raise AttributeError(
        "Could not find an LLM span method on the SledTrace trace object. "
        "Expected one of: llm, llm_span, log_llm, add_llm_span."
    )


def flush_trace(t: Any) -> None:
    flush = getattr(t, "flush", None)

    if not callable(flush):
        raise AttributeError("Could not find flush() on the SledTrace trace object.")

    flush()


def run_case(case_name: str) -> None:
    if case_name not in CASE_QUERIES:
        valid = ", ".join(sorted(CASE_QUERIES.keys())) + ", all"
        raise ValueError(f"Unknown case: {case_name}. Valid cases: {valid}")

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL", DEFAULT_MODEL)
    base_url = os.getenv("OPENAI_BASE_URL", DEFAULT_BASE_URL)

    if not api_key:
        print(
            "\nMissing OPENAI_API_KEY.\n\n"
            "This demo intentionally calls a real OpenAI-compatible LLM.\n"
            "Set OPENAI_API_KEY first, for example:\n\n"
            '  export OPENAI_API_KEY="your_api_key_here"\n\n'
            "Optional:\n\n"
            f'  export OPENAI_MODEL="{DEFAULT_MODEL}"\n'
            f'  export OPENAI_BASE_URL="{DEFAULT_BASE_URL}"\n\n'
            "No trace was sent because the real LLM call was skipped.\n"
        )
        return

    query = CASE_QUERIES[case_name]

    docs_started = now_ms()
    documents = load_documents()
    all_chunks = build_chunks(documents)
    docs_elapsed_ms = now_ms() - docs_started

    retrieval_started = now_ms()
    retrieved_chunks = retrieve(query, all_chunks, top_k=3)
    retrieval_elapsed_ms = now_ms() - retrieval_started

    prompt = build_prompt(query, retrieved_chunks, case_name)

    print("=" * 80)
    print(f"SledTrace Real LLM RAG Demo case: {case_name}")
    print(f"Query: {query}")
    print(f"Model: {model}")
    print(f"Base URL: {base_url}")
    print(f"Loaded documents: {len(documents)}")
    print(f"Built chunks: {len(all_chunks)}")
    print(f"Document/chunk preparation latency: {docs_elapsed_ms}ms")
    print(f"Retrieval latency: {retrieval_elapsed_ms}ms")
    print("\nRetrieved chunks:")

    for chunk in retrieved_chunks:
        print(
            f"  rank={chunk.rank} score={chunk.score:.4f} "
            f"source={chunk.source} id={chunk.id}"
        )

    trace_name = f"real-llm-rag-demo-{case_name}"

    with trace(
        trace_name,
        query=query,
        metadata={
            "demo": "real_llm_rag_demo",
            "demo_version": "v0.3.5",
            "provider": "openai_compatible",
            "model": model,
            "docs_elapsed_ms": docs_elapsed_ms,
            "retrieval_elapsed_ms": retrieval_elapsed_ms,
        },
    ) as t:
        record_retrieval_span(
            t=t,
            query=query,
            chunks=retrieved_chunks,
            elapsed_ms=retrieval_elapsed_ms,
        )

        llm_started = now_ms()
        answer = call_openai_compatible_chat_completion(
            prompt=prompt,
            model=model,
            api_key=api_key,
            base_url=base_url,
        )
        llm_elapsed_ms = now_ms() - llm_started

        record_llm_span(
            t=t,
            model=model,
            prompt=prompt,
            response=answer,
            elapsed_ms=llm_elapsed_ms,
        )

        flush_trace(t)

    print("\nLLM answer:")
    print(answer)
    print(f"\nLLM latency: {llm_elapsed_ms}ms")
    print(f"Trace flushed: {trace_name}")
    print("Open the SledTrace dashboard and inspect the trace detail page.")
    print("=" * 80)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = list(argv if argv is not None else sys.argv[1:])
    case_name = args[0] if args else "refund"

    try:
        if case_name == "all":
            for name in CASE_QUERIES:
                run_case(name)

            return 0

        run_case(case_name)
        return 0
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
    except Exception as exc:
        print(f"\nreal_llm_rag_demo failed: {exc}\n", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


