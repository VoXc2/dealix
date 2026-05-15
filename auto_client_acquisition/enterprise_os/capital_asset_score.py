"""Capital Ledger v2 — weighted asset quality score (0–100)."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class CapitalAssetScoreInputs(NamedTuple):
    """Each dimension 0–100 before weighting."""

    reusable: float
    tied_to_revenue: float
    reduces_delivery_time: float
    improves_trust: float
    supports_productization: float
    supports_market_authority: float


class CapitalAssetBand(StrEnum):
    STRATEGIC = "strategic_asset"
    USEFUL = "useful_asset"
    INTERNAL = "internal_note"
    ARCHIVE = "archive"


def compute_capital_asset_score(inputs: CapitalAssetScoreInputs) -> float:
    w = (
        0.25 * inputs.reusable
        + 0.20 * inputs.tied_to_revenue
        + 0.20 * inputs.reduces_delivery_time
        + 0.15 * inputs.improves_trust
        + 0.10 * inputs.supports_productization
        + 0.10 * inputs.supports_market_authority
    )
    return max(0.0, min(100.0, float(w)))


def capital_asset_band(score: float) -> CapitalAssetBand:
    if score >= 80:
        return CapitalAssetBand.STRATEGIC
    if score >= 60:
        return CapitalAssetBand.USEFUL
    if score >= 40:
        return CapitalAssetBand.INTERNAL
    return CapitalAssetBand.ARCHIVE
