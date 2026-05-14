"""Core metrics tree — North Star and supporting metrics (names only, for dashboards/LEDs)."""

from __future__ import annotations

from typing import Final

NORTH_STAR_METRIC: Final[str] = "Proof-backed operating capabilities created"

SUPPORTING_METRICS: Final[tuple[str, ...]] = (
    "revenue_generated",
    "retainers_created",
    "proof_packs_delivered",
    "governance_incidents_prevented",
    "manual_steps_productized",
    "capital_assets_created",
    "client_capability_score_improved",
)
