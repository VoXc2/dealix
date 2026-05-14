"""Portfolio Matrix v2 — four-axis unit/service classification."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class PortfolioMatrixInputs(NamedTuple):
    """Each axis 0–100 before classification."""

    revenue_potential: float
    proof_strength: float
    product_potential: float
    governance_safety: float


class PortfolioMatrixBand(StrEnum):
    SCALE = "scale"
    BUILD = "build"
    PILOT = "pilot"
    HOLD = "hold"
    KILL = "kill"


def portfolio_matrix_band(inputs: PortfolioMatrixInputs) -> PortfolioMatrixBand:
    """Heuristic bands aligned with META operating docs (conservative kill)."""
    r, p, prod, g = inputs
    avg = (r + p + prod + g) / 4.0
    if r < 40 and p < 40 and g < 50:
        return PortfolioMatrixBand.KILL
    if r >= 75 and p >= 75 and prod >= 75 and g >= 70:
        return PortfolioMatrixBand.SCALE
    if avg >= 60:
        return PortfolioMatrixBand.BUILD
    if avg >= 45:
        return PortfolioMatrixBand.PILOT
    if avg >= 35:
        return PortfolioMatrixBand.HOLD
    return PortfolioMatrixBand.KILL
