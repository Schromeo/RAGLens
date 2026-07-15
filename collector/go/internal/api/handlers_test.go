package api

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"sledtrace-collector/internal/models"
	"sledtrace-collector/internal/storage"
)

func TestPostTraceGeneratesV3WarningAndGetTraceDetailReturnsWarningFields(t *testing.T) {
	store, err := storage.NewStore(":memory:")
	if err != nil {
		t.Fatalf("create in-memory store: %v", err)
	}
	defer store.Close()

	server := NewServer(store)
	handler := server.Routes()

	payload := apiTestNumericMismatchPayload()

	postBody, err := json.Marshal(payload)
	if err != nil {
		t.Fatalf("marshal trace payload: %v", err)
	}

	postReq := httptest.NewRequest(http.MethodPost, "/api/traces", bytes.NewReader(postBody))
	postReq.Header.Set("Content-Type", "application/json")

	postRec := httptest.NewRecorder()
	handler.ServeHTTP(postRec, postReq)

	if postRec.Code != http.StatusCreated {
		t.Fatalf("expected POST /api/traces status %d, got %d body=%s", http.StatusCreated, postRec.Code, postRec.Body.String())
	}

	var postResp map[string]any
	if err := json.Unmarshal(postRec.Body.Bytes(), &postResp); err != nil {
		t.Fatalf("decode post response: %v body=%s", err, postRec.Body.String())
	}

	warningsGenerated := numberField(t, postResp, "warnings_generated", "WarningsGenerated")
	if warningsGenerated < 1 {
		t.Fatalf("expected warnings_generated >= 1, got %v response=%#v", warningsGenerated, postResp)
	}

	getReq := httptest.NewRequest(http.MethodGet, "/api/traces/trace_api_numeric_mismatch", nil)
	getRec := httptest.NewRecorder()
	handler.ServeHTTP(getRec, getReq)

	if getRec.Code != http.StatusOK {
		t.Fatalf("expected GET /api/traces/{trace_id} status %d, got %d body=%s", http.StatusOK, getRec.Code, getRec.Body.String())
	}

	var detail map[string]any
	if err := json.Unmarshal(getRec.Body.Bytes(), &detail); err != nil {
		t.Fatalf("decode trace detail response: %v body=%s", err, getRec.Body.String())
	}

	warningsValue := field(t, detail, "warnings", "Warnings")
	warnings, ok := warningsValue.([]any)
	if !ok {
		t.Fatalf("expected warnings array, got %#v", warningsValue)
	}

	if len(warnings) == 0 {
		t.Fatalf("expected at least one warning in trace detail")
	}

	numericMismatch := findWarningByType(t, warnings, "numeric_mismatch")

	if stringField(t, numericMismatch, "type", "Type") != "numeric_mismatch" {
		t.Fatalf("expected numeric_mismatch type, got %#v", numericMismatch)
	}

	if stringField(t, numericMismatch, "schema_version", "SchemaVersion") != "2" {
		t.Fatalf("expected schema_version=2, got %#v", numericMismatch)
	}

	if stringField(t, numericMismatch, "rule_id", "RuleID") != "numeric_mismatch" {
		t.Fatalf("expected rule_id=numeric_mismatch, got %#v", numericMismatch)
	}

	if stringField(t, numericMismatch, "category", "Category") != "grounding" {
		t.Fatalf("expected category=grounding, got %#v", numericMismatch)
	}

	if numberField(t, numericMismatch, "confidence", "Confidence") <= 0 {
		t.Fatalf("expected confidence > 0, got %#v", numericMismatch)
	}

	if stringField(t, numericMismatch, "recommended_action", "RecommendedAction") == "" {
		t.Fatalf("expected recommended_action to be present, got %#v", numericMismatch)
	}

	evidenceValue := field(t, numericMismatch, "evidence", "Evidence")
	evidence, ok := evidenceValue.([]any)
	if !ok {
		t.Fatalf("expected evidence array, got %#v", evidenceValue)
	}

	if len(evidence) == 0 {
		t.Fatalf("expected evidence to be populated, got %#v", numericMismatch)
	}

	if !hasEvidenceType(evidence, "numeric_value") {
		t.Fatalf("expected numeric_value evidence, got %#v", evidence)
	}

	diagnosticsValue := field(t, numericMismatch, "diagnostics", "Diagnostics")
	diagnostics, ok := diagnosticsValue.([]any)
	if !ok {
		t.Fatalf("expected diagnostics array, got %#v", diagnosticsValue)
	}

	if len(diagnostics) == 0 {
		t.Fatalf("expected diagnostics to be populated, got %#v", numericMismatch)
	}

	signalsValue := field(t, numericMismatch, "signals", "Signals")
	signals, ok := signalsValue.([]any)
	if !ok {
		t.Fatalf("expected signals array, got %#v", signalsValue)
	}

	if len(signals) == 0 {
		t.Fatalf("expected signals to be populated, got %#v", numericMismatch)
	}
}

