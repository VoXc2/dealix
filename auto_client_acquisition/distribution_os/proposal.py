"""Proposal Factory — evidence-bound, quote-only, approval-first.

A legacy catalog product may identify a capability taxonomy, but it is never
price authority for a paid proposal. Paid proposals require qualified discovery
plus a documented customer-specific quote. The Free Mini Diagnostic remains a
zero-price entry motion and does not require a paid quote.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.distribution_os import catalog
from auto_client_acquisition.distribution_os._store import JsonlStore, now_iso
from auto_client_acquisition.distribution_os.draft_quality import check_draft

_PRICE_AUTHORITY = "customer_specific_quote_after_qualified_discovery"


class ProposalStatus(StrEnum):
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    REJECTED = "rejected"
    SENT = "sent"  # reserved; recorded only after a separately authorized send


@dataclass
class Proposal:
    id: str = field(default_factory=lambda: f"prop_{uuid4().hex[:12]}")
    prospect_id: str = ""
    product_id: str = ""
    sector: str = ""
    problem: str = ""
    proposed_solution: str = ""
    scope: list[str] = field(default_factory=list)
    out_of_scope: list[str] = field(default_factory=list)
    timeline: str = ""
    discovery_ref: str = ""
    quote_id: str = ""
    customer_specific_quote_sar: float | None = None
    price_min_sar: float = 0.0
    price_max_sar: float = 0.0
    price_authority: str = _PRICE_AUTHORITY
    public_fixed_price: bool = False
    external_send_allowed: bool = False
    assumptions: list[str] = field(default_factory=list)
    evidence_level: int = 0
    risks: list[str] = field(default_factory=list)
    payment_terms: str = ""
    next_step: str = ""
    approval_status: str = ProposalStatus.PENDING_APPROVAL.value
    quality_issues: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=now_iso)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_store = JsonlStore(
    env_var="DEALIX_PROPOSALS_PATH", default_rel="var/proposals.jsonl", id_field="id"
)


def generate_proposal(
    *,
    prospect_id: str,
    product_id: str,
    sector: str = "",
    problem: str = "",
    proposed_solution: str = "",
    scope: list[str] | None = None,
    out_of_scope: list[str] | None = None,
    timeline: str = "",
    discovery_ref: str = "",
    quote_id: str = "",
    customer_specific_quote_sar: float | None = None,
    assumptions: list[str] | None = None,
    evidence_level: int = 0,
    risks: list[str] | None = None,
    payment_terms: str = "",
    next_step: str = "",
) -> Proposal:
    """Build an internal proposal draft under current commercial authority.

    Paid capability taxonomy entries require discovery + quote evidence. The
    catalog is used only to validate the capability id, never to infer price.
    """
    if not prospect_id:
        raise ValueError("prospect_id is required (no proposal without a prospect)")
    product = catalog.product_by_id(product_id)
    if product is None:
        raise ValueError(f"unknown_product_id:{product_id}")
    out_scope = out_of_scope or []
    if not out_scope:
        raise ValueError("out_of_scope must not be empty (no open scope)")

    is_free_entry = product.tier == catalog.ProductTier.FREE_DIAGNOSTIC
    if is_free_entry:
        if customer_specific_quote_sar not in (None, 0, 0.0):
            raise ValueError("free_diagnostic_cannot_carry_paid_quote")
        quote_amount = 0.0
    else:
        if not discovery_ref.strip():
            raise ValueError("paid_proposal_requires_discovery_ref")
        if not quote_id.strip():
            raise ValueError("paid_proposal_requires_quote_id")
        if customer_specific_quote_sar is None or customer_specific_quote_sar <= 0:
            raise ValueError("paid_proposal_requires_customer_specific_quote")
        quote_amount = float(customer_specific_quote_sar)

    proposal = Proposal(
        prospect_id=prospect_id,
        product_id=product_id,
        sector=sector,
        problem=problem,
        proposed_solution=proposed_solution,
        scope=scope or [],
        out_of_scope=out_scope,
        timeline=timeline,
        discovery_ref=discovery_ref.strip(),
        quote_id=quote_id.strip(),
        customer_specific_quote_sar=(None if is_free_entry else quote_amount),
        price_min_sar=quote_amount,
        price_max_sar=quote_amount,
        assumptions=assumptions or [],
        evidence_level=evidence_level,
        risks=risks or [],
        payment_terms=payment_terms,
        next_step=next_step,
    )
    narrative = " ".join([problem, proposed_solution, next_step, payment_terms])
    quality = check_draft(text=narrative, max_chars=10000)
    if quality.decision == "block":
        raise ValueError(f"proposal_narrative_blocked:{','.join(quality.issues)}")
    proposal.quality_issues = list(quality.issues)
    _store.append(proposal.to_dict())
    return proposal


def get_proposal(proposal_id: str) -> Proposal | None:
    rec = _store.get(proposal_id)
    return Proposal(**rec) if rec else None


def list_proposals(*, approval_status: str | None = None) -> list[Proposal]:
    latest: dict[str, dict[str, Any]] = {}
    for rec in _store.list():
        latest[str(rec.get("id"))] = rec
    proposals = [Proposal(**rec) for rec in latest.values()]
    if approval_status is not None:
        proposals = [p for p in proposals if p.approval_status == approval_status]
    return proposals


def approve_proposal(proposal_id: str) -> Proposal | None:
    rec = _store.patch(proposal_id, {"approval_status": ProposalStatus.APPROVED.value})
    return Proposal(**rec) if rec else None


def reject_proposal(proposal_id: str) -> Proposal | None:
    rec = _store.patch(proposal_id, {"approval_status": ProposalStatus.REJECTED.value})
    return Proposal(**rec) if rec else None


def clear_for_test() -> None:
    _store.clear_for_test()


__all__ = [
    "Proposal",
    "ProposalStatus",
    "approve_proposal",
    "clear_for_test",
    "generate_proposal",
    "get_proposal",
    "list_proposals",
    "reject_proposal",
]
