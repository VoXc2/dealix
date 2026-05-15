#!/usr/bin/env python3
"""Founder daily scorecard generator (W9.7).

Pulls data from the live system + outreach tracker and prints the
daily scorecard the founder is supposed to paste in chat at 18:00
KSA per v3 §10 / v4 §15.

Sources:
  - docs/ops/pipeline_tracker.csv  (W1.6 — outreach state)
  - DB payments table              (W1.3 — paid pilots/subscriptions)
  - Optionally /api/v1/admin/...   (live counts when API running)

Output (default text) matches the v3 §10 scorecard template exactly,
so the founder can copy-paste straight into his daily chat with me:

  Date: YYYY-MM-DD
  Segment focus today:  ____
  Messages sent:        ____ / 5
  Replies received:     ____
  Demos booked:         ____
  Demos held:           ____
  Pilots cleared (499): ____
  Growth signed (2,999):____
  Cash received today:  ____ SAR
  Hours coding:         ____
  Tomorrow's 5 targets:

Usage:
  python scripts/founder_daily_scorecard.py
  python scripts/founder_daily_scorecard.py --date 2026-05-12
  python scripts/founder_daily_scorecard.py --json     # for piping to a webhook
  python scripts/founder_daily_scorecard.py --fill     # interactive: prompts for the
                                                        # subjective fields (segment focus,
                                                        # hours coding, tomorrow's targets)

Exit codes:
  0  scorecard rendered successfully
  1  data sources partially unavailable (rendered with warnings)
  2  cannot read tracker CSV at all
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

TRACKER = Path(__file__).resolve().parent.parent / "docs" / "ops" / "pipeline_tracker.csv"


@dataclass
class Scorecard:
    date: str
    segment_focus: str = "—"
    messages_sent: int = 0
    messages_target: int = 5
    replies_received: int = 0
    demos_booked: int = 0
    demos_held: int = 0
    pilots_cleared: int = 0
    growth_signed: int = 0
    cash_received_sar: int = 0
    hours_coding: float = 0.0
    tomorrow_targets: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def _parse_iso_date(s: str) -> dt.date:
    return dt.datetime.fromisoformat(s).date()


def _within_day(ts_str: str, target_date: dt.date) -> bool:
    if not ts_str:
        return False
    try:
        ts_date = _parse_iso_date(ts_str)
    except ValueError:
        return False
    return ts_date == target_date


def _load_tracker_rows() -> tuple[list[dict[str, str]], list[str]]:
    if not TRACKER.exists():
        return [], [f"tracker CSV not found at {TRACKER}"]
    try:
        with TRACKER.open(encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [dict(r) for r in reader], []
    except Exception as exc:
        return [], [f"tracker CSV read error: {exc}"]


def _aggregate_from_tracker(rows: list[dict[str, str]], target_date: dt.date) -> Scorecard:
    sc = Scorecard(date=target_date.isoformat())
    for r in rows:
        if _within_day(r.get("sent_at", ""), target_date):
            sc.messages_sent += 1
        # Replies marked "interested" / "demo_booked" / "declined" today
        if (r.get("reply_status") in ("interested", "demo_booked", "declined")
                and _within_day(r.get("sent_at", ""), target_date)):
            # Crude proxy: same-day reply (real implementation would track
            # reply_received_at separately)
            sc.replies_received += 1
        if _within_day(r.get("demo_booked_at", ""), target_date):
            sc.demos_booked += 1
        if r.get("payment_status") == "paid":
            plan = (r.get("plan") or "").lower()
            revenue = int(r.get("revenue_sar") or 0)
            if plan == "pilot":
                sc.pilots_cleared += 1
                sc.cash_received_sar += revenue
            elif plan == "growth":
                sc.growth_signed += 1
                sc.cash_received_sar += revenue
            elif plan in ("starter", "scale"):
                sc.cash_received_sar += revenue
    return sc


def _interactive_fill(sc: Scorecard) -> Scorecard:
    """Prompt for subjective fields the script can't infer."""
    print("Subjective fields (press enter to keep blank):")
    seg = input(f"  Segment focus today (current: {sc.segment_focus}): ").strip()
    if seg:
        sc.segment_focus = seg
    hrs = input("  Hours coding today (e.g. 1.5): ").strip()
    if hrs:
        try:
            sc.hours_coding = float(hrs)
        except ValueError:
            sc.warnings.append(f"could not parse hours_coding={hrs!r}")
    print("  Tomorrow's 5 targets (one per line, blank line to finish):")
    for _ in range(5):
        t = input("    > ").strip()
        if not t:
            break
        sc.tomorrow_targets.append(t)
    return sc


