from dataclasses import dataclass

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from examples.local_rag_demo.local_rag.chunker import Chunk


@dataclass(frozen=True)
class RetrievedChunk:
    chunk_id: str
    doc_id: str
    source: str
    text: str
    score: float
    rank: int


class TfidfRetriever:
    """
    A tiny local retriever for the Real Local RAG Demo.

    This intentionally uses TF-IDF + cosine similarity instead of embeddings
    so the demo stays local, transparent, and dependency-light.
    """

    def __init__(self, chunks: list[Chunk]) -> None:
        if not chunks:
            raise ValueError("TfidfRetriever requires at least one chunk")

        self.chunks = chunks
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
        )

        self.chunk_texts = [chunk.text for chunk in chunks]
        self.chunk_matrix = self.vectorizer.fit_transform(self.chunk_texts)

    def retrieve(
        self,
        query: str,
        top_k: int = 3,
        min_score: float = 0.0,
    ) -> list[RetrievedChunk]:
        if not query.strip():
            raise ValueError("query must not be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than 0")

        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.chunk_matrix)[0]

        ranked_indices = similarities.argsort()[::-1]

        results: list[RetrievedChunk] = []

        for index in ranked_indices:
            score = float(similarities[index])

            if score < min_score:
                continue

            chunk = self.chunks[index]

            results.append(
                RetrievedChunk(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    source=chunk.source,
                    text=chunk.text,
                    score=score,
                    rank=len(results) + 1,
                )
            )

            if len(results) >= top_k:
                break

        return results