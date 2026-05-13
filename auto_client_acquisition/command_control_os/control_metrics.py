"""Control Metrics — North Star + supporting metrics snapshot.

See ``docs/command_control/CONTROL_METRICS.md``.
"""

from __future__ import annotations

from dataclasses import dataclass


NORTH_STAR: str = "proof_backed_ai_operating_capabilities_created"


SUPPORTING_METRICS: tuple[str, ...] = (
    "mrr",
    "project_revenue",
    "gross_margin",
    "proof_packs_delivered",
    "proof_strength_score",
    "capital_assets_created",
    "manual_steps_productized",
    "governance_incidents_prevented",
    "retainer_conversion",
    "business_unit_maturity",
)


@dataclass(frozen=True)
class ControlMetricsSnapshot:
    """Immutable snapshot of the metrics used by the Command Center."""

    period: str
    north_star_value: int
    values: dict[str, float]

    def __post_init__(self) -> None:
        unknown = set(self.values) - set(SUPPORTING_METRICS)
        if unknown:
            raise ValueError(
                "unknown_supporting_metric:" + ",".join(sorted(unknown))
            )

    def get(self, metric: str) -> float | None:
        return self.values.get(metric)
