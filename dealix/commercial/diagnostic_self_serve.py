"""Self-Serve Diagnostic Engine — reusable schemas."""

from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

UNKNOWN = "UNKNOWN"

class DiagnosticInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str
    locale: str = "ar"
    sector: str = UNKNOWN
    company_size: str = UNKNOWN
    buyer_role: str = UNKNOWN
    workflow: str = UNKNOWN
    problem: str = UNKNOWN
    frequency: str = UNKNOWN
    current_tools: str = UNKNOWN
    manual_steps: int = 0
    delay_days: int = 0
    cost_hypothesis_sar: float = 0.0
    risk: str = UNKNOWN
    desired_state: str = UNKNOWN
    consent: bool = False

class DiagnosticOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    diagnostic_id: str
    problem_summary: str
    bottleneck_map: list[str]
    automation_candidates: list[str]
    ai_candidates: list[str]
    non_ai_candidates: list[str]
    quick_wins: list[str]
    risk_notes: list[str]
    expected_impact_range: str
    recommended_next_step: str
    economic_cell_candidate: dict[str, Any] = Field(default_factory=dict)

class SelfServeDiagnostic:
    def assess(self, inp: DiagnosticInput) -> DiagnosticOutput:
        # Never promise ROI — provide range
        bottlenecks = []
        if inp.manual_steps > 5:
            bottlenecks.append(f"manual_handoff:{inp.manual_steps} steps")
        if inp.delay_days > 7:
            bottlenecks.append(f"delay:{inp.delay_days} days")
        if inp.frequency in ("daily", "hourly"):
            bottlenecks.append(f"high_frequency:{inp.frequency}")

        automation = [f"automate {inp.workflow} handoff"] if inp.workflow != UNKNOWN else []
        ai = [f"AI classification for {inp.problem}"] if inp.problem != UNKNOWN else []
        non_ai = ["standardize SOP", "RACI + approval queue"] if bottlenecks else []

        quick = automation[:1] if automation else ["map current vs desired state"]

        impact = f"{max(0, inp.cost_hypothesis_sar*0.1):.0f}–{max(0, inp.cost_hypothesis_sar*0.3):.0f} SAR/month range (estimate, requires discovery)"

        return DiagnosticOutput(
            diagnostic_id=inp.diagnostic_id,
            problem_summary=f"{inp.sector} {inp.problem} in {inp.workflow} — {inp.desired_state}",
            bottleneck_map=bottlenecks or ["unknown — discovery needed"],
            automation_candidates=automation,
            ai_candidates=ai,
            non_ai_candidates=non_ai,
            quick_wins=quick,
            risk_notes=[inp.risk] if inp.risk != UNKNOWN else ["unknown — PDPL/approval review needed"],
            expected_impact_range=impact,
            recommended_next_step="discovery" if inp.consent else "request_consent_then_discovery",
            economic_cell_candidate={"sector": inp.sector, "buyer": inp.buyer_role, "problem": inp.problem, "workflow": inp.workflow},
        )

__all__ = ["SelfServeDiagnostic", "DiagnosticInput", "DiagnosticOutput", "UNKNOWN"]
