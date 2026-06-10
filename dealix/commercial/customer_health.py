"""Customer Health Scoring System — AI-powered health monitoring.

Tracks customer health across 6 dimensions to predict churn,
identify expansion opportunities, and prioritize founder attention.

Constitutional gates:
- NO_FAKE_METRICS: scores only from real logged events
- APPROVAL_FIRST: health alerts require founder review before action
"""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

# Health tier thresholds
HEALTH_TIERS = {
    "CHAMPION": (85, 100),    # Expand + get testimonial
    "HEALTHY": (70, 84),      # Maintain momentum
    "AT_RISK": (50, 69),      # Proactive intervention needed
    "CRITICAL": (30, 49),     # Urgent rescue plan required
    "CHURNED": (0, 29),       # Exit or deep intervention
}

SECTOR_BENCHMARKS = {
    "b2b_saas": {"avg_health": 72, "churn_risk_threshold": 55},
    "agency": {"avg_health": 68, "churn_risk_threshold": 50},
    "healthcare_clinic": {"avg_health": 75, "churn_risk_threshold": 60},
    "real_estate": {"avg_health": 65, "churn_risk_threshold": 48},
    "logistics": {"avg_health": 70, "churn_risk_threshold": 52},
    "fintech": {"avg_health": 74, "churn_risk_threshold": 58},
    "engineering": {"avg_health": 67, "churn_risk_threshold": 50},
    "b2b_services": {"avg_health": 69, "churn_risk_threshold": 51},
}


class HealthDimension(BaseModel):
    name_ar: str
    name_en: str
    score: float = Field(ge=0, le=100)
    weight: float = Field(ge=0, le=1)
    signals: list[str] = Field(default_factory=list)
    improvement_ar: str = ""
    improvement_en: str = ""


class CustomerHealthReport(BaseModel):
    account_id: str
    company_name: str
    sector: str
    overall_score: float = Field(ge=0, le=100)
    health_tier: str
    calculated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    dimensions: list[HealthDimension]

    # Risk signals
    is_churn_risk: bool = False
    churn_probability: float = 0.0
    days_to_renewal: int | None = None

    # Expansion signals
    expansion_ready: bool = False
    recommended_upsell_ar: str = ""
    recommended_upsell_en: str = ""

    # Action items
    priority_actions_ar: list[str] = Field(default_factory=list)
    priority_actions_en: list[str] = Field(default_factory=list)

    # Benchmarks
    vs_sector_avg: float = 0.0  # difference from sector average
    sector_percentile: int = 50

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())

    @property
    def needs_immediate_attention(self) -> bool:
        return self.overall_score < 50 or self.churn_probability > 0.6


class HealthInput(BaseModel):
    """Input data for health scoring."""
    account_id: str
    company_name: str
    sector: str = "b2b_services"

    # Engagement signals
    days_since_last_interaction: int = 0
    interactions_last_30_days: int = 0
    response_time_hours: float = 0

    # Delivery signals
    sprints_completed: int = 0
    deliverables_on_time_pct: float = 100
    proof_level_achieved: str = "L0"  # L0-L4
    measurable_outcomes_count: int = 0

    # Financial signals
    invoices_paid_on_time: int = 0
    invoices_total: int = 0
    lifetime_value_sar: float = 0
    months_as_customer: int = 0

    # Satisfaction signals
    nps_score: int | None = None  # -100 to 100
    support_tickets_open: int = 0
    support_tickets_resolved: int = 0
    has_testimonial: bool = False
    has_referral: bool = False

    # Product adoption signals
    features_adopted: int = 0
    features_available: int = 10
    weekly_active_usage: bool = False
    uses_approval_center: bool = False

    # Risk signals
    key_contact_left: bool = False
    budget_at_risk: bool = False
    competitor_mentioned: bool = False
    renewal_date: datetime | None = None


