#!/usr/bin/env python3
"""War Room scorecard generator (Distribution OS).

Aggregates the founder's daily distribution metrics from the immutable revenue
event stream — the single source of truth — and prints the War Room scorecard
defined in ``docs/DISTRIBUTION_OS.md``.

This is distinct from ``scripts/founder_daily_scorecard.py``: that script tracks
the v3 §10 outreach template from ``pipeline_tracker.csv``; this one tracks the
full distribution funnel from typed events, so the two never diverge.

Metrics (all counted from events occurring on the target date):
  messages sent, follow-ups, replies, proof-pack requests, demos booked,
  scopes sent, invoices sent, paid/commitment, proof packs delivered,
  partner conversations, risks blocked, tomorrow priority.

Usage:
  python scripts/war_room_scorecard.py
  python scripts/war_room_scorecard.py --date 2026-05-17 --tenant dealix_founder
  python scripts/war_room_scorecard.py --json

Exit codes:
  0  scorecard rendered successfully
  1  rendered with warnings (no events found for the date)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from dataclasses import asdict, dataclass, field

from auto_client_acquisition.revenue_memory.event_store import EventStore, get_default_store

DEFAULT_TENANT = "dealix_founder"

# Event types the War Room counts — passed as a filter to the event store.
_WAR_ROOM_EVENT_TYPES: tuple[str, ...] = (
    "message.sent",
    "message.rejected",
    "reply.received",
    "proof.pack_requested",
    "proof.pack_delivered",
    "meeting.booked",
    "scope.sent",
    "invoice.sent",
    "invoice.paid",
    "commitment.recorded",
    "partner.conversation_logged",
    "compliance.blocked",
)


@dataclass
class WarRoomCard:
    date: str
    tenant_id: str = DEFAULT_TENANT
    messages_sent: int = 0
    follow_ups: int = 0
    replies: int = 0
    proof_pack_requests: int = 0
    demos_booked: int = 0
    scopes_sent: int = 0
    invoices_sent: int = 0
    paid_or_commitment: int = 0
    proof_packs_delivered: int = 0
    partner_conversations: int = 0
    risks_blocked: int = 0
    tomorrow_priority: str = "—"
    warnings: list[str] = field(default_factory=list)


def _parse_iso_date(s: str) -> dt.date:
    return dt.datetime.fromisoformat(s).date()


def aggregate_war_room(
    store: EventStore,
    *,
    tenant_id: str,
    target_date: dt.date,
    tomorrow_priority: str = "—",
) -> WarRoomCard:
    """Build a War Room card by counting events for ``tenant_id`` on ``target_date``.

    Event ``occurred_at`` timestamps are naive UTC (see ``revenue_memory.events``),
    so the day window is also naive UTC.
    """
    day_start = dt.datetime.combine(target_date, dt.time.min)
    day_end = day_start + dt.timedelta(days=1) - dt.timedelta(microseconds=1)
    card = WarRoomCard(
        date=target_date.isoformat(),
        tenant_id=tenant_id,
        tomorrow_priority=tomorrow_priority,
    )
    seen = 0
    for e in store.read_for_customer(
        tenant_id, since=day_start, until=day_end, event_types=_WAR_ROOM_EVENT_TYPES
    ):
        seen += 1
        if e.event_type == "message.sent":
            card.messages_sent += 1
            if e.payload.get("kind") == "follow_up":
                card.follow_ups += 1
        elif e.event_type == "reply.received":
            card.replies += 1
        elif e.event_type == "proof.pack_requested":
            card.proof_pack_requests += 1
        elif e.event_type == "proof.pack_delivered":
            card.proof_packs_delivered += 1
        elif e.event_type == "meeting.booked":
            card.demos_booked += 1
        elif e.event_type == "scope.sent":
            card.scopes_sent += 1
        elif e.event_type == "invoice.sent":
            card.invoices_sent += 1
        elif e.event_type in ("invoice.paid", "commitment.recorded"):
            card.paid_or_commitment += 1
        elif e.event_type == "partner.conversation_logged":
            card.partner_conversations += 1
        elif e.event_type in ("compliance.blocked", "message.rejected"):
            card.risks_blocked += 1
    if seen == 0:
        card.warnings.append(f"no events found for {tenant_id} on {target_date.isoformat()}")
    return card


def format_text(card: WarRoomCard) -> str:
    lines = [
        f"War Room Scorecard — {card.date}  (tenant: {card.tenant_id})",
        f"  Messages sent:          {card.messages_sent}",
        f"  Follow-ups:             {card.follow_ups}",
        f"  Replies:                {card.replies}",
        f"  Proof Pack requests:    {card.proof_pack_requests}",
        f"  Demos booked:           {card.demos_booked}",
        f"  Scopes sent:            {card.scopes_sent}",
        f"  Invoices sent:          {card.invoices_sent}",
        f"  Paid / commitment:      {card.paid_or_commitment}",
        f"  Proof Packs delivered:  {card.proof_packs_delivered}",
        f"  Partner conversations:  {card.partner_conversations}",
        f"  Risks blocked:          {card.risks_blocked}",
        f"  Tomorrow priority:      {card.tomorrow_priority}",
    ]
    if card.warnings:
        lines.append("")
        lines.append("Warnings:")
        lines.extend(f"  - {w}" for w in card.warnings)
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--date", help="ISO date (default: today UTC)")
    p.add_argument("--tenant", default=DEFAULT_TENANT, help="tenant/customer id")
    p.add_argument("--backend", default="memory", choices=("memory", "postgres"))
    p.add_argument("--json", action="store_true", help="JSON output instead of text")
    args = p.parse_args()

    target_date = _parse_iso_date(args.date) if args.date else dt.datetime.now(dt.UTC).date()
    store = get_default_store(args.backend)
    card = aggregate_war_room(store, tenant_id=args.tenant, target_date=target_date)

    if args.json:
        print(json.dumps(asdict(card), indent=2, ensure_ascii=False))
    else:
        print(format_text(card))
    return 1 if card.warnings else 0


if __name__ == "__main__":
    sys.exit(main())
