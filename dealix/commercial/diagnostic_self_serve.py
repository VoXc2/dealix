"""Self-Serve Diagnostic Engine — evidence-governed reusable schemas."""

from __future__ import annotations

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
    impact_basis: dict[str, Any] = Field(default_factory=dict)
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
    impact_truth_class: str = "UNKNOWN"
    impact_basis: dict[str, Any] = Field(default_factory=dict)
    recommended_next_step: str
    economic_cell_candidate: dict[str, Any] = Field(default_factory=dict)


class SelfServeDiagnostic:
    REQUIRED_IMPACT_BASIS = {
        "source_value",
        "source_type",
        "calculation",
        "assumptions",
        "timeframe",
        "confidence",
        "owner",
    }

    def assess(self, inp: DiagnosticInput) -> DiagnosticOutput:
        bottlenecks: list[str] = []
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

        basis_complete = (
            self.REQUIRED_IMPACT_BASIS.issubset(inp.impact_basis)
            and inp.cost_hypothesis_sar > 0
        )
        if basis_complete:
            impact = (
                f"{inp.cost_hypothesis_sar * 0.1:.0f}–"
                f"{inp.cost_hypothesis_sar * 0.3:.0f} SAR/month ESTIMATED; "
                "validate before use"
            )
            impact_truth = "ESTIMATED"
        else:
            impact = UNKNOWN
            impact_truth = "UNKNOWN"

        return DiagnosticOutput(
            diagnostic_id=inp.diagnostic_id,
            problem_summary=f"{inp.sector} {inp.problem} in {inp.workflow} — {inp.desired_state}",
            bottleneck_map=bottlenecks or ["unknown — evidence needed"],
            automation_candidates=automation,
            ai_candidates=ai,
            non_ai_candidates=non_ai,
            quick_wins=quick,
            risk_notes=[inp.risk]
            if inp.risk != UNKNOWN
            else ["unknown — PDPL/approval review needed"],
            expected_impact_range=impact,
            impact_truth_class=impact_truth,
            impact_basis=dict(inp.impact_basis) if basis_complete else {},
            recommended_next_step="discovery" if inp.consent else "request_consent_then_discovery",
            economic_cell_candidate={
                "sector": inp.sector,
                "buyer": inp.buyer_role,
                "problem": inp.problem,
                "workflow": inp.workflow,
                "truth_class": "PATTERN",
                "counts_as_pipeline": False,
            },
        )


__all__ = ["SelfServeDiagnostic", "DiagnosticInput", "DiagnosticOutput", "UNKNOWN"]
