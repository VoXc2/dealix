#!/usr/bin/env python3
"""RX — first-10 warm intros board generator.

Extends V11's `dealix_first3_board.py` to 10 slots for the 14-day
revenue execution playbook. Same hard rules: placeholders only,
docs/phase-e/live/ is gitignored, no real PII.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "phase-e" / "live"


_PLACEHOLDER_FIELDS: dict[str, Any] = {
    "company_name": "Slot-PLACEHOLDER",
    "contact_name": "Contact-PLACEHOLDER",
    "relationship_strength": "warm_intro",
    "segment": "tbd",
    "pain_hypothesis": "tbd",
    "message_variant": "v1_arabic_warm",
    "consent_status": "not_yet_asked",
    "first_message_status": "not_started",
    "diagnostic_status": "not_started",
    "pilot_status": "not_started",
    "proof_status": "not_started",
    "next_action": "ask_for_30m",
    "last_touch_date": "",
    "owner": "founder",
    "notes_placeholder": "",
}


def build_empty_board(slots: int = 10) -> dict[str, Any]:
    out_slots = []
    # Slots A..J (10)
    for i in range(slots):
        letter = chr(ord("A") + i)  # A, B, C, ...
        slot: dict[str, Any] = {"slot_id": letter}
        for k, v in _PLACEHOLDER_FIELDS.items():
            slot[k] = v.replace("PLACEHOLDER", letter) if isinstance(v, str) else v
        out_slots.append(slot)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": f"أوّل {slots} عملاء — Phase E",
        "title_en": f"First {slots} Customers — Phase E",
        "slots_count": slots,
        "rules": [
            "Placeholders only in this file.",
            "Real names + emails stay in the founder's private vault.",
            "Never publish a customer without signed permission.",
            "Manual sends only — no automation.",
        ],
        "slots": out_slots,
        "hard_gates": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_scraping": True,
            "no_cold_outreach": True,
            "no_fake_proof": True,
        },
    }


def render_markdown(board: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append(f"# {board['title_ar']} / {board['title_en']}")
    lines.append("")
    lines.append(f"_Generated: {board['generated_at']}_")
    lines.append("")
    lines.append(
        "| Slot | Company | Segment | Pain | Variant | Consent | Diagnostic | Pilot | Proof | Next |"
    )
    lines.append(
        "|------|---------|---------|------|---------|---------|------------|-------|-------|------|"
    )
    for s in board["slots"]:
        lines.append(
            "| **{slot_id}** | {company_name} | {segment} | {pain_hypothesis} | "
            "{message_variant} | {consent_status} | {diagnostic_status} | "
            "{pilot_status} | {proof_status} | {next_action} |".format(**s)
        )
    lines.append("")
    lines.append("## Rules")
    lines.append("")
    for rule in board["rules"]:
        lines.append(f"- {rule}")
    lines.append("")
    lines.append("## Hard gates (all blocked)")
    lines.append("")
    for k, v in board["hard_gates"].items():
        lines.append(f"- `{k}` = `{v}`")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="RX — generate empty 10-slot warm-intros board"
    )
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR,
                        help="default: docs/phase-e/live/ (gitignored)")
    parser.add_argument("--slots", type=int, default=10,
                        help="number of slots (default 10)")
    parser.add_argument("--dry-run", action="store_true",
                        help="print to stdout instead of writing files")
    args = parser.parse_args()

    board = build_empty_board(slots=args.slots)
    md = render_markdown(board)
    js = json.dumps(board, indent=2, ensure_ascii=False)

    if args.dry_run:
        print("=== Markdown ===")
        print(md)
        print("=== JSON ===")
        print(js)
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    md_path = args.output_dir / "FIRST_10_CUSTOMER_BOARD.md"
    js_path = args.output_dir / "FIRST_10_CUSTOMER_BOARD.json"
    md_path.write_text(md, encoding="utf-8")
    js_path.write_text(js, encoding="utf-8")

    print(f"Wrote: {md_path}")
    print(f"Wrote: {js_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
