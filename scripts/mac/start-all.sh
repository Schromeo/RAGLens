#!/usr/bin/env bash
set -euo pipefail

echo "Starting SledTrace collector and dashboard..."
echo

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cleanup() {
  if [[ -n "${collector_pid:-}" ]] && kill -0 "$collector_pid" 2>/dev/null; then
    kill "$collector_pid" 2>/dev/null || true
  fi
}

trap cleanup EXIT INT TERM

bash "$script_dir/start-collector.sh" &
collector_pid=$!

sleep 2

bash "$script_dir/start-dashboard.sh"
