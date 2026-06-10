#!/usr/bin/env python3
"""Tag high-priority targets with warm ABM notes (idempotent, no cold channels)."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.paths import AGENCY_TARGETS_CSV
from dealix.commercial_ops.targeting_csv import TARGET_FIELDS

WARM_TAG = "warm_list"


def enrich_warm_notes(*, limit: int = 80, dry_run: bool = False) -> dict[str, int]:
    path = AGENCY_TARGETS_CSV
    with path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    updated = 0
    for row in rows:
        if updated >= limit:
            break
        notes = (row.get("notes") or "").strip()
        low = notes.lower()
        if WARM_TAG in low or "warm" in low or "inbound" in low or "partner" in low:
            continue
        if (row.get("priority") or "").strip() != "high":
            continue
        if (row.get("status") or "").strip() in ("closed_lost", "won"):
            continue
        channel = (row.get("channel") or "").strip()
        if channel in ("cold_whatsapp", "linkedin_auto_send", "scraping"):
            continue
        company = (row.get("company") or "").strip()
        if not company or company.startswith("REPLACE:"):
            continue
        suffix = f"{WARM_TAG}:priority_high"
        row["notes"] = f"{notes} | {suffix}".strip(" |") if notes else suffix
        updated += 1

    if not dry_run and updated:
        with path.open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=TARGET_FIELDS)
            w.writeheader()
            w.writerows(rows)

    return {"rows": len(rows), "warm_tags_added": updated, "dry_run": dry_run}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--limit", type=int, default=80)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    blob = enrich_warm_notes(limit=max(1, args.limit), dry_run=args.dry_run)
    print(f"ENRICH_TARGETING_WARM: {blob}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
