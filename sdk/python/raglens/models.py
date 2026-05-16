from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
import time
import uuid


JsonDict = Dict[str, Any]


def utc_now_iso() -> str:
    """Return current UTC time in ISO-8601 format."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def now_ms() -> float:
    """Return monotonic time in milliseconds."""
    return time.perf_counter() * 1000


def new_id(prefix: str) -> str:
    """Generate a simple prefixed UUID ID."""
    return f"{prefix}_{uuid.uuid4().hex}"


@dataclass
class Span:
    span_id: str
    trace_id: str
    parent_span_id: Optional[str]
    type: str
    name: str
    status: str
    input: JsonDict = field(default_factory=dict)
    output: JsonDict = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)
    started_at: str = field(default_factory=utc_now_iso)
    ended_at: Optional[str] = None
    duration_ms: Optional[int] = None
    error: Optional[JsonDict] = None

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class TraceRecord:
    trace_id: str
    name: str
    status: str
    input: JsonDict = field(default_factory=dict)
    output: JsonDict = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)
    started_at: str = field(default_factory=utc_now_iso)
    ended_at: Optional[str] = None
    duration_ms: Optional[int] = None

    def to_dict(self) -> JsonDict:
        return asdict(self)


@dataclass
class TracePayload:
    trace: TraceRecord
    spans: List[Span] = field(default_factory=list)

    def to_dict(self) -> JsonDict:
        return {
            "trace": self.trace.to_dict(),
            "spans": [span.to_dict() for span in self.spans],
        }