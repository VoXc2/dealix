"""
Commercial guardrails: proposals, pricing, payment handoff, renewals, and
won-deal -> delivery handoff.

These encode the non-negotiable commercial gates:
  * Payment handoff requires explicit human approval.
  * A proposal must map to a real product/service in the catalog.
  * A proposal requires a *qualified* opportunity.
  * A final price requires human approval (AI may only propose a range).
  * Renewal requires demonstrated delivered value.
  * A won deal must hand off to delivery (and customer success) before work.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List, Optional


@dataclass
class GateResult:
    allowed: bool
    reasons: List[str] = field(default_factory=list)
    requires_human: bool = True

    def as_dict(self) -> Dict:
        return {"allowed": self.allowed, "reasons": self.reasons, "requires_human": self.requires_human}


# --- Payment handoff -------------------------------------------------------

def payment_handoff(opportunity: Dict) -> GateResult:
    """Payment handoff is only allowed with explicit human approval.

    AI may *prepare* a payment handoff (collect details, draft the message)
    but the handoff itself never proceeds without ``approved_by_human=True``.
    """
    reasons: List[str] = []
    if not opportunity.get("approved_by_human"):
        reasons.append("payment_handoff_requires_human_approval")
    if not opportunity.get("qualified"):
        reasons.append("payment_handoff_requires_qualified_opportunity")
    return GateResult(allowed=len(reasons) == 0, reasons=reasons, requires_human=True)


# --- Proposals -------------------------------------------------------------

def _catalog_ids(product_catalog: Iterable) -> set:
    ids = set()
    for item in product_catalog or []:
        if isinstance(item, dict):
            for key in ("id", "sku", "code", "name"):
                if item.get(key):
                    ids.add(str(item[key]))
        else:
            ids.add(str(item))
    return ids


def evaluate_proposal(proposal: Dict, product_catalog: Iterable) -> GateResult:
    """Validate a proposal against commercial gates.

    A proposal is allowed only when:
      * it references a product/service that exists in the catalog,
      * the opportunity is qualified,
      * any *final* price carries human approval (a range is fine without it).
    """
    reasons: List[str] = []
    ids = _catalog_ids(product_catalog)

    product_ref = str(proposal.get("product_id") or proposal.get("product") or "")
    if not product_ref or product_ref not in ids:
        reasons.append("proposal_not_mapped_to_catalog")

    if not proposal.get("qualified_opportunity") and not proposal.get("qualified"):
        reasons.append("proposal_requires_qualified_opportunity")

    # Final price requires approval; a quoted range is allowed pre-approval.
    if proposal.get("final_price") is not None and not proposal.get("price_approved_by_human"):
        reasons.append("final_price_requires_human_approval")

    return GateResult(allowed=len(reasons) == 0, reasons=reasons, requires_human=True)


# --- Renewals --------------------------------------------------------------

def renewal_allowed(account: Dict) -> GateResult:
    """Renewal requires evidence of delivered value to the client."""
    reasons: List[str] = []
    if not account.get("delivered_value"):
        reasons.append("renewal_requires_delivered_value")
    if not account.get("delivery_completed"):
        reasons.append("renewal_requires_completed_delivery")
    return GateResult(allowed=len(reasons) == 0, reasons=reasons, requires_human=True)


# --- Won deal -> delivery handoff -----------------------------------------

def won_deal_handoff(deal: Dict) -> GateResult:
    """A won deal must produce a delivery handoff (and CS handoff) before work.

    Without a delivery handoff, the deal cannot move into execution — this
    prevents over-promising and silent scope drift.
    """
    reasons: List[str] = []
    if deal.get("stage") == "won" or deal.get("won") is True:
        if not deal.get("delivery_handoff"):
            reasons.append("won_deal_requires_delivery_handoff")
        if not deal.get("customer_success_handoff"):
            reasons.append("won_deal_requires_customer_success_handoff")
    return GateResult(allowed=len(reasons) == 0, reasons=reasons, requires_human=True)
