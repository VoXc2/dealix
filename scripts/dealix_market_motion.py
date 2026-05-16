#!/usr/bin/env python3
"""CEO Market Motion OS CLI.

Manual-first helper for:
- preparing first-5 personalized outreach drafts,
- logging audited market events,
- reading a compact 7-number scoreboard + board decision.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.sales_os.market_motion import (  # noqa: E402
    MarketEvent,
    MarketMotionEvent,
    append_event,
    build_first5_drafts_from_csv,
    build_scoreboard,
    read_events,
    render_first5_markdown,
)


def _cmd_prepare_first5(args: argparse.Namespace) -> int:
    csv_path = (REPO_ROOT / args.csv).resolve()
    out_path = (REPO_ROOT / args.out).resolve()
    drafts = build_first5_drafts_from_csv(csv_path=csv_path, limit=args.limit)
    if not drafts:
        raise ValueError("warm list has no contacts")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(render_first5_markdown(drafts), encoding="utf-8")
    print(f"OK: wrote first-{len(drafts)} drafts -> {out_path}")
    return 0


def _cmd_log_event(args: argparse.Namespace) -> int:
    ledger_path = (REPO_ROOT / args.ledger).resolve()
    occurred_at = args.occurred_at or datetime.now(UTC).isoformat()
    event = MarketMotionEvent(
        contact_id=args.contact_id.strip(),
        event=MarketEvent(args.event),
        occurred_at=occurred_at,
        source_ref=args.source_ref.strip(),
        note=(args.note or "").strip(),
    )
    append_event(ledger_path=ledger_path, event=event)
    print(f"OK: logged {event.event.value} for {event.contact_id}")
    print(f"ledger: {ledger_path}")
    return 0


def _cmd_status(args: argparse.Namespace) -> int:
    ledger_path = (REPO_ROOT / args.ledger).resolve()
    events = read_events(ledger_path)
    board = build_scoreboard(events)
    payload = {
        "ledger_path": str(ledger_path.relative_to(REPO_ROOT)),
        "events_count": len(events),
        "sent_count": board.sent_count,
        "reply_rate": round(board.reply_rate, 4),
        "meeting_rate": round(board.meeting_rate, 4),
        "l5_count": board.l5_count,
        "l6_count": board.l6_count,
        "invoice_sent_count": board.invoice_sent_count,
        "invoice_paid_count": board.invoice_paid_count,
        "board_decision": board.board_decision.value,
        "diagnostic_inputs": {
            "reply_count": board.reply_count,
            "meeting_count": board.meeting_count,
            "no_response_count": board.no_response_count,
            "asks_for_scope_count": board.asks_for_scope_count,
            "asks_for_pdf_count": board.asks_for_pdf_count,
        },
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix CEO Market Motion OS")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_first5 = subparsers.add_parser(
        "prepare-first5",
        help="Create first-5 personalized drafts from warm list CSV",
    )
    prepare_first5.add_argument("--csv", default="data/warm_list.csv")
    prepare_first5.add_argument(
        "--out",
        default="data/outreach/warm_list_first5_personalized.md",
    )
    prepare_first5.add_argument("--limit", type=int, default=5)
    prepare_first5.set_defaults(func=_cmd_prepare_first5)

    log_event = subparsers.add_parser("log-event", help="Append one audited market event")
    log_event.add_argument("--ledger", default="docs/ops/live/market_motion_events.jsonl")
    log_event.add_argument("--contact-id", required=True)
    log_event.add_argument(
        "--event",
        required=True,
        choices=[member.value for member in MarketEvent],
    )
    log_event.add_argument("--source-ref", required=True)
    log_event.add_argument("--note", default="")
    log_event.add_argument("--occurred-at", default="")
    log_event.set_defaults(func=_cmd_log_event)

    status = subparsers.add_parser("status", help="Show 7-number scoreboard + decision")
    status.add_argument("--ledger", default="docs/ops/live/market_motion_events.jsonl")
    status.set_defaults(func=_cmd_status)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
