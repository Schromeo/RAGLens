import type { TraceListItem } from "../types";

type Props = {
  trace: TraceListItem;
  selected: boolean;
  onClick: () => void;
};

export default function TraceCard({ trace, selected, onClick }: Props) {
  const demoCase = getDemoCase(trace.name);

  return (
    <button
      className={selected ? "trace-card selected" : "trace-card"}
      onClick={onClick}
    >
      <div className="trace-card-top">
        <span className={`status-dot ${trace.status}`} />

        <div className="trace-card-title">
          <strong>{trace.name}</strong>

          {demoCase && (
            <span className="trace-case-badge">demo: {demoCase}</span>
          )}
        </div>
      </div>

      <div className="trace-query">{trace.query || "No query recorded"}</div>

      {trace.answer && <div className="trace-answer">{trace.answer}</div>}

      <div className="trace-meta">
        <span>{formatDuration(trace.duration_ms)}</span>
        <span>{formatWarningCount(trace.warning_count)}</span>
        <span>{formatDate(trace.started_at)}</span>
      </div>
    </button>
  );
}

function getDemoCase(traceName: string): string | null {
  const prefix = "real-local-rag-";

  if (!traceName.startsWith(prefix)) {
    return null;
  }

  return traceName.slice(prefix.length);
}

function formatWarningCount(count: number): string {
  if (count === 1) {
    return "1 warning";
  }

  return `${count} warnings`;
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