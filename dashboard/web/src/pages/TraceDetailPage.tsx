import { useEffect, useMemo, useState } from "react";
import { fetchTraceDetail } from "../api/client";
import ChunkCard from "../components/ChunkCard";
import JsonViewer from "../components/JsonViewer";
import SpanTimeline from "../components/SpanTimeline";
import type { Chunk, Span, TraceDetailResponse } from "../types";

type Props = {
  traceId: string;
};

export default function TraceDetailPage({ traceId }: Props) {
  const [detail, setDetail] = useState<TraceDetailResponse | null>(null);
  const [selectedSpanId, setSelectedSpanId] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  async function loadDetail() {
    try {
      setLoading(true);
      setError(null);

      const data = await fetchTraceDetail(traceId);

      const normalizedData = {
        ...data,
        spans: data.spans ?? [],
        warnings: data.warnings ?? [],
      };

      setDetail(normalizedData);

      if (normalizedData.spans.length > 0) {
        setSelectedSpanId(normalizedData.spans[0].span_id);
      } else {
        setSelectedSpanId(null);
      }
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Failed to load trace detail",
      );
    } finally {
      setLoading(false);
    }
  }
  useEffect(() => {
    void loadDetail();
  }, [traceId]);

  const selectedSpan = useMemo(() => {
    if (!detail || !selectedSpanId) {
      return null;
    }

    return detail.spans.find((span) => span.span_id === selectedSpanId) ?? null;
  }, [detail, selectedSpanId]);

  if (loading) {
    return <div className="muted">Loading trace detail...</div>;
  }

  if (error) {
    return (
      <div className="error-box">
        <strong>Failed to load trace detail</strong>
        <p>{error}</p>
      </div>
    );
  }

  if (!detail) {
    return <div className="muted">Trace not found.</div>;
  }

  const query = getString(detail.trace.input, "query");
  const answer = getString(detail.trace.output, "answer");

  return (
    <div className="trace-detail-page">
      <div className="trace-hero">
        <div>
          <div className="eyebrow">Trace detail</div>
          <h2>{detail.trace.name}</h2>
          <p className="mono small">{detail.trace.trace_id}</p>
        </div>

        <div className={`big-status ${detail.trace.status}`}>
          {detail.trace.status}
        </div>
      </div>

      <div className="summary-grid">
        <div className="summary-card">
          <div className="summary-label">Query</div>
          <div className="summary-value">{query || "No query recorded"}</div>
        </div>

        <div className="summary-card">
          <div className="summary-label">Final answer</div>
          <div className="summary-value">{answer || "No answer recorded"}</div>
        </div>

        <div className="summary-card">
          <div className="summary-label">Duration</div>
          <div className="summary-value">
            {detail.trace.duration_ms ?? "unknown"}ms
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-label">Warnings</div>
          <div className="summary-value">{detail.warnings.length}</div>
        </div>
      </div>

      <div className="detail-grid">
        <div className="timeline-panel">
          <h3>Pipeline timeline</h3>
          <SpanTimeline
            spans={detail.spans}
            selectedSpanId={selectedSpanId}
            onSelectSpan={setSelectedSpanId}
          />

          <h3>Warnings</h3>
          {detail.warnings.length === 0 ? (
            <div className="empty-card compact">
              No warnings generated yet. Warning engine coming soon.
            </div>
          ) : (
            detail.warnings.map((warning) => (
              <div key={warning.warning_id} className="warning-card">
                <strong>{warning.severity}</strong>
                <p>{warning.message}</p>
              </div>
            ))
          )}
        </div>

        <div className="span-detail-panel">
          {selectedSpan ? (
            <SelectedSpanView span={selectedSpan} />
          ) : (
            <div className="empty-card">Select a span to inspect details.</div>
          )}
        </div>
      </div>
    </div>
  );
}

function SelectedSpanView({ span }: { span: Span }) {
  const chunks = getChunks(span);

  return (
    <div>
      <div className="span-detail-header">
        <div>
          <div className="eyebrow">{span.type} span</div>
          <h3>{span.name}</h3>
        </div>

        <div className={`big-status ${span.status}`}>{span.status}</div>
      </div>

      {span.type === "retrieval" && (
        <section className="section">
          <h4>Retrieved chunks</h4>

          {chunks.length === 0 ? (
            <div className="empty-card compact">No chunks recorded.</div>
          ) : (
            <div className="chunk-list">
              {chunks.map((chunk, index) => (
                <ChunkCard
                  key={chunk.id ?? `${span.span_id}-chunk-${index}`}
                  chunk={chunk}
                />
              ))}
            </div>
          )}
        </section>
      )}

      {span.type === "llm" && (
        <section className="section">
          <h4>LLM call</h4>

          <div className="llm-box">
            <div className="summary-label">Model</div>
            <div>{getString(span.input, "model") || "Unknown model"}</div>
          </div>

          <div className="llm-box">
            <div className="summary-label">Prompt</div>
            <pre>{getString(span.input, "prompt") || "No prompt recorded"}</pre>
          </div>

          <div className="llm-box">
            <div className="summary-label">Response</div>
            <pre>
              {getString(span.output, "response") || "No response recorded"}
            </pre>
          </div>
        </section>
      )}

      <section className="section">
        <h4>Input</h4>
        <JsonViewer value={span.input} />
      </section>

      <section className="section">
        <h4>Output</h4>
        <JsonViewer value={span.output} />
      </section>

      <section className="section">
        <h4>Metadata</h4>
        <JsonViewer value={span.metadata} />
      </section>
    </div>
  );
}

function getString(value: Record<string, unknown>, key: string): string {
  const raw = value[key];

  return typeof raw === "string" ? raw : "";
}

function getChunks(span: Span): Chunk[] {
  const raw = span.output["chunks"];

  if (!Array.isArray(raw)) {
    return [];
  }

  return raw as Chunk[];
}