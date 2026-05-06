"""V12.5 RevOps — Invoice lifecycle state machine.

Status transitions:
  draft → sent → paid       (happy path)
       ↘     ↘
        voided  refunded   (any time)
"""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

InvoiceStatus = Literal["draft", "sent", "paid", "refunded", "voided"]


_ALLOWED: dict[InvoiceStatus, set[InvoiceStatus]] = {
    "draft": {"sent", "voided"},
    "sent": {"paid", "voided"},
    "paid": {"refunded"},
    "refunded": set(),
    "voided": set(),
}


class InvoiceState(BaseModel):
    """A single invoice's lifecycle record. Placeholder customer_handle
    only — never real customer name."""

    model_config = ConfigDict(extra="forbid")

    invoice_id: str
    customer_handle: str = Field(min_length=1, max_length=80)
    amount_sar: int = Field(gt=0, le=50000)
    amount_halalah: int
    description: str = ""
    status: InvoiceStatus = "draft"
    moyasar_id: str | None = None
    payment_url: str | None = None
    mode: Literal["test", "live", "manual_only"] = "test"
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def _invoice_id(customer: str, amount: int, ts: datetime) -> str:
    digest = hashlib.sha256(
        f"{customer}|{amount}|{ts.isoformat()}".encode("utf-8")
    ).hexdigest()
    return f"inv_{digest[:16]}"


def create_invoice_draft(
    *,
    customer_handle: str,
    amount_sar: int,
    description: str = "",
    mode: Literal["test", "manual_only"] = "test",
) -> InvoiceState:
    """Create an invoice in DRAFT state. Drafts NEVER count as revenue."""
    if amount_sar <= 0:
        raise ValueError("amount_sar must be > 0")
    if amount_sar > 50000:
        raise ValueError("amount_sar must be ≤ 50000 (safety cap)")
    now = datetime.now(UTC)
    return InvoiceState(
        invoice_id=_invoice_id(customer_handle, amount_sar, now),
        customer_handle=customer_handle,
        amount_sar=amount_sar,
        amount_halalah=amount_sar * 100,
        description=description,
        status="draft",
        mode=mode,
        created_at=now,
        updated_at=now,
    )


def transition_invoice(
    invoice: InvoiceState, target: InvoiceStatus
) -> InvoiceState:
    """Forward-only transition. Returns a new InvoiceState (immutable input).

    Raises ValueError if transition not allowed.
    """
    allowed = _ALLOWED.get(invoice.status, set())
    if target not in allowed:
        raise ValueError(
            f"invalid invoice transition: {invoice.status!r} → {target!r}; "
            f"allowed: {sorted(allowed)}"
        )
    return invoice.model_copy(update={
        "status": target,
        "updated_at": datetime.now(UTC),
    })
