"""V12.5 RevOps router — finance truth endpoints."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_pipeline.pipeline import (
    get_default_pipeline,
)
from auto_client_acquisition.revops import (
    PaymentMethod,
    build_finance_brief,
    compute_margin,
    create_invoice_draft,
    record_payment_confirmation,
    transition_invoice,
)
from auto_client_acquisition.revops.invoice_state import (
    InvoiceState,
    InvoiceStatus,
)
from auto_client_acquisition.revops.payment_confirmation import (
    list_confirmations,
)

router = APIRouter(prefix="/api/v1/revops", tags=["revops"])


_HARD_GATES = {
    "no_live_charge": True,
    "no_fake_revenue": True,
    "draft_invoice_is_not_revenue": True,
    "verbal_yes_is_not_commitment": True,
    "evidence_required_for_payment": True,
    "approval_required_for_external_actions": True,
}


# In-memory invoice store (V12.5 v1; persistence deferred)
_INVOICES: dict[str, InvoiceState] = {}


class _InvoiceCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = Field(min_length=1, max_length=80)
    amount_sar: int = Field(gt=0, le=50000)
    description: str = ""
    mode: str = "test"


class _InvoiceTransitionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    invoice_id: str
    target_status: InvoiceStatus


class _PaymentConfirmRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    invoice_id: str
    customer_handle: str = Field(min_length=1, max_length=80)
    amount_sar: int = Field(gt=0)
    payment_method: PaymentMethod
    evidence_reference: str = Field(min_length=5, max_length=200)
    notes: str = ""


class _MarginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str
    revenue_sar: int = Field(ge=0)
    delivery_cost_sar: int = Field(default=0, ge=0)
    support_cost_sar: int = Field(default=0, ge=0)
    other_cost_sar: int = Field(default=0, ge=0)
    notes: str = ""


@router.get("/status")
async def revops_status() -> dict[str, Any]:
    return {
        "service": "revops",
        "module": "revops",
        "status": "operational",
        "version": "v12.5",
        "degraded": False,
        "active_invoices": len(_INVOICES),
        "payment_confirmations": len(list_confirmations()),
        "checks": {
            "invoice_state_machine": "ok",
            "payment_evidence_gate": "ok",
            "margin_calculator": "ok",
            "finance_brief": "ok",
        },
        "hard_gates": _HARD_GATES,
        "next_action_ar": "أنشئ invoice draft ثم أكّد الدفع بدليل",
        "next_action_en": "Create invoice draft then confirm payment with evidence.",
    }


@router.post("/invoice-state")
async def invoice_state(req: _InvoiceCreateRequest) -> dict[str, Any]:
    try:
        invoice = create_invoice_draft(
            customer_handle=req.customer_handle,
            amount_sar=req.amount_sar,
            description=req.description,
            mode="test" if req.mode == "test" else "manual_only",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _INVOICES[invoice.invoice_id] = invoice
    return {
        "invoice": invoice.model_dump(mode="json"),
        "note_ar": "ملاحظة: invoice draft ≠ إيراد. الإيراد يحتاج دفع مؤكَّد.",
        "note_en": "Reminder: invoice draft is NOT revenue. Revenue requires confirmed payment.",
        "hard_gates": _HARD_GATES,
    }


@router.post("/invoice-transition")
async def invoice_transition(req: _InvoiceTransitionRequest) -> dict[str, Any]:
    invoice = _INVOICES.get(req.invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail=f"unknown invoice: {req.invoice_id}")
    try:
        updated = transition_invoice(invoice, req.target_status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    _INVOICES[req.invoice_id] = updated
    return {"invoice": updated.model_dump(mode="json"), "hard_gates": _HARD_GATES}


@router.post("/payment-confirm")
async def payment_confirm(req: _PaymentConfirmRequest) -> dict[str, Any]:
    try:
        confirmation = record_payment_confirmation(
            invoice_id=req.invoice_id,
            customer_handle=req.customer_handle,
            amount_sar=req.amount_sar,
            payment_method=req.payment_method,
            evidence_reference=req.evidence_reference,
            notes=req.notes,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "confirmation": confirmation.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/margin-snapshot")
async def margin_snapshot(req: _MarginRequest) -> dict[str, Any]:
    snapshot = compute_margin(
        customer_handle=req.customer_handle,
        revenue_sar=req.revenue_sar,
        delivery_cost_sar=req.delivery_cost_sar,
        support_cost_sar=req.support_cost_sar,
        other_cost_sar=req.other_cost_sar,
        notes=req.notes,
    )
    return {
        "customer_handle": snapshot.customer_handle,
        "revenue_sar": snapshot.revenue_sar,
        "delivery_cost_sar": snapshot.delivery_cost_sar,
        "support_cost_sar": snapshot.support_cost_sar,
        "other_cost_sar": snapshot.other_cost_sar,
        "margin_sar": snapshot.margin_sar,
        "margin_pct": snapshot.margin_pct,
        "notes": snapshot.notes,
        "hard_gates": _HARD_GATES,
    }


@router.get("/finance-brief")
async def finance_brief() -> dict[str, Any]:
    pipeline = get_default_pipeline()
    summary = pipeline.summary()
    brief = build_finance_brief(
        pipeline_summary=summary,
        payment_confirmations_count=len(list_confirmations()),
        invoice_drafts_count=sum(
            1 for inv in _INVOICES.values() if inv.status == "draft"
        ),
    )
    return {
        "cash_collected_sar": brief.cash_collected_sar,
        "commitments_open_sar": brief.commitments_open_sar,
        "pipeline_value_sar": brief.pipeline_value_sar,
        "paid_pilots_count": brief.paid_pilots_count,
        "committed_count": brief.committed_count,
        "payment_confirmations_count": brief.payment_confirmations_count,
        "invoice_drafts_count": brief.invoice_drafts_count,
        "avg_margin_pct": brief.avg_margin_pct,
        "data_status": brief.data_status,
        "blockers": brief.blockers,
        "next_action_ar": brief.next_action_ar,
        "next_action_en": brief.next_action_en,
        "hard_gates": _HARD_GATES,
    }


def _reset_invoices() -> None:
    """Test-only — wipe in-memory invoices."""
    _INVOICES.clear()
