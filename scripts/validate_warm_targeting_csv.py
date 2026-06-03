#!/usr/bin/env python3
"""Validate agency targeting CSV before launch — flags REPLACE: placeholders."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DEFAULT = REPO / "docs/commercial/operations/targeting/agency_accounts_seed.csv"


def _stdout_utf8() -> None:
    out = getattr(sys.stdout, "reconfigure", None)
    if callable(out):
        try:
            out(encoding="utf-8")
        except Exception:
            pass


def main() -> int:
    _stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--csv", default=str(DEFAULT))
    p.add_argument("--max-replace-top", type=int, default=0, help="Max REPLACE rows allowed in top N active targets")
    p.add_argument("--top-n", type=int, default=10)
    args = p.parse_args()

    path = Path(args.csv)
    if not path.is_file():
        print(f"MISSING: {path}", file=sys.stderr)
        return 2

    rows = list(csv.DictReader(path.open(encoding="utf-8", newline="")))
    active = [r for r in rows if (r.get("status") or "") not in {"closed_lost", "closed_won"}]
    replace_rows = [r for r in active if "REPLACE:" in (r.get("company") or "") or "REPLACE:" in (r.get("contact") or "")]
    top = active[: args.top_n]
    replace_in_top = [r for r in top if r in replace_rows]

    print(f"rows_total={len(rows)} active={len(active)} replace_active={len(replace_rows)}")
    print(f"replace_in_top_{args.top_n}={len(replace_in_top)}")

    if replace_in_top:
        print("\nTop REPLACE rows (fill before launch):")
        for r in replace_in_top[:10]:
            print(f"  - {r.get('company')} / {r.get('contact')}")

    if len(replace_in_top) > args.max_replace_top:
        print("\nWARM_CSV_VALIDATION=FAIL", file=sys.stderr)
        print("Edit docs/commercial/operations/targeting/agency_accounts_seed.csv", file=sys.stderr)
        print("Then: python scripts/sync_war_room_targets_api.py", file=sys.stderr)
        return 1

    print("\nWARM_CSV_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
