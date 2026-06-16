from dataclasses import dataclass

from examples.local_rag_demo.local_rag.document_loader import Document


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    doc_id: str
    source: str
    text: str


def chunk_document(
    document: Document,
    chunk_size: int = 500,
    overlap: int = 80,
) -> list[Chunk]:
    """
    Split one document into fixed-size overlapping character chunks.

    This is intentionally simple for v0:
    - deterministic
    - no tokenizer dependency
    - good enough for local demo retrieval
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    text = document.text.strip()
    chunks: list[Chunk] = []

    start = 0
    chunk_index = 0

    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk_text = text[start:end].strip()

        if chunk_text:
            chunks.append(
                Chunk(
                    chunk_id=f"{document.doc_id}::chunk_{chunk_index}",
                    doc_id=document.doc_id,
                    source=document.path,
                    text=chunk_text,
                )
            )
            chunk_index += 1

        if end == len(text):
            break

        start = end - overlap

    return chunks


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 500,
    overlap: int = 80,
) -> list[Chunk]:
    all_chunks: list[Chunk] = []

    for document in documents:
        all_chunks.extend(
            chunk_document(
                document=document,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        )

    return all_chunks