package main

import (
	"log"
	"net/http"
	"os"

	"raglens-collector/internal/api"
	"raglens-collector/internal/storage"
)

func main() {
	addr := getEnv("RAGLENS_COLLECTOR_ADDR", ":4319")
	dbPath := getEnv("RAGLENS_DB_PATH", "raglens.db")

	store, err := storage.NewStore(dbPath)
	if err != nil {
		log.Fatalf("failed to initialize storage: %v", err)
	}
	defer store.Close()

	server := api.NewServer(store)

	log.Printf("RAGLens collector listening on %s", addr)
	log.Printf("SQLite database: %s", dbPath)

	if err := http.ListenAndServe(addr, server.Routes()); err != nil {
		log.Fatalf("collector stopped: %v", err)
	}
}

func getEnv(key string, fallback string) string {
	value := os.Getenv(key)
	if value == "" {
		return fallback
	}

	return value
}
