"""Payment Handoff — records a founder-controlled payment step. Never charges.

A payment handoff is valid only when it is tied to an approved proposal and the
same Approval Center customer-specific quote fingerprint used by the canonical
invoice path. Legacy catalog taxonomy may identify the capability, but it is
never price authority. The module cannot create payment links, charge, send, or
publish anything.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.approval_center.schemas import ApprovalRequest, ApprovalStatus
from auto_client_acquisition.distribution_os import catalog
from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso
from auto_client_acquisition.distribution_os.proposal import ProposalStatus, get_proposal

_PRICE_AUTHORITY = "customer_specific_quote_after_qualified_discovery"
_QUOTE_AUTHORITY_SCHEMA = "dealix.customer-specific-quote-authority.v1"
_QUOTE_AUTHORITY_OBJECT_TYPE = "customer_specific_quote"
_QUOTE_AUTHORITY_ACTION_TYPE = "customer_specific_quote"
_CANONICAL_PRIMARY_OFFER_ID = "revenue_command_pilot_30d"
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


def _canonical_sar_amount(value: float) -> str:
    try:
        raw = Decimal(str(value))
        amount = raw.quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError("payment_handoff_invalid_customer_specific_quote_amount") from exc
    if raw != amount or amount <= 0:
        raise ValueError("payment_handoff_invalid_customer_specific_quote_amount")
    return format(amount, ".2f")


def _quote_authority_fingerprint(
    *,
    lead_id: str,
    amount_sar: float,
    discovery_ref: str,
    customer_specific_scope_ref: str,
) -> str:
    """Mirror the canonical quote-authority fingerprint contract exactly."""
    material = {
        "schema": _QUOTE_AUTHORITY_SCHEMA,
        "lead_id": lead_id.strip(),
        "offer_id": _CANONICAL_PRIMARY_OFFER_ID,
        "approved_amount_sar": _canonical_sar_amount(amount_sar),
        "qualified_discovery_ref": discovery_ref.strip(),
        "customer_specific_scope_ref": customer_specific_scope_ref.strip(),
    }
    encoded = json.dumps(
        material,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()


def _approval_is_unexpired(approval: ApprovalRequest) -> bool:
    return approval.expires_at is None or approval.expires_at > datetime.now(UTC)


def _validate_authority_binding(
    *,
    proposal_id: str,
    customer_id: str,
    product_id: str,
    amount_sar: float,
    discovery_ref: str,
    quote_id: str,
    quote_authority_ref: str,
    customer_specific_scope_ref: str,
) -> tuple[str, str]:
    """Return canonical customer id + quote fingerprint, or fail closed."""
    if not proposal_id.strip():
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
    if not quote_authority_ref.strip():
        raise ValueError("payment_handoff_requires_quote_authority_ref")
    if not customer_specific_scope_ref.strip():
        raise ValueError("payment_handoff_requires_customer_specific_scope_ref")
    canonical_amount = _canonical_sar_amount(amount_sar)

    stored_proposal = get_proposal(proposal_id.strip())
    if stored_proposal is None:
        raise ValueError("payment_handoff_requires_existing_proposal")
    if stored_proposal.approval_status != ProposalStatus.APPROVED.value:
        raise ValueError("payment_handoff_requires_approved_proposal")
    if stored_proposal.product_id != product_id:
        raise ValueError("payment_handoff_product_mismatch")
    if stored_proposal.discovery_ref != discovery_ref.strip():
        raise ValueError("payment_handoff_discovery_ref_mismatch")
    if stored_proposal.quote_id != quote_id.strip():
        raise ValueError("payment_handoff_quote_id_mismatch")
    if stored_proposal.customer_specific_quote_sar is None:
        raise ValueError("payment_handoff_proposal_quote_missing")
    if _canonical_sar_amount(stored_proposal.customer_specific_quote_sar) != canonical_amount:
        raise ValueError("payment_handoff_amount_mismatch")

    canonical_customer_id = stored_proposal.prospect_id.strip()
    if not canonical_customer_id:
        raise ValueError("payment_handoff_proposal_customer_missing")
    if customer_id.strip() and customer_id.strip() != canonical_customer_id:
        raise ValueError("payment_handoff_customer_mismatch")

    fingerprint = _quote_authority_fingerprint(
        lead_id=canonical_customer_id,
        amount_sar=amount_sar,
        discovery_ref=discovery_ref,
        customer_specific_scope_ref=customer_specific_scope_ref,
    )
    approval = get_default_approval_store().get(quote_authority_ref.strip())
    if approval is None:
        raise ValueError("payment_handoff_quote_authority_not_found")
    if ApprovalStatus(approval.status) != ApprovalStatus.APPROVED:
        raise ValueError("payment_handoff_quote_authority_not_approved")
    if not _approval_is_unexpired(approval):
        raise ValueError("payment_handoff_quote_authority_expired")

    binding_matches = (
        approval.object_type == _QUOTE_AUTHORITY_OBJECT_TYPE
        and approval.action_type == _QUOTE_AUTHORITY_ACTION_TYPE
        and approval.object_id == fingerprint
        and approval.action_id == f"quote:{fingerprint}"
        and approval.lead_id == canonical_customer_id
        and approval.audit_ref == discovery_ref.strip()
        and approval.proof_target == f"invoice_authority:{fingerprint}"
    )
    if not binding_matches:
        raise ValueError("payment_handoff_quote_authority_fingerprint_mismatch")
    return canonical_customer_id, fingerprint


@dataclass
class PaymentHandoff:
    id: str = field(default_factory=lambda: f"pay_{uuid4().hex[:12]}")
    proposal_id: str = ""
    customer_id: str = ""
    product_id: str = ""
    discovery_ref: str = ""
    quote_id: str = ""
    quote_authority_ref: str = ""
    customer_specific_scope_ref: str = ""
    quote_fingerprint: str = ""
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
    quote_authority_ref: str = "",
    customer_specific_scope_ref: str = "",
    notes: str = "",
) -> PaymentHandoff:
    """Record a pending payment handoff from an approved quote fingerprint.

    The persisted proposal and Approval Center quote are both authoritative
    inputs. Caller-supplied approval flags are intentionally not accepted. This
    function never sends, charges, creates a payment link, or verifies payment.
    """
    canonical_customer_id, fingerprint = _validate_authority_binding(
        proposal_id=proposal_id,
        customer_id=customer_id,
        product_id=product_id,
        amount_sar=amount_sar,
        discovery_ref=discovery_ref,
        quote_id=quote_id,
        quote_authority_ref=quote_authority_ref,
        customer_specific_scope_ref=customer_specific_scope_ref,
    )
    handoff = PaymentHandoff(
        proposal_id=proposal_id.strip(),
        customer_id=canonical_customer_id,
        product_id=product_id,
        discovery_ref=discovery_ref.strip(),
        quote_id=quote_id.strip(),
        quote_authority_ref=quote_authority_ref.strip(),
        customer_specific_scope_ref=customer_specific_scope_ref.strip(),
        quote_fingerprint=fingerprint,
        amount_sar=float(amount_sar),
        approvals=_empty_approvals(),
        status=PaymentHandoffStatus.PENDING_APPROVAL.value,
        governance_status="requires_founder_approval",
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
    """Update one local approval; final promotion revalidates quote authority."""
    if key not in _REQUIRED_APPROVALS:
        raise ValueError(f"unknown_approval:{key}")
    handoff = get_handoff(handoff_id)
    if handoff is None:
        return None
    approvals = dict(handoff.approvals)
    approvals[key] = bool(value)
    approved = _all_approved(approvals)
    if approved:
        _, fingerprint = _validate_authority_binding(
            proposal_id=handoff.proposal_id,
            customer_id=handoff.customer_id,
            product_id=handoff.product_id,
            amount_sar=handoff.amount_sar,
            discovery_ref=handoff.discovery_ref,
            quote_id=handoff.quote_id,
            quote_authority_ref=handoff.quote_authority_ref,
            customer_specific_scope_ref=handoff.customer_specific_scope_ref,
        )
        if fingerprint != handoff.quote_fingerprint:
            raise ValueError("payment_handoff_stored_quote_fingerprint_mismatch")
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