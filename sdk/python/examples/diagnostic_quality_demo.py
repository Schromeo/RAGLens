from __future__ import annotations

import argparse

from sledtrace import trace


def build_prompt(query: str, chunks: list[dict]) -> str:
    context_lines = []

    for chunk in chunks:
        context_lines.append(f"[{chunk['rank']}] {chunk['text']}")

    return (
        "Answer the user question using the retrieved context.\n\n"
        f"Question: {query}\n\n"
        "Retrieved context:\n"
        + "\n".join(context_lines)
    )


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
                "source": "refund_policy.md",
                "document_id": "refund_policy",
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
                "source": "returns_process.md",
                "document_id": "returns_process",
            },
        },
    ]


def numeric_mismatch_answerer(query: str, chunks: list[dict]) -> tuple[str, str]:
    """Demo answerer that intentionally uses the wrong numeric value."""
    prompt = build_prompt(query, chunks)

    # Intentional wrong answer for v0.3 diagnostic demo:
    # retrieved context says 30 days, answer says 60 days.
    answer = "Customers may request a refund within 60 days of purchase."

    return prompt, answer


def weak_overlap_retriever(query: str) -> list[dict]:
    """Demo retriever that returns high-scoring but query-mismatched chunks."""
    return [
        {
            "id": "chunk_shipping_standard",
            "text": "Standard shipping usually takes 5 to 7 business days after an order has shipped.",
            "score": 0.88,
            "rank": 1,
            "source": "shipping_policy.md",
            "document_id": "shipping_policy",
            "metadata": {
                "section": "shipping_window",
                "source": "shipping_policy.md",
                "document_id": "shipping_policy",
            },
        },
        {
            "id": "chunk_warranty_general",
            "text": "Warranty coverage applies to manufacturing defects for eligible physical products.",
            "score": 0.81,
            "rank": 2,
            "source": "warranty_policy.md",
            "document_id": "warranty_policy",
            "metadata": {
                "section": "warranty_coverage",
                "source": "warranty_policy.md",
                "document_id": "warranty_policy",
            },
        },
    ]


def weak_overlap_answerer(query: str, chunks: list[dict]) -> tuple[str, str]:
    """Demo answerer that avoids a hallucinated answer so the retrieval issue is clear."""
    prompt = build_prompt(query, chunks)
    answer = "I could not find enough information in the retrieved context to answer the refund window question."

    return prompt, answer


def unsupported_claim_retriever(query: str) -> list[dict]:
    """Demo retriever that returns relevant evidence but not enough to support every answer claim."""
    return [
        {
            "id": "chunk_refund_current",
            "text": "Customers may request a refund within 30 days of purchase.",
            "score": 0.94,
            "rank": 1,
            "source": "refund_policy.md",
            "document_id": "refund_policy",
            "metadata": {
                "section": "refund_window",
                "policy_version": "current",
                "source": "refund_policy.md",
                "document_id": "refund_policy",
            },
        },
        {
            "id": "chunk_returns_general",
            "text": "Refund requests must be submitted through the customer support portal.",
            "score": 0.79,
            "rank": 2,
            "source": "returns_process.md",
            "document_id": "returns_process",
            "metadata": {
                "section": "submission_process",
                "source": "returns_process.md",
                "document_id": "returns_process",
            },
        },
    ]


def unsupported_claim_answerer(query: str, chunks: list[dict]) -> tuple[str, str]:
    """Demo answerer that adds one unsupported claim after a supported answer."""
    prompt = build_prompt(query, chunks)

    # First sentence is supported. Second sentence is intentionally unsupported by the retrieved context.
    answer = (
        "Customers may request a refund within 30 days of purchase. "
        "Original shipping fees are refundable."
    )

    return prompt, answer



def conflicting_chunks_retriever(query: str) -> list[dict]:
    """Demo retriever that returns current and legacy policy chunks with conflicting values."""
    return [
        {
            "id": "chunk_refund_current",
            "text": "Customers may request a refund within 30 days of purchase.",
            "score": 0.92,
            "rank": 1,
            "source": "refund_policy.md",
            "document_id": "refund_policy",
            "metadata": {
                "section": "refund_window",
                "policy_version": "current",
                "source": "refund_policy.md",
                "document_id": "refund_policy",
            },
        },
        {
            "id": "chunk_refund_legacy",
            "text": "Customers may request a refund within 60 days of purchase under the legacy refund policy.",
            "score": 0.89,
            "rank": 2,
            "source": "legacy_refund_policy.md",
            "document_id": "legacy_refund_policy",
            "metadata": {
                "section": "refund_window",
                "policy_version": "legacy",
                "source": "legacy_refund_policy.md",
                "document_id": "legacy_refund_policy",
            },
        },
    ]


