"""Enterprise Maturity System — 10-capability scorecard for the agentic enterprise.

نظام نضج المؤسسة — يقيس عشر قدرات تنظيمية ويحسب مؤشر نضج المؤسسة (EMI).

This is the answer to "how do you ensure you actually reached this level?":
measure organizational capability, not features. Mirrors the weighted-composite
style of ``intelligence_os.capability_index``.
"""

from __future__ import annotations

from typing import NamedTuple


class EnterpriseCapabilityScores(NamedTuple):
    """The 10 capabilities of an agentic enterprise — each 0–100."""

    redesign_workflows: float
    execute_workflows: float
    govern_workflows: float
    evaluate_workflows: float
    scale_workflows: float
    supervise_agents: float
    manage_digital_workforce: float
    generate_executive_intelligence: float
    measure_operational_impact: float
    improve_continuously: float


class MaturityStage(NamedTuple):
    """A bilingual enterprise maturity stage."""

    key: str
    label_ar: str
    label_en: str


# Weights sum to 1.0; governance and evaluation carry the most weight because an
# ungoverned or unevaluated agentic organization is the highest-risk failure mode.
_EMI_WEIGHTS: dict[str, float] = {
    "govern_workflows": 0.15,
    "execute_workflows": 0.13,
    "evaluate_workflows": 0.12,
    "improve_continuously": 0.12,
    "scale_workflows": 0.10,
    "supervise_agents": 0.10,
    "redesign_workflows": 0.08,
    "manage_digital_workforce": 0.08,
    "generate_executive_intelligence": 0.07,
    "measure_operational_impact": 0.05,
}


def _clamp_pct(value: float) -> float:
    return max(0.0, min(100.0, float(value)))


def compute_emi(scores: EnterpriseCapabilityScores) -> float:
    """Enterprise Maturity Index — weighted composite of the 10 capabilities (0–100)."""
    total = sum(
        _clamp_pct(getattr(scores, name)) * weight for name, weight in _EMI_WEIGHTS.items()
    )
    return _clamp_pct(total)


def enterprise_maturity_stage(emi: float) -> MaturityStage:
    """Map an Enterprise Maturity Index to a bilingual maturity stage."""
    if emi < 35:
        return MaturityStage("ad_hoc", "مؤسسة عشوائية", "Ad-hoc organization")
    if emi < 55:
        return MaturityStage("structured", "مؤسسة منظَّمة", "Structured organization")
    if emi < 75:
        return MaturityStage("governed", "مؤسسة محوكَمة", "Governed organization")
    if emi < 90:
        return MaturityStage("scaled", "مؤسسة مُوسَّعة", "Scaled operating organization")
    return MaturityStage(
        "autonomous_enterprise", "مؤسسة وكيلة محوكَمة", "Governed agentic enterprise"
    )


__all__ = [
    "EnterpriseCapabilityScores",
    "MaturityStage",
    "compute_emi",
    "enterprise_maturity_stage",
]
