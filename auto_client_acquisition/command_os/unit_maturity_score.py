"""Business unit maturity — sovereign command weights (distinct from venture_signal helper)."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class BusinessUnitMaturityInputs(NamedTuple):
    """Subscores 0–100."""

    revenue: float
    repeatability: float
    retainers: float
    product_module: float
    playbook: float
    proof_library: float
    owner_readiness: float


class BusinessUnitMaturityBand(StrEnum):
    VENTURE_CANDIDATE = "venture_candidate"
    BUSINESS_UNIT = "business_unit"
    SERVICE_LINE = "service_line"
    EXPERIMENT = "experiment"


def compute_business_unit_maturity_score(inputs: BusinessUnitMaturityInputs) -> float:
    w = (
        0.20 * inputs.revenue
        + 0.20 * inputs.repeatability
        + 0.15 * inputs.retainers
        + 0.15 * inputs.product_module
        + 0.10 * inputs.playbook
        + 0.10 * inputs.proof_library
        + 0.10 * inputs.owner_readiness
    )
    return max(0.0, min(100.0, float(w)))


def business_unit_maturity_band(score: float) -> BusinessUnitMaturityBand:
    if score >= 85:
        return BusinessUnitMaturityBand.VENTURE_CANDIDATE
    if score >= 70:
        return BusinessUnitMaturityBand.BUSINESS_UNIT
    if score >= 55:
        return BusinessUnitMaturityBand.SERVICE_LINE
    return BusinessUnitMaturityBand.EXPERIMENT
