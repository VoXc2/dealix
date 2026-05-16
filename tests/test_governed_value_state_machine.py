"""Governed value proof state machine — strict L2–L7 transition guards."""

from __future__ import annotations

import pytest

from auto_client_acquisition.governed_value_os.state_machine import (
    PROOF_LEVEL_LABEL,
    ProofState,
    ProofTransitionError,
    level_label,
    revenue_recognized,
    validate_transition,
)


def test_level_labels_cover_every_state() -> None:
    for state in ProofState:
        assert state in PROOF_LEVEL_LABEL
    assert level_label(ProofState.PREPARED_NOT_SENT) == "L2"
    assert level_label(ProofState.USED_IN_MEETING) == "L5"
    assert level_label(ProofState.INVOICE_SENT) == "L7_candidate"
    assert level_label(ProofState.INVOICE_PAID) == "L7_confirmed"


def test_sent_requires_founder_confirmation() -> None:
    with pytest.raises(ProofTransitionError) as exc:
        validate_transition(ProofState.PREPARED_NOT_SENT, ProofState.SENT)
    assert exc.value.code == "sent_requires_founder_confirmation"
    # With founder confirmation it passes.
    validate_transition(
        ProofState.PREPARED_NOT_SENT, ProofState.SENT, founder_confirmed=True
    )


def test_l5_requires_a_prior_meeting() -> None:
    # Illegal jump (not adjacent) is blocked.
    with pytest.raises(ProofTransitionError) as exc:
        validate_transition(ProofState.SENT, ProofState.USED_IN_MEETING)
    assert exc.value.code == "illegal_transition"
    # Legal adjacent transition from MEETING_BOOKED is allowed.
    validate_transition(ProofState.MEETING_BOOKED, ProofState.USED_IN_MEETING)


def test_l6_requires_scope_or_intro_request() -> None:
    with pytest.raises(ProofTransitionError) as exc:
        validate_transition(ProofState.USED_IN_MEETING, ProofState.SCOPE_REQUESTED)
    assert exc.value.code == "l6_requires_scope_or_intro_request"
    validate_transition(
        ProofState.USED_IN_MEETING,
        ProofState.SCOPE_REQUESTED,
        scope_requested=True,
    )
    validate_transition(
        ProofState.USED_IN_MEETING,
        ProofState.PILOT_INTRO_REQUESTED,
        scope_requested=True,
    )


def test_l7_confirmed_requires_payment_reference() -> None:
    with pytest.raises(ProofTransitionError) as exc:
        validate_transition(ProofState.INVOICE_SENT, ProofState.INVOICE_PAID)
    assert exc.value.code == "l7_confirmed_requires_payment"
    validate_transition(
        ProofState.INVOICE_SENT, ProofState.INVOICE_PAID, payment_ref="moyasar_pay_123"
    )


def test_illegal_transition_blocked() -> None:
    with pytest.raises(ProofTransitionError) as exc:
        validate_transition(ProofState.PREPARED_NOT_SENT, ProofState.INVOICE_PAID)
    assert exc.value.code == "illegal_transition"


def test_revenue_recognized_only_at_invoice_paid() -> None:
    for state in ProofState:
        if state is ProofState.INVOICE_PAID:
            assert revenue_recognized(state) is True
        else:
            assert revenue_recognized(state) is False


def test_transition_error_is_bilingual() -> None:
    err = ProofTransitionError("l7_confirmed_requires_payment")
    assert err.reason_ar and err.reason_en
    assert err.reason_ar != err.reason_en


def test_full_happy_path() -> None:
    validate_transition(
        ProofState.PREPARED_NOT_SENT, ProofState.SENT, founder_confirmed=True
    )
    validate_transition(ProofState.SENT, ProofState.REPLIED_INTERESTED)
    validate_transition(ProofState.REPLIED_INTERESTED, ProofState.MEETING_BOOKED)
    validate_transition(ProofState.MEETING_BOOKED, ProofState.USED_IN_MEETING)
    validate_transition(
        ProofState.USED_IN_MEETING, ProofState.SCOPE_REQUESTED, scope_requested=True
    )
    validate_transition(ProofState.SCOPE_REQUESTED, ProofState.INVOICE_SENT)
    validate_transition(
        ProofState.INVOICE_SENT, ProofState.INVOICE_PAID, payment_ref="pay_1"
    )
