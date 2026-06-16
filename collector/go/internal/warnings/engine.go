package warnings

import (
	"crypto/rand"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"regexp"
	"sort"
	"strings"
	"time"

	"raglens-collector/internal/models"
)

const (
	TypeConflictingChunks = "conflicting_chunks"
	TypeNoRetrievedChunks = "no_retrieved_chunks"
	TypeLowRetrievalScore = "low_retrieval_score"
	TypeDuplicateChunks   = "duplicate_chunks"
	TypeAnswerNotGrounded = "answer_not_grounded"

	SeverityInfo    = "info"
	SeverityWarning = "warning"
	SeverityError   = "error"

	DefaultLowScoreThreshold = 0.5
)

type Engine struct{}

func NewEngine() *Engine {
	return &Engine{}
}

func (e *Engine) Generate(payload models.TracePayload) []models.Warning {
	result := make([]models.Warning, 0)

	result = append(result, e.detectNoRetrievedChunks(payload)...)
	result = append(result, e.detectLowRetrievalScore(payload)...)
	result = append(result, e.detectDuplicateChunks(payload)...)
	result = append(result, e.detectConflictingChunks(payload)...)
	result = append(result, e.detectAnswerNotGrounded(payload)...)

	return result
}

func (e *Engine) detectNoRetrievedChunks(payload models.TracePayload) []models.Warning {
	result := make([]models.Warning, 0)

	for _, span := range payload.Spans {
		if span.Type != "retrieval" {
			continue
		}

		chunks := extractRetrievedChunksFromSpan(span)
		if len(chunks) > 0 {
			continue
		}

		spanID := span.SpanID

		result = append(result, models.Warning{
			WarningID: newWarningID(),
			TraceID:   payload.Trace.TraceID,
			SpanID:    &spanID,
			Type:      TypeNoRetrievedChunks,
			Severity:  SeverityWarning,
			Message:   "Retrieval span returned no chunks.",
			Details: models.JSONMap{
				"rule":      TypeNoRetrievedChunks,
				"span_id":   span.SpanID,
				"span_name": span.Name,
				"reason":    "retrieval span output did not contain any retrieved chunks",
			},
			CreatedAt: time.Now().UTC().Format(time.RFC3339Nano),
		})
	}

	return result
}

func (e *Engine) detectLowRetrievalScore(payload models.TracePayload) []models.Warning {
	result := make([]models.Warning, 0)

	for _, span := range payload.Spans {
		if span.Type != "retrieval" {
			continue
		}

		chunks := extractRetrievedChunksFromSpan(span)
		if len(chunks) == 0 {
			continue
		}

		threshold := getLowScoreThreshold(span)

		scoredChunks := make([]models.JSONMap, 0)
		maxScore := -1.0
		scoredCount := 0

		for _, chunk := range chunks {
			if chunk.Score == nil {
				continue
			}

			score := *chunk.Score
			scoredCount++

			if score > maxScore {
				maxScore = score
			}

			scoredChunks = append(scoredChunks, models.JSONMap{
				"chunk_id": chunk.ChunkID,
				"score":    score,
			})
		}

		// If no score was recorded, skip this rule.
		// Some retrievers do not expose normalized relevance scores.
		if scoredCount == 0 {
			continue
		}

		// MVP rule:
		// If even the best retrieved chunk is below threshold,
		// retrieval quality is probably weak.
		if maxScore >= threshold {
			continue
		}

		spanID := span.SpanID

		result = append(result, models.Warning{
			WarningID: newWarningID(),
			TraceID:   payload.Trace.TraceID,
			SpanID:    &spanID,
			Type:      TypeLowRetrievalScore,
			Severity:  SeverityWarning,
			Message:   "Retrieved chunks have low relevance scores.",
			Details: models.JSONMap{
				"rule":         TypeLowRetrievalScore,
				"span_id":      span.SpanID,
				"span_name":    span.Name,
				"threshold":    threshold,
				"max_score":    maxScore,
				"chunk_scores": scoredChunks,
				"reason":       "highest retrieved chunk score is below threshold",
			},
			CreatedAt: time.Now().UTC().Format(time.RFC3339Nano),
		})
	}

	return result
}

func (e *Engine) detectDuplicateChunks(payload models.TracePayload) []models.Warning {
	chunks := extractRetrievedChunks(payload.Spans)
	if len(chunks) < 2 {
		return nil
	}

	groups := map[string][]retrievedChunk{}

	for _, chunk := range chunks {
		normalized := normalizeChunkText(chunk.Text)
		if normalized == "" {
			continue
		}

		groups[normalized] = append(groups[normalized], chunk)
	}

	duplicateGroups := make([]models.JSONMap, 0)

	for normalizedText, group := range groups {
		if len(group) < 2 {
			continue
		}

		chunkIDs := make([]string, 0, len(group))
		spanIDs := make([]string, 0, len(group))

		for _, chunk := range group {
			chunkIDs = append(chunkIDs, chunk.ChunkID)
			spanIDs = append(spanIDs, chunk.SpanID)
		}

		duplicateGroups = append(duplicateGroups, models.JSONMap{
			"normalized_text": normalizedText,
			"chunk_ids":       chunkIDs,
			"span_ids":        spanIDs,
		})
	}

	if len(duplicateGroups) == 0 {
		return nil
	}

	return []models.Warning{
		{
			WarningID: newWarningID(),
			TraceID:   payload.Trace.TraceID,
			SpanID:    nil,
			Type:      TypeDuplicateChunks,
			Severity:  SeverityWarning,
			Message:   "Retrieved chunks contain duplicate text.",
			Details: models.JSONMap{
				"rule":             TypeDuplicateChunks,
				"duplicate_groups": duplicateGroups,
				"reason":           "multiple retrieved chunks have identical normalized text",
			},
			CreatedAt: time.Now().UTC().Format(time.RFC3339Nano),
		},
	}
}

