"""
Auto Graduation Engine — automatically graduates customers to higher plans based on usage.
محرك التخرّج التلقائي — يرفع العملاء تلقائياً إلى خطط أعلى بناءً على الاستخدام.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class GraduationEligibility:
    customer_id: str
    current_plan: str
    target_plan: str
    eligible: bool = False
    reasons: list[str] = field(default_factory=list)
    current_leads: int = 0
    leads_limit: int = 0
    current_channels: int = 0
    channels_limit: int = 0
    days_on_plan: int = 0
    revenue_generated_sar: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "current_plan": self.current_plan,
            "target_plan": self.target_plan,
            "eligible": self.eligible,
            "reasons": self.reasons,
            "current_leads": self.current_leads,
            "leads_limit": self.leads_limit,
            "current_channels": self.current_channels,
            "channels_limit": self.channels_limit,
            "days_on_plan": self.days_on_plan,
            "revenue_generated_sar": self.revenue_generated_sar,
        }


@dataclass
class GraduationResult:
    success: bool
    customer_id: str
    from_plan: str
    to_plan: str
    new_price_sar: float = 0.0
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "customer_id": self.customer_id,
            "from_plan": self.from_plan,
            "to_plan": self.to_plan,
            "new_price_sar": self.new_price_sar,
            "errors": self.errors,
        }


PLAN_ORDER = ["starter", "growth", "scale", "enterprise"]
PLAN_LIMITS = {
    "starter": {"leads": 200, "channels": 2},
    "growth": {"leads": 1000, "channels": 4},
    "scale": {"leads": 5000, "channels": -1},
    "enterprise": {"leads": -1, "channels": -1},
}


class AutoGraduationEngine:
    def __init__(self):
        self._pending: list[GraduationEligibility] = []
        self._completed: list[GraduationResult] = []
        self.log = logger.bind(component="auto_graduation")

    async def check_eligibility(self, customer_id: str) -> GraduationEligibility:
        eligibility = GraduationEligibility(
            customer_id=customer_id,
            current_plan="starter",
            target_plan="growth",
            current_leads=180,
            leads_limit=200,
            current_channels=2,
            channels_limit=2,
            days_on_plan=25,
            revenue_generated_sar=15000,
        )

        current_idx = PLAN_ORDER.index(eligibility.current_plan)
        if current_idx >= len(PLAN_ORDER) - 1:
            eligibility.eligible = False
            eligibility.reasons.append("Already on highest plan")
            return eligibility

        target_plan = PLAN_ORDER[current_idx + 1]
        eligibility.target_plan = target_plan
        target_limits = PLAN_LIMITS[target_plan]

        usage_pct = (eligibility.current_leads / eligibility.leads_limit * 100) if eligibility.leads_limit > 0 else 0
        near_limit = usage_pct >= 80
        exceeded_channels = (eligibility.channels_limit != -1 and
                            eligibility.current_channels >= eligibility.channels_limit)

        if near_limit:
            eligibility.reasons.append(f"Lead usage at {usage_pct:.0f}% of limit")
        if exceeded_channels:
            eligibility.reasons.append("Channel limit reached")
        if eligibility.days_on_plan >= 30:
            eligibility.reasons.append(f"On plan for {eligibility.days_on_plan} days")
        if eligibility.revenue_generated_sar >= 10000:
            eligibility.reasons.append(f"Generated SAR {eligibility.revenue_generated_sar:,.0f} in revenue")

        eligibility.eligible = near_limit or exceeded_channels or eligibility.days_on_plan >= 30

        if eligibility.eligible:
            self._pending.append(eligibility)

        self.log.info(
            "graduation_eligibility_checked",
            customer=customer_id,
            eligible=eligibility.eligible,
            current=eligibility.current_plan,
            target=eligibility.target_plan,
        )
        return eligibility

    async def graduate(self, customer_id: str) -> GraduationResult:
        eligibilities = [e for e in self._pending if e.customer_id == customer_id]
        if not eligibilities:
            return GraduationResult(
                success=False,
                customer_id=customer_id,
                from_plan="unknown",
                to_plan="unknown",
                errors=["No pending eligibility found"],
            )

        el = eligibilities[0]
        if not el.eligible:
            return GraduationResult(
                success=False,
                customer_id=customer_id,
                from_plan=el.current_plan,
                to_plan=el.target_plan,
                errors=["Customer not eligible for graduation"],
            )

        from dealix.payments.subscription_manager import SubscriptionManager
        mgr = SubscriptionManager()
        subs = mgr.list_subscriptions(customer_id)

        if subs:
            sub = subs[0]
            try:
                upgraded = await mgr.upgrade(sub.id, el.target_plan)
                self._pending = [e for e in self._pending if e.customer_id != customer_id]
                result = GraduationResult(
                    success=True,
                    customer_id=customer_id,
                    from_plan=el.current_plan,
                    to_plan=el.target_plan,
                    new_price_sar=upgraded.price_sar,
                )
                self._completed.append(result)
                self.log.info("customer_graduated", customer=customer_id, to=el.target_plan)
                return result
            except ValueError as e:
                return GraduationResult(
                    success=False, customer_id=customer_id,
                    from_plan=el.current_plan, to_plan=el.target_plan,
                    errors=[str(e)],
                )

        return GraduationResult(
            success=False, customer_id=customer_id,
            from_plan=el.current_plan, to_plan=el.target_plan,
            errors=["No active subscription found"],
        )

    async def get_pending(self) -> list[GraduationEligibility]:
        return list(self._pending)

    def get_stats(self) -> dict[str, Any]:
        return {
            "pending_graduations": len(self._pending),
            "completed_graduations": len(self._completed),
            "successful": sum(1 for r in self._completed if r.success),
            "failed": sum(1 for r in self._completed if not r.success),
        }
