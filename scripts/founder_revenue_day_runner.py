#!/usr/bin/env python3
"""Founder Revenue Day — AEO week, War Room summary, evidence reminder, verdict."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.doctrine import format_doctrine_markdown  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

AEO_CALENDAR = REPO_ROOT / "docs/commercial/operations/AEO_CONTENT_CALENDAR_AR.md"
EVIDENCE_CSV = REPO_ROOT / "docs/commercial/operations/evidence_events_tracker.csv"


def aeo_week_number() -> int:
    """Cycle weeks 1–12 from ISO week of year."""
    return (datetime.now(UTC).isocalendar().week % 12) or 12


def parse_aeo_row(week: int) -> dict[str, str] | None:
    if not AEO_CALENDAR.is_file():
        return None
    text = AEO_CALENDAR.read_text(encoding="utf-8")
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) < 4:
            continue
        if parts[0] in ("أسبوع", "-------", "---"):
            continue
        try:
            row_week = int(re.sub(r"[^\d]", "", parts[0]) or "0")
        except ValueError:
            continue
        if row_week == week:
            return {
                "week": parts[0],
                "slug": parts[1] if len(parts) > 1 else "",
                "title_ar": parts[2] if len(parts) > 2 else "",
                "aeo_question": parts[3] if len(parts) > 3 else "",
            }
    return None


def war_room_summary_local() -> dict:
    from dealix.revenue_ops_autopilot.store import get_autopilot_store
    from dealix.revenue_ops_autopilot.war_room import build_daily_summary

    store = get_autopilot_store()
    return build_daily_summary(store.list_leads(limit=600))


def print_war_room(summary: dict) -> None:
    print("## War Room (summary)")
    today = summary.get("today") or {}
    rev = summary.get("revenue") or {}
    print(f"- top_targets: {today.get('top_targets_count', 0)}")
    print(f"- follow_ups_due: {today.get('follow_ups_due', 0)}")
    print(f"- meetings: {rev.get('meetings', 0)} · paid: {rev.get('paid', 0)}")
    for row in (summary.get("top_targets") or [])[:5]:
        name = row.get("company") or row.get("name") or row.get("id") or "—"
        print(f"  · {name} · score={row.get('lead_score')} · status={row.get('status')}")


def main() -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Print plan only; no side effects")
    p.add_argument("--skip-substeps", action="store_true", help="Only AEO + War Room + verdict")
    args = p.parse_args()

    degraded = False

    if args.dry_run:
        print("DRY-RUN · Founder Commercial Day (canonical: run_founder_commercial_day.sh)")
        print("1/6 founder daily brief")
        print("2/6 KPI commercial status")
        print("3/6 war room sync (P0 rotation)")
        print("4/6 commercial digest")
        print("5/6 social queue today")
        print("6/6 AEO + War Room summary + evidence reminder")
        print("FOUNDER_REVENUE_DAY_VERDICT=READY")
        print("FOUNDER_COMMERCIAL_DAY: OK (dry-run)")
        return 0

    print(format_doctrine_markdown())
    print()

    week = aeo_week_number()
    aeo = parse_aeo_row(week)
    print(f"\n## AEO · أسبوع {week}")
    if aeo:
        print(f"- عنوان: {aeo.get('title_ar')}")
        print(f"- slug: {aeo.get('slug')}")
        print(f"- سؤال: {aeo.get('aeo_question')}")
    else:
        print("- (لم يُعثر على صف التقويم — راجع AEO_CONTENT_CALENDAR_AR.md)")
        degraded = True

    try:
        summary = war_room_summary_local()
        print_war_room(summary)
    except Exception as exc:
        print(f"War Room: SKIP ({exc})", file=sys.stderr)
        degraded = True

    print("\n## Evidence")
    print(f"سجّل حدثاً واحداً اليوم: {EVIDENCE_CSV.relative_to(REPO_ROOT)}")
    print("أحداث: message_sent_manual · reply_received · demo_booked · payment_received · proof_pack_delivered")

    verdict = "DEGRADED" if degraded else "READY"
    print(f"\nFOUNDER_REVENUE_DAY_VERDICT={verdict}")
    return 0 if verdict == "READY" else 0  # still exit 0 for operational use


if __name__ == "__main__":
    sys.exit(main())
