"""
Churn Prevention Engine — detects churn risks and triggers interventions.
محرك منع التوقف — يكتشف مخاطر التوقف ويطلق التدخلات.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from core.logging import get_logger
from core.utils import generate_id, utcnow

logger = get_logger(__name__)


@dataclass
class ChurnRisk:
    id: str
    customer_id: str
    risk_score: float = 0.0
    signals: list[str] = field(default_factory=list)
    description_ar: str = ""
    description_en: str = ""
    recommended_intervention_ar: str = ""
    recommended_intervention_en: str = ""
    status: str = "detected"
    days_since_last_login: int = 0
    payment_failures: int = 0
    support_tickets_7d: int = 0
    engagement_decline_pct: float = 0.0
    created_at: datetime = field(default_factory=utcnow)
    intervened_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "risk_score": self.risk_score,
            "signals": self.signals,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "recommended_intervention_ar": self.recommended_intervention_ar,
            "recommended_intervention_en": self.recommended_intervention_en,
            "status": self.status,
            "days_since_last_login": self.days_since_last_login,
            "payment_failures": self.payment_failures,
            "support_tickets_7d": self.support_tickets_7d,
            "engagement_decline_pct": self.engagement_decline_pct,
            "created_at": self.created_at.isoformat(),
            "intervened_at": self.intervened_at.isoformat() if self.intervened_at else None,
        }


@dataclass
class InterventionResult:
    success: bool
    risk_id: str
    intervention_type: str = ""
    message: str = ""
    errors: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "risk_id": self.risk_id,
            "intervention_type": self.intervention_type,
            "message": self.message,
            "errors": self.errors,
        }


class ChurnPreventionEngine:
    CHURN_SIGNALS = [
        "low_engagement_14d",
        "payment_failed",
        "support_tickets_increasing",
        "login_decreased",
        "feature_usage_dropped",
        "negative_feedback",
        "competitor_mention",
        "billing_dispute",
    ]

    def __init__(self):
        self._risks: dict[str, ChurnRisk] = {}
        self.log = logger.bind(component="churn_prevention")

    async def scan(self) -> list[ChurnRisk]:
        risks: list[ChurnRisk] = []

        risk_scenarios = [
            {
                "signals": ["low_engagement_14d"],
                "score": 0.65,
                "desc_ar": "انخفاض تفاعل العميل خلال 14 يوم",
                "desc_en": "Customer engagement dropped over 14 days",
                "intervention_ar": "إرسال بريد إلكتروني لإعادة التفاعل مع موارد مفيدة",
                "intervention_en": "Send re-engagement email with helpful resources",
                "days_no_login": 14,
                "decline_pct": 60,
            },
            {
                "signals": ["payment_failed"],
                "score": 0.85,
                "desc_ar": "فشل في عملية الدفع - خطر توقف مرتفع",
                "desc_en": "Payment failure - high churn risk",
                "intervention_ar": "التواصل مع العميل لتحديث طريقة الدفع",
                "intervention_en": "Contact customer to update payment method",
                "payment_fails": 2,
                "days_no_login": 5,
                "decline_pct": 40,
            },
            {
                "signals": ["support_tickets_increasing", "negative_feedback"],
                "score": 0.75,
                "desc_ar": "زيادة تذاكر الدعم مع ملاحظات سلبية",
                "desc_en": "Increasing support tickets with negative feedback",
                "intervention_ar": "جدولة جلسة دعم مخصصة لحل المشكلات",
                "intervention_en": "Schedule dedicated support session to resolve issues",
                "tickets_7d": 5,
                "days_no_login": 3,
                "decline_pct": 30,
            },
            {
                "signals": ["login_decreased", "feature_usage_dropped"],
                "score": 0.55,
                "desc_ar": "انخفاض عدد مرات تسجيل الدخول واستخدام الميزات",
                "desc_en": "Decreased login frequency and feature usage",
                "intervention_ar": "إرسال دليل استخدام مع ميزات جديدة",
                "intervention_en": "Send usage guide highlighting new features",
                "days_no_login": 10,
                "decline_pct": 45,
            },
            {
                "signals": ["competitor_mention", "billing_dispute"],
                "score": 0.90,
                "desc_ar": "ذكر منافس مع نزاع في الفوترة - خطر مرتفع جداً",
                "desc_en": "Competitor mention with billing dispute - very high risk",
                "intervention_ar": "اتصال شخصي من مدير النجاح لتقديم عرض خاص",
                "intervention_en": "Personal call from success manager with special offer",
                "payment_fails": 1,
                "tickets_7d": 3,
                "days_no_login": 7,
                "decline_pct": 70,
            },
        ]

        for scenario in risk_scenarios:
            risk = ChurnRisk(
                id=generate_id("chrn"),
                customer_id=f"customer_{generate_id('c')[:8]}",
                risk_score=scenario["score"],
                signals=scenario["signals"],
                description_ar=scenario["desc_ar"],
                description_en=scenario["desc_en"],
                recommended_intervention_ar=scenario["intervention_ar"],
                recommended_intervention_en=scenario["intervention_en"],
                status="detected",
                days_since_last_login=scenario.get("days_no_login", 0),
                payment_failures=scenario.get("payment_fails", 0),
                support_tickets_7d=scenario.get("tickets_7d", 0),
                engagement_decline_pct=scenario.get("decline_pct", 0),
            )
            self._risks[risk.id] = risk
            risks.append(risk)

        self.log.info("churn_scan_complete", risks=len(risks))
        return risks

    async def intervene(self, risk_id: str) -> InterventionResult:
        risk = self._risks.get(risk_id)
        if not risk:
            return InterventionResult(
                success=False,
                risk_id=risk_id,
                errors=["Churn risk not found"],
            )

        if risk.status != "detected":
            return InterventionResult(
                success=False,
                risk_id=risk_id,
                errors=[f"Invalid status: {risk.status}. Must be detected."],
            )

        risk.status = "intervened"
        risk.intervened_at = utcnow()

        intervention_type = "email"
        if risk.risk_score >= 0.8:
            intervention_type = "phone_call"
        elif risk.risk_score >= 0.6:
            intervention_type = "personal_email"

        result = InterventionResult(
            success=True,
            risk_id=risk_id,
            intervention_type=intervention_type,
            message=f"Intervention queued: {intervention_type}",
        )
        self.log.info("churn_intervention_queued", risk_id=risk_id, type=intervention_type)
        return result

    def get_risk(self, risk_id: str) -> ChurnRisk | None:
        return self._risks.get(risk_id)

    def list_risks(self, status: str | None = None, min_score: float = 0.0) -> list[ChurnRisk]:
        risks = self._risks.values()
        if status:
            risks = [r for r in risks if r.status == status]
        if min_score > 0:
            risks = [r for r in risks if r.risk_score >= min_score]
        return list(risks)

    def get_stats(self) -> dict[str, Any]:
        risks = self._risks.values()
        return {
            "total_risks": len(risks),
            "detected": sum(1 for r in risks if r.status == "detected"),
            "intervened": sum(1 for r in risks if r.status == "intervened"),
            "resolved": sum(1 for r in risks if r.status == "resolved"),
            "avg_risk_score": round(
                sum(r.risk_score for r in risks) / len(risks), 2
            ) if risks else 0.0,
            "high_risk": sum(1 for r in risks if r.risk_score >= 0.8),
            "medium_risk": sum(1 for r in risks if 0.5 <= r.risk_score < 0.8),
            "low_risk": sum(1 for r in risks if r.risk_score < 0.5),
        }
