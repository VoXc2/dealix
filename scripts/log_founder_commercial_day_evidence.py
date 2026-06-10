#!/usr/bin/env python3
"""Append operating evidence row after founder commercial day if none logged today."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.evidence_append import log_founder_commercial_day_if_needed  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--verdict", default="PASS")
    args = p.parse_args()
    blob = log_founder_commercial_day_if_needed(verdict=args.verdict, dry_run=args.dry_run)
    if blob.get("appended"):
        print(f"EVIDENCE: appended scope_requested · {blob['row'].get('event_date')}")
    else:
        print(f"EVIDENCE: {blob.get('reason')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
