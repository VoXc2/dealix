"""Payment Handoff — records a founder-controlled payment step. Never charges.

A payment handoff is valid only when it is tied to a documented customer-
specific quote. Legacy catalog taxonomy may identify the capability, but it is
never price authority. The module cannot create payment links, charge, send, or
publish anything.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os import catalog
from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso

_PRICE_AUTHORITY = "customer_specific_quote_after_qualified_discovery"
_REQUIRED_APPROVALS: tuple[str, ...] = (
    "proposal_approved",
    "scope_confirmed",
    "price_confirmed",
    "decision_maker_confirmed",
    "risk_reviewed",
    "founder_approved",
)


class PaymentHandoffStatus(StrEnum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT = "sent"  # recorded only after separately authorized founder action
    PAID = "paid"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


def _empty_approvals() -> dict[str, bool]:
    return dict.fromkeys(_REQUIRED_APPROVALS, False)


@dataclass
class PaymentHandoff:
    id: str = field(default_factory=lambda: f"pay_{uuid4().hex[:12]}")
    proposal_id: str = ""
    customer_id: str = ""
    product_id: str = ""
    discovery_ref: str = ""
    quote_id: str = ""
    amount_sar: float = 0.0
    price_authority: str = _PRICE_AUTHORITY
    public_fixed_price: bool = False
    live_charge_allowed: bool = False
    external_send_allowed: bool = False
    status: str = PaymentHandoffStatus.PENDING_APPROVAL.value
    approvals: dict[str, bool] = field(default_factory=_empty_approvals)
    governance_status: str = "requires_founder_approval"
    notes: str = ""
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(
    env_var="DEALIX_PAYMENT_HANDOFFS_PATH",
    default_rel="var/payment_handoffs.jsonl",
    id_field="id",
)


def _all_approved(approvals: dict[str, bool]) -> bool:
    return all(bool(approvals.get(k)) for k in _REQUIRED_APPROVALS)


def prepare_handoff(
    *,
    proposal_id: str,
    customer_id: str,
    product_id: str,
    amount_sar: float,
    discovery_ref: str = "",
    quote_id: str = "",
    approvals: dict[str, bool] | None = None,
    notes: str = "",
) -> PaymentHandoff:
    """Record a payment handoff from explicit quote evidence.

    No catalog price lookup is allowed here. A positive amount must be bound to
    qualified discovery and a customer-specific quote. The Free Mini Diagnostic
    is not payable and therefore cannot create a payment handoff.
    """
    if not proposal_id:
        raise ValueError("proposal_id is required (no handoff without a proposal)")
    product = catalog.product_by_id(product_id)
    if product is None:
        raise ValueError(f"unknown_product_id:{product_id}")
    if product.tier == catalog.ProductTier.FREE_DIAGNOSTIC:
        raise ValueError("free_diagnostic_has_no_payment_handoff")
    if not discovery_ref.strip():
        raise ValueError("payment_handoff_requires_discovery_ref")
    if not quote_id.strip():
        raise ValueError("payment_handoff_requires_quote_id")
    if amount_sar <= 0:
        raise ValueError("payment_handoff_requires_positive_customer_specific_quote")

    merged = _empty_approvals()
    for key, val in (approvals or {}).items():
        if key in merged:
            merged[key] = bool(val)

    approved = _all_approved(merged)
    handoff = PaymentHandoff(
        proposal_id=proposal_id,
        customer_id=customer_id,
        product_id=product_id,
        discovery_ref=discovery_ref.strip(),
        quote_id=quote_id.strip(),
        amount_sar=float(amount_sar),
        approvals=merged,
        status=(
            PaymentHandoffStatus.APPROVED.value
            if approved
            else PaymentHandoffStatus.PENDING_APPROVAL.value
        ),
        governance_status="approved" if approved else "requires_founder_approval",
        notes=notes,
    )
    _store.append(handoff.to_dict())
    return handoff


def get_handoff(handoff_id: str) -> PaymentHandoff | None:
    rec = _store.get(handoff_id)
    return PaymentHandoff(**rec) if rec else None


def list_handoffs(*, status: str | None = None) -> list[PaymentHandoff]:
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    handoffs = [PaymentHandoff(**rec) for rec in latest.values()]
    if status is not None:
        handoffs = [h for h in handoffs if h.status == status]
    return handoffs


def set_approval(handoff_id: str, key: str, value: bool = True) -> PaymentHandoff | None:
    """Flip one approval flag; promotes status to approved when all are true."""
    if key not in _REQUIRED_APPROVALS:
        raise ValueError(f"unknown_approval:{key}")
    handoff = get_handoff(handoff_id)
    if handoff is None:
        return None
    approvals = dict(handoff.approvals)
    approvals[key] = bool(value)
    approved = _all_approved(approvals)
    rec = _store.patch(
        handoff_id,
        {
            "approvals": approvals,
            "status": (
                PaymentHandoffStatus.APPROVED.value
                if approved
                else PaymentHandoffStatus.PENDING_APPROVAL.value
            ),
            "governance_status": "approved" if approved else "requires_founder_approval",
        },
    )
    return PaymentHandoff(**rec) if rec else None


def cancel_handoff(handoff_id: str, reason: str = "") -> PaymentHandoff | None:
    rec = _store.patch(
        handoff_id,
        {"status": PaymentHandoffStatus.CANCELLED.value, "notes": reason},
    )
    return PaymentHandoff(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "PaymentHandoff",
    "PaymentHandoffStatus",
    "cancel_handoff",
    "clear_for_test",
    "get_handoff",
    "list_handoffs",
    "prepare_handoff",
    "set_approval",
]
