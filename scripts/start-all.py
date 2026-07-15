#!/usr/bin/env python3

from __future__ import annotations

import signal
import subprocess
import sys
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    collector_dir = repo_root / "collector" / "go"
    dashboard_dir = repo_root / "dashboard" / "web"

    if not collector_dir.is_dir():
        print(f"Collector directory not found: {collector_dir}", file=sys.stderr)
        return 1

    if not dashboard_dir.is_dir():
        print(f"Dashboard directory not found: {dashboard_dir}", file=sys.stderr)
        return 1

    print("Starting SledTrace collector and dashboard...")
    print()

    collector_proc = start_process(["go", "run", "./cmd/sledtrace-collector"], collector_dir)
    dashboard_proc = start_process(["npm", "run", "dev"], dashboard_dir, use_shell=sys.platform == "win32")

    procs = [collector_proc, dashboard_proc]

    def shutdown(_signal: int | None = None, _frame: object | None = None) -> None:
        for proc in procs:
            if proc.poll() is None:
                proc.terminate()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        dashboard_exit = dashboard_proc.wait()
        shutdown()
        collector_proc.wait(timeout=10)
        return dashboard_exit
    except subprocess.TimeoutExpired:
        shutdown()
        return dashboard_proc.returncode or 1


def start_process(command: list[str], cwd: Path, use_shell: bool = False) -> subprocess.Popen[str]:
    if use_shell:
        return subprocess.Popen(" ".join(command), cwd=str(cwd), text=True, shell=True)

    return subprocess.Popen(command, cwd=str(cwd), text=True)


if __name__ == "__main__":
    raise SystemExit(main())