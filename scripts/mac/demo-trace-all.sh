#!/usr/bin/env bash
set -euo pipefail

echo "SledTrace demo: generating local RAG traces..."
echo "Collector: http://localhost:4319"
echo

export SLEDTRACE_COLLECTOR_URL="http://localhost:4319"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
sdk_python_dir="$repo_root/sdk/python"

cd "$sdk_python_dir"
python -m examples.local_rag_demo.run_demo trace-all

echo
echo "Done."
echo "Open the SledTrace dashboard and inspect the generated traces."