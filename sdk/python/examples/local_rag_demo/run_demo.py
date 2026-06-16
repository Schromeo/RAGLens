import sys
from pathlib import Path

from examples.local_rag_demo.local_rag.chunker import chunk_documents
from examples.local_rag_demo.local_rag.document_loader import load_markdown_documents
from examples.local_rag_demo.local_rag.tfidf_retriever import TfidfRetriever


DEMO_ROOT = Path(__file__).parent
DOCS_DIR = DEMO_ROOT / "docs"


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
    print(f"Top {len(results)} retrieved chunks:")

    for result in results:
        preview = result.text.replace("\n", " ")
        if len(preview) > 220:
            preview = preview[:220] + "..."

        print()
        print(f"{result.rank}. {result.chunk_id}")
        print(f"   doc_id: {result.doc_id}")
        print(f"   score: {result.score:.4f}")
        print(f"   preview: {preview}")


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

    print(f"Unknown command: {command}")
    print("Available commands:")
    print("- inspect")
    print('- retrieve "your query"')
    raise SystemExit(1)


if __name__ == "__main__":
    main()