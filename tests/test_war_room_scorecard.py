"""Distribution OS — War Room scorecard aggregation from the event stream."""

from __future__ import annotations

import datetime as dt

from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore
from auto_client_acquisition.revenue_memory.events import make_event
from scripts.war_room_scorecard import aggregate_war_room

_DAY = dt.date(2026, 5, 17)
_TENANT = "t1"


def _at(hour: int, day: dt.date = _DAY) -> dt.datetime:
    return dt.datetime.combine(day, dt.time(hour, 0))


def _seed_store() -> InMemoryEventStore:
    store = InMemoryEventStore()
    specs = [
        ("message.sent", _TENANT, _at(9), {}),
        ("message.sent", _TENANT, _at(10), {}),
        ("message.sent", _TENANT, _at(11), {"kind": "follow_up"}),
        ("reply.received", _TENANT, _at(12), {}),
        ("proof.pack_requested", _TENANT, _at(12), {}),
        ("proof.pack_delivered", _TENANT, _at(13), {}),
        ("meeting.booked", _TENANT, _at(14), {}),
        ("meeting.booked", _TENANT, _at(15), {}),
        ("scope.sent", _TENANT, _at(15), {}),
        ("invoice.sent", _TENANT, _at(16), {}),
        ("invoice.paid", _TENANT, _at(17), {}),
        ("commitment.recorded", _TENANT, _at(17), {}),
        ("partner.conversation_logged", _TENANT, _at(18), {}),
        ("compliance.blocked", _TENANT, _at(18), {}),
        ("message.rejected", _TENANT, _at(19), {}),
        # Noise: different day, and different tenant — must be excluded.
        ("message.sent", _TENANT, _at(9, dt.date(2026, 5, 16)), {}),
        ("message.sent", "other_tenant", _at(9), {}),
    ]
    for event_type, tenant, occurred_at, payload in specs:
        store.append(
            make_event(
                event_type=event_type,
                customer_id=tenant,
                subject_type="account",
                subject_id="acc_1",
                payload=payload,
                occurred_at=occurred_at,
            )
        )
    return store


def test_war_room_counts_are_correct() -> None:
    card = aggregate_war_room(_seed_store(), tenant_id=_TENANT, target_date=_DAY)
    assert card.messages_sent == 3
    assert card.follow_ups == 1
    assert card.replies == 1
    assert card.proof_pack_requests == 1
    assert card.proof_packs_delivered == 1
    assert card.demos_booked == 2
    assert card.scopes_sent == 1
    assert card.invoices_sent == 1
    assert card.paid_or_commitment == 2
    assert card.partner_conversations == 1
    assert card.risks_blocked == 2
    assert not card.warnings


def test_other_tenant_and_other_day_excluded() -> None:
    card = aggregate_war_room(_seed_store(), tenant_id="other_tenant", target_date=_DAY)
    assert card.messages_sent == 1  # only the one same-day event for other_tenant
    assert card.replies == 0


def test_empty_day_emits_warning() -> None:
    card = aggregate_war_room(
        InMemoryEventStore(), tenant_id=_TENANT, target_date=_DAY
    )
    assert card.messages_sent == 0
    assert card.warnings
