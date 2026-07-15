#!/usr/bin/env python3

from __future__ import annotations

import runpy
import sys
from pathlib import Path


def main() -> int:
    print(
        "DEPRECATED: scripts/start-raglens.py is deprecated and will be removed in a future release. "
        "Use scripts/start-sledtrace.py instead.",
        file=sys.stderr,
    )

    target = Path(__file__).resolve().parent / "start-sledtrace.py"
    runpy.run_path(str(target), run_name="__main__")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
