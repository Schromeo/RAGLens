package models

type JSONMap map[string]any

type TracePayload struct {
	Trace TraceRecord `json:"trace"`
	Spans []Span      `json:"spans"`
}

type TraceRecord struct {
	TraceID    string  `json:"trace_id"`
	Name       string  `json:"name"`
	Status     string  `json:"status"`
	Input      JSONMap `json:"input"`
	Output     JSONMap `json:"output"`
	Metadata   JSONMap `json:"metadata"`
	StartedAt  string  `json:"started_at"`
	EndedAt    *string `json:"ended_at"`
	DurationMS *int    `json:"duration_ms"`
}

type Span struct {
	SpanID       string  `json:"span_id"`
	TraceID      string  `json:"trace_id"`
	ParentSpanID *string `json:"parent_span_id"`
	Type         string  `json:"type"`
	Name         string  `json:"name"`
	Status       string  `json:"status"`
	Input        JSONMap `json:"input"`
	Output       JSONMap `json:"output"`
	Metadata     JSONMap `json:"metadata"`
	StartedAt    string  `json:"started_at"`
	EndedAt      *string `json:"ended_at"`
	DurationMS   *int    `json:"duration_ms"`
	Error        JSONMap `json:"error"`
}

type Warning struct {
	WarningID string  `json:"warning_id"`
	TraceID   string  `json:"trace_id"`
	SpanID    *string `json:"span_id"`
	Type      string  `json:"type"`
	Severity  string  `json:"severity"`
	Message   string  `json:"message"`
	Details   JSONMap `json:"details"`
	CreatedAt string  `json:"created_at"`
}

type TraceListItem struct {
	TraceID      string `json:"trace_id"`
	Name         string `json:"name"`
	Status       string `json:"status"`
	Query        string `json:"query"`
	Answer       string `json:"answer"`
	DurationMS   *int   `json:"duration_ms"`
	WarningCount int    `json:"warning_count"`
	StartedAt    string `json:"started_at"`
}

type TraceListResponse struct {
	Traces []TraceListItem `json:"traces"`
}

type TraceDetailResponse struct {
	Trace    TraceRecord `json:"trace"`
	Spans    []Span      `json:"spans"`
	Warnings []Warning   `json:"warnings"`
}

type StoreTraceResponse struct {
	TraceID           string `json:"trace_id"`
	Status            string `json:"status"`
	WarningsGenerated int    `json:"warnings_generated"`
}

type ErrorResponse struct {
	Error string `json:"error"`
}
