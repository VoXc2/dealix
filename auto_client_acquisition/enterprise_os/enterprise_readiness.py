"""Enterprise service readiness scorecard.

Eight dimensions mapped to the DEALIX_READINESS gates (Gate 1 Offer, Gate 2
Delivery, Gate 3 Product, Gate 4 Governance, Gate 5 Demo, Gate 6 Sales, Gate 8
Retainer, Gate 9 Scale). Governance is weighted highest because Gate 4 has the
strictest pass bar (>=90).

A service is sellable only when its band is ``sellable`` or higher. The
registered scores below are intentionally low: the enterprise tier is tracked
as Planned in dealix/registers/no_overclaim.yaml and is not sellable until the
founder runs the gates and raises the scores against real evidence.
"""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class ReadinessScores(NamedTuple):
    """Each gate dimension, 0-100, before weighting."""

    offer: float
    delivery: float
    product: float
    governance: float
    demo: float
    sales: float
    retainer: float
    scale: float


class ReadinessBand(StrEnum):
    BLOCKED = "blocked"
    BETA = "beta"
    SELLABLE = "sellable"
    PREMIUM = "premium"
    ENTERPRISE_READY = "enterprise_ready"


class ReadinessReport(NamedTuple):
    """Computed readiness for one enterprise service."""

    service_id: str
    scores: ReadinessScores
    total: float
    band: ReadinessBand
    sellable: bool


def compute_readiness_score(scores: ReadinessScores) -> float:
    """Weighted 0-100 readiness score. Governance carries the heaviest weight."""
    weighted = (
        0.14 * scores.offer
        + 0.14 * scores.delivery
        + 0.10 * scores.product
        + 0.20 * scores.governance
        + 0.10 * scores.demo
        + 0.12 * scores.sales
        + 0.10 * scores.retainer
        + 0.10 * scores.scale
    )
    return max(0.0, min(100.0, round(float(weighted), 2)))


def score_band(score: float) -> ReadinessBand:
    """Map a 0-100 score to a readiness band."""
    if score >= 95:
        return ReadinessBand.ENTERPRISE_READY
    if score >= 90:
        return ReadinessBand.PREMIUM
    if score >= 85:
        return ReadinessBand.SELLABLE
    if score >= 70:
        return ReadinessBand.BETA
    return ReadinessBand.BLOCKED


def is_sellable(score: float) -> bool:
    """True only when the score reaches the sellable band or higher."""
    return score_band(score) in (
        ReadinessBand.SELLABLE,
        ReadinessBand.PREMIUM,
        ReadinessBand.ENTERPRISE_READY,
    )


# Honest starting scores — offers are documented, delivery/product/demo are not
# yet built or proven, so every enterprise service starts BLOCKED.
ENTERPRISE_READINESS: dict[str, ReadinessScores] = {
    "enterprise_ai_operating_system": ReadinessScores(
        offer=72, delivery=42, product=38, governance=58,
        demo=28, sales=52, retainer=34, scale=24,
    ),
    "ai_revenue_transformation": ReadinessScores(
        offer=74, delivery=55, product=50, governance=60,
        demo=46, sales=58, retainer=44, scale=34,
    ),
    "company_brain_knowledge_os": ReadinessScores(
        offer=72, delivery=52, product=48, governance=62,
        demo=44, sales=54, retainer=40, scale=30,
    ),
    "ai_governance_trust_program": ReadinessScores(
        offer=70, delivery=48, product=44, governance=70,
        demo=30, sales=50, retainer=30, scale=26,
    ),
    "executive_intelligence_center": ReadinessScores(
        offer=70, delivery=40, product=36, governance=56,
        demo=26, sales=48, retainer=32, scale=22,
    ),
}


def get_readiness(service_id: str) -> ReadinessReport | None:
    """Return the readiness report for one enterprise service, or None."""
    scores = ENTERPRISE_READINESS.get(service_id)
    if scores is None:
        return None
    total = compute_readiness_score(scores)
    return ReadinessReport(
        service_id=service_id,
        scores=scores,
        total=total,
        band=score_band(total),
        sellable=is_sellable(total),
    )


def list_readiness() -> tuple[ReadinessReport, ...]:
    """Readiness reports for every registered enterprise service."""
    reports = (get_readiness(sid) for sid in ENTERPRISE_READINESS)
    return tuple(r for r in reports if r is not None)
