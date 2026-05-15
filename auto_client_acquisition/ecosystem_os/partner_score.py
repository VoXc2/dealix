"""Partner quality score — gates certified vs referral-only partners."""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS: tuple[int, ...] = (20, 20, 20, 20, 10, 10)

PARTNER_GATE_CRITERIA: tuple[str, ...] = (
    "understands_dealix_method",
    "accepts_no_unsafe_automation",
    "uses_proof_pack",
    "accepts_qa_review",
    "accepts_governance_rules",
    "no_guaranteed_outcome_claims",
    "accepts_audit_rights",
)


@dataclass(frozen=True, slots=True)
class PartnerQualityDimensions:
    lead_quality: int
    method_alignment: int
    qa_compliance: int
    governance_compliance: int
    client_feedback: int
    expansion_potential: int


def _clamp_pct(value: int) -> int:
    if value < 0:
        return 0
    if value > 100:
        return 100
    return value


def partner_quality_score(dimensions: PartnerQualityDimensions) -> int:
    d = dimensions
    values = (
        _clamp_pct(d.lead_quality),
        _clamp_pct(d.method_alignment),
        _clamp_pct(d.qa_compliance),
        _clamp_pct(d.governance_compliance),
        _clamp_pct(d.client_feedback),
        _clamp_pct(d.expansion_potential),
    )
    total = sum(v * w for v, w in zip(values, _WEIGHTS, strict=True))
    return min(100, total // 100)


def partner_quality_band(score: int) -> str:
    if score >= 85:
        return "certified_or_strategic"
    if score >= 70:
        return "implementation"
    if score >= 55:
        return "referral_only"
    return "reject_or_pause"


def partner_gate_passes(criteria_met: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [c for c in PARTNER_GATE_CRITERIA if c not in criteria_met]
    return not missing, tuple(missing)
