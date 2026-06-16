import sys
from dataclasses import dataclass
from pathlib import Path

from raglens import trace

from examples.local_rag_demo.local_rag.answerer import generate_answer
from examples.local_rag_demo.local_rag.chunker import chunk_documents
from examples.local_rag_demo.local_rag.document_loader import load_markdown_documents
from examples.local_rag_demo.local_rag.tfidf_retriever import (
    RetrievedChunk,
    TfidfRetriever,
)


DEMO_ROOT = Path(__file__).parent
DOCS_DIR = DEMO_ROOT / "docs"


@dataclass(frozen=True)
class DemoCase:
    name: str
    query: str
    top_k: int = 3
    min_score: float = 0.0
    hallucinate: bool = False


CASES: dict[str, DemoCase] = {
    "refund": DemoCase(
        name="refund",
        query="How many days do I have to return a physical product?",
        top_k=3,
        min_score=0.0,
    ),
    "shipping": DemoCase(
        name="shipping",
        query="How long does standard shipping take?",
        top_k=3,
        min_score=0.0,
    ),
    "warranty": DemoCase(
        name="warranty",
        query="Does the warranty cover water damage?",
        top_k=3,
        min_score=0.0,
    ),
    "account": DemoCase(
        name="account",
        query="How can I reset my password?",
        top_k=3,
        min_score=0.0,
    ),
    "no_match": DemoCase(
        name="no_match",
        query="What is the policy for international livestock transport?",
        top_k=3,
        min_score=0.25,
    ),
    "low_score": DemoCase(
        name="low_score",
        query="Can I do something with my order?",
        top_k=3,
        min_score=0.0,
    ),
    "duplicate": DemoCase(
        name="duplicate",
        query="Do I need to verify my email address before account changes?",
        top_k=4,
        min_score=0.0,
    ),
    "conflict": DemoCase(
        name="conflict",
        query="How many days do I have to return a physical product?",
        top_k=4,
        min_score=0.0,
    ),
    "hallucinated": DemoCase(
        name="hallucinated",
        query="How long do refunds take?",
        top_k=3,
        min_score=0.0,
        hallucinate=True,
    ),
}


def build_chunks():
    documents = load_markdown_documents(DOCS_DIR)
    chunks = chunk_documents(documents)
    return documents, chunks


def inspect_demo() -> None:
    documents, chunks = build_chunks()

    print("RAGLens Real Local RAG Demo")
    print(f"Demo root: {DEMO_ROOT}")
    print(f"Docs dir: {DOCS_DIR}")
    print()
    print(f"Loaded documents: {len(documents)}")

    for document in documents:
        print(f"- {document.doc_id} ({len(document.text)} chars)")

    print()
    print(f"Generated chunks: {len(chunks)}")

    for chunk in chunks:
        preview = chunk.text.replace("\n", " ")
        if len(preview) > 100:
            preview = preview[:100] + "..."

        print()
        print(f"- {chunk.chunk_id}")
        print(f"  doc_id: {chunk.doc_id}")
        print(f"  chars: {len(chunk.text)}")
        print(f"  preview: {preview}")


def print_retrieved_chunks(results: list[RetrievedChunk]) -> None:
    print(f"Retrieved chunks: {len(results)}")

    for result in results:
        preview = result.text.replace("\n", " ")
        if len(preview) > 220:
            preview = preview[:220] + "..."

        print()
        print(f"{result.rank}. {result.chunk_id}")
        print(f"   doc_id: {result.doc_id}")
        print(f"   score: {result.score:.4f}")
        print(f"   preview: {preview}")


def retrieve_demo(query: str) -> None:
    _, chunks = build_chunks()
    retriever = TfidfRetriever(chunks)

    results = retriever.retrieve(
        query=query,
        top_k=3,
        min_score=0.0,
    )

    print("RAGLens Real Local RAG Demo")
    print(f"Query: {query}")
    print()
    print_retrieved_chunks(results)


def run_case(case: DemoCase) -> None:
    _, chunks = build_chunks()
    retriever = TfidfRetriever(chunks)

    results = retriever.retrieve(
        query=case.query,
        top_k=case.top_k,
        min_score=case.min_score,
    )

    answer = generate_answer(
        query=case.query,
        retrieved_chunks=results,
        hallucinate=case.hallucinate,
    )

    print("=" * 80)
    print(f"Case: {case.name}")
    print(f"Query: {case.query}")
    print(f"top_k: {case.top_k}")
    print(f"min_score: {case.min_score}")
    print(f"hallucinate: {case.hallucinate}")
    print()
    print_retrieved_chunks(results)
    print()
    print("Answer:")
    print(answer)
    print("=" * 80)


def run_all_cases() -> None:
    for case in CASES.values():
        run_case(case)


