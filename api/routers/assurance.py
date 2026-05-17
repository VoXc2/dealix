"""Dealix Assurance System — HTTP surface.

Read-only endpoints over the 7-layer assurance pipeline
(Gate -> Scorecard -> Test -> Evidence -> KPI -> Review -> Improvement).

GET endpoints run with empty inputs and honestly surface ``unknown`` for
any business fact not yet measured. POST /report accepts supplied facts
(funnel counts, gate answers, machine maturity, acceptance results, KPIs)
and returns the full composite report with a scale / no-scale verdict.

Hard rules: read-only; never sends, never charges, never auto-acts.
"""
from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel, Field

from auto_client_acquisition.assurance_os.assurance_system import (
    LAYERS,
    report_to_dict,
    run_assurance,
)
from auto_client_acquisition.assurance_os.config_loader import load_config
from auto_client_acquisition.assurance_os.funnel import build_funnel
from auto_client_acquisition.assurance_os.models import AssuranceInputs
from auto_client_acquisition.assurance_os.review import build_board_pack

router = APIRouter(prefix="/api/v1/assurance", tags=["Assurance System"])

_HARD_GATES = {
    "read_only": True,
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_data": True,
    "unknown_blocks_scale": True,
}


class AssuranceInputsBody(BaseModel):
    """Caller-supplied business facts. Anything omitted surfaces as
    ``unknown`` in the report — the system never fabricates data."""

    funnel_counts: dict[str, int] = Field(default_factory=dict)
    gate_answers: dict[str, bool] = Field(default_factory=dict)
    machine_maturity: dict[str, int] = Field(default_factory=dict)
    acceptance_results: dict[str, str] = Field(default_factory=dict)
    kpi_values: dict[str, float] = Field(default_factory=dict)
    evidence_completeness_pct: float | None = None
    lead_scoring_coverage_pct: float | None = None
    support_high_risk_escalation_pct: float | None = None
    affiliate_payout_before_payment_count: int | None = None
    approval_compliance_pct: float | None = None
    week_of: str = ""
    month: str = ""
    experiments: list[dict[str, Any]] = Field(default_factory=list)
    improvement_items: list[dict[str, Any]] = Field(default_factory=list)

    def to_inputs(self) -> AssuranceInputs:
        return AssuranceInputs(**self.model_dump())


@router.get("/status")
async def assurance_status() -> dict[str, Any]:
    cfg = load_config()
    return {
        "status": "ok",
        "system": "dealix_assurance_system",
        "layers": list(LAYERS),
        "config_loaded": cfg.loaded_ok,
        "config_errors": cfg.errors,
        "hard_gates": _HARD_GATES,
    }


@router.get("/report")
async def assurance_report() -> dict[str, Any]:
    """Full 7-layer report with empty inputs (everything unknown)."""
    return report_to_dict(run_assurance(AssuranceInputs()))


@router.post("/report")
async def assurance_report_with_inputs(body: AssuranceInputsBody) -> dict[str, Any]:
    """Full 7-layer report computed from supplied business facts."""
    return report_to_dict(run_assurance(body.to_inputs()))


@router.get("/gates")
async def assurance_gates() -> dict[str, Any]:
    report = run_assurance(AssuranceInputs())
    return {"gates": [asdict(g) for g in report.gates]}


@router.get("/scorecards")
async def assurance_scorecards() -> dict[str, Any]:
    report = run_assurance(AssuranceInputs())
    return {"scorecards": [asdict(s) for s in report.scorecards]}


@router.get("/health-score")
async def assurance_health_score() -> dict[str, Any]:
    report = run_assurance(AssuranceInputs())
    return {
        "health": asdict(report.health),
        "no_scale_conditions": [asdict(c) for c in report.no_scale_conditions],
        "verdict": report.verdict,
        "verdict_reasons": report.verdict_reasons,
    }


@router.get("/acceptance-tests")
async def assurance_acceptance_tests() -> dict[str, Any]:
    report = run_assurance(AssuranceInputs())
    return {"acceptance_tests": [asdict(t) for t in report.acceptance_tests]}


@router.get("/funnel")
async def assurance_funnel() -> dict[str, Any]:
    return asdict(build_funnel(AssuranceInputs()))


@router.get("/weekly-review")
async def assurance_weekly_review() -> dict[str, Any]:
    return asdict(run_assurance(AssuranceInputs()).review)


@router.get("/board-pack")
async def assurance_board_pack() -> dict[str, Any]:
    return asdict(build_board_pack(AssuranceInputs()))
