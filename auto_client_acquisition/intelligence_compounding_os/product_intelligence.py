"""Product intelligence — build / hold / kill heuristics from delivery signals."""

from __future__ import annotations

from enum import StrEnum


class ProductIntelligenceVerdict(StrEnum):
    BUILD = "build"
    HOLD = "hold"
    KILL = "kill"


PRODUCT_SIGNAL_SOURCES: tuple[str, ...] = (
    "repeated_delivery",
    "adoption_friction",
    "governance_event",
    "client_request",
)


def product_intelligence_verdict(
    *,
    usage_high: bool,
    delivery_hours_saved_high: bool,
    client_demand_high: bool,
    governance_risk_low: bool,
    maintenance_high: bool,
    repetition_low: bool,
) -> ProductIntelligenceVerdict:
    if maintenance_high and not usage_high:
        return ProductIntelligenceVerdict.KILL
    if repetition_low:
        return ProductIntelligenceVerdict.HOLD
    if usage_high and delivery_hours_saved_high and client_demand_high and governance_risk_low:
        return ProductIntelligenceVerdict.BUILD
    return ProductIntelligenceVerdict.HOLD
