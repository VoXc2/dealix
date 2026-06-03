"""Compounding decision taxonomy — signals → operating decisions."""

from __future__ import annotations

from enum import StrEnum


class CompoundingDecision(StrEnum):
    SCALE = "scale"
    BUILD = "build"
    PILOT = "pilot"
    HOLD = "hold"
    KILL = "kill"
    RAISE_PRICE = "raise_price"
    OFFER_RETAINER = "offer_retainer"
    CREATE_PLAYBOOK = "create_playbook"
    CREATE_BENCHMARK = "create_benchmark"
    CREATE_BUSINESS_UNIT = "create_business_unit"
    CREATE_VENTURE_CANDIDATE = "create_venture_candidate"


def suggest_compounding_decision(
    *,
    pattern_occurrences: int,
    avg_proof_score: float,
    retainer_path_exists: bool,
    governance_risk_low: bool,
) -> CompoundingDecision | None:
    """Minimal deterministic mapper for tests and internal tooling."""
    if not governance_risk_low:
        return CompoundingDecision.HOLD
    if pattern_occurrences >= 6 and avg_proof_score >= 86.0 and retainer_path_exists:
        return CompoundingDecision.SCALE
    if pattern_occurrences >= 3 and avg_proof_score >= 80.0:
        return CompoundingDecision.CREATE_PLAYBOOK
    if pattern_occurrences >= 6:
        return CompoundingDecision.CREATE_BENCHMARK
    return None