def to_sdk_chunks(results: list[RetrievedChunk]) -> list[dict]:
    sdk_chunks: list[dict] = []

    for result in results:
        sdk_chunks.append(
            {
                "id": result.chunk_id,
                "text": result.text,
                "score": result.score,
                "source": result.source,
                "document_id": result.doc_id,
                "metadata": {
                    "doc_id": result.doc_id,
                    "source": result.source,
                    "retriever": "tfidf",
                    "rank": result.rank,
                },
                "rank": result.rank,
            }
        )

    return sdk_chunks


def ensure_duplicate_case_chunks(
    case: DemoCase,
    results: list[RetrievedChunk],
) -> list[RetrievedChunk]:
    """
    Guarantee duplicate_chunks signal for the duplicate traced case.

    The warning rule currently requires exact text equality after normalization,
    so we append a synthetic copy of the top chunk with a different chunk ID.
    """
    if case.name != "duplicate" or not results:
        return results

    top = results[0]

    duplicate_copy = RetrievedChunk(
        chunk_id=f"{top.chunk_id}::dup_copy",
        doc_id=top.doc_id,
        source=top.source,
        text=top.text,
        score=top.score,
        rank=len(results) + 1,
    )

    return [*results, duplicate_copy]


def build_prompt(query: str, results: list[RetrievedChunk]) -> str:
    context_blocks = []

    for result in results:
        context_blocks.append(
            f"[{result.rank}] source={result.source} score={result.score:.4f}\n"
            f"{result.text}"
        )

    context = "\n\n---\n\n".join(context_blocks)

    return (
        "Answer the user question using the retrieved context.\n\n"
        f"Question: {query}\n\n"
        f"Retrieved context:\n{context}"
    )


def run_traced_case(case: DemoCase) -> None:
    _, chunks = build_chunks()
    retriever = TfidfRetriever(chunks)

    results = retriever.retrieve(
        query=case.query,
        top_k=case.top_k,
        min_score=case.min_score,
    )

    results = ensure_duplicate_case_chunks(case, results)

    answer = generate_answer(
        query=case.query,
        retrieved_chunks=results,
        hallucinate=case.hallucinate,
    )

    sdk_chunks = to_sdk_chunks(results)
    prompt = build_prompt(case.query, results)

    with trace(
        name=f"real-local-rag-{case.name}",
        query=case.query,
        metadata={
            "sdk_language": "python",
            "sdk_version": "0.1.0",
            "app": "real-local-rag-demo",
            "case": case.name,
            "environment": "local",
            "demo": "real_local_rag",
            "retriever": "tfidf",
        },
    ) as t:
        t.retrieval(
            name="local_tfidf_retriever",
            query=case.query,
            chunks=sdk_chunks,
            top_k=case.top_k,
            metadata={
                "retriever": "tfidf",
                "similarity": "cosine",
                "vectorizer": "sklearn.TfidfVectorizer",
                "min_score": case.min_score,
                "chunks_indexed": len(chunks),
            },
        )

        t.llm(
            name="simple_local_answerer",
            model="local-simple-answerer-v0",
            prompt=prompt,
            response=answer,
            metadata={
                "answerer": "template",
                "hallucinate": case.hallucinate,
                "uses_external_llm": False,
            },
        )

    print("=" * 80)
    print(f"Traced case: {case.name}")
    print(f"Query: {case.query}")
    print()
    print_retrieved_chunks(results)
    print()
    print("Answer:")
    print(answer)
    print()
    print("Trace JSON:")
    print(t.to_json())
    print()

    response = t.flush()

    print("Sent trace to RAGLens collector:")
    print(response)
    print("=" * 80)


def run_all_traced_cases() -> None:
    for case in CASES.values():
        run_traced_case(case)


def print_help() -> None:
    print("Available commands:")
    print("- inspect")
    print('- retrieve "your query"')
    print("- all")
    print("- trace <case>")
    print("- trace-all")
    for case_name in CASES:
        print(f"- {case_name}")


def main() -> None:
    command = sys.argv[1] if len(sys.argv) > 1 else "inspect"

    if command == "inspect":
        inspect_demo()
        return

    if command == "retrieve":
        if len(sys.argv) < 3:
            print('Usage: python -m examples.local_rag_demo.run_demo retrieve "your query"')
            raise SystemExit(1)

        query = " ".join(sys.argv[2:])
        retrieve_demo(query)
        return

    if command == "all":
        run_all_cases()
        return

    if command == "trace":
        if len(sys.argv) < 3:
            print("Usage: python -m examples.local_rag_demo.run_demo trace <case>")
            print("Example: python -m examples.local_rag_demo.run_demo trace conflict")
            raise SystemExit(1)

        case_name = sys.argv[2]

        if case_name not in CASES:
            print(f"Unknown case: {case_name}")
            print_help()
            raise SystemExit(1)

        run_traced_case(CASES[case_name])
        return

    if command == "trace-all":
        run_all_traced_cases()
        return

    if command in CASES:
        run_case(CASES[command])
        return

    print(f"Unknown command: {command}")
    print_help()
    raise SystemExit(1)


if __name__ == "__main__":
    main()