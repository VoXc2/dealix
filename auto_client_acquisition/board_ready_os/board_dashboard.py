"""Board Dashboard — 12 canonical board-level metrics."""

from __future__ import annotations

from dataclasses import dataclass


BOARD_DASHBOARD_METRICS: tuple[str, ...] = (
    "revenue",
    "mrr",
    "gross_margin",
    "proof_packs_delivered",
    "proof_to_retainer_conversion",
    "governance_incidents",
    "ai_run_audit_coverage",
    "capital_assets_created",
    "productization_candidates",
    "client_health",
    "business_unit_maturity",
    "market_power_signals",
)


@dataclass(frozen=True)
class BoardDashboardSnapshot:
    period: str
    values: dict[str, float]

    def __post_init__(self) -> None:
        unknown = set(self.values) - set(BOARD_DASHBOARD_METRICS)
        if unknown:
            raise ValueError(
                "unknown_board_metric:" + ",".join(sorted(unknown))
            )

    def get(self, name: str) -> float | None:
        return self.values.get(name)
