"""Category ownership score from market adoption signals."""

from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class CategoryOwnershipSignals:
    clients_use_dealix_terms: bool = False
    partners_repeat_method: bool = False
    proof_pack_requested: bool = False
    capability_score_requested: bool = False
    inbound_revenue_intelligence: bool = False
    benchmark_requests: bool = False
    academy_interest: bool = False
    enterprise_governance_runtime_asks: bool = False


_OWNERSHIP_WEIGHTS: dict[str, int] = {
    "clients_use_dealix_terms": 15,
    "partners_repeat_method": 12,
    "proof_pack_requested": 13,
    "capability_score_requested": 12,
    "inbound_revenue_intelligence": 14,
    "benchmark_requests": 8,
    "academy_interest": 8,
    "enterprise_governance_runtime_asks": 18,
}


def compute_category_ownership_score(signals: CategoryOwnershipSignals) -> int:
    """Weighted score 0-100 from eight boolean adoption signals."""
    field_names = {f.name for f in fields(CategoryOwnershipSignals)}
    if field_names != set(_OWNERSHIP_WEIGHTS):
        raise RuntimeError("CategoryOwnershipSignals fields out of sync with weights")
    total_w = sum(_OWNERSHIP_WEIGHTS.values())
    if total_w != 100:
        raise RuntimeError(f"ownership weights must sum to 100, got {total_w}")
    return sum(_OWNERSHIP_WEIGHTS[name] for name in field_names if getattr(signals, name))
