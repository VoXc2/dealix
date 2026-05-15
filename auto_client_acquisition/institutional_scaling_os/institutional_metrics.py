"""Institutional scaling discipline — when not to scale."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ScalingDisciplineSnapshot:
    """Composite health signals (set by leadership from metrics)."""

    trust_strong: bool
    proof_strong: bool
    productization_strong: bool
    market_language_strong: bool


def scaling_discipline_blockers(snapshot: ScalingDisciplineSnapshot) -> tuple[str, ...]:
    """Blocking reasons aligned with doctrine: trust/proof/product/market."""
    s = snapshot
    out: list[str] = []
    if not s.trust_strong:
        out.append("trust_metrics_weak_no_scale")
    if not s.proof_strong:
        out.append("proof_metrics_weak_no_claims")
    if not s.productization_strong:
        out.append("productization_weak_agency_risk")
    if not s.market_language_strong:
        out.append("market_metrics_weak_language_not_owned")
    return tuple(out)
