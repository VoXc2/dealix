"""Service scorecard — documented dimensions."""

from __future__ import annotations

from typing import Final

SERVICE_SCORECARD_FIELDS: Final[tuple[str, ...]] = (
    "win_rate",
    "margin",
    "repeatability",
    "proof_quality",
    "retainer_conversion",
    "productization_potential",
)
