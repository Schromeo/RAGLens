#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

COLLECTOR_URL = "http://localhost:4319/health"
DASHBOARD_URL = "http://localhost:5173"
TIMEOUT_SECONDS = 2.0


def check_url(url: str) -> tuple[bool, str]:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8", errors="replace")
            return True, body
    except urllib.error.URLError as exc:
        return False, str(exc)


def main() -> int:
    collector_ok, collector_data = check_url(COLLECTOR_URL)
    dashboard_ok, dashboard_data = check_url(DASHBOARD_URL)

    print("SledTrace local checks")
    print("===================")

    if collector_ok:
        print("collector: OK")
        try:
            parsed = json.loads(collector_data)
            status = parsed.get("status", "unknown")
            service = parsed.get("service", "unknown")
            print(f"  health: service={service}, status={status}")
        except json.JSONDecodeError:
            print("  health: unexpected non-JSON response")
    else:
        print("collector: FAILED")
        print(f"  reason: {collector_data}")
        print("  next: run 'docker compose up --build' or 'python scripts/start-sledtrace.py'")

    if dashboard_ok:
        print("dashboard: OK")
    else:
        print("dashboard: FAILED")
        print(f"  reason: {dashboard_data}")
        print("  next: confirm dashboard is running at http://localhost:5173")

    if collector_ok and dashboard_ok:
        print("\nnext: cd sdk/python ; python -m examples.reference_rag_app.run all")
        return 0

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
