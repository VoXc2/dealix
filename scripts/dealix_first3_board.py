#!/usr/bin/env python3
"""V11 — First-3 customer board generator.

Generates an empty 3-slot board (Markdown + JSON) at
``docs/phase-e/live/FIRST_3_CUSTOMER_BOARD.{md,json}`` with placeholder
data. NEVER writes a real customer name.

Usage:
    python scripts/dealix_first3_board.py
    python scripts/dealix_first3_board.py --output-dir /tmp/board
    python scripts/dealix_first3_board.py --dry-run          # print to stdout

Exit code is always 0. This is a setup helper, not a CI gate. The
``docs/phase-e/live/`` path is intentionally gitignored so real
customer state never lands in the repo.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

# Make the repo importable when run as a script.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT_DIR = REPO_ROOT / "docs" / "phase-e" / "live"


_PLACEHOLDER_FIELDS: dict[str, Any] = {
    "company_name": "Slot-PLACEHOLDER",
    "contact_name": "Contact-PLACEHOLDER",
    "relationship": "warm_intro",
    "sector": "tbd",
    "region": "tbd",
    "source": "warm_intro",
    "consent_status": "not_yet_asked",
    "first_message_status": "not_started",
    "diagnostic_status": "not_started",
    "pilot_status": "not_started",
    "proof_status": "not_started",
    "next_action": "ask_for_30m",
    "owner": "founder",
    "notes": "",
}


def build_empty_board() -> dict[str, Any]:
    """Return the canonical 3-slot empty board structure."""
    slots = []
    for letter in ("A", "B", "C"):
        slot: dict[str, Any] = {"slot_id": letter}
        for k, v in _PLACEHOLDER_FIELDS.items():
            slot[k] = (
                v.replace("PLACEHOLDER", letter)
                if isinstance(v, str)
                else v
            )
        slots.append(slot)
    return {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "title_ar": "أول 3 عملاء — Phase E",
        "title_en": "First 3 Customers — Phase E",
        "rules": [
            "Use placeholders only in this file.",
            "Real names + emails stay in the founder's private vault.",
            "Never publish a customer without signed permission.",
        ],
        "slots": slots,
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
        "| Slot | Company | Contact | Relationship | Sector | Region | "
        "Consent | Diagnostic | Pilot | Proof | Next | Owner |"
    )
    lines.append(
        "|------|---------|---------|--------------|--------|--------|"
        "---------|------------|-------|-------|------|-------|"
    )
    for s in board["slots"]:
        lines.append(
            "| **{slot_id}** | {company_name} | {contact_name} | {relationship} | "
            "{sector} | {region} | {consent_status} | {diagnostic_status} | "
            "{pilot_status} | {proof_status} | {next_action} | {owner} |"
            .format(**s)
        )
    lines.append("")
    lines.append("## Hard rules")
    lines.append("")
    for rule in board["rules"]:
        lines.append(f"- {rule}")
    lines.append("")
    lines.append("## Hard gates (all blocked)")
    lines.append("")
    for k, v in board["hard_gates"].items():
        lines.append(f"- `{k}` = `{v}`")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate empty Phase E first-3 customer board."
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Where to write the board (default: docs/phase-e/live/)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print to stdout instead of writing files",
    )
    args = parser.parse_args()

    board = build_empty_board()
    md = render_markdown(board)
    js = json.dumps(board, indent=2, ensure_ascii=False)

    if args.dry_run:
        print("=== Markdown ===")
        print(md)
        print("=== JSON ===")
        print(js)
        return 0

    args.output_dir.mkdir(parents=True, exist_ok=True)
    md_path = args.output_dir / "FIRST_3_CUSTOMER_BOARD.md"
    js_path = args.output_dir / "FIRST_3_CUSTOMER_BOARD.json"
    md_path.write_text(md, encoding="utf-8")
    js_path.write_text(js, encoding="utf-8")

    print(f"Wrote: {md_path}")
    print(f"Wrote: {js_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
