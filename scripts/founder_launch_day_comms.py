#!/usr/bin/env python3
"""Print founder soft-launch comms checklist."""

from __future__ import annotations

import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
DOC = REPO / "docs" / "commercial" / "operations" / "FOUNDER_LAUNCH_DAY_COMMS_AR.md"


def main() -> int:
    print(DOC.read_text(encoding="utf-8") if DOC.is_file() else f"Missing {DOC}")
    print("\n--- QA URLs ---")
    for path in ("/ar", "/ar/dealix-diagnostic", "/ar/risk-score", "/ar/proof-pack", "/ar/learn", "/ar/partners"):
        print(f"  https://dealix.me{path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
