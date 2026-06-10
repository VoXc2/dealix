#!/usr/bin/env python3
"""Founder evening — evidence reminder + optional append (no auto external send)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.evidence_append import (  # noqa: E402
    append_evidence_row,
    evening_reminder_ar,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    p.add_argument(
        "--append",
        action="store_true",
        help="Append one row (requires --event-type and --company)",
    )
    p.add_argument("--event-type", default="message_sent_manual")
    p.add_argument("--company", default="")
    p.add_argument("--notes", default="")
    p.add_argument("--motion", default="A")
    p.add_argument("--offer-id", default="ten_lead_audit")
    args = p.parse_args()

    if args.append:
        if not (args.company or "").strip():
            print("FOUNDER_EVENING: FAIL --company required with --append")
            return 1
        row = append_evidence_row(
            event_type=args.event_type,
            company=args.company,
            notes=args.notes,
            motion=args.motion,
            offer_id=args.offer_id,
        )
        blob = {"appended": row, **evening_reminder_ar()}
    else:
        blob = evening_reminder_ar()

    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== founder_evening_evidence ==")
        if "appended" in blob:
            print(f"  appended: {blob['appended'].get('event_type')} · {blob['appended'].get('company')}")
        print(f"  logged_today: {blob.get('logged_today')}")
        print(f"  {blob.get('reminder_ar')}")
        print(f"  tracker: {blob.get('tracker_path')}")

    print(f"FOUNDER_EVENING_VERDICT={'OK' if blob.get('logged_today') else 'ACTION'}")
    return 0 if blob.get("logged_today") else 0


if __name__ == "__main__":
    raise SystemExit(main())
