"""Revenue Ops Machine — funnel state machine + transition guards."""

from __future__ import annotations

import pytest

from auto_client_acquisition.revenue_ops_machine.context import new_context
from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    HARD_RULES,
    MILESTONE_GUARDS,
    TERMINAL_STATES,
    TRANSITIONS,
    FunnelState,
    IllegalTransition,
    advance,
    can_transition,
)


def _walk(ctx, *states: FunnelState) -> None:
    for state in states:
        ctx.transition_to(state)


HAPPY_PATH = (
    FunnelState.lead_captured,
    FunnelState.qualified_A,
    FunnelState.meeting_booked,
    FunnelState.meeting_done,
    FunnelState.scope_requested,
    FunnelState.scope_sent,
    FunnelState.invoice_sent,
    FunnelState.invoice_paid,
    FunnelState.delivery_started,
    FunnelState.proof_pack_sent,
    FunnelState.upsell_sprint,
    FunnelState.retainer_candidate,
)


def test_all_sixteen_states_present() -> None:
    assert len(list(FunnelState)) == 16


def test_every_legal_transition_is_allowed() -> None:
    for src, targets in TRANSITIONS.items():
        for target in targets:
            ok, reason = can_transition(src, target)
            assert ok, f"{src}->{target} should be allowed: {reason}"


def test_full_happy_path_walks_end_to_end() -> None:
    ctx = new_context("lead_happy")
    _walk(ctx, *HAPPY_PATH)
    assert ctx.funnel_state == FunnelState.retainer_candidate


def test_illegal_transition_raises() -> None:
    ctx = new_context("lead_x")
    ctx.transition_to(FunnelState.lead_captured)
    with pytest.raises(IllegalTransition):
        ctx.transition_to(FunnelState.invoice_sent)


def test_no_invoice_before_scope() -> None:
    ctx = new_context("lead_inv")
    _walk(
        ctx,
        FunnelState.lead_captured,
        FunnelState.qualified_A,
        FunnelState.meeting_booked,
        FunnelState.meeting_done,
        FunnelState.scope_requested,
    )
    # invoice_sent is not reachable until scope_sent.
    with pytest.raises(IllegalTransition):
        ctx.transition_to(FunnelState.invoice_sent)
    ctx.transition_to(FunnelState.scope_sent)
    ctx.transition_to(FunnelState.invoice_sent)  # now allowed
    assert ctx.funnel_state == FunnelState.invoice_sent


def test_no_delivery_before_invoice_paid() -> None:
    ctx = new_context("lead_del")
    _walk(ctx, *HAPPY_PATH[:6])  # ...through scope_sent
    ctx.transition_to(FunnelState.invoice_sent)
    with pytest.raises(IllegalTransition):
        ctx.transition_to(FunnelState.delivery_started)
    ctx.transition_to(FunnelState.invoice_paid)
    ctx.transition_to(FunnelState.delivery_started)
    assert ctx.funnel_state == FunnelState.delivery_started


def test_no_proof_pack_before_delivery() -> None:
    ctx = new_context("lead_pp")
    _walk(ctx, *HAPPY_PATH[:8])  # ...through invoice_paid
    with pytest.raises(IllegalTransition):
        ctx.transition_to(FunnelState.proof_pack_sent)


def test_no_upsell_before_proof_pack() -> None:
    ctx = new_context("lead_up")
    _walk(ctx, *HAPPY_PATH[:9])  # ...through delivery_started
    with pytest.raises(IllegalTransition):
        ctx.transition_to(FunnelState.upsell_sprint)


def test_milestone_guards_cover_the_four_ordering_rules() -> None:
    assert MILESTONE_GUARDS == {
        FunnelState.invoice_sent: FunnelState.scope_sent,
        FunnelState.delivery_started: FunnelState.invoice_paid,
        FunnelState.proof_pack_sent: FunnelState.delivery_started,
        FunnelState.upsell_sprint: FunnelState.proof_pack_sent,
    }
    assert len(HARD_RULES) == 5  # four ordering + case-study approval


def test_closed_lost_reachable_from_every_non_terminal_state() -> None:
    for state in FunnelState:
        if state in TERMINAL_STATES or state == FunnelState.closed_lost:
            continue
        ok, reason = can_transition(state, FunnelState.closed_lost)
        assert ok, f"closed_lost must be reachable from {state}: {reason}"


def test_closed_lost_can_revive_to_nurture() -> None:
    ctx = new_context("lead_revive")
    ctx.transition_to(FunnelState.lead_captured)
    ctx.transition_to(FunnelState.closed_lost)
    ctx.transition_to(FunnelState.nurture)
    assert ctx.funnel_state == FunnelState.nurture


def test_self_transition_rejected() -> None:
    ok, _ = can_transition(FunnelState.lead_captured, FunnelState.lead_captured)
    assert ok is False


def test_advance_returns_target_on_success() -> None:
    assert advance(FunnelState.visitor, FunnelState.lead_captured) == (FunnelState.lead_captured)
