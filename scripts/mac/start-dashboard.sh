#!/usr/bin/env bash
set -euo pipefail

echo "Starting RAGLens dashboard..."
echo

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
dashboard_dir="$repo_root/dashboard/web"

if [[ ! -d "$dashboard_dir" ]]; then
  echo "Dashboard directory not found: $dashboard_dir" >&2
  exit 1
fi

cd "$dashboard_dir"

if [[ ! -d "node_modules" ]]; then
  echo "node_modules not found."
  echo "Run npm install in the dashboard directory first:"
  echo "  cd dashboard/web"
  echo "  npm install"
  exit 1
fi

npm run dev