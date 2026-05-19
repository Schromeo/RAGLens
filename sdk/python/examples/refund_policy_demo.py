from raglens import trace


def main() -> None:
    query = "What is the refund window?"

    with trace(
        "refund-policy-qa",
        query=query,
        metadata={
            "app": "refund-policy-demo",
            "environment": "local",
        },
    ) as t:
        t.retrieval(
            name="search_refund_docs",
            query=query,
            top_k=2,
            chunks=[
                {
                    "id": "chunk_1",
                    "text": "Customers may request a refund within 30 days.",
                    "score": 0.91,
                    "source": "refund_policy_new.md",
                    "document_id": "refund_policy_new",
                    "metadata": {
                        "version": "2026",
                        "policy_type": "refund",
                    },
                },
                {
                    "id": "chunk_2",
                    "text": "Customers may request a refund within 14 days.",
                    "score": 0.84,
                    "source": "refund_policy_old.md",
                    "document_id": "refund_policy_old",
                    "metadata": {
                        "version": "2024",
                        "policy_type": "refund",
                    },
                },
            ],
            metadata={
                "retriever": "mock_vector_store",
                "embedding_model": "mock-embedding-model",
            },
        )

        t.llm(
            name="generate_answer",
            provider="openai",
            model="gpt-4o-mini",
            prompt=(
                "Answer the user question using the retrieved context.\n\n"
                "Question: What is the refund window?\n\n"
                "Context:\n"
                "1. Customers may request a refund within 30 days.\n"
                "2. Customers may request a refund within 14 days."
            ),
            response="Customers may request a refund within 14 days.",
            input_tokens=320,
            output_tokens=80,
            latency_ms=900,
            metadata={
                "temperature": 0.2,
            },
        )

    print(t.to_json())

    response = t.flush()
    print("\nSent trace to RAGLens collector:")
    print(response)


if __name__ == "__main__":
    main()
