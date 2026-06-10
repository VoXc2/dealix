"""Dealix Capability Index (DCI) — client maturity 0–100 across seven capabilities."""

from __future__ import annotations

from typing import NamedTuple


class CapabilityScores(NamedTuple):
    """Each 0–100 for Revenue, Data, Governance, Operations, Knowledge, Customer, Reporting."""

    revenue_capability: float
    data_capability: float
    governance_capability: float
    operations_capability: float
    knowledge_capability: float
    customer_capability: float
    reporting_capability: float


def compute_dci(scores: CapabilityScores) -> float:
    """Dealix Capability Index (weighted composite)."""
    w = (
        0.20 * scores.revenue_capability
        + 0.15 * scores.data_capability
        + 0.20 * scores.governance_capability
        + 0.15 * scores.operations_capability
        + 0.10 * scores.knowledge_capability
        + 0.10 * scores.customer_capability
        + 0.10 * scores.reporting_capability
    )
    return max(0.0, min(100.0, float(w)))
