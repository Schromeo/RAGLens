from __future__ import annotations

from typing import Any, Dict, List, Optional
import json
import traceback

from .models import (
    JsonDict,
    Span,
    TraceRecord,
    TracePayload,
    new_id,
    now_ms,
    utc_now_iso,
)


class RAGLensTrace:
    """
    A lightweight trace context manager for recording one RAG request.

    Public API example:

        from raglens import trace

        with trace("refund-policy-qa") as t:
            t.retrieval(query="...", chunks=[...])
            t.llm(model="...", prompt="...", response="...")
    """

    def __init__(
        self,
        name: str,
        query: Optional[str] = None,
        metadata: Optional[JsonDict] = None,
    ) -> None:
        self.trace_id = new_id("trace")
        self.name = name
        self.query = query
        self.metadata = metadata or {}

        self._started_at: Optional[str] = None
        self._ended_at: Optional[str] = None
        self._start_ms: Optional[float] = None
        self._duration_ms: Optional[int] = None

        self._status = "ok"
        self._output: JsonDict = {}
        self._spans: List[Span] = []
        self._error: Optional[JsonDict] = None

    def __enter__(self) -> "RAGLensTrace":
        self._started_at = utc_now_iso()
        self._start_ms = now_ms()
        return self

    def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
        self._ended_at = utc_now_iso()

        if self._start_ms is not None:
            self._duration_ms = int(now_ms() - self._start_ms)

        if exc is not None:
            self._status = "error"
            self._error = {
                "type": exc_type.__name__ if exc_type else "Error",
                "message": str(exc),
                "stack": "".join(traceback.format_exception(exc_type, exc, tb)),
            }

        # Do not suppress exceptions.
        return False

    def retrieval(
        self,
        query: str,
        chunks: List[JsonDict],
        name: str = "retrieval",
        top_k: Optional[int] = None,
        metadata: Optional[JsonDict] = None,
    ) -> None:
        """
        Record a retrieval span.

        Args:
            query: Query sent to retriever.
            chunks: Retrieved chunks.
            name: Human-readable span name.
            top_k: Number of requested chunks.
            metadata: Retriever metadata.
        """
        start = now_ms()
        started_at = utc_now_iso()

        normalized_chunks = self._normalize_chunks(chunks)

        span_input: JsonDict = {
            "query": query,
        }

        if top_k is not None:
            span_input["top_k"] = top_k

        span = Span(
            span_id=new_id("span"),
            trace_id=self.trace_id,
            parent_span_id=None,
            type="retrieval",
            name=name,
            status="ok",
            input=span_input,
            output={
                "chunks": normalized_chunks,
            },
            metadata=metadata or {},
            started_at=started_at,
            ended_at=utc_now_iso(),
            duration_ms=int(now_ms() - start),
            error=None,
        )

        self._spans.append(span)

        if self.query is None:
            self.query = query

    def llm(
        self,
        model: str,
        prompt: Optional[str] = None,
        response: Optional[str] = None,
        messages: Optional[List[JsonDict]] = None,
        name: str = "llm",
        provider: Optional[str] = None,
        input_tokens: Optional[int] = None,
        output_tokens: Optional[int] = None,
        latency_ms: Optional[int] = None,
        metadata: Optional[JsonDict] = None,
    ) -> None:
        """
        Record an LLM span.

        Args:
            model: Model name.
            prompt: Prompt text.
            response: Model response text.
            messages: Optional chat messages.
            name: Human-readable span name.
            provider: LLM provider.
            input_tokens: Input token count.
            output_tokens: Output token count.
            latency_ms: LLM call latency.
            metadata: Additional metadata.
        """
        start = now_ms()
        started_at = utc_now_iso()

        span_input: JsonDict = {
            "model": model,
        }

        if prompt is not None:
            span_input["prompt"] = prompt

        if messages is not None:
            span_input["messages"] = messages

        span_output: JsonDict = {}

        if response is not None:
            span_output["response"] = response
            self._output["answer"] = response

        span_metadata: JsonDict = metadata.copy() if metadata else {}

        if provider is not None:
            span_metadata["provider"] = provider

        if input_tokens is not None:
            span_metadata["input_tokens"] = input_tokens

        if output_tokens is not None:
            span_metadata["output_tokens"] = output_tokens

        if input_tokens is not None and output_tokens is not None:
            span_metadata["total_tokens"] = input_tokens + output_tokens

        if latency_ms is not None:
            span_metadata["latency_ms"] = latency_ms

        span = Span(
            span_id=new_id("span"),
            trace_id=self.trace_id,
            parent_span_id=None,
            type="llm",
            name=name,
            status="ok",
            input=span_input,
            output=span_output,
            metadata=span_metadata,
            started_at=started_at,
            ended_at=utc_now_iso(),
            duration_ms=latency_ms if latency_ms is not None else int(now_ms() - start),
            error=None,
        )

        self._spans.append(span)

    def log_answer(self, answer: str) -> None:
        """Record the final answer at trace level."""
        self._output["answer"] = answer

    def to_payload(self) -> TracePayload:
        trace_input: JsonDict = {}

        if self.query is not None:
            trace_input["query"] = self.query

        trace_metadata = {
            "sdk_language": "python",
            "sdk_version": "0.1.0",
            **self.metadata,
        }

        if self._error is not None:
            trace_metadata["error"] = self._error

        record = TraceRecord(
            trace_id=self.trace_id,
            name=self.name,
            status=self._status,
            input=trace_input,
            output=self._output,
            metadata=trace_metadata,
            started_at=self._started_at or utc_now_iso(),
            ended_at=self._ended_at,
            duration_ms=self._duration_ms,
        )

        return TracePayload(trace=record, spans=self._spans)

    def to_dict(self) -> JsonDict:
        return self.to_payload().to_dict()

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def print_json(self) -> None:
        print(self.to_json())

    def _normalize_chunks(self, chunks: List[JsonDict]) -> List[JsonDict]:
        normalized: List[JsonDict] = []

        for index, chunk in enumerate(chunks):
            normalized_chunk = dict(chunk)

            if "rank" not in normalized_chunk:
                normalized_chunk["rank"] = index + 1

            if "metadata" not in normalized_chunk or normalized_chunk["metadata"] is None:
                normalized_chunk["metadata"] = {}

            normalized.append(normalized_chunk)

        return normalized


def trace(
    name: str,
    query: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> RAGLensTrace:
    """
    Create a RAGLens trace context manager.
    """
    return RAGLensTrace(name=name, query=query, metadata=metadata)