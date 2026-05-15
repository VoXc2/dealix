"""Venture readiness — normalize signals into a 0–100 score and band."""

from __future__ import annotations

from enum import StrEnum
from typing import NamedTuple


class VentureInputs(NamedTuple):
    """Subscores on 0–100 (inclusive), except counts normalized upstream."""

    paid_clients_maturity: float
    retainers_maturity: float
    repeatability: float
    product_module_usage: float
    playbook_maturity: float
    margin: float
    owner_readiness: float


class VentureReadinessBand(StrEnum):
    VENTURE_CANDIDATE = "venture_candidate"
    BUSINESS_UNIT = "business_unit"
    SERVICE_LINE = "service_line"
    CORE_SERVICES = "core_services"


def compute_venture_readiness_score(inputs: VentureInputs) -> float:
    """Return venture readiness 0–100 per institutional weights."""
    w = (
        0.15 * inputs.paid_clients_maturity
        + 0.20 * inputs.retainers_maturity
        + 0.20 * inputs.repeatability
        + 0.15 * inputs.product_module_usage
        + 0.10 * inputs.playbook_maturity
        + 0.10 * inputs.margin
        + 0.10 * inputs.owner_readiness
    )
    return max(0.0, min(100.0, float(w)))


def classify_venture_readiness(score: float) -> VentureReadinessBand:
    if score >= 85:
        return VentureReadinessBand.VENTURE_CANDIDATE
    if score >= 70:
        return VentureReadinessBand.BUSINESS_UNIT
    if score >= 55:
        return VentureReadinessBand.SERVICE_LINE
    return VentureReadinessBand.CORE_SERVICES
