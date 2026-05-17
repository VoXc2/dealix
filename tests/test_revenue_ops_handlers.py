"""Revenue Ops Machine — the six ops handlers end to end."""

from __future__ import annotations

import pytest

from auto_client_acquisition.proof_ledger.schemas import ProofEventType
from auto_client_acquisition.revenue_ops_machine.context import new_context
from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    FunnelState,
    IllegalTransition,
)
from auto_client_acquisition.revenue_ops_machine.handlers import (
    booking_ops,
    delivery_proof_ops,
    lead_capture_ops,
    qualification_ops,
    sales_call_ops,
    scope_invoice_ops,
)

A_GRADE_FORM = {
    "company": "Acme Trading Co",
    "role": "Founder",
    "current_crm": "HubSpot",
    "ai_usage": "chatbot pilot",
    "region": "Riyadh",
    "urgency": "asap",
    "budget": 6000,
}


def _capture_and_qualify(lead_id: str = "lead_h"):
    ctx = new_context(lead_id)
    lead_capture_ops(ctx, A_GRADE_FORM)
    qualification_ops(ctx)
    return ctx


def test_lead_capture_scores_and_advances() -> None:
    ctx = new_context("lead_cap")
    result = lead_capture_ops(ctx, A_GRADE_FORM)
    assert ctx.funnel_state == FunnelState.lead_captured
    assert ctx.abcd_grade == "A"
    assert ctx.recommended_offer_id == "revenue_proof_sprint_499"
    kinds = {d.kind for d in result.drafts}
    assert kinds == {"founder_notification", "follow_up"}
    assert result.proof_events[0].event_type == ProofEventType.LEAD_INTAKE


def test_qualification_routes_grade_a_to_qualified_a() -> None:
    ctx = new_context("lead_q")
    lead_capture_ops(ctx, A_GRADE_FORM)
    qualification_ops(ctx)
    assert ctx.funnel_state == FunnelState.qualified_A


def test_qualification_routes_low_grade_to_nurture() -> None:
    ctx = new_context("lead_low")
    lead_capture_ops(ctx, {"role": "student", "ai_usage": "curious"})
    qualification_ops(ctx)
    assert ctx.funnel_state == FunnelState.nurture


def test_booking_book_then_done() -> None:
    ctx = _capture_and_qualify()
    booking_ops(ctx, "book")
    assert ctx.funnel_state == FunnelState.meeting_booked
    booking_ops(ctx, "done")
    assert ctx.funnel_state == FunnelState.meeting_done


def test_full_funnel_runs_to_retainer_candidate() -> None:
    ctx = _capture_and_qualify("lead_full")
    booking_ops(ctx, "book")
    booking_ops(ctx, "done")
    sales_call_ops(ctx)
    assert ctx.funnel_state == FunnelState.scope_requested

    scope_invoice_ops(ctx, "scope")
    inv = scope_invoice_ops(ctx, "invoice")
    assert ctx.funnel_state == FunnelState.invoice_sent
    assert any(e.event_type == ProofEventType.INVOICE_PREPARED for e in inv.proof_events)
    paid = scope_invoice_ops(ctx, "paid")
    assert any(e.event_type == ProofEventType.PAYMENT_CONFIRMED for e in paid.proof_events)

    delivery_proof_ops(ctx, "start")
    proof = delivery_proof_ops(ctx, "proof")
    assert ctx.funnel_state == FunnelState.proof_pack_sent
    assert {e.event_type for e in proof.proof_events} == {
        ProofEventType.PROOF_PACK_ASSEMBLED,
        ProofEventType.PROOF_PACK_SENT,
    }
    delivery_proof_ops(ctx, "upsell")
    delivery_proof_ops(ctx, "retainer")
    assert ctx.funnel_state == FunnelState.retainer_candidate


def test_invoice_before_scope_is_rejected() -> None:
    ctx = _capture_and_qualify("lead_bad")
    booking_ops(ctx, "book")
    booking_ops(ctx, "done")
    sales_call_ops(ctx)  # at scope_requested
    with pytest.raises(IllegalTransition):
        scope_invoice_ops(ctx, "invoice")


def test_unknown_step_raises() -> None:
    ctx = _capture_and_qualify("lead_step")
    with pytest.raises(Exception):
        booking_ops(ctx, "teleport")
