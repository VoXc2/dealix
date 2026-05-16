"""Tests for CommercialEngine recording + the current-state projection."""

from __future__ import annotations

import pytest

from auto_client_acquisition.commercial_os.engine import (
    CommercialEngine,
    event_type_for_state,
)
from auto_client_acquisition.commercial_os.market_proof import (
    record_meeting_used,
    record_prepared,
    record_reply_classified,
    record_sent,
)
from auto_client_acquisition.commercial_os.projections import (
    current_commercial_state,
)
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore


def _engine() -> CommercialEngine:
    return CommercialEngine(store=InMemoryEventStore())


def test_event_type_for_state_maps_known_states() -> None:
    assert event_type_for_state("prepared_not_sent") == "commercial.prepared"
    assert event_type_for_state("sent") == "commercial.sent"
    assert event_type_for_state("invoice_paid") == "commercial.invoice_paid"
    with pytest.raises(ValueError):
        event_type_for_state("not_a_state")


def test_record_transition_appends_event() -> None:
    engine = _engine()
    recorded = engine.record_transition(
        customer_id="c1",
        subject_type="account",
        subject_id="acc1",
        next_state="prepared_not_sent",
    )
    assert recorded.cel == "CEL2"
    assert recorded.state == "prepared_not_sent"
    assert recorded.event.event_type == "commercial.prepared"
    events = list(engine.store.read_for_customer("c1"))
    assert len(events) == 1


def test_record_transition_rejects_illegal_transition() -> None:
    engine = _engine()
    # Cannot go straight to `sent` without a `prepared_not_sent` first.
    with pytest.raises(ValueError) as exc:
        engine.record_transition(
            customer_id="c1",
            subject_type="account",
            subject_id="acc1",
            next_state="sent",
            founder_confirmed=True,
        )
    assert "illegal_transition" in str(exc.value)
    # Nothing was written.
    assert engine.store.count("c1") == 0


def test_record_sent_requires_founder_confirmed() -> None:
    engine = _engine()
    record_prepared(engine, customer_id="c1", subject_type="account", subject_id="a1")
    with pytest.raises(ValueError):
        record_sent(
            engine,
            customer_id="c1",
            subject_type="account",
            subject_id="a1",
            founder_confirmed=False,
        )


def test_engine_full_chain_projects_latest_state() -> None:
    engine = _engine()
    record_prepared(engine, customer_id="c1", subject_type="account", subject_id="a1")
    record_sent(
        engine,
        customer_id="c1",
        subject_type="account",
        subject_id="a1",
        founder_confirmed=True,
    )
    record_reply_classified(
        engine,
        customer_id="c1",
        subject_type="account",
        subject_id="a1",
        classification="replied_interested",
    )
    engine.record_transition(
        customer_id="c1",
        subject_type="account",
        subject_id="a1",
        next_state="meeting_booked",
    )
    record_meeting_used(
        engine, customer_id="c1", subject_type="account", subject_id="a1"
    )

    state = engine.current_state(
        customer_id="c1", subject_type="account", subject_id="a1"
    )
    assert state == {"state": "used_in_meeting", "cel": "CEL5"}


def test_current_commercial_state_folds_multiple_subjects() -> None:
    engine = _engine()
    record_prepared(engine, customer_id="c1", subject_type="account", subject_id="a1")
    record_prepared(engine, customer_id="c1", subject_type="account", subject_id="a2")
    record_sent(
        engine,
        customer_id="c1",
        subject_type="account",
        subject_id="a2",
        founder_confirmed=True,
    )
    states = current_commercial_state(list(engine.store.read_for_customer("c1")))
    assert states["a1"] == {"state": "prepared_not_sent", "cel": "CEL2"}
    assert states["a2"] == {"state": "sent", "cel": "CEL4"}


def test_projection_ignores_non_commercial_events() -> None:
    from auto_client_acquisition.revenue_memory.events import make_event

    store = InMemoryEventStore()
    store.append(
        make_event(
            event_type="lead.created",
            customer_id="c1",
            subject_type="account",
            subject_id="a1",
        )
    )
    assert current_commercial_state(list(store.read_for_customer("c1"))) == {}