def conflicting_chunks_answerer(query: str, chunks: list[dict]) -> tuple[str, str]:
    """Demo answerer that abstains from resolving the conflict so the chunk conflict is clear."""
    prompt = build_prompt(query, chunks)
    answer = "I could not determine a single refund window from the retrieved context."
    
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


def run_weak_overlap_case() -> str:
    query = "What is the refund window?"

    with trace(
        name="v0.3-diagnostic-weak-overlap",
        query=query,
        metadata={
            "app": "diagnostic-quality-demo",
            "environment": "local",
            "demo": "v0.3_diagnostic_intelligence",
            "case": "weak_query_chunk_overlap",
            "expected_warning": "weak_query_chunk_overlap",
        },
    ) as t:
        chunks = weak_overlap_retriever(query)

        t.retrieval(
            query=query,
            chunks=chunks,
            name="diagnostic_retrieval",
            top_k=len(chunks),
            metadata={
                "retriever": "deterministic_weak_overlap_fixture",
            },
        )

        prompt, answer = weak_overlap_answerer(query, chunks)

        t.llm(
            model="local-template-answerer-v1",
            prompt=prompt,
            response=answer,
            name="diagnostic_answer_generation",
            provider="local-demo",
        )

    t.flush()
    return answer


def run_unsupported_claim_case() -> str:
    query = "What is the refund window?"

    with trace(
        name="v0.3-diagnostic-unsupported-claim",
        query=query,
        metadata={
            "app": "diagnostic-quality-demo",
            "environment": "local",
            "demo": "v0.3_diagnostic_intelligence",
            "case": "unsupported_claim",
            "expected_warning": "answer_not_grounded",
        },
    ) as t:
        chunks = unsupported_claim_retriever(query)

        t.retrieval(
            query=query,
            chunks=chunks,
            name="diagnostic_retrieval",
            top_k=len(chunks),
            metadata={
                "retriever": "deterministic_unsupported_claim_fixture",
            },
        )

        prompt, answer = unsupported_claim_answerer(query, chunks)

        t.llm(
            model="local-template-answerer-v1",
            prompt=prompt,
            response=answer,
            name="diagnostic_answer_generation",
            provider="local-demo",
        )

    t.flush()
    return answer



def run_conflicting_chunks_case() -> str:
    query = "What is the refund window?"

    with trace(
        name="v0.3-diagnostic-conflicting-chunks",
        query=query,
        metadata={
            "app": "diagnostic-quality-demo",
            "environment": "local",
            "demo": "v0.3_diagnostic_intelligence",
            "case": "conflicting_chunks",
            "expected_warning": "conflicting_chunks",
        },
    ) as t:
        chunks = conflicting_chunks_retriever(query)

        t.retrieval(
            query=query,
            chunks=chunks,
            name="diagnostic_retrieval",
            top_k=len(chunks),
            metadata={
                "retriever": "deterministic_conflicting_chunks_fixture",
            },
        )

        prompt, answer = conflicting_chunks_answerer(query, chunks)

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
        description="Run SledTrace v0.3 diagnostic intelligence demo cases."
    )
    parser.add_argument(
        "case",
        nargs="?",
        default="numeric-mismatch",
        choices=["numeric-mismatch", "weak-overlap", "unsupported-claim", "conflicting-chunks", "all"],
        help="Diagnostic demo case to run.",
    )

    args = parser.parse_args()

    if args.case in {"numeric-mismatch", "all"}:
        answer = run_numeric_mismatch_case()
        print("Ran diagnostic case: numeric_mismatch")
        print("Query: What is the refund window?")
        print(f"Answer: {answer}")
        print("Expected warning: numeric_mismatch")
        print("Trace flushed to the local SledTrace collector.")
        print()

    if args.case in {"weak-overlap", "all"}:
        answer = run_weak_overlap_case()
        print("Ran diagnostic case: weak_query_chunk_overlap")
        print("Query: What is the refund window?")
        print(f"Answer: {answer}")
        print("Expected warning: weak_query_chunk_overlap")
        print("Trace flushed to the local SledTrace collector.")
        print()

    if args.case in {"unsupported-claim", "all"}:
        answer = run_unsupported_claim_case()
        print("Ran diagnostic case: unsupported_claim")
        print("Query: What is the refund window?")
        print(f"Answer: {answer}")
        print("Expected warning: answer_not_grounded")
        print("Trace flushed to the local SledTrace collector.")
        print()

    if args.case in {"conflicting-chunks", "all"}:
        answer = run_conflicting_chunks_case()
        print("Ran diagnostic case: conflicting_chunks")
        print("Query: What is the refund window?")
        print(f"Answer: {answer}")
        print("Expected warning: conflicting_chunks")
        print("Trace flushed to the local SledTrace collector.")


if __name__ == "__main__":
    main()



