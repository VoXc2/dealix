"""Content pillars for category creation engine."""

from __future__ import annotations

CONTENT_ENGINE_PILLARS: tuple[str, ...] = (
    "AI adoption is not AI value",
    "Why AI projects fail",
    "Data readiness before AI",
    "Governance runtime, not PDF policy",
    "Proof Pack as AI ROI evidence",
    "Company Brain with sources",
    "Revenue Intelligence vs lead scraping",
    "Saudi Arabic AI quality",
    "PDPL-aware AI operations",
    "Human-amplified AI, not humanless AI",
)

CONTENT_ENGINE_PILLAR_IDS: tuple[str, ...] = (
    "adoption_not_value",
    "why_projects_fail",
    "data_readiness_first",
    "governance_runtime",
    "proof_pack_roi",
    "company_brain_sources",
    "revenue_intel_not_scraping",
    "arabic_ai_quality",
    "pdpl_aware_ops",
    "human_amplified",
)

_PILLAR_WEIGHTS: dict[str, int] = dict(zip(CONTENT_ENGINE_PILLAR_IDS, [10] * 10, strict=True))


def content_pillar_coverage_score(addressed: set[str]) -> int:
    """Score 0-100 from how many canonical pillar ids are covered."""
    unknown = addressed - set(CONTENT_ENGINE_PILLAR_IDS)
    if unknown:
        raise ValueError(f"Unknown pillar ids: {sorted(unknown)}")
    return sum(_PILLAR_WEIGHTS[pid] for pid in addressed)
