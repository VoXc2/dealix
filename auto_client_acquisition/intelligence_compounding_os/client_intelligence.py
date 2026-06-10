"""Client intelligence — cross-account health and expansion signals."""

from __future__ import annotations

CLIENT_INTELLIGENCE_METRICS: tuple[str, ...] = (
    "client_health_score",
    "adoption_score",
    "proof_score",
    "governance_alignment",
    "expansion_readiness",
    "data_readiness",
    "stakeholder_engagement",
)


def client_intelligence_coverage_score(metrics_tracked: frozenset[str]) -> int:
    if not CLIENT_INTELLIGENCE_METRICS:
        return 0
    n = sum(1 for m in CLIENT_INTELLIGENCE_METRICS if m in metrics_tracked)
    return (n * 100) // len(CLIENT_INTELLIGENCE_METRICS)