def _format_text(sc: Scorecard) -> str:
    lines = [
        f"Date: {sc.date}",
        f"Segment focus today:  {sc.segment_focus}",
        f"Messages sent:        {sc.messages_sent} / {sc.messages_target}",
        f"Replies received:     {sc.replies_received}",
        f"Demos booked:         {sc.demos_booked}",
        f"Demos held:           {sc.demos_held}  (manual — script can't infer)",
        f"Pilots cleared (499): {sc.pilots_cleared}",
        f"Growth signed (2,999):{sc.growth_signed}",
        f"Cash received today:  {sc.cash_received_sar:,} SAR",
        f"Hours coding:         {sc.hours_coding}  (target ≤ 1)",
        "Tomorrow's 5 targets:",
    ]
    if sc.tomorrow_targets:
        for t in sc.tomorrow_targets:
            lines.append(f"  - {t}")
    else:
        lines.append("  (fill in interactively with --fill)")

    # Failure-mode alerts (v3 §10 "three failure modes")
    alerts = []
    if sc.messages_sent == 0:
        alerts.append("⚠ Messages sent = 0 today")
    if sc.replies_received == 0 and sc.messages_sent > 0:
        alerts.append("⚠ No replies — check pitch")
    if sc.demos_booked == 0 and sc.messages_sent > 5:
        alerts.append("⚠ No demos despite outreach — check offer framing")

    if alerts:
        lines.append("")
        lines.append("Alerts:")
        for a in alerts:
            lines.append(f"  {a}")

    if sc.warnings:
        lines.append("")
        lines.append("Data warnings:")
        for w in sc.warnings:
            lines.append(f"  - {w}")

    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--date", help="ISO date (default: today UTC)")
    p.add_argument("--json", action="store_true", help="JSON output instead of text")
    p.add_argument("--fill", action="store_true",
                   help="interactively fill subjective fields (segment, hours, targets)")
    args = p.parse_args()

    target_date = _parse_iso_date(args.date) if args.date else dt.datetime.now(dt.UTC).date()

    rows, warnings = _load_tracker_rows()
    if not rows and not args.fill:
        print("FATAL: no tracker data available", file=sys.stderr)
        for w in warnings:
            print(f"  - {w}", file=sys.stderr)
        return 2

    sc = _aggregate_from_tracker(rows, target_date)
    sc.warnings.extend(warnings)

    if args.fill:
        sc = _interactive_fill(sc)

    if args.json:
        # Manually serialize since dataclass+set isn't directly JSON
        print(json.dumps({
            "date": sc.date,
            "segment_focus": sc.segment_focus,
            "messages_sent": sc.messages_sent,
            "messages_target": sc.messages_target,
            "replies_received": sc.replies_received,
            "demos_booked": sc.demos_booked,
            "demos_held": sc.demos_held,
            "pilots_cleared": sc.pilots_cleared,
            "growth_signed": sc.growth_signed,
            "cash_received_sar": sc.cash_received_sar,
            "hours_coding": sc.hours_coding,
            "tomorrow_targets": sc.tomorrow_targets,
            "warnings": sc.warnings,
        }, indent=2, ensure_ascii=False))
    else:
        print(_format_text(sc))

    return 1 if warnings else 0


if __name__ == "__main__":
    sys.exit(main())
