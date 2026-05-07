#!/usr/bin/env python3
"""Wave 6 Phase 8 — demo outcome logger.

Append-only JSONL at docs/wave6/live/demo_outcomes.jsonl (gitignored).

Hard rules:
- Local-only (gitignored)
- Auto-redact email + phone from notes
- `paid` outcome requires evidence_note >= 5 chars
- `pilot_requested` is NOT revenue
- No PII in committed files
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

LIVE_DIR = Path("docs/wave6/live")
LIVE_PATH = LIVE_DIR / "demo_outcomes.jsonl"

VALID_OUTCOMES = {
    "interested", "not_now", "pilot_requested", "paid", "follow_up",
}

VALID_SECTORS = {
    "real_estate", "agencies", "services", "consulting",
    "training", "construction", "hospitality", "logistics", "other",
}

_EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
_PHONE_RE = re.compile(r"\+?\d[\d\s().-]{6,}\d")


def redact(text: str) -> str:
    if not text:
        return text
    text = _EMAIL_RE.sub("[EMAIL]", text)
    text = _PHONE_RE.sub("[PHONE]", text)
    return text


def main() -> int:
    p = argparse.ArgumentParser(description="Wave 6 demo outcome logger")
    p.add_argument("--prospect-handle", required=True)
    p.add_argument("--sector", required=True)
    p.add_argument("--outcome", required=True, choices=sorted(VALID_OUTCOMES))
    p.add_argument("--next-action", required=True)
    p.add_argument("--notes", default="")
    p.add_argument("--evidence-note", default="")
    p.add_argument("--out-path", default=str(LIVE_PATH))
    args = p.parse_args()

    if args.sector not in VALID_SECTORS:
        print(f"REFUSING: sector must be one of {sorted(VALID_SECTORS)}", file=sys.stderr)
        return 1

    if args.outcome == "paid":
        if len(args.evidence_note.strip()) < 5:
            print(
                "REFUSING: outcome=paid requires --evidence-note (>=5 chars)",
                file=sys.stderr,
            )
            return 1

    record = {
        "at": datetime.now(timezone.utc).isoformat(),
        "prospect_handle": args.prospect_handle,
        "sector": args.sector,
        "outcome": args.outcome,
        "next_action": redact(args.next_action),
        "notes": redact(args.notes),
        "evidence_note": redact(args.evidence_note) if args.outcome == "paid" else "",
        "is_revenue": args.outcome == "paid",
        "schema": "wave6_demo_outcome_v1",
    }

    out = Path(args.out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"OK: appended to {out}")
    print(f"  outcome: {record['outcome']}")
    print(f"  is_revenue: {record['is_revenue']}")
    if args.outcome == "pilot_requested":
        print(f"  NOTE: pilot_requested is NOT revenue — wait for payment_confirmed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
