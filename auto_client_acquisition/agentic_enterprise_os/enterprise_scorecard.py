"""Enterprise Scorecard — the combined capstone view over the agentic enterprise.

البطاقة الموحَّدة للمؤسسة — تجمع مؤشر النضج والتغطية والتقييم والتطوّر والعرض.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from auto_client_acquisition.agentic_enterprise_os.coverage_registry import coverage_summary
from auto_client_acquisition.agentic_enterprise_os.enterprise_maturity import (
    EnterpriseCapabilityScores,
    MaturityStage,
    compute_emi,
    enterprise_maturity_stage,
)
from auto_client_acquisition.agentic_enterprise_os.evaluation_harness import (
    EvalDimensionResult,
    EvaluationReport,
    run_evaluation_harness,
)
from auto_client_acquisition.agentic_enterprise_os.evolution_loop import (
    EvolutionLoopResult,
    FrictionEntry,
    run_evolution_loop,
)
from auto_client_acquisition.agentic_enterprise_os.service_ladder import (
    enterprise_offer_recommendation,
)

if TYPE_CHECKING:
    from auto_client_acquisition.learning_flywheel.aggregator import WeeklyLearningReport


@dataclass(frozen=True, slots=True)
class EnterpriseScorecard:
    """The unified scorecard composing all capstone signals."""

    emi: float
    stage: MaturityStage
    coverage: dict
    evaluation: EvaluationReport
    evolution: EvolutionLoopResult
    offer: dict


def build_enterprise_scorecard(
    *,
    scores: EnterpriseCapabilityScores,
    eval_results: Sequence[EvalDimensionResult] = (),
    weekly_report: WeeklyLearningReport | None = None,
    friction_log: Sequence[FrictionEntry] = (),
) -> EnterpriseScorecard:
    """Compose maturity, coverage, evaluation, evolution, and offer into one view."""
    emi = compute_emi(scores)
    evaluation = run_evaluation_harness(eval_results)
    evolution = run_evolution_loop(
        weekly_report=weekly_report,
        evaluation=evaluation,
        friction_log=friction_log,
    )
    return EnterpriseScorecard(
        emi=emi,
        stage=enterprise_maturity_stage(emi),
        coverage=coverage_summary(),
        evaluation=evaluation,
        evolution=evolution,
        offer=enterprise_offer_recommendation(emi),
    )


__all__ = ["EnterpriseScorecard", "build_enterprise_scorecard"]
