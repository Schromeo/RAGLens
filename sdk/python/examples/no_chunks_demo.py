import json

from raglens import trace


def main():
    query = "What is the warranty policy?"

    with trace(
        name="empty-retrieval-qa",
        query=query,
        metadata={
            "sdk_language": "python",
            "sdk_version": "0.1.0",
            "app": "no-chunks-demo",
            "environment": "local",
        },
    ) as t:
        retrieved_chunks = []

        t.retrieval(
            name="search_empty_docs",
            query=query,
            chunks=retrieved_chunks,
            top_k=3,
            metadata={
                "retriever": "mock_vector_store",
                "embedding_model": "mock-embedding-model",
            },
        )

        answer = "I could not find enough information to answer this question."

        t.llm(
            name="generate_answer",
            model="gpt-4o-mini",
            prompt=(
                "Answer the user question using the retrieved context.\n\n"
                f"Question: {query}\n\n"
                "Context:\n"
            ),
            response=answer,
            metadata={
                "temperature": 0.2,
                "provider": "openai",
                "input_tokens": 120,
                "output_tokens": 20,
                "total_tokens": 140,
                "latency_ms": 500,
            },
        )

        print(t.to_json())

        response = t.flush()
        print("\nSent trace to RAGLens collector:")
        print(response)


if __name__ == "__main__":
    main()