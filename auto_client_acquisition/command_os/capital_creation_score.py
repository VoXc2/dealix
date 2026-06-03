"""Capital creation — minimum bar for strategic projects (trust + product/knowledge + path)."""

from __future__ import annotations


def meets_minimum_capital_creation(
    *,
    trust_assets: int,
    product_assets: int,
    knowledge_assets: int,
    expansion_paths: int,
) -> bool:
    """Strategic project bar: ≥1 trust, ≥1 product or knowledge, ≥1 expansion path."""
    if trust_assets < 1:
        return False
    if product_assets < 1 and knowledge_assets < 1:
        return False
    return expansion_paths >= 1
