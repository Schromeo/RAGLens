package storage

import (
	"context"
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"time"

	"raglens-collector/internal/models"

	_ "modernc.org/sqlite"
)

type Store struct {
	db *sql.DB
}

func NewStore(path string) (*Store, error) {
	db, err := sql.Open("sqlite", path)
	if err != nil {
		return nil, fmt.Errorf("open sqlite database: %w", err)
	}

	store := &Store{db: db}

	if err := store.migrate(context.Background()); err != nil {
		_ = db.Close()
		return nil, err
	}

	return store, nil
}

func (s *Store) Close() error {
	return s.db.Close()
}

func (s *Store) migrate(ctx context.Context) error {
	schema := `
CREATE TABLE IF NOT EXISTS traces (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    input_json TEXT,
    output_json TEXT,
    metadata_json TEXT,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    duration_ms INTEGER,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS spans (
    id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    parent_span_id TEXT,
    type TEXT NOT NULL,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    input_json TEXT,
    output_json TEXT,
    metadata_json TEXT,
    started_at TEXT NOT NULL,
    ended_at TEXT,
    duration_ms INTEGER,
    error_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(trace_id) REFERENCES traces(id)
);

CREATE TABLE IF NOT EXISTS warnings (
    id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    span_id TEXT,
    type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    details_json TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY(trace_id) REFERENCES traces(id),
    FOREIGN KEY(span_id) REFERENCES spans(id)
);

CREATE INDEX IF NOT EXISTS idx_traces_started_at
ON traces(started_at);

CREATE INDEX IF NOT EXISTS idx_spans_trace_id
ON spans(trace_id);

CREATE INDEX IF NOT EXISTS idx_warnings_trace_id
ON warnings(trace_id);

CREATE INDEX IF NOT EXISTS idx_warnings_span_id
ON warnings(span_id);
`

	_, err := s.db.ExecContext(ctx, schema)
	if err != nil {
		return fmt.Errorf("run sqlite migrations: %w", err)
	}

	return nil
}

func (s *Store) SaveTracePayload(ctx context.Context, payload models.TracePayload) error {
	if payload.Trace.TraceID == "" {
		return errors.New("trace.trace_id is required")
	}

	if payload.Trace.Name == "" {
		return errors.New("trace.name is required")
	}

	if payload.Trace.Status == "" {
		return errors.New("trace.status is required")
	}

	if payload.Trace.StartedAt == "" {
		return errors.New("trace.started_at is required")
	}

	tx, err := s.db.BeginTx(ctx, nil)
	if err != nil {
		return fmt.Errorf("begin transaction: %w", err)
	}

	defer func() {
		_ = tx.Rollback()
	}()

	now := time.Now().UTC().Format(time.RFC3339Nano)

	inputJSON, err := marshalJSON(payload.Trace.Input)
	if err != nil {
		return fmt.Errorf("marshal trace input: %w", err)
	}

	outputJSON, err := marshalJSON(payload.Trace.Output)
	if err != nil {
		return fmt.Errorf("marshal trace output: %w", err)
	}

	metadataJSON, err := marshalJSON(payload.Trace.Metadata)
	if err != nil {
		return fmt.Errorf("marshal trace metadata: %w", err)
	}

	_, err = tx.ExecContext(
		ctx,
		`
INSERT INTO traces (
    id, name, status, input_json, output_json, metadata_json,
    started_at, ended_at, duration_ms, created_at
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`,
		payload.Trace.TraceID,
		payload.Trace.Name,
		payload.Trace.Status,
		inputJSON,
		outputJSON,
		metadataJSON,
		payload.Trace.StartedAt,
		nullableString(payload.Trace.EndedAt),
		nullableInt(payload.Trace.DurationMS),
		now,
	)

	if err != nil {
		return fmt.Errorf("insert trace: %w", err)
	}

	for _, span := range payload.Spans {
		if span.SpanID == "" {
			return errors.New("span.span_id is required")
		}

		if span.TraceID == "" {
			return errors.New("span.trace_id is required")
		}

		if span.TraceID != payload.Trace.TraceID {
			return fmt.Errorf("span %s trace_id does not match payload trace_id", span.SpanID)
		}

		inputJSON, err := marshalJSON(span.Input)
		if err != nil {
			return fmt.Errorf("marshal span input: %w", err)
		}

		outputJSON, err := marshalJSON(span.Output)
		if err != nil {
			return fmt.Errorf("marshal span output: %w", err)
		}

		metadataJSON, err := marshalJSON(span.Metadata)
		if err != nil {
			return fmt.Errorf("marshal span metadata: %w", err)
		}

		errorJSON, err := marshalJSON(span.Error)
		if err != nil {
			return fmt.Errorf("marshal span error: %w", err)
		}

		_, err = tx.ExecContext(
			ctx,
			`
INSERT INTO spans (
    id, trace_id, parent_span_id, type, name, status,
    input_json, output_json, metadata_json,
    started_at, ended_at, duration_ms, error_json, created_at
)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`,
			span.SpanID,
			span.TraceID,
			nullableString(span.ParentSpanID),
			span.Type,
			span.Name,
			span.Status,
			inputJSON,
			outputJSON,
			metadataJSON,
			span.StartedAt,
			nullableString(span.EndedAt),
			nullableInt(span.DurationMS),
			errorJSON,
			now,
		)

		if err != nil {
			return fmt.Errorf("insert span %s: %w", span.SpanID, err)
		}
	}

	if err := tx.Commit(); err != nil {
		return fmt.Errorf("commit transaction: %w", err)
	}

	return nil
}

