from __future__ import annotations

import argparse

from raglens import trace


def numeric_mismatch_retriever(query: str) -> list[dict]:
    """Demo retriever that returns correct refund-window evidence."""
    return [
        {
            "id": "chunk_refund_current",
            "text": "Customers may request a refund within 30 days of purchase.",
            "score": 0.93,
            "rank": 1,
            "source": "refund_policy.md",
            "document_id": "refund_policy",
            "metadata": {
                "section": "refund_window",
                "policy_version": "current",
            },
        },
        {
            "id": "chunk_returns_general",
            "text": "Refund requests must be submitted through the customer support portal.",
            "score": 0.78,
            "rank": 2,
            "source": "returns_process.md",
            "document_id": "returns_process",
            "metadata": {
                "section": "submission_process",
            },
        },
    ]


def numeric_mismatch_answerer(query: str, chunks: list[dict]) -> tuple[str, str]:
    """Demo answerer that intentionally uses the wrong numeric value."""
    context_lines = []

    for chunk in chunks:
        context_lines.append(f"[{chunk['rank']}] {chunk['text']}")

    prompt = (
        "Answer the user question using the retrieved context.\n\n"
        f"Question: {query}\n\n"
        "Retrieved context:\n"
        + "\n".join(context_lines)
    )

    # Intentional wrong answer for v0.3 diagnostic demo:
    # retrieved context says 30 days, answer says 60 days.
    answer = "Customers may request a refund within 60 days of purchase."

    return prompt, answer


def run_numeric_mismatch_case() -> str:
    query = "What is the refund window?"

    with trace(
        name="v0.3-diagnostic-numeric-mismatch",
        query=query,
        metadata={
            "app": "diagnostic-quality-demo",
            "environment": "local",
            "demo": "v0.3_diagnostic_intelligence",
            "case": "numeric_mismatch",
            "expected_warning": "numeric_mismatch",
        },
    ) as t:
        chunks = numeric_mismatch_retriever(query)

        t.retrieval(
            query=query,
            chunks=chunks,
            name="diagnostic_retrieval",
            top_k=len(chunks),
            metadata={
                "retriever": "deterministic_numeric_mismatch_fixture",
            },
        )

        prompt, answer = numeric_mismatch_answerer(query, chunks)

        t.llm(
            model="local-template-answerer-v1",
            prompt=prompt,
            response=answer,
            name="diagnostic_answer_generation",
            provider="local-demo",
        )

    t.flush()
    return answer


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run RAGLens v0.3 diagnostic intelligence demo cases."
    )
    parser.add_argument(
        "case",
        nargs="?",
        default="numeric-mismatch",
        choices=["numeric-mismatch"],
        help="Diagnostic demo case to run.",
    )

    args = parser.parse_args()

    if args.case == "numeric-mismatch":
        answer = run_numeric_mismatch_case()
        print("Ran diagnostic case: numeric_mismatch")
        print("Query: What is the refund window?")
        print(f"Answer: {answer}")
        print("Expected warning: numeric_mismatch")
        print("Trace flushed to the local RAGLens collector.")


if __name__ == "__main__":
    main()