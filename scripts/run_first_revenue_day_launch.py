#!/usr/bin/env python3
"""Day-0 revenue launch checklist — evidence row + founder day script."""

from __future__ import annotations

import csv
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EVIDENCE = REPO / "docs/commercial/operations/evidence_events_tracker.csv"


def _append_evidence_if_missing() -> None:
    if not EVIDENCE.is_file():
        return
    today = date.today().isoformat()
    rows = list(csv.DictReader(EVIDENCE.open(encoding="utf-8", newline="")))
    if any((r.get("event_date") or "").startswith(today) and "launch_day" in (r.get("notes") or "") for r in rows):
        return
    fieldnames = rows[0].keys() if rows else [
        "event_date",
        "event_type",
        "company",
        "channel",
        "offer_id",
        "amount_sar",
        "evidence_level",
        "notes",
    ]
    new_row = {
        "event_date": today,
        "event_type": "scope_requested",
        "company": "founder_launch_day",
        "channel": "founder_ops",
        "offer_id": "ten_lead_audit",
        "amount_sar": "",
        "evidence_level": "L2",
        "notes": "launch_day — first revenue day orchestrator",
    }
    with EVIDENCE.open("a", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        if not rows:
            w.writeheader()
        w.writerow(new_row)
    print(f"Evidence row appended: {EVIDENCE}")


def main() -> int:
    _append_evidence_if_missing()
    script = REPO / "scripts" / "run_founder_revenue_day.ps1"
    if os.name == "nt" and script.is_file():
        return subprocess.call(["powershell", "-File", str(script)], cwd=str(REPO))
    sh = REPO / "scripts" / "run_founder_revenue_day.sh"
    if sh.is_file():
        return subprocess.call(["bash", str(sh)], cwd=str(REPO))
    print("Founder revenue day script not found", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
