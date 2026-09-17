"""
Commission Engine — calculates and processes partner commissions.
محرك العمولات — يحسب ويعالج عمولات الشركاء.

Legacy `calculate()` is projection-only compatibility. Partner Network V2 economics and
verified collection determine real commission eligibility.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class Commission:
    id: str
    referral_id: str
    partner_id: str
    deal_value_sar: float
    rate: float
    amount_sar: float
    status: str = "projected_unpaid"
    paid_at: datetime | None = None
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "referral_id": self.referral_id,
            "partner_id": self.partner_id,
            "deal_value_sar": self.deal_value_sar,
            "rate": self.rate,
            "amount_sar": self.amount_sar,
            "status": self.status,
            "paid_at": self.paid_at.isoformat() if self.paid_at else None,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class PaymentResult:
    success: bool
    commission_id: str
    amount_sar: float = 0.0
    payment_method: str = "external_payment_not_executed"
    reference: str = ""
    status: str = "hold"
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "commission_id": self.commission_id,
            "amount_sar": self.amount_sar,
            "payment_method": self.payment_method,
            "reference": self.reference,
            "status": self.status,
            "errors": self.errors,
        }


class CommissionEngine:
    def __init__(self, tracker=None):
        self._commissions: dict[str, Commission] = {}
        self._tracker = tracker
        self.log = logger.bind(component="commission_engine")

    async def calculate(self, referral_id: str) -> Commission:
        """Create a legacy commission projection, never earned/payment truth."""
        from integrations.partner_portal.referral_tracking import ReferralTracker

        tracker = self._tracker or ReferralTracker()
        referral = tracker.get_referral(referral_id)
        if not referral:
            raise ValueError(f"Referral {referral_id} not found")

        commission = Commission(
            id=generate_id("comm"),
            referral_id=referral_id,
            partner_id=referral.partner_id,
            deal_value_sar=referral.deal_value_sar,
            rate=referral.commission_rate,
            amount_sar=referral.deal_value_sar * referral.commission_rate,
            status="projected_unpaid",
        )
        self._commissions[commission.id] = commission
        self.log.info(
            "commission_projected_legacy",
            id=commission.id,
            amount=commission.amount_sar,
            rate=commission.rate,
        )
        return commission

    async def pay(
        self,
        commission_id: str,
        *,
        approval_reference: str = "",
        verified_collection_reference: str = "",
        clearing_complete: bool = False,
    ) -> PaymentResult:
        """Stage an externally payable commission; never execute money movement."""
        commission = self._commissions.get(commission_id)
        if not commission:
            return PaymentResult(
                success=False,
                commission_id=commission_id,
                errors=["Commission not found"],
            )

        if commission.status == "paid":
            return PaymentResult(
                success=False,
                commission_id=commission_id,
                errors=["Commission already paid"],
            )
        if commission.status == "approved_for_payment":
            return PaymentResult(
                success=False,
                commission_id=commission_id,
                amount_sar=commission.amount_sar,
                reference=f"STAGED-{commission_id}",
                status="staged_not_paid",
                errors=["commission_already_staged"],
            )

        missing = []
        if not approval_reference.strip():
            missing.append("approval_reference_required")
        if not verified_collection_reference.strip():
            missing.append("verified_collection_reference_required")
        if not clearing_complete:
            missing.append("clearing_period_not_complete")
        if missing:
            return PaymentResult(
                success=False,
                commission_id=commission_id,
                errors=missing,
            )

        commission.status = "approved_for_payment"
        result = PaymentResult(
            success=True,
            commission_id=commission_id,
            amount_sar=commission.amount_sar,
            payment_method="external_payment_not_executed",
            reference=f"STAGED-{commission_id}",
            status="staged_not_paid",
        )

        self.log.info(
            "commission_payment_staged",
            id=commission_id,
            amount=commission.amount_sar,
            reference=result.reference,
        )
        return result

    async def get_history(self, partner_id: str) -> list[Commission]:
        return [
            c for c in self._commissions.values()
            if c.partner_id == partner_id
        ]

    def get_commission(self, commission_id: str) -> Commission | None:
        return self._commissions.get(commission_id)

    def get_stats(self) -> dict[str, Any]:
        commissions = self._commissions.values()
        pending_statuses = {"projected_unpaid", "pending", "approved_for_payment"}
        return {
            "total_commissions": len(commissions),
            "total_paid": sum(c.amount_sar for c in commissions if c.status == "paid"),
            "total_pending": sum(c.amount_sar for c in commissions if c.status in pending_statuses),
            "paid_count": sum(1 for c in commissions if c.status == "paid"),
            "pending_count": sum(1 for c in commissions if c.status in pending_statuses),
        }
