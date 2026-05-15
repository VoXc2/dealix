"""Proof Pack scoring for governance (not only sales)."""

from __future__ import annotations

from dataclasses import dataclass

# Weights sum to 100; each dimension is 0–100.
_WEIGHTS: tuple[tuple[str, int], ...] = (
    ("metric_clarity", 20),
    ("evidence_quality", 20),
    ("source_clarity", 15),
    ("governance_confidence", 15),
    ("business_relevance", 15),
    ("retainer_linkage", 15),
)

# Proof Pack as governance artifact — sections expected for enterprise narrative.
PROOF_PACK_GOVERNANCE_SECTIONS: tuple[str, ...] = (
    "problem",
    "inputs",
    "source_passports",
    "work_completed",
    "metrics",
    "before_after",
    "ai_outputs",
    "governance_events",
    "blocked_actions",
    "business_value",
    "risks",
    "limitations",
    "recommended_next_step",
)


@dataclass(frozen=True, slots=True)
class ProofGovernanceDimensions:
    metric_clarity: int
    evidence_quality: int
    source_clarity: int
    governance_confidence: int
    business_relevance: int
    retainer_linkage: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def proof_governance_score(dimensions: ProofGovernanceDimensions) -> int:
    """Weighted 0–100 institutional proof score."""
    d = dimensions
    values = (
        _clamp_pct(d.metric_clarity),
        _clamp_pct(d.evidence_quality),
        _clamp_pct(d.source_clarity),
        _clamp_pct(d.governance_confidence),
        _clamp_pct(d.business_relevance),
        _clamp_pct(d.retainer_linkage),
    )
    weights = tuple(w for _, w in _WEIGHTS)
    total = sum(v * w for v, w in zip(values, weights, strict=True))
    return min(100, total // 100)


def proof_pack_section_coverage(present: frozenset[str]) -> tuple[int, int]:
    """Return (filled_count, total_required) for proof pack governance outline."""
    req = PROOF_PACK_GOVERNANCE_SECTIONS
    filled = sum(1 for s in req if s in present)
    return filled, len(req)


def proof_case_band(score: int) -> str:
    if score >= 85:
        return "case_candidate"
    if score >= 70:
        return "sales_support"
    return "internal_learning_only"
