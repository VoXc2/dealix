"""Affiliate commission computation — pure logic, no I/O.

A ``Commission`` is computed as a DRAFT the moment a deal is registered.
It only becomes payable after the deal invoice reaches ``paid`` AND a
founder ApprovalRequest is approved. Refund inside the clawback window
reverses it. See ``eligibility.py`` and ``clawback.py``.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import uuid4

from auto_client_acquisition.affiliate_os.tiers import (
    AffiliateTier,
    commission_rate,
    is_handoff_tier,
)


class CommissionStatus(StrEnum):
    PENDING = "pending"          # computed; deal invoice not yet paid
    ELIGIBLE = "eligible"        # invoice paid + lead clean → payout can be requested
    PAYOUT_REQUESTED = "payout_requested"  # ApprovalRequest opened, awaiting founder
    PAID = "paid"                # payout confirmed after approval
    CLAWED_BACK = "clawed_back"  # refund inside the clawback window
    VOID = "void"                # disqualified (disallowed lead, etc.)


def _now() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class Commission:
    commission_id: str = field(default_factory=lambda: f"com_{uuid4().hex[:12]}")
    affiliate_id: str = ""
    referral_id: str = ""
    deal_invoice_id: str = ""
    tier: str = AffiliateTier.TIER_1_AFFILIATE_LEAD.value
    deal_amount_sar: int = 0
    rate: float = 0.0
    amount_sar: float = 0.0
    status: str = CommissionStatus.PENDING.value
    approval_id: str = ""
    eligibility_reasons: list[str] = field(default_factory=list)
    notes: str = ""
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def compute_commission(
    *,
    affiliate_id: str,
    tier: AffiliateTier | str,
    deal_amount_sar: int,
    referral_id: str = "",
    deal_invoice_id: str = "",
) -> Commission:
    """Compute a DRAFT commission for the first paid deal of a referral.

    Raises ValueError on invalid input. The returned commission is always
    ``PENDING`` — eligibility and approval are separate, gated steps.
    """
    if not affiliate_id:
        raise ValueError("affiliate_id is required")
    if deal_amount_sar <= 0:
        raise ValueError("deal_amount_sar must be > 0")
    tier_obj = AffiliateTier(tier)
    rate = commission_rate(tier_obj)
    amount = round(deal_amount_sar * rate, 2)
    notes = ""
    if is_handoff_tier(tier_obj):
        notes = "handoff_fee_negotiated_separately — no percentage commission"
    return Commission(
        affiliate_id=affiliate_id,
        referral_id=referral_id,
        deal_invoice_id=deal_invoice_id,
        tier=tier_obj.value,
        deal_amount_sar=int(deal_amount_sar),
        rate=rate,
        amount_sar=amount,
        status=CommissionStatus.PENDING.value,
        notes=notes,
    )


__all__ = ["Commission", "CommissionStatus", "compute_commission"]
