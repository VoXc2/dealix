"""Low-Touch Income Registry — recurring/productized rails.

Score each by time_to_first_cash, setup_cost, gross_margin, recurrence, support_load, churn_risk, proof_required, distribution_fit, automation_ratio, founder_minutes, defensibility.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class IncomeRail(StrEnum):
    DIGITAL_TEMPLATES = "digital_templates"
    DIAGNOSTIC_PRODUCT = "diagnostic_product"
    PAID_REPORTS = "paid_reports"
    INTELLIGENCE_SUBSCRIPTION = "intelligence_subscription"
    TENDER_INTELLIGENCE_SUB = "tender_intelligence_sub"
    MARKET_ENTRY_INTELLIGENCE = "market_entry_intelligence"
    API_USAGE = "api_usage"
    MICRO_SAAS = "micro_saas"
    FULL_SAAS = "full_saas"
    MANAGED_AUTOMATION = "managed_automation"
    AI_AGENT_SUBSCRIPTION = "ai_agent_subscription"
    PRIVATE_AI_MAINTENANCE = "private_ai_maintenance"
    SUPPORT_RETAINER = "support_retainer"
    WHITE_LABEL = "white_label"
    INTEGRATION_PACKS = "integration_packs"
    MARKETPLACE_APPS = "marketplace_apps"
    PARTNER_REVENUE_SHARE = "partner_revenue_share"
    REFERRAL_REVENUE = "referral_revenue"
    TRAINING_ACADEMY = "training_academy"
    CORPORATE_WORKSHOPS = "corporate_workshops"
    CERTIFICATION = "certification"
    BENCHMARK_PRODUCT = "benchmark_product"

class LowTouchCandidate(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    rail: IncomeRail
    title_ar: str = UNKNOWN
    title_en: str = UNKNOWN
    time_to_first_cash_days: int = 30
    setup_cost_sar: float = 0.0
    gross_margin_pct: float = 0.5
    recurrence: int = Field(default=1, ge=0, le=5)  # 0 one-off, 5 high recurring
    support_load: int = Field(default=3, ge=1, le=5)
    churn_risk: int = Field(default=3, ge=1, le=5)
    proof_required: int = Field(default=3, ge=1, le=5)
    distribution_fit: int = Field(default=3, ge=1, le=5)
    automation_ratio: float = Field(default=0.5, ge=0.0, le=1.0)
    founder_minutes: int = 60
    defensibility: int = Field(default=2, ge=1, le=5)

    def score(self) -> float:
        # Higher is better: margin*recurrence*automation*defensibility / (cost+time+support+churn+proof+founder)
        numerator = self.gross_margin_pct * (self.recurrence+1) * (self.automation_ratio+0.5) * self.defensibility * self.distribution_fit
        denominator = (self.setup_cost_sar/5000 + self.time_to_first_cash_days/30 + self.support_load + self.churn_risk + self.proof_required + self.founder_minutes/60)
        return round(numerator * 10 / max(1, denominator), 3)

class LowTouchRegistry:
    def __init__(self) -> None:
        self.candidates: list[LowTouchCandidate] = []

    def add(self, c: LowTouchCandidate) -> None:
        self.candidates.append(c)

    def rank(self) -> list[LowTouchCandidate]:
        return sorted(self.candidates, key=lambda x: x.score(), reverse=True)

    def seed_defaults(self) -> None:
        self.add(LowTouchCandidate(rail=IncomeRail.DIAGNOSTIC_PRODUCT, title_en="Paid Diagnostic Product", time_to_first_cash_days=7, setup_cost_sar=2000, gross_margin_pct=0.7, recurrence=2, support_load=2, churn_risk=2, proof_required=2, distribution_fit=4, automation_ratio=0.8, founder_minutes=30, defensibility=3))
        self.add(LowTouchCandidate(rail=IncomeRail.TENDER_INTELLIGENCE_SUB, title_en="Tender Intelligence Subscription", time_to_first_cash_days=14, setup_cost_sar=5000, gross_margin_pct=0.6, recurrence=4, support_load=3, churn_risk=3, proof_required=3, distribution_fit=3, automation_ratio=0.7, founder_minutes=45, defensibility=4))
        self.add(LowTouchCandidate(rail=IncomeRail.MARKET_ENTRY_INTELLIGENCE, title_en="Saudi Market Entry Intelligence", time_to_first_cash_days=21, setup_cost_sar=8000, gross_margin_pct=0.6, recurrence=3, support_load=3, churn_risk=2, proof_required=3, distribution_fit=4, automation_ratio=0.6, founder_minutes=60, defensibility=4))
        self.add(LowTouchCandidate(rail=IncomeRail.DIGITAL_TEMPLATES, title_en="Procurement Readiness Toolkit", time_to_first_cash_days=3, setup_cost_sar=1000, gross_margin_pct=0.85, recurrence=1, support_load=1, churn_risk=1, proof_required=1, distribution_fit=5, automation_ratio=0.95, founder_minutes=15, defensibility=2))
        self.add(LowTouchCandidate(rail=IncomeRail.API_USAGE, title_en="Document Intelligence API", time_to_first_cash_days=30, setup_cost_sar=15000, gross_margin_pct=0.5, recurrence=5, support_load=4, churn_risk=3, proof_required=4, distribution_fit=3, automation_ratio=0.6, founder_minutes=90, defensibility=5))

    def to_dict(self) -> dict[str, Any]:
        return {"ranked": [(c.rail.value, c.score()) for c in self.rank()], "count": len(self.candidates)}

__all__ = ["LowTouchRegistry", "LowTouchCandidate", "IncomeRail", "UNKNOWN"]
