"""Market education funnel topic coverage (levels 1-5)."""

from __future__ import annotations

FUNNEL_LEVEL_TOPICS: dict[int, tuple[str, ...]] = {
    1: (
        "why_ai_fails",
        "tool_vs_operations",
        "data_before_model",
    ),
    2: (
        "no_cold_whatsapp_automation",
        "what_is_governance_runtime",
        "protect_pii",
    ),
    3: (
        "what_is_proof_pack",
        "measure_ai_roi",
        "ai_assisted_workflow_evidence",
    ),
    4: (
        "revenue_intelligence_sprint",
        "company_brain_sprint",
        "ai_quick_win_sprint",
        "ai_governance_review",
    ),
    5: (
        "book_capability_diagnostic",
        "book_revenue_intelligence_sprint",
        "request_proof_pack_sample",
    ),
}


def education_funnel_coverage_percent(level: int, topics_covered: set[str]) -> float:
    """Percent of canonical topics covered for a funnel level (0-100)."""
    if level not in FUNNEL_LEVEL_TOPICS:
        raise ValueError(f"level must be 1-5, got {level}")
    expected = set(FUNNEL_LEVEL_TOPICS[level])
    unknown = topics_covered - expected
    if unknown:
        raise ValueError(f"Unknown topic ids for level {level}: {sorted(unknown)}")
    if not expected:
        return 100.0
    return round(len(topics_covered & expected) / len(expected) * 100.0, 2)
