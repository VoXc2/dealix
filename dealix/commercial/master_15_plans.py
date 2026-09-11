"""Master 15 Plans — best, smart, comprehensive, future, real, launch, money, expanded."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from dealix.commercial.probability_engine import ProbBand, ProbabilityVector

class MasterPlan(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    plan_id: str
    title_ar: str
    title_en: str
    sector: str
    buyer: str
    problem: str
    offer: str
    channel: str
    time_to_cash_days: int
    deep_wip_slot: str  # A/B/C
    evidence_ref: str = ""
    expected_value_range: str = "5,000–15,000 SAR (estimate)"
    status: str = "IDEA"

PLANS: list[MasterPlan] = [
    MasterPlan(plan_id="P01", title_ar="ZATCA Wave25", title_en="ZATCA Wave25", sector="finance_fintech_insurance", buyer="cfo", problem="fatoora", offer="Fatoora Ops", channel="website", time_to_cash_days=14, deep_wip_slot="B", evidence_ref="zatca.gov.sa"),
    MasterPlan(plan_id="P02", title_ar="Etimad Tender", title_en="Etimad Tender", sector="government_b2g", buyer="procurement_director", problem="procurement_delay", offer="Tender Intelligence", channel="etimad", time_to_cash_days=30, deep_wip_slot="B", evidence_ref="tenders.etimad.sa"),
    MasterPlan(plan_id="P03", title_ar="MISA Market Entry", title_en="MISA Market Entry", sector="export_import_rhq", buyer="ceo", problem="market_entry_friction", offer="Saudi Market Entry Sprint", channel="misa", time_to_cash_days=21, deep_wip_slot="B", evidence_ref="misa.gov.sa"),
    MasterPlan(plan_id="P04", title_ar="AI Governance", title_en="AI Governance", sector="technology_saas_si", buyer="ciso", problem="ai_governance_risk", offer="AI Governance Sprint", channel="website", time_to_cash_days=14, deep_wip_slot="B", evidence_ref="NCA ECC"),
    MasterPlan(plan_id="P05", title_ar="Private AI", title_en="Private AI", sector="technology_saas_si", buyer="cto", problem="cyber_risk", offer="Private AI", channel="partner", time_to_cash_days=30, deep_wip_slot="B", evidence_ref="local LLM"),
    MasterPlan(plan_id="P06", title_ar="Revenue Leakage", title_en="Revenue Leakage", sector="professional_services", buyer="sales_director", problem="revenue_leakage", offer="Revenue Command", channel="website", time_to_cash_days=14, deep_wip_slot="B", evidence_ref="CRM"),
    MasterPlan(plan_id="P07", title_ar="Document Intelligence", title_en="Document Intelligence", sector="construction_epc", buyer="operations_director", problem="document_chaos", offer="Document Intelligence", channel="website", time_to_cash_days=21, deep_wip_slot="B", evidence_ref="documents"),
    MasterPlan(plan_id="P08", title_ar="B2G Readiness", title_en="B2G Readiness", sector="government_b2g", buyer="procurement_director", problem="supplier_readiness", offer="B2G Readiness", channel="etimad", time_to_cash_days=30, deep_wip_slot="B", evidence_ref="Jadeer"),
    MasterPlan(plan_id="P09", title_ar="Partner Economy", title_en="Partner Economy", sector="technology_saas_si", buyer="sales_director", problem="partner", offer="Partner Desk", channel="partner", time_to_cash_days=45, deep_wip_slot="C", evidence_ref="partner"),
    MasterPlan(plan_id="P10", title_ar="Marketplace", title_en="Marketplace", sector="technology_saas_si", buyer="sales_director", problem="marketplace", offer="Azure/AWS", channel="marketplace", time_to_cash_days=30, deep_wip_slot="C", evidence_ref="marketplace"),
    MasterPlan(plan_id="P11", title_ar="Diagnostic Product", title_en="Diagnostic Product", sector="technology_saas_si", buyer="ceo", problem="diagnostic", offer="Paid Diagnostic 2500", channel="website", time_to_cash_days=7, deep_wip_slot="A", evidence_ref="diagnostic"),
    MasterPlan(plan_id="P12", title_ar="Content Factory", title_en="Content Factory", sector="technology_saas_si", buyer="marketing_director", problem="content", offer="Proof→4 atoms", channel="distribution", time_to_cash_days=7, deep_wip_slot="C", evidence_ref="proof"),
    MasterPlan(plan_id="P13", title_ar="SaaS Onboarding", title_en="SaaS Onboarding", sector="technology_saas_si", buyer="ceo", problem="onboarding", offer="SaaS 6 stages", channel="website", time_to_cash_days=7, deep_wip_slot="A", evidence_ref="SaaS"),
    MasterPlan(plan_id="P14", title_ar="Market Control", title_en="Market Control", sector="technology_saas_si", buyer="ceo", problem="market_control", offer="20×44 Dashboard", channel="website", time_to_cash_days=0, deep_wip_slot="A", evidence_ref="dashboard"),
    MasterPlan(plan_id="P15", title_ar="Next Expansion", title_en="Next Expansion", sector="technology_saas_si", buyer="ceo", problem="expansion", offer="AI Sector 5", channel="website", time_to_cash_days=30, deep_wip_slot="C", evidence_ref="AI"),
]

class Master15Executor:
    def top3(self) -> list[MasterPlan]:
        # Best thought: rank by time_to_cash + evidence + DeepWIP slot A first (Product/Production Trust), then B (Money), then C (Scale)
        order = {"A": 0, "B": 1, "C": 2}
        return sorted(PLANS, key=lambda p: (order[p.deep_wip_slot], p.time_to_cash_days))[:3]

    def to_dict(self) -> dict[str, Any]:
        return {"total": len(PLANS), "top3": [p.plan_id for p in self.top3()], "plans": [p.model_dump() for p in PLANS]}

__all__ = ["MasterPlan", "PLANS", "Master15Executor"]
