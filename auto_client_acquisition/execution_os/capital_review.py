"""Post-project capital review completeness."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CapitalReviewOutputs:
    trust_asset: bool
    product_or_knowledge_asset: bool
    expansion_path: bool
    productization_signal: bool
    sales_lesson: bool


def capital_review_complete(outputs: CapitalReviewOutputs) -> bool:
    """All five mandatory outputs must be True."""
    return all(
        (
            outputs.trust_asset,
            outputs.product_or_knowledge_asset,
            outputs.expansion_path,
            outputs.productization_signal,
            outputs.sales_lesson,
        ),
    )
