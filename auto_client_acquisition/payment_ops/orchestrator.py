"""Payment Ops orchestrator — single state machine for one payment.

Wraps revops/invoice_state + revops/payment_confirmation while adding
the customer_handle envelope + delivery_kickoff trigger.

Storage: in-memory + JSONL (data/payment_states.jsonl).

Hard rule: NO_LIVE_CHARGE — Moyasar mode must NOT be 'live' unless the
explicit env var DEALIX_MOYASAR_MODE=live is set. We default to manual.
"""
from __future__ import annotations

import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import (
    PaymentMethod,
    PaymentStateRecord,
    PaymentStatus,
)

_JSONL_PATH = os.path.join("data", "payment_states.jsonl")
_INDEX: dict[str, PaymentStateRecord] = {}

# Status transition truth table
_TRANSITIONS: dict[PaymentStatus, set[PaymentStatus]] = {
    "invoice_intent": {"invoice_sent_manual", "voided"},
    "invoice_sent_manual": {"payment_pending", "voided"},
    "payment_pending": {"payment_evidence_uploaded", "voided"},
    "payment_evidence_uploaded": {"payment_confirmed", "voided"},
    "payment_confirmed": {"delivery_kickoff", "refunded"},
    "delivery_kickoff": {"refunded"},
    "refunded": set(),
    "voided": set(),
}


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(rec: PaymentStateRecord) -> None:
    _ensure_dir()
    _INDEX[rec.payment_id] = rec
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(rec.model_dump_json() + "\n")


def _check_transition(current: PaymentStatus, target: PaymentStatus) -> bool:
    return target in _TRANSITIONS.get(current, set())


def _enforce_no_live_charge(method: PaymentMethod) -> None:
    """Refuse moyasar_live unless explicit env opt-in."""
    if method == "moyasar_live" and os.environ.get("DEALIX_MOYASAR_MODE") != "live":
        raise ValueError(
            "moyasar_live requires DEALIX_MOYASAR_MODE=live env var "
            "(NO_LIVE_CHARGE gate)"
        )


def create_invoice_intent(
    *,
    customer_handle: str,
    amount_sar: float,
    method: PaymentMethod,
    service_session_id: str | None = None,
) -> PaymentStateRecord:
    _enforce_no_live_charge(method)
    rec = PaymentStateRecord(
        payment_id=f"pay_{uuid.uuid4().hex[:10]}",
        customer_handle=customer_handle,
        service_session_id=service_session_id,
        invoice_intent_id=f"inv_intent_{uuid.uuid4().hex[:8]}",
        amount_sar=amount_sar,
        method=method,
        status="invoice_intent",
    )
    _persist(rec)
    return rec


def upload_manual_evidence(
    *,
    payment_id: str,
    evidence_reference: str,
) -> tuple[PaymentStateRecord | None, str]:
    """Upload bank-transfer receipt or screenshot reference."""
    rec = _INDEX.get(payment_id)
    if rec is None:
        return (None, "payment_not_found")
    # Allow upload from any pre-confirmed state
    if rec.status not in (
        "invoice_intent", "invoice_sent_manual", "payment_pending"
    ):
        return (None, f"cannot_upload_evidence_in_state:{rec.status}")
    if not evidence_reference or len(evidence_reference) < 5:
        return (None, "evidence_reference_must_be_at_least_5_chars")
    rec.status = "payment_evidence_uploaded"
    rec.evidence_reference = evidence_reference
    _persist(rec)
    return (rec, "evidence_uploaded")


def confirm_payment(
    *,
    payment_id: str,
    confirmed_by: str,
) -> tuple[PaymentStateRecord | None, str]:
    """Founder confirms payment received. Required before delivery_kickoff.

    Hard rule: must have evidence_reference (uploaded) before confirm.
    """
    rec = _INDEX.get(payment_id)
    if rec is None:
        return (None, "payment_not_found")
    if rec.status != "payment_evidence_uploaded":
        return (None, f"cannot_confirm_in_state:{rec.status}")
    if not rec.evidence_reference:
        return (None, "evidence_reference_missing")
    if not confirmed_by:
        return (None, "confirmed_by_required")
    rec.status = "payment_confirmed"
    rec.confirmed_by = confirmed_by
    rec.confirmed_at = datetime.now(timezone.utc)
    _persist(rec)
    return (rec, "payment_confirmed")


def kickoff_delivery(
    *,
    payment_id: str,
) -> tuple[PaymentStateRecord | None, str]:
    """Trigger delivery — only after payment_confirmed."""
    rec = _INDEX.get(payment_id)
    if rec is None:
        return (None, "payment_not_found")
    if rec.status != "payment_confirmed":
        return (None, "delivery_requires_payment_confirmed")
    rec.status = "delivery_kickoff"
    rec.delivery_kickoff_id = f"dk_{uuid.uuid4().hex[:8]}"
    _persist(rec)
    return (rec, "delivery_kicked_off")


def get_payment_state(payment_id: str) -> PaymentStateRecord | None:
    return _INDEX.get(payment_id)
