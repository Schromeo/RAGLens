"""
Chunk normalization helpers for RAGLens.

RAG frameworks return retrieved chunks in many shapes:

- Standard dict:
    {"text": "...", "source": "...", "score": 0.9}

- LangChain-like:
    {"page_content": "...", "metadata": {"source": "..."}}

- Haystack-like:
    {"content": "...", "meta": {"source": "..."}}

- LlamaIndex-like:
    {"node": {"text": "...", "metadata": {"file_name": "..."}}, "score": 0.8}

- Tuple result:
    (document, score)

- Bare string:
    "chunk text..."

RAGLens only needs a normalized chunk payload:

{
    "id": "...",
    "text": "...",
    "source": "...",
    "score": 0.9,
    "rank": 1,
    "metadata": {...}
}

Minimum diagnostic contract:
- text is required
- source is recommended, falls back to "unknown"
- score is optional
- rank is optional but auto-filled by normalize_chunks
- metadata is optional
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping
from typing import Any, Callable, Dict, Iterable, List, Optional, Union


TextExtractor = Union[str, Callable[[Any], Optional[str]]]
ValueExtractor = Union[str, Callable[[Any], Any]]


class ChunkNormalizationError(ValueError):
    """Raised when a retrieved item cannot be normalized into a RAGLens chunk."""


def normalize_chunk(
    raw: Any,
    rank: Optional[int] = None,
    *,
    text: Optional[TextExtractor] = None,
    source: Optional[ValueExtractor] = None,
    score: Optional[ValueExtractor] = None,
    chunk_id: Optional[ValueExtractor] = None,
    metadata: Optional[ValueExtractor] = None,
    default_source: str = "unknown",
) -> Dict[str, Any]:
    """
    Normalize one raw retrieved item into the RAGLens chunk contract.

    Parameters:
        raw:
            A raw retrieved item. Can be a dict, object, tuple, string, etc.

        rank:
            Optional 1-based rank. If omitted, rank is left as None.

        text/source/score/chunk_id/metadata:
            Optional explicit extractors. Each can be:
            - a dotted path string, such as "metadata.source" or "node.text"
            - a callable, such as lambda d: d.page_content

        default_source:
            Used when no source-like field can be found.

    Returns:
        A dict with:
        - id
        - text
        - source
        - score
        - rank
        - metadata
    """
    item, tuple_score = _unwrap_tuple_result(raw)

    extracted_text = _extract_text(item, explicit=text)
    if not extracted_text:
        raise ChunkNormalizationError(
            "Could not normalize retrieved chunk because no text/content field was found. "
            "Provide text='...' or pass an object with text/page_content/content/node.text."
        )

    extracted_metadata = _extract_metadata(item, explicit=metadata)
    extracted_source = _extract_source(item, extracted_metadata, explicit=source)
    extracted_score = _extract_score(item, tuple_score=tuple_score, explicit=score)
    extracted_id = _extract_id(item, explicit=chunk_id)

    if not extracted_id:
        extracted_id = _stable_chunk_id(extracted_text, extracted_source or default_source)

    normalized_metadata = dict(extracted_metadata)
    normalized_metadata.setdefault("normalized_by", "raglens.normalize_chunk")

    return {
        "id": extracted_id,
        "text": extracted_text,
        "source": extracted_source or default_source,
        "score": extracted_score,
        "rank": rank,
        "metadata": normalized_metadata,
    }


def normalize_chunks(
    raw_chunks: Iterable[Any],
    *,
    text: Optional[TextExtractor] = None,
    source: Optional[ValueExtractor] = None,
    score: Optional[ValueExtractor] = None,
    chunk_id: Optional[ValueExtractor] = None,
    metadata: Optional[ValueExtractor] = None,
    default_source: str = "unknown",
    start_rank: int = 1,
    skip_invalid: bool = False,
) -> List[Dict[str, Any]]:
    """
    Normalize many raw retrieved items into RAGLens chunks.

    By default, invalid items raise ChunkNormalizationError.
    Set skip_invalid=True to drop invalid items.
    """
    normalized: List[Dict[str, Any]] = []

    for index, raw in enumerate(raw_chunks):
        rank = start_rank + index

        try:
            normalized.append(
                normalize_chunk(
                    raw,
                    rank=rank,
                    text=text,
                    source=source,
                    score=score,
                    chunk_id=chunk_id,
                    metadata=metadata,
                    default_source=default_source,
                )
            )
        except ChunkNormalizationError:
            if not skip_invalid:
                raise

    return normalized


def _unwrap_tuple_result(raw: Any) -> tuple[Any, Any]:
    """
    Common vector-store pattern:
        (document, score)

    Also supports:
        [document, score]
    """
    if isinstance(raw, tuple) and len(raw) == 2:
        return raw[0], raw[1]

    if isinstance(raw, list) and len(raw) == 2 and not _looks_like_chunk_list(raw):
        return raw[0], raw[1]

    return raw, None


def _looks_like_chunk_list(value: list[Any]) -> bool:
    if not value:
        return False

    return all(isinstance(item, (str, Mapping)) for item in value)


def _extract_text(item: Any, explicit: Optional[TextExtractor]) -> str:
    if isinstance(item, str):
        return item.strip()

    if explicit is not None:
        value = _extract_with_spec(item, explicit)
        return _to_clean_string(value)

    candidates = [
        "text",
        "page_content",
        "content",
        "body",
        "chunk",
        "node.text",
        "node.content",
        "node.page_content",
        "node.text_resource.text",
        "document.text",
        "document.page_content",
        "document.content",
    ]

    for path in candidates:
        value = _get_path(item, path)
        cleaned = _to_clean_string(value)

        if cleaned:
            return cleaned

    # Object fallback for LangChain-style Document.
    for attr in ("page_content", "text", "content"):
        value = getattr(item, attr, None)
        cleaned = _to_clean_string(value)

        if cleaned:
            return cleaned

    # LlamaIndex-style node sometimes exposes get_content().
    get_content = getattr(item, "get_content", None)
    if callable(get_content):
        cleaned = _to_clean_string(get_content())
        if cleaned:
            return cleaned

    node = getattr(item, "node", None)
    if node is not None:
        get_content = getattr(node, "get_content", None)
        if callable(get_content):
            cleaned = _to_clean_string(get_content())
            if cleaned:
                return cleaned

    return ""


def _extract_metadata(
    item: Any,
    explicit: Optional[ValueExtractor],
) -> Dict[str, Any]:
    if explicit is not None:
        value = _extract_with_spec(item, explicit)
        return _to_metadata_dict(value)

    candidates = [
        "metadata",
        "meta",
        "extra_info",
        "node.metadata",
        "node.meta",
        "document.metadata",
        "document.meta",
    ]

    merged: Dict[str, Any] = {}

    for path in candidates:
        value = _get_path(item, path)
        if isinstance(value, Mapping):
            merged.update(dict(value))

    # Object fallback.
    for attr in ("metadata", "meta", "extra_info"):
        value = getattr(item, attr, None)
        if isinstance(value, Mapping):
            merged.update(dict(value))

    node = getattr(item, "node", None)
    if node is not None:
        for attr in ("metadata", "meta", "extra_info"):
            value = getattr(node, attr, None)
            if isinstance(value, Mapping):
                merged.update(dict(value))

    return merged


def _extract_source(
    item: Any,
    metadata: Mapping[str, Any],
    explicit: Optional[ValueExtractor],
) -> str:
    if explicit is not None:
        return _to_clean_string(_extract_with_spec(item, explicit))

    direct_candidates = [
        "source",
        "file_name",
        "filename",
        "doc_id",
        "document_id",
        "uri",
        "url",
        "path",
        "title",
        "name",
        "node.source",
        "node.file_name",
        "node.id_",
        "document.source",
        "document.file_name",
        "document.id",
    ]

    metadata_candidates = [
        "source",
        "file_name",
        "filename",
        "doc_id",
        "document_id",
        "file_id",
        "uri",
        "url",
        "path",
        "title",
        "name",
    ]

    for path in direct_candidates:
        value = _to_clean_string(_get_path(item, path))
        if value:
            return value

    for key in metadata_candidates:
        value = _to_clean_string(metadata.get(key))
        if value:
            return value

    return ""


def _extract_score(
    item: Any,
    *,
    tuple_score: Any,
    explicit: Optional[ValueExtractor],
) -> Optional[float]:
    if explicit is not None:
        return _to_float_or_none(_extract_with_spec(item, explicit))

    tuple_score_float = _to_float_or_none(tuple_score)
    if tuple_score_float is not None:
        return tuple_score_float

    candidates = [
        "score",
        "similarity",
        "similarity_score",
        "rerank_score",
        "relevance_score",
        "distance",
        "metadata.score",
        "metadata.similarity",
        "metadata.similarity_score",
        "metadata.rerank_score",
        "meta.score",
        "meta.similarity",
        "node.score",
    ]

    for path in candidates:
        value = _to_float_or_none(_get_path(item, path))
        if value is not None:
            return value

    for attr in (
        "score",
        "similarity",
        "similarity_score",
        "rerank_score",
        "relevance_score",
        "distance",
    ):
        value = _to_float_or_none(getattr(item, attr, None))
        if value is not None:
            return value

    return None


def _extract_id(
    item: Any,
    explicit: Optional[ValueExtractor],
) -> str:
    if explicit is not None:
        return _to_clean_string(_extract_with_spec(item, explicit))

    candidates = [
        "id",
        "chunk_id",
        "doc_id",
        "document_id",
        "node_id",
        "id_",
        "node.id",
        "node.id_",
        "node.node_id",
        "document.id",
        "metadata.id",
        "metadata.chunk_id",
        "metadata.doc_id",
        "metadata.document_id",
        "meta.id",
        "meta.chunk_id",
    ]

    for path in candidates:
        value = _to_clean_string(_get_path(item, path))
        if value:
            return value

    for attr in ("id", "id_", "chunk_id", "doc_id", "document_id", "node_id"):
        value = _to_clean_string(getattr(item, attr, None))
        if value:
            return value

    return ""


def _extract_with_spec(item: Any, spec: Union[str, Callable[[Any], Any]]) -> Any:
    if callable(spec):
        return spec(item)

    return _get_path(item, spec)


def _get_path(item: Any, path: str) -> Any:
    current = item

    for part in path.split("."):
        if current is None:
            return None

        if isinstance(current, Mapping):
            current = current.get(part)
            continue

        current = getattr(current, part, None)

    return current


def _to_clean_string(value: Any) -> str:
    if value is None:
        return ""

    if isinstance(value, str):
        return value.strip()

    if isinstance(value, (int, float)):
        return str(value)

    return ""


def _to_float_or_none(value: Any) -> Optional[float]:
    if value is None:
        return None

    if isinstance(value, bool):
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, str) and value.strip():
        try:
            return float(value.strip())
        except ValueError:
            return None

    return None


def _to_metadata_dict(value: Any) -> Dict[str, Any]:
    if value is None:
        return {}

    if isinstance(value, Mapping):
        return dict(value)

    return {"raw_metadata": value}


def _stable_chunk_id(text: str, source: str) -> str:
    digest = hashlib.sha1(f"{source}\n{text}".encode("utf-8")).hexdigest()[:12]
    return f"chunk_{digest}"