func (s *Store) ListTraces(ctx context.Context) ([]models.TraceListItem, error) {
	rows, err := s.db.QueryContext(
		ctx,
		`
SELECT
    t.id,
    t.name,
    t.status,
    t.input_json,
    t.output_json,
    t.duration_ms,
    t.started_at,
    COUNT(w.id) AS warning_count
FROM traces t
LEFT JOIN warnings w ON w.trace_id = t.id
GROUP BY t.id
ORDER BY t.started_at DESC
LIMIT 100
`,
	)

	if err != nil {
		return nil, fmt.Errorf("query traces: %w", err)
	}

	defer rows.Close()

	traces := make([]models.TraceListItem, 0)

	for rows.Next() {
		var (
			id           string
			name         string
			status       string
			inputJSON    sql.NullString
			outputJSON   sql.NullString
			duration     sql.NullInt64
			startedAt    string
			warningCount int
		)

		if err := rows.Scan(
			&id,
			&name,
			&status,
			&inputJSON,
			&outputJSON,
			&duration,
			&startedAt,
			&warningCount,
		); err != nil {
			return nil, fmt.Errorf("scan trace row: %w", err)
		}

		inputMap := parseJSONMap(inputJSON.String)
		outputMap := parseJSONMap(outputJSON.String)

		item := models.TraceListItem{
			TraceID:      id,
			Name:         name,
			Status:       status,
			Query:        stringFromMap(inputMap, "query"),
			Answer:       stringFromMap(outputMap, "answer"),
			DurationMS:   nullableIntFromSQL(duration),
			WarningCount: warningCount,
			StartedAt:    startedAt,
		}

		traces = append(traces, item)
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate traces: %w", err)
	}

	return traces, nil
}

func (s *Store) GetTraceDetail(ctx context.Context, traceID string) (*models.TraceDetailResponse, error) {
	trace, err := s.getTrace(ctx, traceID)
	if err != nil {
		return nil, err
	}

	spans, err := s.getSpans(ctx, traceID)
	if err != nil {
		return nil, err
	}

	warnings, err := s.getWarnings(ctx, traceID)
	if err != nil {
		return nil, err
	}

	return &models.TraceDetailResponse{
		Trace:    *trace,
		Spans:    spans,
		Warnings: warnings,
	}, nil
}

func (s *Store) getTrace(ctx context.Context, traceID string) (*models.TraceRecord, error) {
	row := s.db.QueryRowContext(
		ctx,
		`
SELECT
    id, name, status, input_json, output_json, metadata_json,
    started_at, ended_at, duration_ms
FROM traces
WHERE id = ?
`,
		traceID,
	)

	var (
		id           string
		name         string
		status       string
		inputJSON    sql.NullString
		outputJSON   sql.NullString
		metadataJSON sql.NullString
		startedAt    string
		endedAt      sql.NullString
		duration     sql.NullInt64
	)

	if err := row.Scan(
		&id,
		&name,
		&status,
		&inputJSON,
		&outputJSON,
		&metadataJSON,
		&startedAt,
		&endedAt,
		&duration,
	); err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, sql.ErrNoRows
		}

		return nil, fmt.Errorf("scan trace detail: %w", err)
	}

	return &models.TraceRecord{
		TraceID:    id,
		Name:       name,
		Status:     status,
		Input:      parseJSONMap(inputJSON.String),
		Output:     parseJSONMap(outputJSON.String),
		Metadata:   parseJSONMap(metadataJSON.String),
		StartedAt:  startedAt,
		EndedAt:    nullableStringFromSQL(endedAt),
		DurationMS: nullableIntFromSQL(duration),
	}, nil
}