class CustomerHealthEngine:
    """Calculates comprehensive customer health scores."""

    PROOF_LEVEL_SCORES = {"L0": 20, "L1": 45, "L2": 65, "L3": 80, "L4": 95}

    def calculate(self, inp: HealthInput) -> CustomerHealthReport:
        dimensions = self._score_dimensions(inp)
        overall = self._weighted_average(dimensions)
        health_tier = self._get_tier(overall)
        churn_prob = self._estimate_churn(inp, overall)
        expansion_ready = self._check_expansion_readiness(inp, overall)

        sector_bench = SECTOR_BENCHMARKS.get(inp.sector, {"avg_health": 70, "churn_risk_threshold": 52})
        vs_avg = round(overall - sector_bench["avg_health"], 1)

        # Estimate sector percentile
        if overall >= sector_bench["avg_health"] + 15:
            percentile = 90
        elif overall >= sector_bench["avg_health"] + 5:
            percentile = 75
        elif overall >= sector_bench["avg_health"]:
            percentile = 60
        elif overall >= sector_bench["avg_health"] - 10:
            percentile = 40
        else:
            percentile = 20

        actions_ar, actions_en = self._build_action_items(inp, dimensions, overall)
        upsell_ar, upsell_en = self._recommend_upsell(inp, overall) if expansion_ready else ("", "")

        days_to_renewal = None
        if inp.renewal_date:
            delta = (inp.renewal_date - datetime.now(UTC)).days
            days_to_renewal = max(0, delta)

        return CustomerHealthReport(
            account_id=inp.account_id,
            company_name=inp.company_name,
            sector=inp.sector,
            overall_score=round(overall, 1),
            health_tier=health_tier,
            dimensions=dimensions,
            is_churn_risk=churn_prob > 0.4,
            churn_probability=round(churn_prob, 2),
            days_to_renewal=days_to_renewal,
            expansion_ready=expansion_ready,
            recommended_upsell_ar=upsell_ar,
            recommended_upsell_en=upsell_en,
            priority_actions_ar=actions_ar,
            priority_actions_en=actions_en,
            vs_sector_avg=vs_avg,
            sector_percentile=percentile,
        )

    def _score_dimensions(self, inp: HealthInput) -> list[HealthDimension]:
        return [
            self._score_engagement(inp),
            self._score_delivery(inp),
            self._score_financial(inp),
            self._score_satisfaction(inp),
            self._score_adoption(inp),
            self._score_risk(inp),
        ]

    def _score_engagement(self, inp: HealthInput) -> HealthDimension:
        score = 100.0
        signals = []

        if inp.days_since_last_interaction > 30:
            score -= 40
            signals.append("no_interaction_30_days")
        elif inp.days_since_last_interaction > 14:
            score -= 20
            signals.append("no_interaction_14_days")
        elif inp.days_since_last_interaction <= 3:
            signals.append("active_engagement")

        if inp.interactions_last_30_days >= 8:
            signals.append("high_engagement_frequency")
        elif inp.interactions_last_30_days < 2:
            score -= 25
            signals.append("low_engagement_frequency")

        if inp.response_time_hours > 48:
            score -= 15
            signals.append("slow_response_time")
        elif inp.response_time_hours <= 4:
            signals.append("fast_response_time")

        return HealthDimension(
            name_ar="مستوى التفاعل",
            name_en="Engagement",
            score=max(0, min(100, score)),
            weight=0.20,
            signals=signals,
            improvement_ar="زيادة نقاط التواصل الأسبوعية — هدف: 2 تفاعلات/أسبوع على الأقل",
            improvement_en="Increase weekly touchpoints — target: at least 2 interactions/week",
        )

    def _score_delivery(self, inp: HealthInput) -> HealthDimension:
        signals = []

        proof_score = self.PROOF_LEVEL_SCORES.get(inp.proof_level_achieved, 20)
        score = float(proof_score)

        if inp.sprints_completed >= 2:
            score = min(100, score + 15)
            signals.append("multi_sprint_client")
        elif inp.sprints_completed >= 1:
            signals.append("first_sprint_complete")

        if inp.deliverables_on_time_pct >= 90:
            score = min(100, score + 10)
            signals.append("on_time_delivery")
        elif inp.deliverables_on_time_pct < 70:
            score -= 15
            signals.append("delayed_deliverables")

        if inp.measurable_outcomes_count >= 3:
            score = min(100, score + 15)
            signals.append("strong_outcomes")

        return HealthDimension(
            name_ar="جودة التسليم",
            name_en="Delivery Quality",
            score=max(0, min(100, score)),
            weight=0.25,
            signals=signals,
            improvement_ar="رفع مستوى الإثبات إلى L2+ من خلال توثيق 3 نتائج قابلة للقياس",
            improvement_en="Elevate proof level to L2+ by documenting 3 measurable outcomes",
        )

    def _score_financial(self, inp: HealthInput) -> HealthDimension:
        score = 60.0
        signals = []

        if inp.invoices_total > 0:
            pay_rate = inp.invoices_paid_on_time / inp.invoices_total
            if pay_rate >= 0.95:
                score = 90
                signals.append("excellent_payment_history")
            elif pay_rate >= 0.80:
                score = 70
                signals.append("good_payment_history")
            else:
                score = 40
                signals.append("payment_delays")

        if inp.lifetime_value_sar >= 15000:
            score = min(100, score + 15)
            signals.append("high_ltv")
        elif inp.lifetime_value_sar >= 5000:
            signals.append("growing_ltv")

        if inp.months_as_customer >= 12:
            score = min(100, score + 10)
            signals.append("long_term_customer")

        return HealthDimension(
            name_ar="الصحة المالية",
            name_en="Financial Health",
            score=max(0, min(100, score)),
            weight=0.20,
            signals=signals,
            improvement_ar="تحسين تتبع الدفعات وإرسال تذكيرات ودية قبل 7 أيام من موعد الدفع",
            improvement_en="Improve payment tracking and send gentle reminders 7 days before due date",
        )

    def _score_satisfaction(self, inp: HealthInput) -> HealthDimension:
        score = 65.0
        signals = []

        if inp.nps_score is not None:
            if inp.nps_score >= 50:
                score = 95
                signals.append("promoter_nps")
            elif inp.nps_score >= 0:
                score = 70
                signals.append("passive_nps")
            else:
                score = 30
                signals.append("detractor_nps")

        if inp.has_testimonial:
            score = min(100, score + 10)
            signals.append("has_testimonial")

        if inp.has_referral:
            score = min(100, score + 15)
            signals.append("active_referrer")

        if inp.support_tickets_open > 3:
            score -= 20
            signals.append("multiple_open_tickets")
        elif inp.support_tickets_open == 0:
            signals.append("no_open_issues")

        return HealthDimension(
            name_ar="رضا العميل",
            name_en="Customer Satisfaction",
            score=max(0, min(100, score)),
            weight=0.20,
            signals=signals,
            improvement_ar="جمع NPS بعد كل Sprint وحل التذاكر المفتوحة خلال 48 ساعة",
            improvement_en="Collect NPS after each Sprint and resolve open tickets within 48 hours",
        )

    def _score_adoption(self, inp: HealthInput) -> HealthDimension:
        score = 50.0
        signals = []

        if inp.features_available > 0:
            adoption_rate = inp.features_adopted / inp.features_available
            score = adoption_rate * 100
            if adoption_rate >= 0.7:
                signals.append("high_adoption")
            elif adoption_rate < 0.3:
                signals.append("low_adoption")

        if inp.weekly_active_usage:
            score = min(100, score + 15)
            signals.append("weekly_active")

        if inp.uses_approval_center:
            score = min(100, score + 10)
            signals.append("uses_governance_features")

        return HealthDimension(
            name_ar="تبني المنتج",
            name_en="Product Adoption",
            score=max(0, min(100, score)),
            weight=0.10,
            signals=signals,
            improvement_ar="تقديم جلسة توجيهية لميزات Approval Center ولوحة KPI",
            improvement_en="Offer onboarding session for Approval Center and KPI dashboard features",
        )

    def _score_risk(self, inp: HealthInput) -> HealthDimension:
        score = 100.0
        signals = []

        if inp.key_contact_left:
            score -= 35
            signals.append("key_contact_departure")

        if inp.budget_at_risk:
            score -= 30
            signals.append("budget_risk")

        if inp.competitor_mentioned:
            score -= 20
            signals.append("competitive_threat")

        days_to_renewal = None
        if inp.renewal_date:
            delta = (inp.renewal_date - datetime.now(UTC)).days
            days_to_renewal = max(0, delta)

        if days_to_renewal is not None and days_to_renewal < 30:
            signals.append("renewal_approaching")
            if days_to_renewal < 14:
                score -= 10
                signals.append("renewal_critical")

        return HealthDimension(
            name_ar="مؤشرات الخطر",
            name_en="Risk Indicators",
            score=max(0, min(100, score)),
            weight=0.05,
            signals=signals,
            improvement_ar="معالجة إشارات الخطر فوراً — لا تترك أكثر من 72 ساعة بدون استجابة",
            improvement_en="Address risk signals immediately — never leave more than 72 hours without response",
        )

    def _weighted_average(self, dimensions: list[HealthDimension]) -> float:
        total = sum(d.score * d.weight for d in dimensions)
        total_weight = sum(d.weight for d in dimensions)
        return total / total_weight if total_weight > 0 else 0

    def _get_tier(self, score: float) -> str:
        for tier, (lo, hi) in HEALTH_TIERS.items():
            if lo <= score <= hi:
                return tier
        return "CRITICAL"

    def _estimate_churn(self, inp: HealthInput, overall: float) -> float:
        base = max(0, (100 - overall) / 100)
        if inp.key_contact_left:
            base = min(1.0, base + 0.3)
        if inp.competitor_mentioned:
            base = min(1.0, base + 0.2)
        if inp.days_since_last_interaction > 30:
            base = min(1.0, base + 0.15)
        if inp.budget_at_risk:
            base = min(1.0, base + 0.25)
        if inp.nps_score is not None and inp.nps_score < 0:
            base = min(1.0, base + 0.1)
        return round(base * 0.7, 2)  # Cap influence

    def _check_expansion_readiness(self, inp: HealthInput, score: float) -> bool:
        return (
            score >= 70
            and inp.sprints_completed >= 1
            and inp.proof_level_achieved in ("L2", "L3", "L4")
            and (inp.nps_score is None or inp.nps_score >= 30)
        )

    def _recommend_upsell(self, inp: HealthInput, score: float) -> tuple[str, str]:
        ltv = inp.lifetime_value_sar
        if ltv < 1500:
            return (
                "ترقية إلى Agency Proof Pack (1,500 ر.س) — توثيق النتائج الكاملة",
                "Upgrade to Agency Proof Pack (1,500 SAR) — document full outcomes",
            )
        elif ltv < 5000:
            return (
                "انضم إلى Managed Ops Retainer (2,999 ر.س/شهر) — تشغيل مُدار مستمر",
                "Join Managed Ops Retainer (2,999 SAR/mo) — continuous managed operations",
            )
        else:
            return (
                "Custom AI Project (5,000–25,000 ر.س) — تطوير ذكاء اصطناعي مخصص لعملياتك",
                "Custom AI Project (5,000–25,000 SAR) — bespoke AI for your operations",
            )

    def _build_action_items(
        self, inp: HealthInput, dims: list[HealthDimension], score: float,
    ) -> tuple[list[str], list[str]]:
        actions_ar = []
        actions_en = []

        # Sort dimensions by score (worst first)
        sorted_dims = sorted(dims, key=lambda d: d.score * d.weight)

        for dim in sorted_dims[:3]:
            if dim.score < 60 and dim.improvement_ar:
                actions_ar.append(dim.improvement_ar)
                actions_en.append(dim.improvement_en)

        if inp.key_contact_left:
            actions_ar.insert(0, "🚨 تواصل فوراً مع الحساب — جهة الاتصال الرئيسية غادرت")
            actions_en.insert(0, "🚨 Contact account immediately — key contact has left")

        if inp.days_since_last_interaction > 21:
            actions_ar.append("📞 اتصل أو أرسل رسالة واتساب بحلول اليوم — 21+ يوم بلا تواصل")
            actions_en.append("📞 Call or WhatsApp today — 21+ days without contact")

        return actions_ar[:5], actions_en[:5]