func (e *Engine) detectConflictingChunks(payload models.TracePayload) []models.Warning {
	chunks := extractRetrievedChunks(payload.Spans)
	if len(chunks) < 2 {
		return nil
	}

	// refund window value -> source chunk ids
	refundWindows := map[string][]string{}

	for _, chunk := range chunks {
		text := strings.TrimSpace(chunk.Text)
		if text == "" {
			continue
		}

		days := extractRefundWindowDays(text)
		for _, day := range days {
			refundWindows[day] = append(refundWindows[day], chunk.ChunkID)
		}
	}

	if len(refundWindows) < 2 {
		return nil
	}

	values := make([]string, 0, len(refundWindows))
	for value := range refundWindows {
		values = append(values, value)
	}
	sort.Strings(values)

	message := fmt.Sprintf(
		"Retrieved chunks contain conflicting refund windows: %s days.",
		strings.Join(values, " vs "),
	)

	return []models.Warning{
		{
			WarningID: newWarningID(),
			TraceID:   payload.Trace.TraceID,
			SpanID:    nil,
			Type:      TypeConflictingChunks,
			Severity:  SeverityWarning,
			Message:   message,
			Details: models.JSONMap{
				"detected_values": values,
				"source_chunks":   refundWindows,
				"rule":            TypeConflictingChunks,
			},
			CreatedAt: time.Now().UTC().Format(time.RFC3339Nano),
		},
	}
}

func (e *Engine) detectAnswerNotGrounded(payload models.TracePayload) []models.Warning {
	answer, llmSpanID := extractFinalAnswer(payload)
	answer = strings.TrimSpace(answer)

	if answer == "" {
		return nil
	}

	if containsUncertaintyPhrase(answer) {
		return nil
	}

	chunks := extractRetrievedChunks(payload.Spans)

	// Case 1:
	// The model gave a concrete answer even though retrieval returned no chunks.
	if len(chunks) == 0 {
		return []models.Warning{
			{
				WarningID: newWarningID(),
				TraceID:   payload.Trace.TraceID,
				SpanID:    llmSpanID,
				Type:      TypeAnswerNotGrounded,
				Severity:  SeverityWarning,
				Message:   "Answer may not be grounded because no retrieved chunks were available.",
				Details: models.JSONMap{
					"rule":   TypeAnswerNotGrounded,
					"answer": answer,
					"reason": "final answer was produced without retrieved chunks",
				},
				CreatedAt: time.Now().UTC().Format(time.RFC3339Nano),
			},
		}
	}

	// Case 2:
	// Simplified MVP grounding check:
	// If the answer contains concrete refund-window day values that do not
	// appear in retrieved chunks, flag it.
	answerDays := extractRefundWindowDays(answer)
	if len(answerDays) == 0 {
		return nil
	}

	contextDays := map[string]bool{}
	for _, chunk := range chunks {
		for _, day := range extractRefundWindowDays(chunk.Text) {
			contextDays[day] = true
		}
	}

	unsupportedDays := make([]string, 0)
	for _, day := range answerDays {
		if !contextDays[day] {
			unsupportedDays = append(unsupportedDays, day)
		}
	}

	if len(unsupportedDays) == 0 {
		return nil
	}

	sort.Strings(unsupportedDays)

	return []models.Warning{
		{
			WarningID: newWarningID(),
			TraceID:   payload.Trace.TraceID,
			SpanID:    llmSpanID,
			Type:      TypeAnswerNotGrounded,
			Severity:  SeverityWarning,
			Message:   "Answer contains claims not found in retrieved chunks.",
			Details: models.JSONMap{
				"rule":             TypeAnswerNotGrounded,
				"answer":           answer,
				"unsupported_days": unsupportedDays,
				"reason":           "answer contains day values that do not appear in retrieved chunks",
			},
			CreatedAt: time.Now().UTC().Format(time.RFC3339Nano),
		},
	}
}

type retrievedChunk struct {
	ChunkID  string         `json:"chunk_id"`
	ID       string         `json:"id"`
	Text     string         `json:"text"`
	Content  string         `json:"content"`
	Score    *float64       `json:"score"`
	Metadata models.JSONMap `json:"metadata"`

	SpanID   string
	SpanName string
}

