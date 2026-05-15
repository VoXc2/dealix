#!/usr/bin/env python3
"""Pipeline tracker update helper.

Logs a status change to docs/ops/pipeline_tracker.csv keyed by lead id.
Single-source-of-truth for outreach state — avoids stale spreadsheets.

Usage:
  python scripts/pipeline_tracker_update.py sent --id 1 --channel WhatsApp
  python scripts/pipeline_tracker_update.py reply --id 1 --status interested
  python scripts/pipeline_tracker_update.py demo --id 1 --at 2026-05-13T15:00:00
  python scripts/pipeline_tracker_update.py paid --id 1 --plan growth --revenue 2999
  python scripts/pipeline_tracker_update.py list
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import sys
from pathlib import Path

TRACKER = Path(__file__).resolve().parent.parent / "docs" / "ops" / "pipeline_tracker.csv"


def _load() -> tuple[list[str], list[dict[str, str]]]:
    with TRACKER.open(encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fields = list(reader.fieldnames or [])
        rows = [dict(r) for r in reader]
    return fields, rows


def _save(fields: list[str], rows: list[dict[str, str]]) -> None:
    with TRACKER.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def _now() -> str:
    return dt.datetime.now(dt.UTC).isoformat(timespec="seconds")


def _find(rows: list[dict[str, str]], lead_id: str) -> dict[str, str]:
    for r in rows:
        if r["id"] == lead_id:
            return r
    raise SystemExit(f"lead id={lead_id!r} not found in tracker")


def cmd_sent(args: argparse.Namespace) -> None:
    fields, rows = _load()
    r = _find(rows, args.id)
    r["sent_at"] = args.at or _now()
    r["channel"] = args.channel or r.get("channel", "")
    r["reply_status"] = r.get("reply_status") or "pending"
    _save(fields, rows)
    print(f"OK: lead {args.id} marked sent at {r['sent_at']} via {r['channel']}")


def cmd_reply(args: argparse.Namespace) -> None:
    fields, rows = _load()
    r = _find(rows, args.id)
    r["reply_status"] = args.status
    if args.note:
        r["notes"] = (r.get("notes") or "") + f" | reply: {args.note}"
    _save(fields, rows)
    print(f"OK: lead {args.id} reply_status={args.status}")


def cmd_demo(args: argparse.Namespace) -> None:
    fields, rows = _load()
    r = _find(rows, args.id)
    r["demo_booked_at"] = args.at or _now()
    r["reply_status"] = "demo_booked"
    _save(fields, rows)
    print(f"OK: lead {args.id} demo booked at {r['demo_booked_at']}")


def cmd_paid(args: argparse.Namespace) -> None:
    fields, rows = _load()
    r = _find(rows, args.id)
    r["plan"] = args.plan
    r["payment_status"] = "paid"
    r["revenue_sar"] = str(args.revenue)
    _save(fields, rows)
    print(f"OK: lead {args.id} PAID — plan={args.plan} revenue={args.revenue} SAR 🎉")


def cmd_list(_args: argparse.Namespace) -> None:
    _fields, rows = _load()
    width = max(len(r["lead_name"]) for r in rows)
    print(f"{'id':<3}  {'name':<{width}}  {'company':<25}  {'status':<14}  {'sent':<20}")
    print("-" * (5 + width + 28 + 16 + 20))
    for r in rows:
        sent = (r.get("sent_at") or "—")[:19]
        status = r.get("reply_status") or "—"
        print(f"{r['id']:<3}  {r['lead_name']:<{width}}  {r['company']:<25}  {status:<14}  {sent:<20}")
    sent_count = sum(1 for r in rows if r.get("sent_at"))
    replied = sum(1 for r in rows if r.get("reply_status") and r["reply_status"] not in ("pending", ""))
    demos = sum(1 for r in rows if r.get("demo_booked_at"))
    paid = sum(1 for r in rows if r.get("payment_status") == "paid")
    revenue = sum(int(r.get("revenue_sar") or 0) for r in rows)
    print()
    print(f"Summary: {len(rows)} total · {sent_count} sent · {replied} replied · {demos} demos · {paid} paid · {revenue} SAR revenue")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("sent")
    s.add_argument("--id", required=True)
    s.add_argument("--channel", help="WhatsApp / LinkedIn / Twitter / Email")
    s.add_argument("--at", help="ISO timestamp (default: now UTC)")
    s.set_defaults(func=cmd_sent)

    s = sub.add_parser("reply")
    s.add_argument("--id", required=True)
    s.add_argument("--status", required=True,
                   help="interested / no_response / declined / demo_booked")
    s.add_argument("--note")
    s.set_defaults(func=cmd_reply)

    s = sub.add_parser("demo")
    s.add_argument("--id", required=True)
    s.add_argument("--at", help="ISO timestamp of booked demo")
    s.set_defaults(func=cmd_demo)

    s = sub.add_parser("paid")
    s.add_argument("--id", required=True)
    s.add_argument("--plan", required=True, choices=["pilot", "starter", "growth", "scale"])
    s.add_argument("--revenue", type=int, required=True, help="SAR amount")
    s.set_defaults(func=cmd_paid)

    s = sub.add_parser("list")
    s.set_defaults(func=cmd_list)

    args = p.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
