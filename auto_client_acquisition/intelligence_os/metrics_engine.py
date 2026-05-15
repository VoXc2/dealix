"""Metric families for ledgers — names only; aggregation lives in product/analytics."""

from __future__ import annotations

from typing import Final

METRIC_FAMILIES: Final[frozenset[str]] = frozenset(
    {
        "ai_run",
        "audit",
        "proof",
        "capital",
        "productization",
        "client_health",
        "unit_performance",
        "partner",
        "venture",
        "data",
        "governance",
        "delivery",
        "commercial",
        "revenue",
    }
)


def is_known_metric_family(name: str) -> bool:
    return name in METRIC_FAMILIES
