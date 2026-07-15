package main

import (
	"log"
	"net/http"
	"os"

	"sledtrace-collector/internal/api"
	"sledtrace-collector/internal/storage"
)

func main() {
	addr := getEnvWithLegacy("SLEDTRACE_COLLECTOR_ADDR", "RAGLENS_COLLECTOR_ADDR", ":4319")
	// Keep the legacy default DB filename so existing local trace data remains visible.
	dbPath := getEnvWithLegacy("SLEDTRACE_DB_PATH", "RAGLENS_DB_PATH", "raglens.db")

	store, err := storage.NewStore(dbPath)
	if err != nil {
		log.Fatalf("failed to initialize storage: %v", err)
	}
	defer store.Close()

	server := api.NewServer(store)

	log.Printf("SledTrace collector listening on %s", addr)
	log.Printf("SQLite database: %s", dbPath)

	if err := http.ListenAndServe(addr, server.Routes()); err != nil {
		log.Fatalf("collector stopped: %v", err)
	}
}

func getEnvWithLegacy(key string, legacyKey string, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}

	if legacyValue := os.Getenv(legacyKey); legacyValue != "" {
		return legacyValue
	}

	return fallback
}
