"""Tests for the pure CEL transition validator and the CEL vocabulary."""

from __future__ import annotations

from auto_client_acquisition.commercial_os.cel import (
    CEL_LEVELS,
    COMMERCIAL_STATES,
    STATE_TO_CEL,
    cel_for_state,
)
from auto_client_acquisition.commercial_os.transitions import (
    is_revenue_recognized,
    validate_transition,
)


def test_cel_vocabulary_matches_spec() -> None:
    assert CEL_LEVELS == (
        "CEL2",
        "CEL4",
        "CEL5",
        "CEL6",
        "CEL7_candidate",
        "CEL7_confirmed",
    )
    for state in (
        "prepared_not_sent",
        "sent",
        "replied_interested",
        "meeting_booked",
        "used_in_meeting",
        "scope_requested",
        "pilot_intro_requested",
        "invoice_sent",
        "invoice_paid",
        "silent",
        "not_interested",
    ):
        assert state in COMMERCIAL_STATES


def test_cel_for_state_maps_each_state() -> None:
    assert cel_for_state("prepared_not_sent") == "CEL2"
    assert cel_for_state("sent") == "CEL4"
    assert cel_for_state("used_in_meeting") == "CEL5"
    assert cel_for_state("scope_requested") == "CEL6"
    assert cel_for_state("invoice_sent") == "CEL7_candidate"
    assert cel_for_state("invoice_paid") == "CEL7_confirmed"


def test_start_to_prepared_is_legal() -> None:
    result = validate_transition(None, "prepared_not_sent")
    assert result.ok is True
    assert result.reason == "ok"


def test_rule1_sent_requires_founder_confirmed() -> None:
    blocked = validate_transition("prepared_not_sent", "sent", founder_confirmed=False)
    assert blocked.ok is False
    assert blocked.reason == "rule1_sent_requires_founder_confirmed"

    allowed = validate_transition("prepared_not_sent", "sent", founder_confirmed=True)
    assert allowed.ok is True


def test_rule2_cel5_requires_used_in_meeting() -> None:
    blocked = validate_transition("meeting_booked", "used_in_meeting", used_in_meeting=False)
    assert blocked.ok is False
    assert blocked.reason == "rule2_cel5_requires_used_in_meeting"

    allowed = validate_transition("meeting_booked", "used_in_meeting", used_in_meeting=True)
    assert allowed.ok is True


def test_rule3_cel6_requires_scope_or_intro() -> None:
    for next_state in ("scope_requested", "pilot_intro_requested"):
        blocked = validate_transition(
            "used_in_meeting", next_state, scope_or_intro_requested=False
        )
        assert blocked.ok is False
        assert blocked.reason == "rule3_cel6_requires_scope_or_intro"
        allowed = validate_transition(
            "used_in_meeting", next_state, scope_or_intro_requested=True
        )
        assert allowed.ok is True


def test_rule4_invoice_paid_requires_payment() -> None:
    blocked = validate_transition("invoice_sent", "invoice_paid", invoice_paid=False)
    assert blocked.ok is False
    assert blocked.reason == "rule4_invoice_paid_requires_payment"

    allowed = validate_transition("invoice_sent", "invoice_paid", invoice_paid=True)
    assert allowed.ok is True


def test_rule5_revenue_only_recognized_at_cel7_confirmed() -> None:
    assert is_revenue_recognized("invoice_paid") is True
    assert is_revenue_recognized("invoice_sent") is False
    assert is_revenue_recognized("used_in_meeting") is False


def test_illegal_transition_graph_jumps_are_rejected() -> None:
    # Cannot skip from prepared straight to used_in_meeting.
    skip = validate_transition("prepared_not_sent", "used_in_meeting")
    assert skip.ok is False
    assert skip.reason.startswith("illegal_transition:")

    # Cannot go backwards.
    back = validate_transition("invoice_paid", "sent", founder_confirmed=True)
    assert back.ok is False
    assert back.reason.startswith("illegal_transition:")


def test_unknown_states_are_rejected() -> None:
    assert validate_transition(None, "not_a_state").ok is False
    assert validate_transition("not_a_state", "sent").ok is False


def test_legal_happy_path_full_chain() -> None:
    chain = [
        (None, "prepared_not_sent", {}),
        ("prepared_not_sent", "sent", {"founder_confirmed": True}),
        ("sent", "replied_interested", {}),
        ("replied_interested", "meeting_booked", {}),
        ("meeting_booked", "used_in_meeting", {"used_in_meeting": True}),
        ("used_in_meeting", "scope_requested", {"scope_or_intro_requested": True}),
        ("scope_requested", "invoice_sent", {}),
        ("invoice_sent", "invoice_paid", {"invoice_paid": True}),
    ]
    for current, nxt, kwargs in chain:
        result = validate_transition(current, nxt, **kwargs)
        assert result.ok is True, f"{current}->{nxt}: {result.reason}"
        assert nxt in STATE_TO_CEL
