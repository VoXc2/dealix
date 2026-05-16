"""Tests for the market-proof L2 to L7 lifecycle state machine.

Covers every transition guard rule, a full happy-path L2 to L7 progression,
the command-center snapshot counts, and a doctrine non-negotiable breach.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_os.market_proof_lifecycle import (
    ALLOWED_TRANSITIONS,
    LIFECYCLE_STATES,
    STATE_TO_LEVEL,
    clear_blocked_for_test,
    clear_for_test,
    current_state,
    ledger,
    list_blocked,
    record_blocked,
    record_transition,
    snapshot,
    state_machine_definition,
)


@pytest.fixture(autouse=True)
def _reset_ledger() -> None:
    """Reset the in-memory ledger and blocked list before each test."""
    clear_for_test()
    clear_blocked_for_test()


# ── State machine definition ───────────────────────────────────────


def test_state_machine_definition_shape() -> None:
    definition = state_machine_definition()
    assert definition["revenue_confirmed_state"] == "invoice_paid"
    assert set(definition["states"]) == set(LIFECYCLE_STATES)
    assert definition["state_to_level"] == STATE_TO_LEVEL
    assert definition["allowed_transitions"]["prepared_not_sent"] == ["sent"]


def test_state_to_level_mapping() -> None:
    assert STATE_TO_LEVEL["prepared_not_sent"] == "L2"
    assert STATE_TO_LEVEL["sent"] == "L4"
    assert STATE_TO_LEVEL["used_in_meeting"] == "L5"
    assert STATE_TO_LEVEL["scope_requested"] == "L6"
    assert STATE_TO_LEVEL["pilot_intro_requested"] == "L6"
    assert STATE_TO_LEVEL["invoice_sent"] == "L7_candidate"
    assert STATE_TO_LEVEL["invoice_paid"] == "L7_confirmed"


# ── Guard rule: sent requires founder_confirmed ────────────────────


def test_sent_without_founder_confirmed_fails() -> None:
    with pytest.raises(ValueError, match="founder_confirmed"):
        record_transition("c1", "prepared_not_sent", "sent")


def test_sent_with_founder_confirmed_succeeds() -> None:
    record = record_transition(
        "c1", "prepared_not_sent", "sent", founder_confirmed=True
    )
    assert record["to_state"] == "sent"
    assert record["to_level"] == "L4"
    assert record["founder_confirmed"] is True


# ── Guard rule: L5 requires meeting_booked in history ──────────────


def test_used_in_meeting_without_meeting_booked_fails() -> None:
    # An invalid transition path: jumping into used_in_meeting is not allowed
    # from a state that never passed through meeting_booked.
    with pytest.raises(ValueError):
        record_transition("c2", "replied_interested", "used_in_meeting")


def test_used_in_meeting_after_meeting_booked_succeeds() -> None:
    record_transition("c3", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c3", "sent", "meeting_booked")
    record = record_transition("c3", "meeting_booked", "used_in_meeting")
    assert record["to_state"] == "used_in_meeting"
    assert record["to_level"] == "L5"


# ── Guard rule: L6 requires a recorded scope/intro request ─────────


def test_scope_requested_without_request_fails() -> None:
    record_transition("c4", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c4", "sent", "meeting_booked")
    record_transition("c4", "meeting_booked", "used_in_meeting")
    with pytest.raises(ValueError, match="scope_or_intro_request"):
        record_transition("c4", "used_in_meeting", "scope_requested")


def test_pilot_intro_requested_without_request_fails() -> None:
    record_transition("c5", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c5", "sent", "meeting_booked")
    record_transition("c5", "meeting_booked", "used_in_meeting")
    with pytest.raises(ValueError, match="scope_or_intro_request"):
        record_transition("c5", "used_in_meeting", "pilot_intro_requested")


def test_scope_requested_with_request_succeeds() -> None:
    record_transition("c6", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c6", "sent", "meeting_booked")
    record_transition("c6", "meeting_booked", "used_in_meeting")
    record = record_transition(
        "c6",
        "used_in_meeting",
        "scope_requested",
        scope_or_intro_request="scope doc requested in meeting",
    )
    assert record["to_state"] == "scope_requested"
    assert record["to_level"] == "L6"


# ── Guard rule: invoice_paid requires payment_confirmed ────────────


def test_invoice_paid_without_payment_confirmed_fails() -> None:
    record_transition("c7", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c7", "sent", "meeting_booked")
    record_transition("c7", "meeting_booked", "used_in_meeting")
    record_transition(
        "c7",
        "used_in_meeting",
        "scope_requested",
        scope_or_intro_request="scope requested",
    )
    record_transition("c7", "scope_requested", "invoice_sent")
    with pytest.raises(ValueError, match="payment_confirmed"):
        record_transition("c7", "invoice_sent", "invoice_paid")


def test_revenue_not_counted_before_invoice_paid() -> None:
    record_transition("c8", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c8", "sent", "meeting_booked")
    record_transition("c8", "meeting_booked", "used_in_meeting")
    record_transition(
        "c8",
        "used_in_meeting",
        "scope_requested",
        scope_or_intro_request="scope requested",
    )
    invoice_sent = record_transition("c8", "scope_requested", "invoice_sent")
    assert invoice_sent["revenue_counted"] is False
    assert snapshot()["revenue_confirmed"] is False
    assert snapshot()["contacts_with_confirmed_revenue"] == 0


# ── Happy path: full L2 to L7 progression ──────────────────────────


def test_happy_path_full_l2_to_l7() -> None:
    cid = "happy-1"
    record_transition(cid, "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition(cid, "sent", "replied_interested")
    record_transition(cid, "replied_interested", "meeting_booked")
    record_transition(cid, "meeting_booked", "used_in_meeting")
    record_transition(
        cid,
        "used_in_meeting",
        "scope_requested",
        scope_or_intro_request="scope doc requested",
    )
    record_transition(cid, "scope_requested", "invoice_sent")
    final = record_transition(
        cid, "invoice_sent", "invoice_paid", payment_confirmed=True
    )

    assert final["to_state"] == "invoice_paid"
    assert final["to_level"] == "L7_confirmed"
    assert final["revenue_counted"] is True
    assert current_state(cid) == "invoice_paid"

    history = ledger()[cid]
    assert len(history) == 7
    assert [r["to_state"] for r in history] == [
        "sent",
        "replied_interested",
        "meeting_booked",
        "used_in_meeting",
        "scope_requested",
        "invoice_sent",
        "invoice_paid",
    ]


def test_happy_path_via_pilot_intro() -> None:
    cid = "happy-2"
    record_transition(cid, "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition(cid, "sent", "meeting_booked")
    record_transition(cid, "meeting_booked", "used_in_meeting")
    record_transition(
        cid,
        "used_in_meeting",
        "pilot_intro_requested",
        scope_or_intro_request="pilot intro requested",
    )
    record_transition(cid, "pilot_intro_requested", "invoice_sent")
    final = record_transition(
        cid, "invoice_sent", "invoice_paid", payment_confirmed=True
    )
    assert final["revenue_counted"] is True


# ── Invalid transitions ────────────────────────────────────────────


def test_invalid_transition_rejected() -> None:
    with pytest.raises(ValueError, match="invalid transition"):
        record_transition(
            "c9", "prepared_not_sent", "meeting_booked", founder_confirmed=True
        )


def test_from_state_must_match_current_state() -> None:
    record_transition("c10", "prepared_not_sent", "sent", founder_confirmed=True)
    with pytest.raises(ValueError, match="does not match"):
        record_transition("c10", "prepared_not_sent", "sent", founder_confirmed=True)


def test_unknown_state_rejected() -> None:
    with pytest.raises(ValueError, match="unknown"):
        record_transition("c11", "prepared_not_sent", "not_a_state")
    with pytest.raises(ValueError, match="unknown"):
        record_transition("c11", "not_a_state", "sent")


def test_contact_id_required() -> None:
    with pytest.raises(ValueError, match="contact_id"):
        record_transition("", "prepared_not_sent", "sent", founder_confirmed=True)


def test_terminal_state_no_reply() -> None:
    record_transition("c12", "prepared_not_sent", "sent", founder_confirmed=True)
    record = record_transition("c12", "sent", "no_reply")
    assert record["to_state"] == "no_reply"
    assert ALLOWED_TRANSITIONS["no_reply"] == ()


# ── Snapshot counts ────────────────────────────────────────────────


def test_snapshot_level_counts() -> None:
    # Contact a -> L4
    record_transition("a", "prepared_not_sent", "sent", founder_confirmed=True)
    # Contact b -> L5
    record_transition("b", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("b", "sent", "meeting_booked")
    record_transition("b", "meeting_booked", "used_in_meeting")
    # Contact c -> L6
    record_transition("c", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("c", "sent", "meeting_booked")
    record_transition("c", "meeting_booked", "used_in_meeting")
    record_transition(
        "c",
        "used_in_meeting",
        "scope_requested",
        scope_or_intro_request="scope requested",
    )
    # Contact d -> L7 confirmed
    record_transition("d", "prepared_not_sent", "sent", founder_confirmed=True)
    record_transition("d", "sent", "meeting_booked")
    record_transition("d", "meeting_booked", "used_in_meeting")
    record_transition(
        "d",
        "used_in_meeting",
        "scope_requested",
        scope_or_intro_request="scope requested",
    )
    record_transition("d", "scope_requested", "invoice_sent")
    record_transition("d", "invoice_sent", "invoice_paid", payment_confirmed=True)

    snap = snapshot()
    assert snap["level_counts"] == {"L4": 1, "L5": 1, "L6": 1, "L7": 1}
    assert snap["current_state_by_contact"]["a"] == "sent"
    assert snap["current_state_by_contact"]["d"] == "invoice_paid"
    assert snap["contacts_with_confirmed_revenue"] == 1
    assert snap["revenue_confirmed"] is True


def test_snapshot_empty_ledger_revenue_zero() -> None:
    snap = snapshot()
    assert snap["level_counts"] == {"L4": 0, "L5": 0, "L6": 0, "L7": 0}
    assert snap["current_state_by_contact"] == {}
    assert snap["contacts_with_confirmed_revenue"] == 0
    assert snap["revenue_confirmed"] is False


def test_snapshot_blocked_items() -> None:
    record_blocked("blocked-1", "used_in_meeting", "scope_requested", "no scope request")
    snap = snapshot()
    assert len(snap["blocked_items"]) == 1
    assert snap["blocked_items"][0]["contact_id"] == "blocked-1"
    assert list_blocked()[0]["reason"] == "no scope request"


# ── Doctrine non-negotiable breach ─────────────────────────────────


@pytest.mark.governance
def test_doctrine_external_send_without_approval_trips() -> None:
    with pytest.raises(ValueError, match="doctrine_violations"):
        record_transition(
            "doc-1",
            "prepared_not_sent",
            "sent",
            founder_confirmed=True,
            doctrine_flags={"request_external_send_without_approval": True},
        )


@pytest.mark.governance
@pytest.mark.parametrize(
    "flag",
    [
        "request_cold_whatsapp",
        "request_linkedin_automation",
        "request_scraping",
        "request_bulk_outreach",
        "request_guaranteed_sales_claim",
        "request_fake_proof",
        "request_external_send_without_approval",
    ],
)
def test_doctrine_flags_all_trip(flag: str) -> None:
    with pytest.raises(ValueError, match="doctrine_violations"):
        record_transition(
            "doc-2",
            "prepared_not_sent",
            "sent",
            founder_confirmed=True,
            doctrine_flags={flag: True},
        )


@pytest.mark.governance
def test_no_auto_send_function_exists() -> None:
    """The lifecycle module must expose no message-send or external-action path."""
    import auto_client_acquisition.revenue_os.market_proof_lifecycle as mpl

    forbidden = ("send", "deliver", "dispatch", "execute", "post_message")
    public_names = [n for n in dir(mpl) if not n.startswith("_")]
    for name in public_names:
        lowered = name.lower()
        assert not any(token in lowered for token in forbidden), (
            f"unexpected send-like symbol exposed: {name}"
        )
