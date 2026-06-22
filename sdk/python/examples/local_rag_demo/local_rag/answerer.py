from examples.local_rag_demo.local_rag.tfidf_retriever import RetrievedChunk


def generate_answer(
    query: str,
    retrieved_chunks: list[RetrievedChunk],
    hallucinate: bool = False,
) -> str:
    """
    A deliberately simple answer generator for the local RAG demo.

    This is not meant to be smart. Its job is to create a realistic RAG-shaped
    pipeline without requiring a real LLM API.
    """
    if hallucinate:
        return (
            "All orders arrive instantly through teleportation, and customers receive "
            "a complimentary lifetime hardware upgrade with every shipment after 45 days."
        )

    if not retrieved_chunks:
        return "I could not find enough information in the local documents to answer this question."

    top_chunk = retrieved_chunks[0]

    return (
        "Based on the retrieved local policy document, here is the most relevant information:\n\n"
        f"{top_chunk.text}"
    )