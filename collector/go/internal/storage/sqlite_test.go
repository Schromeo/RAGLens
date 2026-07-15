package storage

import (
	"context"
	"testing"

	"sledtrace-collector/internal/models"
)

func TestStoreWarningV2RoundTrip(t *testing.T) {
	ctx := context.Background()

	store, err := NewStore(":memory:")
	if err != nil {
		t.Fatalf("create in-memory store: %v", err)
	}
	defer store.Close()

	traceID := "trace_warning_v2_round_trip"
	retrievalSpanID := "span_retrieval"
	llmSpanID := "span_llm"

	payload := models.TracePayload{
		Trace: models.TraceRecord{
			TraceID: traceID,
			Name:    "warning-v2-round-trip",
			Status:  "ok",
			Input: models.JSONMap{
				"query": "What is the refund window?",
			},
			Output: models.JSONMap{
				"answer": "Customers may request a refund within 60 days of purchase.",
			},
			Metadata:  models.JSONMap{"test": "storage_round_trip"},
			StartedAt: "2026-07-06T00:00:00Z",
		},
		Spans: []models.Span{
			{
				SpanID:  retrievalSpanID,
				TraceID: traceID,
				Type:    "retrieval",
				Name:    "test_retrieval",
				Status:  "ok",
				Input: models.JSONMap{
					"query": "What is the refund window?",
				},
				Output: models.JSONMap{
					"chunks": []models.JSONMap{
						{
							"id":     "chunk_refund_current",
							"text":   "Customers may request a refund within 30 days of purchase.",
							"score":  0.93,
							"source": "refund_policy.md",
						},
					},
				},
				Metadata:  models.JSONMap{},
				StartedAt: "2026-07-06T00:00:01Z",
			},
			{
				SpanID:  llmSpanID,
				TraceID: traceID,
				Type:    "llm",
				Name:    "test_llm",
				Status:  "ok",
				Input: models.JSONMap{
					"prompt": "Answer using retrieved context.",
				},
				Output: models.JSONMap{
					"response": "Customers may request a refund within 60 days of purchase.",
				},
				Metadata:  models.JSONMap{},
				StartedAt: "2026-07-06T00:00:02Z",
			},
		},
	}

	if err := store.SaveTracePayload(ctx, payload); err != nil {
		t.Fatalf("save trace payload: %v", err)
	}

	schemaVersion := "2"
	ruleID := "numeric_mismatch"
	ruleVersion := "1"
	title := "Answer numeric value conflicts with retrieved context"
	category := "grounding"
	confidence := 0.9
	explanation := "SledTrace found a numeric value in the final answer that differs from a retrieved chunk with overlapping local context."
	recommendedAction := "Inspect whether the answer copied an outdated value or ignored stronger retrieved evidence."

	warnings := []models.Warning{
		{
			WarningID:     "warn_numeric_mismatch",
			TraceID:       traceID,
			SpanID:        &llmSpanID,
			Type:          "numeric_mismatch",
			Severity:      "high",
			Message:       "Answer says 60 days, but retrieved context says 30 days.",
			SchemaVersion: &schemaVersion,
			RuleID:        &ruleID,
			RuleVersion:   &ruleVersion,
			Title:         &title,
			Category:      &category,
			Confidence:    &confidence,
			Explanation:   &explanation,
			Details: models.JSONMap{
				"answer_value":    "60 days",
				"retrieved_value": "30 days",
				"shared_terms":    []string{"refund", "purchase"},
			},
			Evidence: []models.EvidenceItem{
				{
					EvidenceID: "evidence_answer_value",
					Type:       "answer_snippet",
					Label:      "Answer numeric claim",
					SpanID:     &llmSpanID,
					Snippet:    "Customers may request a refund within 60 days of purchase.",
					Attributes: models.JSONMap{
						"value":            "60",
						"unit":             "days",
						"normalized_value": "60 days",
					},
				},
				{
					EvidenceID: "evidence_chunk_value",
					Type:       "chunk_snippet",
					Label:      "Retrieved chunk numeric value",
					SpanID:     &retrievalSpanID,
					ChunkID:    stringPtrForTest("chunk_refund_current"),
					Source:     stringPtrForTest("refund_policy.md"),
					Snippet:    "Customers may request a refund within 30 days of purchase.",
					Attributes: models.JSONMap{
						"value":            "30",
						"unit":             "days",
						"normalized_value": "30 days",
						"score":            0.93,
					},
				},
			},
			Diagnostics: []models.DiagnosticObject{
				{
					DiagnosticObjectID: "diag_answer_numeric_claim",
					Type:               "numeric_claim",
					Label:              "Numeric value in final answer",
					SpanID:             &llmSpanID,
					Text:               "Customers may request a refund within 60 days of purchase.",
					Normalized: models.JSONMap{
						"value": "60",
						"unit":  "days",
					},
					Attributes: models.JSONMap{
						"source": "answer",
					},
				},
			},
			Signals: []models.DiagnosticSignal{
				{
					SignalID:   "same_unit_different_value",
					Label:      "Same unit but different numeric value",
					Observed:   "60 days",
					Expected:   "30 days",
					Comparator: "not_equal",
					Strength:   "strong",
				},
			},
			RecommendedAction: &recommendedAction,
			CreatedAt:         "2026-07-06T00:00:03Z",
		},
	}

	if err := store.SaveWarnings(ctx, warnings); err != nil {
		t.Fatalf("save warnings: %v", err)
	}

	detail, err := store.GetTraceDetail(ctx, traceID)
	if err != nil {
		t.Fatalf("get trace detail: %v", err)
	}

	if len(detail.Warnings) != 1 {
		t.Fatalf("expected 1 warning, got %d", len(detail.Warnings))
	}

	got := detail.Warnings[0]

	if got.WarningID != "warn_numeric_mismatch" {
		t.Fatalf("expected warning id warn_numeric_mismatch, got %q", got.WarningID)
	}

	if got.Type != "numeric_mismatch" {
		t.Fatalf("expected type numeric_mismatch, got %q", got.Type)
	}

	requireStringPtr(t, got.SchemaVersion, "2", "schema_version")
	requireStringPtr(t, got.RuleID, "numeric_mismatch", "rule_id")
	requireStringPtr(t, got.RuleVersion, "1", "rule_version")
	requireStringPtr(t, got.Title, title, "title")
	requireStringPtr(t, got.Category, "grounding", "category")
	requireStringPtr(t, got.Explanation, explanation, "explanation")
	requireStringPtr(t, got.RecommendedAction, recommendedAction, "recommended_action")

	if got.Confidence == nil {
		t.Fatalf("expected confidence to round-trip, got nil")
	}

	if *got.Confidence != 0.9 {
		t.Fatalf("expected confidence 0.9, got %v", *got.Confidence)
	}

	if got.Details["answer_value"] != "60 days" {
		t.Fatalf("expected details.answer_value=60 days, got %#v", got.Details["answer_value"])
	}

	if got.Details["retrieved_value"] != "30 days" {
		t.Fatalf("expected details.retrieved_value=30 days, got %#v", got.Details["retrieved_value"])
	}

	if len(got.Evidence) != 2 {
		t.Fatalf("expected 2 evidence items, got %d", len(got.Evidence))
	}

	if got.Evidence[0].EvidenceID != "evidence_answer_value" {
		t.Fatalf("expected first evidence id evidence_answer_value, got %q", got.Evidence[0].EvidenceID)
	}

	if got.Evidence[0].Type != "answer_snippet" {
		t.Fatalf("expected first evidence type answer_snippet, got %q", got.Evidence[0].Type)
	}

	if got.Evidence[0].Attributes["normalized_value"] != "60 days" {
		t.Fatalf("expected first evidence normalized_value=60 days, got %#v", got.Evidence[0].Attributes["normalized_value"])
	}

	if len(got.Diagnostics) != 1 {
		t.Fatalf("expected 1 diagnostic object, got %d", len(got.Diagnostics))
	}

	if got.Diagnostics[0].DiagnosticObjectID != "diag_answer_numeric_claim" {
		t.Fatalf("expected diagnostic id diag_answer_numeric_claim, got %q", got.Diagnostics[0].DiagnosticObjectID)
	}

	if got.Diagnostics[0].Normalized["value"] != "60" {
		t.Fatalf("expected diagnostic normalized value 60, got %#v", got.Diagnostics[0].Normalized["value"])
	}

	if len(got.Signals) != 1 {
		t.Fatalf("expected 1 signal, got %d", len(got.Signals))
	}

	if got.Signals[0].SignalID != "same_unit_different_value" {
		t.Fatalf("expected signal id same_unit_different_value, got %q", got.Signals[0].SignalID)
	}

	if got.Signals[0].Observed != "60 days" {
		t.Fatalf("expected signal observed 60 days, got %#v", got.Signals[0].Observed)
	}

	if got.Signals[0].Expected != "30 days" {
		t.Fatalf("expected signal expected 30 days, got %#v", got.Signals[0].Expected)
	}
}

