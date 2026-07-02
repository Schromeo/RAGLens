#!/usr/bin/env python3

from __future__ import annotations

import signal
import subprocess
import sys
import time
from pathlib import Path


COLLECTOR_URL = "http://localhost:4319"
DASHBOARD_HINT_URL = "http://localhost:5173"


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    collector_dir = repo_root / "collector" / "go"
    dashboard_dir = repo_root / "dashboard" / "web"
    dashboard_node_modules = dashboard_dir / "node_modules"

    if not collector_dir.is_dir():
        print(f"Collector directory not found: {collector_dir}", file=sys.stderr)
        return 1

    if not dashboard_dir.is_dir():
        print(f"Dashboard directory not found: {dashboard_dir}", file=sys.stderr)
        return 1

    if not dashboard_node_modules.exists():
        print("If this is your first time running the dashboard, run: cd dashboard/web && npm install")
        print()

    print("Starting collector...")
    collector_proc = start_process(["go", "run", "./cmd/raglens-collector"], collector_dir)

    print("Starting dashboard...")
    dashboard_proc = start_process([npm_command(), "run", "dev"], dashboard_dir)

    print(f"Collector URL: {COLLECTOR_URL}")
    print(f"Dashboard URL is shown by Vite output, usually {DASHBOARD_HINT_URL}")
    print("Press Ctrl+C to stop both services")
    print()

    procs = [collector_proc, dashboard_proc]
    shutting_down = False

    def shutdown() -> None:
        nonlocal shutting_down
        if shutting_down:
            return

        shutting_down = True

        for proc in procs:
            if proc.poll() is None:
                proc.terminate()

        deadline = time.monotonic() + 10.0

        for proc in procs:
            remaining = deadline - time.monotonic()
            if proc.poll() is not None:
                continue

            try:
                proc.wait(timeout=max(0.0, remaining))
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait()

    def handle_signal(_signal: int, _frame: object | None) -> None:
        shutdown()
        raise SystemExit(130)

    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    try:
        while True:
            collector_code = collector_proc.poll()
            if collector_code is not None:
                print(f"Collector exited with code {collector_code}")
                shutdown()
                return collector_code

            dashboard_code = dashboard_proc.poll()
            if dashboard_code is not None:
                print(f"Dashboard exited with code {dashboard_code}")
                shutdown()
                return dashboard_code

            time.sleep(0.2)
    finally:
        shutdown()


def start_process(command: list[str], cwd: Path) -> subprocess.Popen[str]:
    try:
        return subprocess.Popen(command, cwd=str(cwd), text=True)
    except FileNotFoundError as exc:
        print(f"Failed to start command: {' '.join(command)}", file=sys.stderr)
        print(f"Missing executable: {command[0]}", file=sys.stderr)
        raise SystemExit(1) from exc


def npm_command() -> str:
    return "npm.cmd" if sys.platform == "win32" else "npm"


if __name__ == "__main__":
    raise SystemExit(main())