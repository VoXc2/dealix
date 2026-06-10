"""
Commission Engine — calculates and processes partner commissions.
محرك العمولات — يحسب ويعالج عمولات الشركاء.
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
    status: str = "pending"
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
    payment_method: str = "bank_transfer"
    reference: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "commission_id": self.commission_id,
            "amount_sar": self.amount_sar,
            "payment_method": self.payment_method,
            "reference": self.reference,
            "errors": self.errors,
        }


class CommissionEngine:
    def __init__(self):
        self._commissions: dict[str, Commission] = {}
        self.log = logger.bind(component="commission_engine")

    async def calculate(self, referral_id: str) -> Commission:
        from integrations.partner_portal.referral_tracking import ReferralTracker

        tracker = ReferralTracker()
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
            status="pending",
        )
        self._commissions[commission.id] = commission
        self.log.info(
            "commission_calculated",
            id=commission.id,
            amount=commission.amount_sar,
            rate=commission.rate,
        )
        return commission

    async def pay(self, commission_id: str) -> PaymentResult:
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

        commission.status = "paid"
        commission.paid_at = utcnow()

        result = PaymentResult(
            success=True,
            commission_id=commission_id,
            amount_sar=commission.amount_sar,
            payment_method="bank_transfer",
            reference=f"PAY-{commission_id}",
        )

        self.log.info(
            "commission_paid",
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
        return {
            "total_commissions": len(commissions),
            "total_paid": sum(c.amount_sar for c in commissions if c.status == "paid"),
            "total_pending": sum(c.amount_sar for c in commissions if c.status == "pending"),
            "paid_count": sum(1 for c in commissions if c.status == "paid"),
            "pending_count": sum(1 for c in commissions if c.status == "pending"),
        }
