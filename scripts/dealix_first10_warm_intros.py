#!/usr/bin/env python3
"""Generate a placeholder warm-intros board (no PII). Writes under docs/revenue/live/ (gitignored)."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT_DIR = REPO / "docs" / "revenue" / "live"
BOARD = OUT_DIR / "first10_warm_intros.json"
CHECKLIST = OUT_DIR / "first10_warm_intros.md"

def build_slots() -> list[dict]:
    slots = []
    for i in range(1, 11):
        slots.append(
            {
                "slot_id": f"slot_{i:02d}",
                "segment": "saudi_b2b_agency_placeholder",
                "relationship_strength": "unknown",
                "pain_hypothesis": "[fill after research]",
                "message_variant": "A" if i % 2 == 1 else "B",
                "status": "not_selected",
                "consent_status": "unknown",
                "next_action": "Pick relationship + paste one fact from their last 3 posts",
                "last_touch_date": "",
                "proof_event_id": "",
                "notes_placeholder": "",
            }
        )
    return slots


def main() -> int:
    p = argparse.ArgumentParser(description="Warm intro board generator (placeholders only).")
    p.add_argument("--dry-run", action="store_true", help="print JSON to stdout only")
    args = p.parse_args()
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "guardrails": {
            "no_cold_whatsapp": True,
            "manual_send_only": True,
            "no_pii_in_repo": True,
        },
        "slots": build_slots(),
    }
    if args.dry_run:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    BOARD.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    lines = [
        "# First 10 warm intros — checklist",
        "",
        "Fill names **outside** the repo (Notion/Sheet). This file is gitignored if under `docs/revenue/live/`.",
        "",
        "## Slots",
    ]
    for s in payload["slots"]:
        lines.append(f"- [ ] `{s['slot_id']}` — {s['next_action']}")
    CHECKLIST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"OK: wrote {BOARD} and {CHECKLIST}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
