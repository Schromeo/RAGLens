import type { TraceListItem } from "../types";

type Props = {
  trace: TraceListItem;
  selected: boolean;
  onClick: () => void;
};

export default function TraceCard({ trace, selected, onClick }: Props) {
  return (
    <button
      className={selected ? "trace-card selected" : "trace-card"}
      onClick={onClick}
    >
      <div className="trace-card-top">
        <span className={`status-dot ${trace.status}`} />
        <strong>{trace.name}</strong>
      </div>

      <div className="trace-query">{trace.query || "No query recorded"}</div>

      {trace.answer && <div className="trace-answer">{trace.answer}</div>}

      <div className="trace-meta">
        <span>{formatDuration(trace.duration_ms)}</span>
        <span>{trace.warning_count} warnings</span>
        <span>{formatDate(trace.started_at)}</span>
      </div>
    </button>
  );
}

function formatDuration(durationMs: number | null): string {
  if (durationMs === null || durationMs === undefined) {
    return "unknown duration";
  }

  if (durationMs < 1000) {
    return `${durationMs}ms`;
  }

  return `${(durationMs / 1000).toFixed(2)}s`;
}

function formatDate(value: string): string {
  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleTimeString();
}