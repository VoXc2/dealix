#!/usr/bin/env python3
"""Deprecated — use expand_social_queue_12w.py --cycle-weeks 20|24."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    py = sys.executable
    print("NOTE: expand_social_queue_16w is deprecated; delegating to expand_social_queue_12w --cycle-weeks 20")
    return subprocess.call(
        [py, str(ROOT / "scripts/expand_social_queue_12w.py"), "--cycle-weeks", "20"],
        cwd=ROOT,
    )


if __name__ == "__main__":
    raise SystemExit(main())
