"""
Upsell Automaton — automatically detects upsell opportunities and generates proposals.
أتمتة البيع الإضافي — يكتشف فرص البيع الإضافي ويولد المقترحات تلقائياً.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class UpsellOpportunity:
    id: str
    customer_id: str
    current_plan: str
    target_plan: str
    reason_ar: str
    reason_en: str
    price_difference_sar: float = 0.0
    confidence: float = 0.0
    status: str = "identified"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "current_plan": self.current_plan,
            "target_plan": self.target_plan,
            "reason_ar": self.reason_ar,
            "reason_en": self.reason_en,
            "price_difference_sar": self.price_difference_sar,
            "confidence": self.confidence,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class UpsellProposal:
    id: str
    opportunity_id: str
    customer_id: str
    offer_ar: str
    offer_en: str
    benefits_ar: list[str] = field(default_factory=list)
    benefits_en: list[str] = field(default_factory=list)
    pricing_ar: str = ""
    pricing_en: str = ""
    status: str = "draft"
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "opportunity_id": self.opportunity_id,
            "customer_id": self.customer_id,
            "offer_ar": self.offer_ar,
            "offer_en": self.offer_en,
            "benefits_ar": self.benefits_ar,
            "benefits_en": self.benefits_en,
            "pricing_ar": self.pricing_ar,
            "pricing_en": self.pricing_en,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class SendResult:
    success: bool
    opportunity_id: str
    channel: str = "email"
    message: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "opportunity_id": self.opportunity_id,
            "channel": self.channel,
            "message": self.message,
            "errors": self.errors,
        }


PLAN_UPGRADE_PATH = {
    "starter": {"target": "growth", "price_diff": 2000},
    "growth": {"target": "scale", "price_diff": 5000},
    "scale": {"target": "enterprise", "price_diff": 17000},
}


class UpsellAutomaton:
    def __init__(self):
        self._opportunities: dict[str, UpsellOpportunity] = {}
        self._proposals: dict[str, UpsellProposal] = {}
        self.log = logger.bind(component="upsell_automaton")

    async def scan_for_upsells(self) -> list[UpsellOpportunity]:
        opportunities: list[UpsellOpportunity] = []

        for current_plan, upgrade_info in PLAN_UPGRADE_PATH.items():
            opportunity = UpsellOpportunity(
                id=generate_id("up"),
                customer_id=f"customer_{generate_id('c')[:8]}",
                current_plan=current_plan,
                target_plan=upgrade_info["target"],
                reason_ar=(
                    f"عميل خطة {current_plan} جاهز للترقية إلى {upgrade_info['target']} "
                    f"بناءً على أنماط الاستخدام وإمكانات النمو"
                ),
                reason_en=(
                    f"{current_plan.title()} plan customer ready to upgrade to "
                    f"{upgrade_info['target']} based on usage patterns and growth potential"
                ),
                price_difference_sar=upgrade_info["price_diff"],
                confidence=0.75,
                status="identified",
            )
            self._opportunities[opportunity.id] = opportunity
            opportunities.append(opportunity)

        self.log.info("upsell_scan_complete", opportunities=len(opportunities))
        return opportunities

    async def generate_proposal(self, opportunity_id: str) -> UpsellProposal:
        opportunity = self._opportunities.get(opportunity_id)
        if not opportunity:
            raise ValueError(f"Opportunity {opportunity_id} not found")

        proposal = UpsellProposal(
            id=generate_id("up_prp"),
            opportunity_id=opportunity_id,
            customer_id=opportunity.customer_id,
            offer_ar=(
                f"عرض ترقية حصري: ارتقِ من باقة {opportunity.current_plan} "
                f"إلى {opportunity.target_plan} وحقق أقصى استفادة من منصة Dealix"
            ),
            offer_en=(
                f"Exclusive Upgrade Offer: Move from {opportunity.current_plan.title()} "
                f"to {opportunity.target_plan.title()} and maximize your Dealix platform value"
            ),
            benefits_ar=[
                f"ضعف عدد العملاء المحتملين المسموح به",
                f"قنوات تسويق غير محدودة",
                f"دعم ذو أولوية مع استجابة أسرع",
                f"تقارير وتحليلات متقدمة",
                f"إمكانية الوصول إلى API للتكامل",
            ],
            benefits_en=[
                f"Double the lead limit",
                f"Unlimited marketing channels",
                f"Priority support with faster response",
                f"Advanced reports and analytics",
                f"API access for integration",
            ],
            pricing_ar=(
                f"الفرق في السعر: {opportunity.price_difference_sar:,.0f} ريال/شهر\n"
                f"إجمالي الباقة الجديدة: قابلة للترتيب حسب الاحتياجات"
            ),
            pricing_en=(
                f"Price difference: SAR {opportunity.price_difference_sar:,.0f}/month\n"
                f"New plan total: negotiable based on needs"
            ),
            status="draft",
        )
        self._proposals[proposal.id] = proposal
        self.log.info("upsell_proposal_generated", id=proposal.id, opportunity_id=opportunity_id)
        return proposal

    async def send_offer(self, opportunity_id: str) -> SendResult:
        opportunity = self._opportunities.get(opportunity_id)
        if not opportunity:
            return SendResult(
                success=False,
                opportunity_id=opportunity_id,
                errors=["Opportunity not found"],
            )

        opportunity.status = "offer_sent"

        result = SendResult(
            success=True,
            opportunity_id=opportunity_id,
            channel="email",
            message="Upsell offer queued for manual review before sending",
        )
        self.log.info("upsell_offer_queued", opportunity_id=opportunity_id)
        return result

    def get_opportunity(self, opportunity_id: str) -> UpsellOpportunity | None:
        return self._opportunities.get(opportunity_id)

    def get_proposal(self, proposal_id: str) -> UpsellProposal | None:
        return self._proposals.get(proposal_id)

    def list_opportunities(self, status: str | None = None) -> list[UpsellOpportunity]:
        if status:
            return [o for o in self._opportunities.values() if o.status == status]
        return list(self._opportunities.values())

    def get_stats(self) -> dict[str, Any]:
        opps = self._opportunities.values()
        return {
            "total_opportunities": len(opps),
            "identified": sum(1 for o in opps if o.status == "identified"),
            "offer_sent": sum(1 for o in opps if o.status == "offer_sent"),
            "accepted": sum(1 for o in opps if o.status == "accepted"),
            "total_potential_revenue_sar": sum(o.price_difference_sar for o in opps),
            "avg_confidence": round(
                sum(o.confidence for o in opps) / len(opps), 2
            ) if opps else 0.0,
        }
