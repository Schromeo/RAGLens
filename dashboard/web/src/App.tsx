import { useState } from "react";
import TraceDetailPage from "./pages/TraceDetailPage";
import TraceListPage from "./pages/TraceListPage";

export default function App() {
  const [selectedTraceId, setSelectedTraceId] = useState<string | null>(null);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <div className="eyebrow">Local-first RAG debugger</div>
          <h1>RAGLens</h1>
        </div>

        <div className="topbar-right">
          <span className="status-pill">Collector: localhost:4319</span>
        </div>
      </header>

      <main className="layout">
        <section className="sidebar">
          <TraceListPage
            selectedTraceId={selectedTraceId}
            onSelectTrace={setSelectedTraceId}
          />
        </section>

        <section className="detail">
          {selectedTraceId ? (
            <TraceDetailPage traceId={selectedTraceId} />
          ) : (
            <div className="empty-state">
              <h2>Select a trace</h2>
              <p>
                Choose a trace from the left panel to inspect retrieval chunks,
                LLM calls, metadata, and warnings.
              </p>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
