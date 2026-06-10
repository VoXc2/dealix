"""Training products surfaced from adoption — champions and operators."""

from __future__ import annotations

TRAINING_PRODUCT_SLUGS: tuple[str, ...] = (
    "ai_ops_for_executives",
    "revenue_intelligence_operator",
    "ai_governance_basics",
    "company_brain_user_training",
    "internal_champion_program",
)


def training_product_known(slug: str) -> bool:
    return slug in TRAINING_PRODUCT_SLUGS
