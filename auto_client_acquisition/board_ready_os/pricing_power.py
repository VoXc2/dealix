"""Pricing Power — six triggers that justify a price increase."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class PriceIncreaseTrigger(str, Enum):
    PROOF_SCORE_CONSISTENTLY_HIGH = "proof_score_consistently_high"
    DELIVERY_REPEATABLE = "delivery_repeatable"
    DEMAND_EXCEEDS_CAPACITY = "demand_exceeds_capacity"
    RETAINER_CONVERSION_EXISTS = "retainer_conversion_exists"
    GOVERNANCE_TRUST_STRONG = "governance_trust_strong"
    PRODUCT_MODULES_REDUCE_EFFORT = "product_modules_reduce_effort"


PRICE_INCREASE_TRIGGERS: tuple[PriceIncreaseTrigger, ...] = tuple(PriceIncreaseTrigger)


@dataclass(frozen=True)
class PricingPowerEvidence:
    proof_score_avg: float           # 0..100
    delivery_is_repeatable: bool
    demand_exceeds_capacity: bool
    retainer_conversion_rate: float  # 0..1
    governance_trust_strong: bool
    product_modules_reduce_effort: bool


@dataclass(frozen=True)
class PricingPowerDecision:
    raise_price: bool
    triggers_met: tuple[PriceIncreaseTrigger, ...]


def should_raise_price(evidence: PricingPowerEvidence) -> PricingPowerDecision:
    triggers: list[PriceIncreaseTrigger] = []
    if evidence.proof_score_avg > 85:
        triggers.append(PriceIncreaseTrigger.PROOF_SCORE_CONSISTENTLY_HIGH)
    if evidence.delivery_is_repeatable:
        triggers.append(PriceIncreaseTrigger.DELIVERY_REPEATABLE)
    if evidence.demand_exceeds_capacity:
        triggers.append(PriceIncreaseTrigger.DEMAND_EXCEEDS_CAPACITY)
    if evidence.retainer_conversion_rate >= 0.3:
        triggers.append(PriceIncreaseTrigger.RETAINER_CONVERSION_EXISTS)
    if evidence.governance_trust_strong:
        triggers.append(PriceIncreaseTrigger.GOVERNANCE_TRUST_STRONG)
    if evidence.product_modules_reduce_effort:
        triggers.append(PriceIncreaseTrigger.PRODUCT_MODULES_REDUCE_EFFORT)
    # Doctrine: at least 4 of 6 triggers required.
    return PricingPowerDecision(
        raise_price=len(triggers) >= 4,
        triggers_met=tuple(triggers),
    )
