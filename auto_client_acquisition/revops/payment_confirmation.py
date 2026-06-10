"""V12.5 RevOps — Manual payment confirmation record.

Hard rule: payment confirmation REQUIRES evidence. A draft invoice
is never payment. A verbal "yes" is never payment. Cash landing in
the bank or Moyasar dashboard is payment.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

PaymentMethod = Literal[
    "moyasar_test",
    "moyasar_live",
    "bank_transfer",
    "cash_in_person",
    "other_manual",
]


class PaymentConfirmation(BaseModel):
    """A founder-confirmed payment. The founder MUST attach evidence
    (screenshot reference / bank statement reference / Moyasar txn id)
    before a payment is recorded."""

    model_config = ConfigDict(extra="forbid")

    confirmation_id: str
    invoice_id: str
    customer_handle: str = Field(min_length=1, max_length=80)
    amount_sar: int = Field(gt=0)
    payment_method: PaymentMethod
    evidence_reference: str = Field(
        min_length=5,
        max_length=200,
        description=(
            "Required: 'moyasar_dashboard_screenshot.png', "
            "'bank_statement_2026MMDD_ref_X', etc."
        ),
    )
    confirmed_by: str = "founder"
    confirmed_at: datetime
    notes: str = ""


_RECORDS: list[PaymentConfirmation] = []


def record_payment_confirmation(
    *,
    invoice_id: str,
    customer_handle: str,
    amount_sar: int,
    payment_method: PaymentMethod,
    evidence_reference: str,
    notes: str = "",
) -> PaymentConfirmation:
    """Record a manual payment confirmation. Evidence is REQUIRED.

    Raises ValueError if evidence is missing or trivially short.
    """
    if not evidence_reference or len(evidence_reference) < 5:
        raise ValueError(
            "evidence_reference is required (min 5 chars). "
            "Acceptable: 'moyasar_dashboard_2026-MM-DD.png', "
            "'bank_statement_ref_123', 'cash_receipt_v0042.pdf'. "
            "Verbal yes is NOT acceptable."
        )
    now = datetime.now(UTC)
    cid = f"pcf_{invoice_id[-8:]}_{int(now.timestamp())}"
    confirmation = PaymentConfirmation(
        confirmation_id=cid,
        invoice_id=invoice_id,
        customer_handle=customer_handle,
        amount_sar=amount_sar,
        payment_method=payment_method,
        evidence_reference=evidence_reference,
        confirmed_at=now,
        notes=notes,
    )
    _RECORDS.append(confirmation)
    return confirmation


def list_confirmations() -> list[PaymentConfirmation]:
    return list(_RECORDS)


def reset_confirmations() -> None:
    """Test-only — wipe in-memory records."""
    _RECORDS.clear()
