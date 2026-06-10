"""Arabic / Saudi intelligence layer — rubric dimensions for compounding QA."""

from __future__ import annotations

ARABIC_INTELLIGENCE_DIMENSIONS: tuple[str, ...] = (
    "executive_tone",
    "saudi_business_phrasing",
    "sector_terms",
    "city_region_normalization",
    "objection_handling",
    "privacy_sensitive_phrasing",
    "claim_safety_language",
)


def arabic_intelligence_coverage_score(dimensions_tracked: frozenset[str]) -> int:
    if not ARABIC_INTELLIGENCE_DIMENSIONS:
        return 0
    n = sum(1 for d in ARABIC_INTELLIGENCE_DIMENSIONS if d in dimensions_tracked)
    return (n * 100) // len(ARABIC_INTELLIGENCE_DIMENSIONS)
