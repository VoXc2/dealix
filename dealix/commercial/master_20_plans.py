"""Master 20 Plans — best, smart, comprehensive, all aspects, merged 15 + 5 new, expanded."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict

from dealix.commercial.master_15_plans import PLANS as PLANS_15, MasterPlan

# 5 new plans to reach 20, best thought
NEW_5: list[MasterPlan] = [
    MasterPlan(plan_id="P16", title_ar="جاهزية البيانات", title_en="Data Readiness", sector="technology_saas_si", buyer="cio", problem="data_fragmentation", offer="Data Diagnostic", channel="website", time_to_cash_days=14, deep_wip_slot="B", evidence_ref="CIO"),
    MasterPlan(plan_id="P17", title_ar="أتمتة", title_en="Automation Sprint", sector="industrial_manufacturing", buyer="coo", problem="operational_exception_overload", offer="Automation Sprint", channel="website", time_to_cash_days=21, deep_wip_slot="B", evidence_ref="operations"),
    MasterPlan(plan_id="P18", title_ar="نجاح عميل", title_en="Customer Success", sector="professional_services", buyer="customer_service", problem="churn", offer="Customer Success", channel="support", time_to_cash_days=30, deep_wip_slot="C", evidence_ref="support"),
    MasterPlan(plan_id="P19", title_ar="تقوية أمنية", title_en="Security Hardening", sector="technology_saas_si", buyer="ciso", problem="cyber_risk", offer="Cyber Readiness", channel="website", time_to_cash_days=14, deep_wip_slot="B", evidence_ref="NCA"),
    MasterPlan(plan_id="P20", title_ar="أكاديمية", title_en="Training Academy", sector="education_training", buyer="hr_director", problem="workforce", offer="Training Academy", channel="website", time_to_cash_days=21, deep_wip_slot="C", evidence_ref="training"),
]

PLANS_20: list[MasterPlan] = PLANS_15 + NEW_5

class Master20Executor:
    def top3(self) -> list[MasterPlan]:
        order = {"A": 0, "B": 1, "C": 2}
        return sorted(PLANS_20, key=lambda p: (order[p.deep_wip_slot], p.time_to_cash_days))[:3]

    def to_dict(self) -> dict[str, Any]:
        return {"total": len(PLANS_20), "merged_15": len(PLANS_15), "new_5": len(NEW_5), "top3": [p.plan_id for p in self.top3()], "plans": [p.model_dump() for p in PLANS_20]}

__all__ = ["MasterPlan", "PLANS_20", "Master20Executor"]
