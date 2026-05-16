"""Payment Ops HTTP surface.

  POST /api/v1/payment-ops/invoice-intent
  POST /api/v1/payment-ops/manual-evidence
  POST /api/v1/payment-ops/confirm
  POST /api/v1/payment-ops/{id}/kickoff-delivery
  GET  /api/v1/payment-ops/{id}/state

Hard rules:
- invoice_created != revenue
- payment_confirmed = revenue (only after evidence_reference)
- delivery starts ONLY after payment_confirmed
- moyasar_live blocked unless DEALIX_MOYASAR_MODE=live env opt-in
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.payment_ops import (
    confirm_payment,
    create_invoice_intent,
    get_payment_state,
    kickoff_delivery,
    upload_manual_evidence,
)

router = APIRouter(prefix="/api/v1/payment-ops", tags=["payment-ops"])

_HARD_GATES: dict[str, bool] = {
    "no_live_charge": True,
    "no_fake_revenue": True,
    "evidence_reference_required_for_confirm": True,
    "delivery_requires_payment_confirmed": True,
}

_VALID_METHODS = {
    "moyasar_test", "moyasar_live", "bank_transfer",
    "cash_in_person", "manual_other",
}


@router.post("/invoice-intent")
async def invoice_intent(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    customer_handle = payload.get("customer_handle")
    amount_sar = payload.get("amount_sar")
    method = payload.get("method")
    if not customer_handle or amount_sar is None or not method:
        raise HTTPException(
            status_code=422,
            detail="customer_handle + amount_sar + method required",
        )
    if method not in _VALID_METHODS:
        raise HTTPException(status_code=422, detail=f"invalid method: {method}")
    try:
        rec = create_invoice_intent(
            customer_handle=customer_handle,
            amount_sar=float(amount_sar),
            method=method,
            service_session_id=payload.get("service_session_id"),
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    return {
        "payment": rec.model_dump(mode="json"),
        "warning_invoice_not_revenue": "invoice_intent != revenue",
        "hard_gates": _HARD_GATES,
    }


@router.post("/manual-evidence")
async def manual_evidence(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    payment_id = payload.get("payment_id")
    evidence_reference = payload.get("evidence_reference")
    if not payment_id or not evidence_reference:
        raise HTTPException(
            status_code=422,
            detail="payment_id + evidence_reference required",
        )
    rec, reason = upload_manual_evidence(
        payment_id=payment_id,
        evidence_reference=evidence_reference,
    )
    if rec is None:
        raise HTTPException(status_code=409, detail=reason)
    return {
        "payment": rec.model_dump(mode="json"),
        "transition_reason": reason,
        "hard_gates": _HARD_GATES,
    }


@router.post("/confirm")
async def confirm(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    payment_id = payload.get("payment_id")
    confirmed_by = payload.get("confirmed_by")
    if not payment_id or not confirmed_by:
        raise HTTPException(
            status_code=422,
            detail="payment_id + confirmed_by required",
        )
    rec, reason = confirm_payment(
        payment_id=payment_id, confirmed_by=confirmed_by,
    )
    if rec is None:
        raise HTTPException(status_code=409, detail=reason)
    return {
        "payment": rec.model_dump(mode="json"),
        "transition_reason": reason,
        "is_revenue_now": True,
        "hard_gates": _HARD_GATES,
    }


@router.get("/{payment_id}/state")
async def state(payment_id: str) -> dict[str, Any]:
    rec = get_payment_state(payment_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="payment_not_found")
    return {
        "payment": rec.model_dump(mode="json"),
        "is_revenue": rec.status in ("payment_confirmed", "delivery_kickoff"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{payment_id}/kickoff-delivery")
async def kickoff(payment_id: str) -> dict[str, Any]:
    rec, reason = kickoff_delivery(payment_id=payment_id)
    if rec is None:
        raise HTTPException(status_code=409, detail=reason)
    return {
        "payment": rec.model_dump(mode="json"),
        "delivery_kickoff_id": rec.delivery_kickoff_id,
        "transition_reason": reason,
        "hard_gates": _HARD_GATES,
        # The Sprint is not auto-run: at kickoff the customer's data is not
        # yet uploaded. The founder runs it next, passing delivery_kickoff_id
        # as engagement_id — that id is the audit link between payment and
        # delivery.
        "next_action": {
            "step": "run_sprint",
            "endpoint": "POST /api/v1/sprint/run",
            "engagement_id": rec.delivery_kickoff_id,
            "customer_id": rec.customer_handle,
            "note": (
                "Run the Sprint with the customer's data, then render the "
                "Proof Pack via POST /api/v1/sprint/render/pdf."
            ),
        },
    }
