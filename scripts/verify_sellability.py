#!/usr/bin/env python3
"""Verify sellability policy and readiness matrix documentation exist."""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]

REQUIRED = (
    "docs/company/SELLABILITY_POLICY.md",
    "docs/company/SERVICE_READINESS_MATRIX.md",
    "docs/company/SERVICE_REGISTRY.md",
)


def main() -> int:
    missing = [p for p in REQUIRED if not (REPO / p).is_file()]
    for m in missing:
        print(f"missing_sellability:{m}", file=sys.stderr)
    ok = not missing
    print(f"SELLABILITY_DOCS_PASS={'true' if ok else 'false'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
