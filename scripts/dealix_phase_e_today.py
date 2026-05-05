#!/usr/bin/env python3
"""V11 — Phase E "today" checklist + next-best founder action.

Read-only. Prints a bilingual snapshot of:
  - Today's date + KSA local time
  - Hard-gates status (must all be blocked)
  - First-3 board status (from docs/phase-e/live/ if present)
  - Today's checklist (from the canonical daily founder loop)
  - Next-best founder action

Never sends a message. Never charges. Never writes to a customer's
data. Exits 0 always — this is diagnostics, not a CI gate.

Usage:
    python scripts/dealix_phase_e_today.py
    python scripts/dealix_phase_e_today.py --json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

# KSA is UTC+3
_KSA = timezone(timedelta(hours=3))


_DAILY_CHECKLIST = (
    {
        "time_ksa": "08:30",
        "task_ar": "افحص /health + dealix_status + dealix_phase_e_today",
        "task_en": "Check /health + dealix_status + dealix_phase_e_today",
    },
    {
        "time_ksa": "10:00",
        "task_ar": "أرسل warm intros يدوياً (من قالب 02_FIRST_10_WARM_MESSAGES)",
        "task_en": "Send warm intros manually (template 02_FIRST_10_WARM_MESSAGES)",
    },
    {
        "time_ksa": "13:00",
        "task_ar": "جهّز Mini Diagnostic لمن قبل (dealix_diagnostic.py)",
        "task_en": "Prepare Mini Diagnostic for accepted slots (dealix_diagnostic.py)",
    },
    {
        "time_ksa": "16:00",
        "task_ar": "متابعة يدوية للـ Diagnostic بدون رد ≥7 أيام",
        "task_en": "Manual follow-up for Diagnostics with no reply ≥7 days",
    },
    {
        "time_ksa": "18:00",
        "task_ar": "حدّث first-3 board + سجّل أحداث اليوم",
        "task_en": "Update first-3 board + log today's events",
    },
)

_HARD_GATES = (
    "no_live_send",
    "no_live_charge",
    "no_scraping",
    "no_cold_outreach",
    "no_linkedin_automation",
    "no_fake_proof",
)


def _load_first_3_board() -> dict[str, Any]:
    live_dir = REPO_ROOT / "docs" / "phase-e" / "live"
    json_path = live_dir / "FIRST_3_CUSTOMER_BOARD.json"
    if not json_path.exists():
        return {
            "present": False,
            "reason": "Run python scripts/dealix_first3_board.py first",
            "slots": [],
        }
    try:
        data = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return {
            "present": False,
            "reason": f"failed to load: {type(exc).__name__}",
            "slots": [],
        }
    return {"present": True, "slots": data.get("slots", [])}


def _next_best_action(board: dict[str, Any]) -> dict[str, str]:
    """Pick the next best action based on board state.

    Returns a bilingual recommendation. Pure logic — no I/O.
    """
    if not board.get("present"):
        return {
            "action_ar": (
                "ابدأ بإنشاء first-3 board: "
                "python scripts/dealix_first3_board.py"
            ),
            "action_en": (
                "Start by creating the first-3 board: "
                "python scripts/dealix_first3_board.py"
            ),
        }
    slots = board.get("slots", [])
    # Find first slot still ask_for_30m
    for slot in slots:
        if slot.get("next_action") == "ask_for_30m" and slot.get(
            "consent_status"
        ) == "not_yet_asked":
            return {
                "action_ar": (
                    f"اطلب 30 دقيقة من {slot.get('company_name', 'الشركة')} "
                    f"(slot {slot.get('slot_id')})."
                ),
                "action_en": (
                    f"Request a 30-min call with {slot.get('company_name', 'company')} "
                    f"(slot {slot.get('slot_id')})."
                ),
            }
    return {
        "action_ar": "كل الـ 3 slots متابعة — تابع حسب القائمة اليومية.",
        "action_en": "All 3 slots in motion — follow daily checklist.",
    }


def build_today_snapshot() -> dict[str, Any]:
    now_utc = datetime.now(UTC)
    now_ksa = now_utc.astimezone(_KSA)
    board = _load_first_3_board()
    return {
        "schema_version": 1,
        "generated_at_utc": now_utc.isoformat(),
        "ksa_date": now_ksa.date().isoformat(),
        "ksa_time": now_ksa.strftime("%H:%M"),
        "title_ar": f"يوم {now_ksa.date().isoformat()} — Phase E",
        "title_en": f"Day {now_ksa.date().isoformat()} — Phase E",
        "hard_gates": {gate: "BLOCKED" for gate in _HARD_GATES},
        "checklist": list(_DAILY_CHECKLIST),
        "first_3_board": board,
        "next_best_action": _next_best_action(board),
        "rules": [
            "No external send — every message manual + approved.",
            "No live charge — Moyasar test mode or bank transfer.",
            "No customer name in repo without signed permission.",
        ],
    }


def render_text(snapshot: dict[str, Any]) -> str:
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append(f"  {snapshot['title_ar']}")
    lines.append(f"  {snapshot['title_en']}")
    lines.append(f"  KSA time: {snapshot['ksa_time']}")
    lines.append("=" * 60)
    lines.append("")
    lines.append("Hard gates (all must be BLOCKED):")
    for gate, status in snapshot["hard_gates"].items():
        lines.append(f"  - {gate:30s} {status}")
    lines.append("")
    lines.append("Today's checklist (KSA time):")
    for step in snapshot["checklist"]:
        lines.append(f"  {step['time_ksa']}  {step['task_ar']}")
        lines.append(f"          {step['task_en']}")
    lines.append("")
    board = snapshot["first_3_board"]
    if board["present"]:
        lines.append(f"First-3 board: {len(board['slots'])} slots")
        for slot in board["slots"]:
            lines.append(
                f"  Slot {slot.get('slot_id')}: "
                f"diag={slot.get('diagnostic_status')} "
                f"pilot={slot.get('pilot_status')} "
                f"proof={slot.get('proof_status')} "
                f"next={slot.get('next_action')}"
            )
    else:
        lines.append(f"First-3 board: NOT PRESENT — {board.get('reason')}")
    lines.append("")
    nba = snapshot["next_best_action"]
    lines.append("Next best action:")
    lines.append(f"  AR: {nba['action_ar']}")
    lines.append(f"  EN: {nba['action_en']}")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Phase E today — bilingual snapshot")
    parser.add_argument("--json", action="store_true",
                        help="emit JSON instead of human-readable text")
    args = parser.parse_args()
    snapshot = build_today_snapshot()
    if args.json:
        print(json.dumps(snapshot, indent=2, ensure_ascii=False))
    else:
        print(render_text(snapshot))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