func TestGetTraceDetailReturnsNotFoundForMissingTrace(t *testing.T) {
	store, err := storage.NewStore(":memory:")
	if err != nil {
		t.Fatalf("create in-memory store: %v", err)
	}
	defer store.Close()

	server := NewServer(store)
	handler := server.Routes()

	req := httptest.NewRequest(http.MethodGet, "/api/traces/missing_trace", nil)
	rec := httptest.NewRecorder()

	handler.ServeHTTP(rec, req)

	if rec.Code != http.StatusNotFound {
		t.Fatalf("expected status %d, got %d body=%s", http.StatusNotFound, rec.Code, rec.Body.String())
	}
}

func apiTestNumericMismatchPayload() models.TracePayload {
	traceID := "trace_api_numeric_mismatch"

	return models.TracePayload{
		Trace: models.TraceRecord{
			TraceID: traceID,
			Name:    "api-numeric-mismatch",
			Status:  "ok",
			Input: models.JSONMap{
				"query": "What is the refund window?",
			},
			Output: models.JSONMap{
				"answer": "Customers may request a refund within 60 days of purchase.",
			},
			Metadata:  models.JSONMap{},
			StartedAt: "2026-07-06T00:00:00Z",
		},
		Spans: []models.Span{
			{
				SpanID:  "span_api_retrieval",
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
							"id":    "chunk_refund_current",
							"text":  "Customers may request a refund within 30 days of purchase.",
							"score": 0.93,
							"metadata": models.JSONMap{
								"source": "refund_policy.md",
							},
						},
						{
							"id":    "chunk_returns_general",
							"text":  "Refund requests must be submitted through the customer support portal.",
							"score": 0.78,
							"metadata": models.JSONMap{
								"source": "returns_process.md",
							},
						},
					},
				},
				Metadata:  models.JSONMap{},
				StartedAt: "2026-07-06T00:00:01Z",
			},
			{
				SpanID:  "span_api_llm",
				TraceID: traceID,
				Type:    "llm",
				Name:    "test_llm",
				Status:  "ok",
				Input: models.JSONMap{
					"prompt": "Answer the user question using the retrieved context.",
				},
				Output: models.JSONMap{
					"response": "Customers may request a refund within 60 days of purchase.",
				},
				Metadata:  models.JSONMap{},
				StartedAt: "2026-07-06T00:00:02Z",
			},
		},
	}
}

func findWarningByType(t *testing.T, warnings []any, warningType string) map[string]any {
	t.Helper()

	for _, warningValue := range warnings {
		warning, ok := warningValue.(map[string]any)
		if !ok {
			t.Fatalf("expected warning object, got %#v", warningValue)
		}

		if stringField(t, warning, "type", "Type") == warningType {
			return warning
		}
	}

	t.Fatalf("expected warning type %q, got warnings=%#v", warningType, warnings)
	return nil
}

func hasEvidenceType(evidence []any, evidenceType string) bool {
	for _, evidenceValue := range evidence {
		item, ok := evidenceValue.(map[string]any)
		if !ok {
			continue
		}

		value, ok := item["type"]
		if !ok {
			value = item["Type"]
		}

		if value == evidenceType {
			return true
		}
	}

	return false
}

func field(t *testing.T, object map[string]any, names ...string) any {
	t.Helper()

	for _, name := range names {
		value, ok := object[name]
		if ok {
			return value
		}
	}

	t.Fatalf("expected one of fields %v in object %#v", names, object)
	return nil
}

func stringField(t *testing.T, object map[string]any, names ...string) string {
	t.Helper()

	value := field(t, object, names...)

	if value == nil {
		return ""
	}

	stringValue, ok := value.(string)
	if !ok {
		t.Fatalf("expected string field %v, got %#v", names, value)
	}

	return stringValue
}

func numberField(t *testing.T, object map[string]any, names ...string) float64 {
	t.Helper()

	value := field(t, object, names...)

	numberValue, ok := value.(float64)
	if !ok {
		t.Fatalf("expected numeric field %v, got %#v", names, value)
	}

	return numberValue
}
