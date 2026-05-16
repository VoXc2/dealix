"""Customer health 2.0 — composite from signals (initiative 151)."""

from __future__ import annotations

from typing import Any


def compute_health_v2(*, signals: dict[str, Any]) -> dict[str, Any]:
    score = 0
    if signals.get("proof_pack_opened"):
        score += 25
    if signals.get("nps_promoter"):
        score += 25
    if signals.get("adoption_milestone_met"):
        score += 25
    if signals.get("renewal_risk"):
        score -= 30
    if score >= 70:
        band = "healthy"
    elif score >= 40:
        band = "expansion_ready"
    elif score >= 20:
        band = "at_risk"
    else:
        band = "critical"
    return {"score": score, "band": band, "signals": signals}
