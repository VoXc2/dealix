#!/usr/bin/env python3
"""Append a row to gtm_conversation_tracker.csv — progress toward GTM blitz targets."""

from __future__ import annotations

import argparse
import csv
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.gtm_blitz_tracker import build_gtm_blitz_snapshot  # noqa: E402
from dealix.commercial_ops.paths import REPO_ROOT  # noqa: E402

CONV_CSV = REPO_ROOT / "docs/commercial/operations/gtm_conversation_tracker.csv"
GTM_BLITZ = REPO_ROOT / "dealix/config/gtm_blitz_90d.yaml"

FIELDNAMES = [
    "date",
    "company",
    "contact",
    "channel",
    "qualified",
    "proposal_sent",
    "meeting_type",
    "meeting_date",
    "notes",
]


def _ensure_csv() -> None:
    CONV_CSV.parent.mkdir(parents=True, exist_ok=True)
    if CONV_CSV.is_file():
        return
    with CONV_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerow(
            {
                "date": "",
                "company": "TEMPLATE_ROW_DELETE_BEFORE_USE",
                "contact": "",
                "channel": "",
                "qualified": "false",
                "proposal_sent": "false",
                "meeting_type": "",
                "meeting_date": "",
                "notes": "template_row",
            }
        )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--company", required=True)
    p.add_argument("--contact", default="")
    p.add_argument("--channel", default="linkedin_manual")
    p.add_argument("--qualified", action="store_true")
    p.add_argument("--proposal-sent", action="store_true")
    p.add_argument("--in-person", action="store_true", help="Mark in_person meeting with --meeting-date")
    p.add_argument("--meeting-date", default="", help="YYYY-MM-DD for in-person meeting")
    p.add_argument("--notes", default="")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    company = args.company.strip()
    if not company or company.upper().startswith("TEMPLATE"):
        print("REFUSE: provide a real company name", file=sys.stderr)
        return 1

    meeting_type = "in_person" if args.in_person else ""
    meeting_date = (args.meeting_date or "").strip()
    if args.in_person and not meeting_date:
        meeting_date = datetime.now(UTC).date().isoformat()

    row = {
        "date": datetime.now(UTC).date().isoformat(),
        "company": company,
        "contact": args.contact.strip(),
        "channel": args.channel.strip(),
        "qualified": "true" if args.qualified else "false",
        "proposal_sent": "true" if args.proposal_sent else "false",
        "meeting_type": meeting_type,
        "meeting_date": meeting_date,
        "notes": args.notes.strip(),
    }

    if args.dry_run:
        print(f"DRY-RUN: {row}")
        return 0

    _ensure_csv()
    with CONV_CSV.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, extrasaction="ignore")
        writer.writerow(row)
    print(f"APPENDED {CONV_CSV.relative_to(REPO_ROOT)}: {company}")

    snap = build_gtm_blitz_snapshot()
    targets = snap.get("targets") or {}
    actuals = snap.get("actuals") or {}
    print(f"\nGTM_BLITZ_VERDICT={snap.get('verdict')} ({snap.get('pct')}%)")
    print(f"  qualified target={targets.get('qualified_conversations')} actual_rows={actuals.get('conversation_rows')}")
    print(f"  config: {GTM_BLITZ.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
