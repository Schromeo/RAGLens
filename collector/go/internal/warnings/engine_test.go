package warnings

import (
	"testing"

	"raglens-collector/internal/models"
)

func TestGenerateNumericMismatchWarning(t *testing.T) {
	payload := basePayload(
		"trace_numeric_mismatch",
		"What is the refund window?",
		[]models.JSONMap{
			chunk("chunk_refund_current", "Customers may request a refund within 30 days of purchase.", 0.93, "refund_policy.md"),
			chunk("chunk_returns_general", "Refund requests must be submitted through the customer support portal.", 0.78, "returns_process.md"),
		},
		"Customers may request a refund within 60 days of purchase.",
	)

	warnings := NewEngine().Generate(payload)

	warning := requireWarningType(t, warnings, TypeNumericMismatch)

	requireStringPtrValue(t, warning.Category, "grounding", "category")
	requireStringPtrValue(t, warning.RuleVersion, "1", "rule_version")

	if warning.Confidence == nil {
		t.Fatalf("expected numeric_mismatch confidence to be set")
	}

	if *warning.Confidence < 0.89 {
		t.Fatalf("expected numeric_mismatch confidence >= 0.89, got %v", *warning.Confidence)
	}

	if len(warning.Evidence) == 0 {
		t.Fatalf("expected numeric_mismatch evidence to be populated")
	}

	if !hasEvidenceType(warning, "numeric_value") {
		t.Fatalf("expected numeric_mismatch to include numeric_value evidence, got %#v", warning.Evidence)
	}

	if warning.Details["answer_value"] != "60 days" {
		t.Fatalf("expected answer_value=60 days, got %#v", warning.Details["answer_value"])
	}

	if warning.Details["retrieved_value"] != "30 days" {
		t.Fatalf("expected retrieved_value=30 days, got %#v", warning.Details["retrieved_value"])
	}
}

func TestGenerateWeakQueryChunkOverlapWarning(t *testing.T) {
	payload := basePayload(
		"trace_weak_overlap",
		"What is the refund window?",
		[]models.JSONMap{
			chunk("chunk_shipping_standard", "Standard shipping usually takes 5 to 7 business days after an order has shipped.", 0.88, "shipping_policy.md"),
			chunk("chunk_warranty_general", "Warranty coverage applies to manufacturing defects for eligible physical products.", 0.81, "warranty_policy.md"),
		},
		"I could not find enough information in the retrieved context to answer the refund window question.",
	)

	warnings := NewEngine().Generate(payload)

	warning := requireWarningType(t, warnings, TypeWeakQueryChunkOverlap)

	requireStringPtrValue(t, warning.Category, "retrieval", "category")
	requireStringPtrValue(t, warning.RuleVersion, "1", "rule_version")

	if warning.Confidence == nil {
		t.Fatalf("expected weak_query_chunk_overlap confidence to be set")
	}

	if *warning.Confidence < 0.74 {
		t.Fatalf("expected weak_query_chunk_overlap confidence >= 0.74, got %v", *warning.Confidence)
	}

	if len(warning.Evidence) == 0 {
		t.Fatalf("expected weak_query_chunk_overlap evidence to be populated")
	}

	if !hasEvidenceType(warning, "query_text") {
		t.Fatalf("expected weak_query_chunk_overlap to include query_text evidence, got %#v", warning.Evidence)
	}

	if !hasEvidenceType(warning, "overlap_measure") {
		t.Fatalf("expected weak_query_chunk_overlap to include overlap_measure evidence, got %#v", warning.Evidence)
	}

	if warning.Details["best_overlap_ratio"] == nil {
		t.Fatalf("expected best_overlap_ratio in details")
	}
}

func TestGenerateAnswerNotGroundedV2Warning(t *testing.T) {
	payload := basePayload(
		"trace_answer_not_grounded",
		"What is the refund window?",
		[]models.JSONMap{
			chunk("chunk_refund_current", "Customers may request a refund within 30 days of purchase.", 0.93, "refund_policy.md"),
			chunk("chunk_returns_general", "Refund requests must be submitted through the customer support portal.", 0.78, "returns_process.md"),
		},
		"Customers may request a refund within 30 days of purchase. Original shipping fees are refundable.",
	)

	warnings := NewEngine().Generate(payload)

	warning := requireWarningType(t, warnings, TypeAnswerNotGrounded)

	requireStringPtrValue(t, warning.Category, "grounding", "category")
	requireStringPtrValue(t, warning.RuleVersion, "2", "rule_version")
	requireStringPtrValue(t, warning.Title, "Answer contains an unsupported claim", "title")

	if warning.Confidence == nil {
		t.Fatalf("expected answer_not_grounded confidence to be set")
	}

	if *warning.Confidence < 0.79 {
		t.Fatalf("expected answer_not_grounded confidence >= 0.79, got %v", *warning.Confidence)
	}

	if len(warning.Evidence) == 0 {
		t.Fatalf("expected answer_not_grounded evidence to be populated")
	}

	if !hasEvidenceLabel(warning, "Unsupported answer claim") {
		t.Fatalf("expected answer_not_grounded to include unsupported answer claim evidence, got %#v", warning.Evidence)
	}

	if warning.Details["claim"] != "Original shipping fees are refundable." {
		t.Fatalf("expected unsupported claim in details, got %#v", warning.Details["claim"])
	}
}

