"""Dealix internal economy — currency labels for planning dashboards."""

from __future__ import annotations

from typing import Final

ECONOMY_CURRENCIES: Final[tuple[str, ...]] = (
    "cash",
    "proof",
    "capital",
    "distribution",
    "control",
)
