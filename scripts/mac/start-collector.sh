#!/usr/bin/env bash
set -euo pipefail

echo "Starting RAGLens collector..."
echo "Expected URL: http://localhost:4319"
echo

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
collector_dir="$repo_root/collector/go"

if [[ ! -d "$collector_dir" ]]; then
  echo "Collector directory not found: $collector_dir" >&2
  exit 1
fi

cd "$collector_dir"
go run ./cmd/raglens-collector