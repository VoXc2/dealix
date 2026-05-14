#!/usr/bin/env python3
"""Verify core quality documentation exists for scored delivery."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/quality/OUTPUT_QA_SCORECARD.md",
    "docs/quality/QUALITY_REVIEW_BOARD.md",
    "docs/quality/RED_TEAM_SCENARIOS.md",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_quality_doc:{m}", file=sys.stderr)
    ok = not missing
    print(f"QUALITY_SCORE_DOCS_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