func extractRetrievedChunks(spans []models.Span) []retrievedChunk {
	result := make([]retrievedChunk, 0)

	for _, span := range spans {
		if span.Type != "retrieval" {
			continue
		}

		result = append(result, extractRetrievedChunksFromSpan(span)...)
	}

	return result
}

func extractRetrievedChunksFromSpan(span models.Span) []retrievedChunk {
	result := make([]retrievedChunk, 0)

	result = append(result, chunksFromMap(span.Output)...)
	result = append(result, chunksFromMap(span.Metadata)...)

	normalizeChunks(result)

	for i := range result {
		result[i].SpanID = span.SpanID
		result[i].SpanName = span.Name
	}

	return result
}

func chunksFromMap(value models.JSONMap) []retrievedChunk {
	if value == nil {
		return nil
	}

	keys := []string{
		"retrieved_chunks",
		"chunks",
		"documents",
		"contexts",
	}

	for _, key := range keys {
		raw, ok := value[key]
		if !ok {
			continue
		}

		chunks := parseChunks(raw)
		if len(chunks) > 0 {
			return chunks
		}
	}

	return nil
}

func parseChunks(raw any) []retrievedChunk {
	data, err := json.Marshal(raw)
	if err != nil {
		return nil
	}

	var chunks []retrievedChunk
	if err := json.Unmarshal(data, &chunks); err == nil {
		normalizeChunks(chunks)
		return chunks
	}

	// Fallback for simple []string contexts.
	var texts []string
	if err := json.Unmarshal(data, &texts); err == nil {
		result := make([]retrievedChunk, 0, len(texts))
		for i, text := range texts {
			result = append(result, retrievedChunk{
				ChunkID: fmt.Sprintf("chunk_%d", i+1),
				Text:    text,
			})
		}
		return result
	}

	return nil
}

func normalizeChunks(chunks []retrievedChunk) {
	for i := range chunks {
		if chunks[i].ChunkID == "" {
			chunks[i].ChunkID = chunks[i].ID
		}

		if chunks[i].ChunkID == "" {
			chunks[i].ChunkID = fmt.Sprintf("chunk_%d", i+1)
		}

		if chunks[i].Text == "" {
			chunks[i].Text = chunks[i].Content
		}
	}
}

func getLowScoreThreshold(span models.Span) float64 {
	if span.Metadata == nil {
		return DefaultLowScoreThreshold
	}

	raw, ok := span.Metadata["low_score_threshold"]
	if !ok {
		return DefaultLowScoreThreshold
	}

	switch value := raw.(type) {
	case float64:
		return value
	case float32:
		return float64(value)
	case int:
		return float64(value)
	default:
		return DefaultLowScoreThreshold
	}
}

func normalizeChunkText(text string) string {
	text = strings.ToLower(strings.TrimSpace(text))
	if text == "" {
		return ""
	}

	fields := strings.Fields(text)
	return strings.Join(fields, " ")
}

var refundWindowRegex = regexp.MustCompile(`(?i)\b(\d{1,3})\s*[- ]?\s*days?\b`)

func extractRefundWindowDays(text string) []string {
	matches := refundWindowRegex.FindAllStringSubmatch(text, -1)

	seen := map[string]bool{}
	result := make([]string, 0)

	for _, match := range matches {
		if len(match) < 2 {
			continue
		}

		value := match[1]
		if seen[value] {
			continue
		}

		seen[value] = true
		result = append(result, value)
	}

	sort.Strings(result)

	return result
}

func extractFinalAnswer(payload models.TracePayload) (string, *string) {
	if payload.Trace.Output != nil {
		if answer := stringFromMap(payload.Trace.Output, "answer"); answer != "" {
			return answer, nil
		}

		if response := stringFromMap(payload.Trace.Output, "response"); response != "" {
			return response, nil
		}
	}

	// Prefer the last LLM span output.
	for i := len(payload.Spans) - 1; i >= 0; i-- {
		span := payload.Spans[i]
		if span.Type != "llm" {
			continue
		}

		if span.Output == nil {
			continue
		}

		spanID := span.SpanID

		if answer := stringFromMap(span.Output, "answer"); answer != "" {
			return answer, &spanID
		}

		if response := stringFromMap(span.Output, "response"); response != "" {
			return response, &spanID
		}
	}

	return "", nil
}

func stringFromMap(value models.JSONMap, key string) string {
	if value == nil {
		return ""
	}

	raw, ok := value[key]
	if !ok {
		return ""
	}

	text, ok := raw.(string)
	if !ok {
		return ""
	}

	return text
}

func containsUncertaintyPhrase(answer string) bool {
	normalized := strings.ToLower(answer)

	phrases := []string{
		"i could not find",
		"not enough information",
		"insufficient information",
		"i don't know",
		"cannot determine",
		"unable to determine",
		"no information",
	}

	for _, phrase := range phrases {
		if strings.Contains(normalized, phrase) {
			return true
		}
	}

	return false
}

func newWarningID() string {
	buffer := make([]byte, 8)

	if _, err := rand.Read(buffer); err != nil {
		return fmt.Sprintf("warning_%d", time.Now().UnixNano())
	}

	return "warning_" + hex.EncodeToString(buffer)
}
