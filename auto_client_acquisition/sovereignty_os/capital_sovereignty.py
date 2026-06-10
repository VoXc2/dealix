"""Capital sovereignty — asset classes + minimum project output."""

from __future__ import annotations

from dataclasses import dataclass

CAPITAL_TYPES: tuple[str, ...] = (
    "service",
    "product",
    "knowledge",
    "trust",
    "market",
    "standard",
    "partner",
    "venture",
)


@dataclass(frozen=True, slots=True)
class CapitalSovereigntyMinimum:
    trust_asset: bool
    product_or_knowledge_asset: bool
    expansion_path: bool


def capital_minimum_met(c: CapitalSovereigntyMinimum) -> bool:
    return c.trust_asset and c.product_or_knowledge_asset and c.expansion_path


def capital_diversification_score(types_created: frozenset[str]) -> int:
    if not CAPITAL_TYPES:
        return 0
    n = sum(1 for t in CAPITAL_TYPES if t in types_created)
    return (n * 100) // len(CAPITAL_TYPES)
