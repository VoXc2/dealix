"""
Weighted scoring for AI / RevOps use cases — Strategy OS intake.

Weights match the commercial playbook (revenue 30%, time 20%, data 20%, ease 15%, risk 15%).
All inputs are 0.0–1.0 floats provided by humans or upstream assessments.
"""

from __future__ import annotations

from dataclasses import dataclass

_WEIGHTS = (0.30, 0.20, 0.20, 0.15, 0.15)


@dataclass(frozen=True)
class UseCaseScores:
    """Normalized sub-scores for one named use case."""

    name: str
    revenue_impact: float
    time_save: float
    data_readiness: float
    ease: float
    low_risk: float

    def __post_init__(self) -> None:
        for field_name in (
            "revenue_impact",
            "time_save",
            "data_readiness",
            "ease",
            "low_risk",
        ):
            v = float(getattr(self, field_name))
            if v < 0.0 or v > 1.0:
                raise ValueError(f"{field_name}_out_of_range:{v}")


def composite_score(use_case: UseCaseScores) -> float:
    vals = (
        use_case.revenue_impact,
        use_case.time_save,
        use_case.data_readiness,
        use_case.ease,
        use_case.low_risk,
    )
    return round(sum(w * v for w, v in zip(_WEIGHTS, vals, strict=True)), 4)


def rank_use_cases(use_cases: list[UseCaseScores]) -> list[tuple[str, float]]:
    """Return (name, score) sorted descending."""
    ranked = [(u.name, composite_score(u)) for u in use_cases]
    ranked.sort(key=lambda x: x[1], reverse=True)
    return ranked


def roadmap_buckets(top_names: list[str]) -> dict[str, list[str]]:
    """
    Placeholder 30/60/90 structure — assigns up to nine use cases across horizons.

    Real roadmaps should be edited per client; this keeps a deterministic default.
    """
    names = list(top_names[:9])
    out: dict[str, list[str]] = {"days_30": [], "days_60": [], "days_90": []}
    for i, n in enumerate(names):
        if i < 3:
            out["days_30"].append(n)
        elif i < 6:
            out["days_60"].append(n)
        else:
            out["days_90"].append(n)
    return out
