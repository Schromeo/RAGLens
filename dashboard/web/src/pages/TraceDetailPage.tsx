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
  const warningCount = detail.warnings.length;
  const warningCountClass =
    warningCount > 0 ? "summary-value-danger" : "summary-value-ok";

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
          <div className="summary-value summary-value-query">
            {query || "No query recorded"}
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-label">Final answer</div>
          <div className="summary-value summary-value-answer">
            {answer || "No answer recorded"}
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-label">Duration</div>
          <div className="summary-value summary-value-duration">
            {detail.trace.duration_ms ?? "unknown"}ms
          </div>
        </div>

        <div className="summary-card">
          <div className="summary-label">Warnings</div>
          <div className={`summary-value ${warningCountClass}`}>
            {warningCount}
          </div>
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
              No warnings generated for this trace.
            </div>
          ) : (
            <div className="warning-list">
              {detail.warnings.map((warning) => (
                <div key={warning.warning_id} className="warning-card">
                  <div className="warning-card-header">
                    <strong>{formatWarningType(warning.type)}</strong>
                    <span className="warning-severity">{warning.severity}</span>
                  </div>

                  <p>{warning.message}</p>

                  <div className="warning-help">
                    {getWarningHelpText(warning.type)}
                  </div>
                </div>
              ))}
            </div>
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

function formatWarningType(type: string): string {
  return type.split("_").join(" ");
}

function getWarningHelpText(type: string): string {
  switch (type) {
    case "no_retrieved_chunks":
      return "The retriever did not return usable evidence for the query.";

    case "low_retrieval_score":
      return "The retrieved chunks may be weakly related to the query.";

    case "duplicate_chunks":
      return "The context contains repeated evidence, which can waste context window space or over-weight one source.";

    case "conflicting_chunks":
      return "The retrieved chunks appear to contain conflicting information.";

    case "answer_not_grounded":
      return "The answer appears to include a claim that is not supported by the retrieved context.";

    default:
      return "RAGLens detected a potential issue in this trace.";
  }
}