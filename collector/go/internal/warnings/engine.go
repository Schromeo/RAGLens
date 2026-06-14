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

	SeverityInfo    = "info"
	SeverityWarning = "warning"
	SeverityError   = "error"
)

type Engine struct{}

func NewEngine() *Engine {
	return &Engine{}
}

func (e *Engine) Generate(payload models.TracePayload) []models.Warning {
	result := make([]models.Warning, 0)

	result = append(result, e.detectConflictingChunks(payload)...)

	return result
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

type retrievedChunk struct {
	ChunkID  string         `json:"chunk_id"`
	ID       string         `json:"id"`
	Text     string         `json:"text"`
	Content  string         `json:"content"`
	Score    float64        `json:"score"`
	Metadata models.JSONMap `json:"metadata"`
}

func extractRetrievedChunks(spans []models.Span) []retrievedChunk {
	result := make([]retrievedChunk, 0)

	for _, span := range spans {
		if span.Type != "retrieval" {
			continue
		}

		result = append(result, chunksFromMap(span.Output)...)
		result = append(result, chunksFromMap(span.Metadata)...)
	}

	normalizeChunks(result)

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
	if err := json.Unmarshal(data, &chunks); err != nil {
		return nil
	}

	normalizeChunks(chunks)

	return chunks
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

func newWarningID() string {
	buffer := make([]byte, 8)

	if _, err := rand.Read(buffer); err != nil {
		return fmt.Sprintf("warning_%d", time.Now().UnixNano())
	}

	return "warning_" + hex.EncodeToString(buffer)
}