func TestGenerateConflictingChunksV2Warning(t *testing.T) {
	payload := basePayload(
		"trace_conflicting_chunks",
		"What is the refund window?",
		[]models.JSONMap{
			chunk("chunk_refund_current", "Customers may request a refund within 30 days of purchase.", 0.93, "refund_policy.md"),
			chunk("chunk_refund_legacy", "Customers may request a refund within 60 days of purchase under the legacy refund policy.", 0.89, "legacy_refund_policy.md"),
		},
		"I could not determine a single refund window because the retrieved context is inconsistent.",
	)

	warnings := NewEngine().Generate(payload)

	warning := requireWarningType(t, warnings, TypeConflictingChunks)

	requireStringPtrValue(t, warning.Category, "conflict", "category")
	requireStringPtrValue(t, warning.RuleVersion, "2", "rule_version")
	requireStringPtrValue(t, warning.Title, "Retrieved chunks contain conflicting values", "title")

	if warning.Confidence == nil {
		t.Fatalf("expected conflicting_chunks confidence to be set")
	}

	if *warning.Confidence < 0.87 {
		t.Fatalf("expected conflicting_chunks confidence >= 0.87, got %v", *warning.Confidence)
	}

	if len(warning.Evidence) == 0 {
		t.Fatalf("expected conflicting_chunks evidence to be populated")
	}

	if !hasEvidenceType(warning, "conflict_pair") {
		t.Fatalf("expected conflicting_chunks to include conflict_pair evidence, got %#v", warning.Evidence)
	}

	values, ok := warning.Details["detected_values"].([]string)
	if !ok {
		t.Fatalf("expected detected_values []string, got %#v", warning.Details["detected_values"])
	}

	if len(values) != 2 {
		t.Fatalf("expected two detected values, got %#v", values)
	}

	if !containsString(values, "30 days") || !containsString(values, "60 days") {
		t.Fatalf("expected detected values to contain 30 days and 60 days, got %#v", values)
	}
}

func basePayload(traceID string, query string, chunks []models.JSONMap, answer string) models.TracePayload {
	return models.TracePayload{
		Trace: models.TraceRecord{
			TraceID: traceID,
			Name:    traceID,
			Status:  "ok",
			Input: models.JSONMap{
				"query": query,
			},
			Output: models.JSONMap{
				"answer": answer,
			},
			Metadata:  models.JSONMap{},
			StartedAt: "2026-07-06T00:00:00Z",
		},
		Spans: []models.Span{
			{
				SpanID:  "span_retrieval",
				TraceID: traceID,
				Type:    "retrieval",
				Name:    "test_retrieval",
				Status:  "ok",
				Input: models.JSONMap{
					"query": query,
				},
				Output: models.JSONMap{
					"chunks": chunks,
				},
				Metadata:  models.JSONMap{},
				StartedAt: "2026-07-06T00:00:00Z",
			},
			{
				SpanID:  "span_llm",
				TraceID: traceID,
				Type:    "llm",
				Name:    "test_llm",
				Status:  "ok",
				Input: models.JSONMap{
					"prompt": "Answer the user question using the retrieved context.",
				},
				Output: models.JSONMap{
					"response": answer,
				},
				Metadata:  models.JSONMap{},
				StartedAt: "2026-07-06T00:00:00Z",
			},
		},
	}
}

func chunk(id string, text string, score float64, source string) models.JSONMap {
	return models.JSONMap{
		"id":    id,
		"text":  text,
		"score": score,
		"metadata": models.JSONMap{
			"source": source,
		},
	}
}

func requireWarningType(t *testing.T, warnings []models.Warning, warningType string) models.Warning {
	t.Helper()

	for _, warning := range warnings {
		if warning.Type == warningType {
			return warning
		}
	}

	t.Fatalf("expected warning type %q, got warning types %v", warningType, warningTypes(warnings))

	return models.Warning{}
}

func warningTypes(warnings []models.Warning) []string {
	result := make([]string, 0, len(warnings))

	for _, warning := range warnings {
		result = append(result, warning.Type)
	}

	return result
}

func requireStringPtrValue(t *testing.T, actual *string, expected string, fieldName string) {
	t.Helper()

	if actual == nil {
		t.Fatalf("expected %s to be %q, got nil", fieldName, expected)
	}

	if *actual != expected {
		t.Fatalf("expected %s to be %q, got %q", fieldName, expected, *actual)
	}
}

func hasEvidenceType(warning models.Warning, evidenceType string) bool {
	for _, evidence := range warning.Evidence {
		if evidence.Type == evidenceType {
			return true
		}
	}

	return false
}

func hasEvidenceLabel(warning models.Warning, label string) bool {
	for _, evidence := range warning.Evidence {
		if evidence.Label == label {
			return true
		}
	}

	return false
}

func containsString(values []string, target string) bool {
	for _, value := range values {
		if value == target {
			return true
		}
	}

	return false
}
