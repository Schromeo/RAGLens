#!/usr/bin/env bash
set -euo pipefail

echo "SledTrace smoke test"
echo "Collector: http://localhost:4319"
echo

export SLEDTRACE_COLLECTOR_URL="http://localhost:4319"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/../.." && pwd)"
sdk_python_dir="$repo_root/sdk/python"

cd "$sdk_python_dir"

echo "Step 1/2: Running warning rules demo..."
python -m examples.warning_rules_demo all

echo
echo "Step 2/2: Running local RAG trace demo..."
python -m examples.local_rag_demo.run_demo trace-all

echo
echo "Smoke test completed."
echo "Now verify traces and warning cards in the dashboard."