func (s *Store) getSpans(ctx context.Context, traceID string) ([]models.Span, error) {
	rows, err := s.db.QueryContext(
		ctx,
		`
SELECT
    id, trace_id, parent_span_id, type, name, status,
    input_json, output_json, metadata_json,
    started_at, ended_at, duration_ms, error_json
FROM spans
WHERE trace_id = ?
ORDER BY started_at ASC
`,
		traceID,
	)

	if err != nil {
		return nil, fmt.Errorf("query spans: %w", err)
	}

	defer rows.Close()

	spans := make([]models.Span, 0)

	for rows.Next() {
		var (
			id           string
			parentSpanID sql.NullString
			spanTraceID  string
			spanType     string
			name         string
			status       string
			inputJSON    sql.NullString
			outputJSON   sql.NullString
			metadataJSON sql.NullString
			startedAt    string
			endedAt      sql.NullString
			duration     sql.NullInt64
			errorJSON    sql.NullString
		)

		if err := rows.Scan(
			&id,
			&spanTraceID,
			&parentSpanID,
			&spanType,
			&name,
			&status,
			&inputJSON,
			&outputJSON,
			&metadataJSON,
			&startedAt,
			&endedAt,
			&duration,
			&errorJSON,
		); err != nil {
			return nil, fmt.Errorf("scan span: %w", err)
		}

		spans = append(spans, models.Span{
			SpanID:       id,
			TraceID:      spanTraceID,
			ParentSpanID: nullableStringFromSQL(parentSpanID),
			Type:         spanType,
			Name:         name,
			Status:       status,
			Input:        parseJSONMap(inputJSON.String),
			Output:       parseJSONMap(outputJSON.String),
			Metadata:     parseJSONMap(metadataJSON.String),
			StartedAt:    startedAt,
			EndedAt:      nullableStringFromSQL(endedAt),
			DurationMS:   nullableIntFromSQL(duration),
			Error:        parseJSONMap(errorJSON.String),
		})
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate spans: %w", err)
	}

	return spans, nil
}

func (s *Store) getWarnings(ctx context.Context, traceID string) ([]models.Warning, error) {
	rows, err := s.db.QueryContext(
		ctx,
		`
SELECT
    id, trace_id, span_id, type, severity, message, details_json, created_at
FROM warnings
WHERE trace_id = ?
ORDER BY created_at ASC
`,
		traceID,
	)

	if err != nil {
		return nil, fmt.Errorf("query warnings: %w", err)
	}

	defer rows.Close()

	warnings := make([]models.Warning, 0)

	for rows.Next() {
		var (
			id             string
			warningTraceID string
			spanID         sql.NullString
			warningType    string
			severity       string
			message        string
			detailsJSON    sql.NullString
			createdAt      string
		)

		if err := rows.Scan(
			&id,
			&warningTraceID,
			&spanID,
			&warningType,
			&severity,
			&message,
			&detailsJSON,
			&createdAt,
		); err != nil {
			return nil, fmt.Errorf("scan warning: %w", err)
		}

		warnings = append(warnings, models.Warning{
			WarningID: id,
			TraceID:   warningTraceID,
			SpanID:    nullableStringFromSQL(spanID),
			Type:      warningType,
			Severity:  severity,
			Message:   message,
			Details:   parseJSONMap(detailsJSON.String),
			CreatedAt: createdAt,
		})
	}

	if err := rows.Err(); err != nil {
		return nil, fmt.Errorf("iterate warnings: %w", err)
	}

	return warnings, nil
}

func marshalJSON(value any) (string, error) {
	if value == nil {
		return "{}", nil
	}

	data, err := json.Marshal(value)
	if err != nil {
		return "", err
	}

	return string(data), nil
}

func parseJSONMap(raw string) models.JSONMap {
	if raw == "" {
		return models.JSONMap{}
	}

	var result models.JSONMap
	if err := json.Unmarshal([]byte(raw), &result); err != nil {
		return models.JSONMap{}
	}

	if result == nil {
		return models.JSONMap{}
	}

	return result
}

func stringFromMap(value models.JSONMap, key string) string {
	raw, ok := value[key]
	if !ok || raw == nil {
		return ""
	}

	str, ok := raw.(string)
	if !ok {
		return ""
	}

	return str
}

func nullableString(value *string) any {
	if value == nil {
		return nil
	}

	return *value
}

func nullableInt(value *int) any {
	if value == nil {
		return nil
	}

	return *value
}

func nullableStringFromSQL(value sql.NullString) *string {
	if !value.Valid {
		return nil
	}

	return &value.String
}

func nullableIntFromSQL(value sql.NullInt64) *int {
	if !value.Valid {
		return nil
	}

	result := int(value.Int64)
	return &result
}
