"""The 7-layer Assurance System orchestrator.

Runs every layer in order and emits one composite ``AssuranceReport``
with a binary scale / no-scale verdict:

    Gate -> Scorecard -> Test -> Evidence -> KPI -> Review -> Improvement

The verdict is ``scale`` only when ALL 7 no-scale conditions are satisfied
AND all 6 readiness gates pass. Any unknown blocks scaling — the system
never green-lights growth on missing evidence.
"""
from __future__ import annotations

from dataclasses import asdict
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.assurance_os.acceptance_tests import run_acceptance_tests
from auto_client_acquisition.assurance_os.conditions import (
    evaluate_no_scale_conditions,
)
from auto_client_acquisition.assurance_os.funnel import build_funnel
from auto_client_acquisition.assurance_os.gates import evaluate_gates
from auto_client_acquisition.assurance_os.health_score import compute_health
from auto_client_acquisition.assurance_os.improvement import (
    build_improvement_backlog,
    select_experiments,
)
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    AssuranceReport,
)
from auto_client_acquisition.assurance_os.review import (
    build_board_pack,
    build_operating_review,
)
from auto_client_acquisition.assurance_os.scorecards import evaluate_scorecards

LAYERS: list[str] = [
    "gate", "scorecard", "test", "evidence", "kpi", "review", "improvement",
]


def run_assurance(inputs: AssuranceInputs | None = None) -> AssuranceReport:
    """Run the full 7-layer assurance pipeline."""
    inputs = inputs or AssuranceInputs()

    # Layer 1 — Gates
    gates = evaluate_gates(inputs)
    # Layer 2 — Scorecards + Full Ops Health Score
    scorecards = evaluate_scorecards(inputs)
    health = compute_health(inputs)
    # Layer 3 — Acceptance Tests
    acceptance = run_acceptance_tests(inputs)
    # Layer 4 — Evidence / No-Scale Conditions
    conditions = evaluate_no_scale_conditions(inputs, health)
    # Layer 5 — KPI / Funnel
    funnel = build_funnel(inputs)
    # Layer 6 — Review
    review = build_operating_review(inputs, funnel, gates, acceptance)
    # Layer 7 — Improvement
    experiments = select_experiments(inputs)
    improvement = build_improvement_backlog(inputs)

    verdict, reasons = _verdict(gates, conditions)

    return AssuranceReport(
        generated_at=datetime.now(UTC).isoformat(),
        layers=list(LAYERS),
        gates=gates,
        scorecards=scorecards,
        health=health,
        acceptance_tests=acceptance,
        no_scale_conditions=conditions,
        funnel=funnel,
        review=review,
        experiments=experiments,
        improvement=improvement,
        verdict=verdict,
        verdict_reasons=reasons,
    )


def _verdict(gates: list[Any], conditions: list[Any]) -> tuple[str, list[str]]:
    """Decide scale / no_scale and collect the blocking reasons."""
    reasons: list[str] = []
    for cond in conditions:
        if cond.satisfied is None:
            reasons.append(f"condition '{cond.id}' is unknown ({cond.requirement})")
        elif cond.satisfied is False:
            reasons.append(
                f"condition '{cond.id}' not met: {cond.actual} vs {cond.requirement}"
            )
    for gate in gates:
        if not gate.passed:
            detail = (f"{gate.unknown_count} unknown criteria"
                      if gate.unknown_count else "criteria failing")
            reasons.append(f"gate '{gate.gate_id}' not passed ({detail})")
    verdict = "scale" if not reasons else "no_scale"
    return verdict, reasons


def report_to_dict(report: AssuranceReport) -> dict[str, Any]:
    """JSON-serializable view of an AssuranceReport (for HTTP responses)."""
    return asdict(report)