func TestStoreMigratesWarningV2ColumnsOnExistingWarningTable(t *testing.T) {
	ctx := context.Background()

	store, err := NewStore(":memory:")
	if err != nil {
		t.Fatalf("create in-memory store: %v", err)
	}
	defer store.Close()

	_, err = store.db.ExecContext(ctx, `
DROP TABLE warnings;

CREATE TABLE warnings (
    id TEXT PRIMARY KEY,
    trace_id TEXT NOT NULL,
    span_id TEXT,
    type TEXT NOT NULL,
    severity TEXT NOT NULL,
    message TEXT NOT NULL,
    details_json TEXT,
    created_at TEXT NOT NULL
);
`)
	if err != nil {
		t.Fatalf("create legacy warnings table: %v", err)
	}

	if err := store.ensureWarningColumns(ctx); err != nil {
		t.Fatalf("ensure warning columns: %v", err)
	}

	expectedColumns := []string{
		"schema_version",
		"rule_id",
		"rule_version",
		"title",
		"category",
		"confidence",
		"explanation",
		"evidence_json",
		"diagnostics_json",
		"signals_json",
		"recommended_action",
	}

	for _, column := range expectedColumns {
		if !warningColumnExists(t, store, column) {
			t.Fatalf("expected warnings.%s column to exist after migration", column)
		}
	}
}

func requireStringPtr(t *testing.T, actual *string, expected string, fieldName string) {
	t.Helper()

	if actual == nil {
		t.Fatalf("expected %s=%q, got nil", fieldName, expected)
	}

	if *actual != expected {
		t.Fatalf("expected %s=%q, got %q", fieldName, expected, *actual)
	}
}

func warningColumnExists(t *testing.T, store *Store, columnName string) bool {
	t.Helper()

	rows, err := store.db.QueryContext(context.Background(), `PRAGMA table_info(warnings)`)
	if err != nil {
		t.Fatalf("query warning table info: %v", err)
	}
	defer rows.Close()

	for rows.Next() {
		var (
			cid        int
			name       string
			columnType string
			notNull    int
			defaultVal any
			pk         int
		)

		if err := rows.Scan(&cid, &name, &columnType, &notNull, &defaultVal, &pk); err != nil {
			t.Fatalf("scan warning column info: %v", err)
		}

		if name == columnName {
			return true
		}
	}

	if err := rows.Err(); err != nil {
		t.Fatalf("iterate warning table info: %v", err)
	}

	return false
}

func stringPtrForTest(value string) *string {
	return &value
}
