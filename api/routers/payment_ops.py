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

T13a — `invoice-intent` now offers a real Moyasar hosted-checkout URL
when `method == "moyasar_test"` AND `MOYASAR_SECRET_KEY` is set, so
the landing checkout flow stops dead-ending at a "TEST mode" panel.
The constitutional "no_live_charge" gate is preserved — `moyasar_live`
still requires the env opt-in, and we never auto-flip the payment to
`payment_confirmed`; the founder still confirms manually after
evidence upload.
"""
from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.payment_ops import (
    confirm_payment,
    create_invoice_intent,
    get_payment_state,
    kickoff_delivery,
    upload_manual_evidence,
)
from core.logging import get_logger

router = APIRouter(prefix="/api/v1/payment-ops", tags=["payment-ops"])
log = get_logger(__name__)

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


async def _maybe_attach_moyasar_url(
    rec_dump: dict[str, Any],
    *,
    amount_sar: float,
    method: str,
    service_session_id: str | None,
    customer_handle: str,
) -> dict[str, Any]:
    """Best-effort: attach a real Moyasar hosted-checkout URL to the
    payment record when the env keys allow it.

    Returns the (possibly enriched) rec_dump. Never raises — a Moyasar
    upstream failure here must not break the invoice-intent contract,
    so the founder's manual bank-transfer path remains usable.
    """
    if method != "moyasar_test":
        return rec_dump
    if not os.getenv("MOYASAR_SECRET_KEY", "").strip():
        rec_dump["checkout_url"] = None
        rec_dump["checkout_mode"] = "test_no_gateway"
        return rec_dump
    try:
        from dealix.payments.moyasar import MoyasarClient

        client = MoyasarClient()
        callback_base = os.getenv("APP_URL", "https://dealix.me")
        invoice = await client.create_invoice(
            amount_halalas=int(round(amount_sar * 100)),
            currency="SAR",
            description=f"Dealix — {service_session_id or 'service'}",
            callback_url=f"{callback_base}/checkout/return",
            metadata={
                "tier": service_session_id or "",
                "intent_id": rec_dump.get("invoice_intent_id", ""),
                "payment_id": rec_dump.get("payment_id", ""),
                "source": "payment-ops.invoice-intent",
            },
        )
        rec_dump["checkout_url"] = invoice.get("url")
        rec_dump["moyasar_invoice_id"] = invoice.get("id")
        rec_dump["checkout_mode"] = "moyasar_test"
        log.info(
            "moyasar_intent_attached",
            payment_id=rec_dump.get("payment_id"),
            moyasar_invoice_id=invoice.get("id"),
            tier=service_session_id,
        )
    except Exception:
        log.exception(
            "moyasar_intent_attach_failed",
            payment_id=rec_dump.get("payment_id"),
            tier=service_session_id,
        )
        rec_dump["checkout_url"] = None
        rec_dump["checkout_mode"] = "test_upstream_error"
    return rec_dump


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
    rec_dump = rec.model_dump(mode="json")
    rec_dump = await _maybe_attach_moyasar_url(
        rec_dump,
        amount_sar=float(amount_sar),
        method=str(method),
        service_session_id=payload.get("service_session_id"),
        customer_handle=str(customer_handle),
    )
    return {
        "payment": rec_dump,
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
    }
