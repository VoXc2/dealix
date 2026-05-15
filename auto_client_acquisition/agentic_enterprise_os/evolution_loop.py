"""Continuous Evolution Loop — closes the feedback loop into prioritized actions.

نظام التطوّر المستمر — يحوّل التغذية الراجعة إلى توصيات تحسين مرتَّبة بالأولوية.

Reads three feedback sources — the weekly learning report, evaluation gaps, and
the friction log — and emits prioritized recommendations. The loop performs no
I/O: every source is supplied by the caller. Article 8 (no fabrication): every
recommendation cites a concrete source; absent sources yield no recommendations.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from typing import TYPE_CHECKING

from auto_client_acquisition.agentic_enterprise_os.evaluation_harness import EvaluationReport

if TYPE_CHECKING:
    from auto_client_acquisition.learning_flywheel.aggregator import WeeklyLearningReport

_FRICTION_RECURRENCE_THRESHOLD = 3


@dataclass(frozen=True, slots=True)
class FrictionEntry:
    """One recurring friction signal."""

    area: str
    detail_en: str
    detail_ar: str
    occurrences: int


@dataclass(frozen=True, slots=True)
class EvolutionRecommendation:
    """A prioritized improvement action with a cited source."""

    priority: int
    area: str
    rationale_ar: str
    rationale_en: str
    source: str


@dataclass(frozen=True, slots=True)
class EvolutionLoopResult:
    """Output of one evolution-loop pass."""

    recommendations: tuple[EvolutionRecommendation, ...]
    sources_present: dict[str, bool]


def run_evolution_loop(
    *,
    weekly_report: WeeklyLearningReport | None = None,
    evaluation: EvaluationReport | None = None,
    friction_log: Sequence[FrictionEntry] = (),
) -> EvolutionLoopResult:
    """Convert feedback signals into prioritized recommendations.

    Priority order: evaluation gaps (1) > recurring friction (2) > weekly
    learning failures (3). With no source data, returns no recommendations.
    """
    recommendations: list[EvolutionRecommendation] = []

    if evaluation is not None:
        for dimension in evaluation.gaps:
            recommendations.append(
                EvolutionRecommendation(
                    priority=1,
                    area=f"evaluation:{dimension}",
                    rationale_ar=(
                        f"بُعد التقييم «{dimension}» بلا عيّنات — "
                        "أضف حالات تقييم قبل توسيع الأتمتة."
                    ),
                    rationale_en=(
                        f"Evaluation dimension '{dimension}' has no samples — "
                        "add eval cases before scaling automation."
                    ),
                    source="evaluation_harness",
                )
            )

    for entry in friction_log:
        if entry.occurrences >= _FRICTION_RECURRENCE_THRESHOLD:
            recommendations.append(
                EvolutionRecommendation(
                    priority=2,
                    area=f"friction:{entry.area}",
                    rationale_ar=f"احتكاك متكرر ({entry.occurrences}×): {entry.detail_ar}",
                    rationale_en=f"Repeated friction ({entry.occurrences}x): {entry.detail_en}",
                    source="friction_log",
                )
            )

    if weekly_report is not None:
        for failed in getattr(weekly_report, "what_failed", ()):
            recommendations.append(
                EvolutionRecommendation(
                    priority=3,
                    area="weekly_learning",
                    rationale_ar=f"تعلُّم أسبوعي — لم ينجح: {failed}",
                    rationale_en=f"Weekly learning — did not work: {failed}",
                    source="learning_flywheel",
                )
            )

    recommendations.sort(key=lambda rec: rec.priority)
    sources_present = {
        "evaluation_harness": evaluation is not None,
        "friction_log": len(friction_log) > 0,
        "learning_flywheel": weekly_report is not None,
    }
    return EvolutionLoopResult(
        recommendations=tuple(recommendations),
        sources_present=sources_present,
    )


__all__ = [
    "EvolutionLoopResult",
    "EvolutionRecommendation",
    "FrictionEntry",
    "run_evolution_loop",
]
