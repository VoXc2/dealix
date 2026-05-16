"""Tests for the commercial gates G1-G7."""

from __future__ import annotations

from auto_client_acquisition.commercial_os.engine import CommercialEngine
from auto_client_acquisition.commercial_os.gates import evaluate_gates
from auto_client_acquisition.commercial_os.market_proof import (
    record_prepared,
    record_reply_classified,
    record_sent,
)
from auto_client_acquisition.revenue_memory.event_store import InMemoryEventStore
from auto_client_acquisition.revenue_memory.events import make_event


def _commercial_event(event_type: str, subject_id: str, **payload: object):
    return make_event(
        event_type=event_type,
        customer_id="c1",
        subject_type="account",
        subject_id=subject_id,
        payload=dict(payload),
    )


def test_all_gates_start_not_passed() -> None:
    gates = evaluate_gates([])
    assert set(gates.keys()) == {"G1", "G2", "G3", "G4", "G5", "G6", "G7"}
    for g in gates.values():
        assert g.passed is False


def test_g1_first_market_proof_needs_5_sent_and_a_classification() -> None:
    engine = CommercialEngine(store=InMemoryEventStore())
    for i in range(5):
        sid = f"a{i}"
        record_prepared(engine, customer_id="c1", subject_type="account", subject_id=sid)
        record_sent(
            engine,
            customer_id="c1",
            subject_type="account",
            subject_id=sid,
            founder_confirmed=True,
        )
    events = list(engine.store.read_for_customer("c1"))
    # 5 sent but no classification yet -> G1 not passed.
    assert evaluate_gates(events)["G1"].passed is False

    record_reply_classified(
        engine,
        customer_id="c1",
        subject_type="account",
        subject_id="a0",
        classification="silent",
    )
    events = list(engine.store.read_for_customer("c1"))
    assert evaluate_gates(events)["G1"].passed is True


def test_g2_meeting_proof_needs_used_in_meeting() -> None:
    events = [
        _commercial_event(
            "commercial.meeting_used", "a1", commercial_state="used_in_meeting"
        )
    ]
    assert evaluate_gates(events)["G2"].passed is True
    # A merely-booked meeting does not pass G2.
    booked = [
        _commercial_event(
            "commercial.meeting_used", "a2", commercial_state="meeting_booked"
        )
    ]
    assert evaluate_gates(booked)["G2"].passed is False


def test_g3_pull_proof_needs_scope_or_intro() -> None:
    events = [_commercial_event("commercial.scope_requested", "a1")]
    assert evaluate_gates(events)["G3"].passed is True
    events2 = [_commercial_event("commercial.pilot_intro_requested", "a2")]
    assert evaluate_gates(events2)["G3"].passed is True


def test_g4_revenue_proof_needs_invoice_paid() -> None:
    events = [_commercial_event("commercial.invoice_paid", "a1", offer_id="o1")]
    assert evaluate_gates(events)["G4"].passed is True


def test_g5_repeatability_needs_same_offer_paid_twice() -> None:
    once = [_commercial_event("commercial.invoice_paid", "a1", offer_id="o1")]
    assert evaluate_gates(once)["G5"].passed is False
    twice = [
        _commercial_event("commercial.invoice_paid", "a1", offer_id="o1"),
        _commercial_event("commercial.invoice_paid", "a2", offer_id="o1"),
    ]
    assert evaluate_gates(twice)["G5"].passed is True
    # Two paid invoices for different offers does NOT pass G5.
    different = [
        _commercial_event("commercial.invoice_paid", "a1", offer_id="o1"),
        _commercial_event("commercial.invoice_paid", "a2", offer_id="o2"),
    ]
    assert evaluate_gates(different)["G5"].passed is False


def test_g6_retainer_needs_active_retainer_flag() -> None:
    assert evaluate_gates([], has_active_retainer=False)["G6"].passed is False
    assert evaluate_gates([], has_active_retainer=True)["G6"].passed is True


def test_g7_platform_signal_from_friction_count() -> None:
    assert (
        evaluate_gates([], friction_repeated_workflow_count=3)["G7"].passed is True
    )
    assert (
        evaluate_gates([], friction_repeated_workflow_count=2)["G7"].passed is False
    )


def test_g7_platform_signal_fallback_from_event_stream() -> None:
    events = [
        _commercial_event("commercial.prepared", f"a{i}", workflow_signature="diag_flow")
        for i in range(3)
    ]
    assert evaluate_gates(events)["G7"].passed is True
    fewer = [
        _commercial_event("commercial.prepared", f"a{i}", workflow_signature="diag_flow")
        for i in range(2)
    ]
    assert evaluate_gates(fewer)["G7"].passed is False
