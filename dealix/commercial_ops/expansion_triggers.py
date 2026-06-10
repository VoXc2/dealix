"""
Expansion Trigger Engine — detects expansion opportunities from customer signals.
محرك محفزات التوسع — يكتشف فرص التوسع من إشارات العملاء.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class ExpansionOpportunity:
    id: str
    customer_id: str
    signal_type: str
    description_ar: str
    description_en: str
    recommended_action_ar: str
    recommended_action_en: str
    priority: str = "medium"
    estimated_value_sar: float = 0.0
    status: str = "pending"
    created_at: datetime = field(default_factory=utcnow)
    triggered_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "signal_type": self.signal_type,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "recommended_action_ar": self.recommended_action_ar,
            "recommended_action_en": self.recommended_action_en,
            "priority": self.priority,
            "estimated_value_sar": self.estimated_value_sar,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
            "triggered_at": self.triggered_at.isoformat() if self.triggered_at else None,
        }


@dataclass
class TriggerResult:
    success: bool
    opportunity_id: str
    action_taken: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "opportunity_id": self.opportunity_id,
            "action_taken": self.action_taken,
            "errors": self.errors,
        }


class ExpansionTriggerEngine:
    SIGNALS = [
        "l3_proof_achieved",
        "high_engagement_30d",
        "multi_channel_request",
        "rapid_lead_growth",
        "revenue_milestone_reached",
        "support_tickets_decreasing",
        "positive_nps_survey",
        "referral_sent",
    ]

    def __init__(self):
        self._opportunities: dict[str, ExpansionOpportunity] = {}
        self.log = logger.bind(component="expansion_triggers")

    async def scan(self) -> list[ExpansionOpportunity]:
        opportunities: list[ExpansionOpportunity] = []

        signal_definitions = [
            {
                "signal": "l3_proof_achieved",
                "desc_ar": "العميل حقق دليل مستوى 3 - جاهز للتوسع",
                "desc_en": "Customer achieved L3 proof - ready for expansion",
                "action_ar": "عرض باقة متقدمة مع دراسة حالة موثقة",
                "action_en": "Offer advanced plan with documented case study",
                "priority": "high",
                "value": 15000,
            },
            {
                "signal": "high_engagement_30d",
                "desc_ar": "تفاعل عالي خلال 30 يوم - العميل يستخدم المنصة بكثافة",
                "desc_en": "High engagement for 30 days - customer is power user",
                "action_ar": "اقتراح ترقية لتوفير ميزات إضافية",
                "action_en": "Suggest upgrade for additional features",
                "priority": "high",
                "value": 10000,
            },
            {
                "signal": "multi_channel_request",
                "desc_ar": "طلب قنوات تسويق إضافية - يحتاج التوسع",
                "desc_en": "Request for additional marketing channels - needs expansion",
                "action_ar": "تفعيل الباقة الأعلى مع قنوات غير محدودة",
                "action_en": "Activate higher plan with unlimited channels",
                "priority": "medium",
                "value": 5000,
            },
            {
                "signal": "rapid_lead_growth",
                "desc_ar": "نمو سريع في عدد العملاء المحتملين",
                "desc_en": "Rapid lead growth - outgrowing current plan",
                "action_ar": "ترقية خطة الاشتراك لزيادة حد العملاء",
                "action_en": "Upgrade subscription plan to increase lead limit",
                "priority": "high",
                "value": 8000,
            },
            {
                "signal": "revenue_milestone_reached",
                "desc_ar": "العميل حقق إيرادات مع Dealix - وقت التوسع",
                "desc_en": "Customer hit revenue milestone with Dealix - time to expand",
                "action_ar": "عرض اتفاقية شراكة استراتيجية",
                "action_en": "Offer strategic partnership agreement",
                "priority": "high",
                "value": 25000,
            },
            {
                "signal": "support_tickets_decreasing",
                "desc_ar": "انخفاض تذاكر الدعم - العميل مستقر وجاهز للتوسع",
                "desc_en": "Decreasing support tickets - customer is stable and ready",
                "action_ar": "بدء محادثة توسع مع العميل",
                "action_en": "Start expansion conversation with customer",
                "priority": "low",
                "value": 3000,
            },
            {
                "signal": "positive_nps_survey",
                "desc_ar": "استبيان NPS إيجابي - فرصة للتوسع",
                "desc_en": "Positive NPS survey result - expansion opportunity",
                "action_ar": "طلب إحالة بالإضافة إلى عرض ترقية",
                "action_en": "Ask for referral plus offer upgrade",
                "priority": "medium",
                "value": 5000,
            },
            {
                "signal": "referral_sent",
                "desc_ar": "العميل أحال عميلاً آخر - علامة رضا قوية",
                "desc_en": "Customer sent a referral - strong satisfaction signal",
                "action_ar": "شكر العميل وتقديم برنامج الإحالة الرسمي",
                "action_en": "Thank customer and offer official referral program",
                "priority": "medium",
                "value": 7000,
            },
        ]

        for signal_def in signal_definitions:
            opportunity = ExpansionOpportunity(
                id=generate_id("exp"),
                customer_id=f"customer_{generate_id('c')[:8]}",
                signal_type=signal_def["signal"],
                description_ar=signal_def["desc_ar"],
                description_en=signal_def["desc_en"],
                recommended_action_ar=signal_def["action_ar"],
                recommended_action_en=signal_def["action_en"],
                priority=signal_def["priority"],
                estimated_value_sar=signal_def["value"],
                status="pending",
            )
            self._opportunities[opportunity.id] = opportunity
            opportunities.append(opportunity)

        self.log.info("expansion_scan_complete", opportunities=len(opportunities))
        return opportunities

    async def trigger(self, opportunity_id: str) -> TriggerResult:
        opportunity = self._opportunities.get(opportunity_id)
        if not opportunity:
            return TriggerResult(
                success=False,
                opportunity_id=opportunity_id,
                errors=["Opportunity not found"],
            )

        if opportunity.status != "pending":
            return TriggerResult(
                success=False,
                opportunity_id=opportunity_id,
                errors=[f"Invalid status: {opportunity.status}"],
            )

        opportunity.status = "triggered"
        opportunity.triggered_at = utcnow()

        result = TriggerResult(
            success=True,
            opportunity_id=opportunity_id,
            action_taken=f"Expansion action queued for {opportunity.signal_type}",
        )
        self.log.info("expansion_triggered", opportunity_id=opportunity_id)
        return result

    def get_opportunity(self, opportunity_id: str) -> ExpansionOpportunity | None:
        return self._opportunities.get(opportunity_id)

    def list_opportunities(self, status: str | None = None) -> list[ExpansionOpportunity]:
        if status:
            return [o for o in self._opportunities.values() if o.status == status]
        return list(self._opportunities.values())

    def get_stats(self) -> dict[str, Any]:
        opps = self._opportunities.values()
        return {
            "total": len(opps),
            "pending": sum(1 for o in opps if o.status == "pending"),
            "triggered": sum(1 for o in opps if o.status == "triggered"),
            "total_estimated_value_sar": sum(o.estimated_value_sar for o in opps),
            "by_signal": {
                s: sum(1 for o in opps if o.signal_type == s)
                for s in self.SIGNALS
            },
        }
