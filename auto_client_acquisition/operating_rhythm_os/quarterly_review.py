"""Quarterly strategic review — mandatory outputs checklist."""

from __future__ import annotations

from collections.abc import Mapping

QUARTERLY_REQUIRED_OUTPUTS: tuple[str, ...] = (
    "strategic_bet",
    "service_to_scale",
    "service_to_kill",
    "product_module_to_build",
    "risk_to_reduce",
    "market_narrative_to_push",
)


def quarterly_outputs_complete(outputs: Mapping[str, str]) -> tuple[bool, tuple[str, ...]]:
    missing = [k for k in QUARTERLY_REQUIRED_OUTPUTS if not (outputs.get(k) or "").strip()]
    return not missing, tuple(missing)
