"""Intelligence quality controls — compounding must not amplify bad data."""

from __future__ import annotations

INTELLIGENCE_QUALITY_CONTROLS: tuple[str, ...] = (
    "anonymize_before_benchmark",
    "separate_client_from_pattern_data",
    "human_review_for_insights",
    "no_pii_in_intelligence_layer",
    "no_confidential_metrics_in_public_content",
    "confidence_score_on_every_pattern",
)


def intelligence_quality_controls_met(controls_satisfied: frozenset[str]) -> tuple[bool, tuple[str, ...]]:
    missing = [c for c in INTELLIGENCE_QUALITY_CONTROLS if c not in controls_satisfied]
    return not missing, tuple(missing)
