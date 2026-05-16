"""Deterministic revenue-readiness scoring for the Diagnostic.

Modeled on `proof_os.proof_score`: a transparent, no-LLM 0-100 score built from
the share of present readiness signals, with a band label. Pure: no I/O.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

# The readiness signals the diagnostic checks. Each present signal contributes
# an equal share of the 0-100 score. Ordered for stable reporting.
READINESS_SIGNALS: tuple[str, ...] = (
    "crm_source_documented",
    "pipeline_stages_defined",
    "follow_up_process_exists",
    "data_quality_reviewed",
    "ai_usage_governed",
    "forecast_evidence_based",
    "decision_passport_present",
)


@dataclass(frozen=True)
class ReadinessScore:
    """A deterministic revenue-readiness score with a band label."""

    score: int
    band: str
    present_signals: tuple[str, ...]
    missing_signals: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "score": self.score,
            "band": self.band,
            "present_signals": list(self.present_signals),
            "missing_signals": list(self.missing_signals),
            "is_estimate": True,
        }


def readiness_band(score: int) -> str:
    """Map a 0-100 readiness score to a band label."""
    if score >= 85:
        return "ai_ready"
    if score >= 60:
        return "sprint_ready"
    if score >= 35:
        return "diagnostic_in_progress"
    return "foundational_gaps"


def score_readiness(signals: Mapping[str, bool]) -> ReadinessScore:
    """Score revenue readiness from a map of present/absent signals.

    Args:
        signals: `{signal_name: bool}`. Unknown keys are ignored; missing keys
            count as absent.

    Returns:
        A `ReadinessScore` — `score` is the rounded share of present signals.
    """
    present = tuple(s for s in READINESS_SIGNALS if bool(signals.get(s)))
    missing = tuple(s for s in READINESS_SIGNALS if not bool(signals.get(s)))
    total = len(READINESS_SIGNALS)
    score = int(round(100.0 * len(present) / total)) if total else 0
    return ReadinessScore(
        score=score,
        band=readiness_band(score),
        present_signals=present,
        missing_signals=missing,
    )
