"""Client scorecard — documented dimensions for aggregation/UI."""

from __future__ import annotations

from typing import Final

CLIENT_SCORECARD_FIELDS: Final[tuple[str, ...]] = (
    "capability_score",
    "transformation_gap",
    "data_readiness",
    "governance_risk",
    "proof_strength",
    "retainer_readiness",
)
