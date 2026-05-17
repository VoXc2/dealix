"""Partner engine — classify partners and gate commission eligibility (no LLM, no I/O).

Not every partner is an affiliate. This module sorts a partner into one of five
types and answers a single hard question: *is a commission payout allowed yet?*

Two non-negotiable guardrails are enforced:

* No commission payout before the customer invoice is paid.
* No white-label partnership before three completed Proof Packs.

This module contains **no payout execution path** — it only returns an
eligibility verdict. The affiliate engine itself remains documentation-only
(see ``docs/distribution-os/AFFILIATE_GOVERNANCE_SPEC.md``).
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


class PartnerType(StrEnum):
    """The five partner relationship types."""

    REFERRAL = "referral"
    IMPLEMENTATION = "implementation"
    CO_SELLING = "co_selling"
    SERVICE_EXCHANGE = "service_exchange"
    WHITE_LABEL = "white_label"


WHITE_LABEL_MIN_PROOF_PACKS = 3


def classify_partner(
    *,
    can_refer: bool = False,
    can_deliver: bool = False,
    sells_alongside: bool = False,
    trades_service: bool = False,
    rebrands_product: bool = False,
) -> PartnerType:
    """Classify a partner from what they can do.

    Checked most-committed first: a partner who rebrands the product is
    white-label even if they can also refer.
    """
    if rebrands_product:
        return PartnerType.WHITE_LABEL
    if sells_alongside:
        return PartnerType.CO_SELLING
    if can_deliver:
        return PartnerType.IMPLEMENTATION
    if trades_service:
        return PartnerType.SERVICE_EXCHANGE
    if can_refer:
        return PartnerType.REFERRAL
    return PartnerType.REFERRAL


@dataclass(frozen=True, slots=True)
class CommissionContext:
    """Inputs to a commission-eligibility check."""

    partner_type: PartnerType
    invoice_paid: bool
    completed_proof_packs: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def commission_eligible(ctx: CommissionContext) -> tuple[bool, str]:
    """Return ``(eligible, reason)`` for paying a partner commission.

    Both guardrails are hard: a failing context can never be overridden here.
    """
    if not ctx.invoice_paid:
        return False, "no_payout_before_invoice_paid"
    if (
        ctx.partner_type == PartnerType.WHITE_LABEL
        and ctx.completed_proof_packs < WHITE_LABEL_MIN_PROOF_PACKS
    ):
        return False, "white_label_requires_3_proof_packs"
    return True, "eligible"


__all__ = [
    "WHITE_LABEL_MIN_PROOF_PACKS",
    "CommissionContext",
    "PartnerType",
    "classify_partner",
    "commission_eligible",
]
