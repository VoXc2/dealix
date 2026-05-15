"""Pricing evolution stage inference."""

from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum


class PricingEvolutionStage(IntEnum):
    FOUNDER_PROOF = 1
    REPEATABLE_SPRINT = 2
    MANAGED_RETAINER = 3
    PLATFORM_PLUS_SERVICE = 4
    ENTERPRISE = 5


@dataclass(frozen=True, slots=True)
class PricingSignals:
    """Highest applicable stage wins (enterprise down to founder)."""

    enterprise_contract: bool = False
    subscription_plus_managed_service: bool = False
    has_mrr_retainers_material: bool = False
    repeatable_sprint_catalog_live: bool = False
    founder_proof_engagements: bool = False


def infer_pricing_stage(s: PricingSignals) -> PricingEvolutionStage:
    if s.enterprise_contract:
        return PricingEvolutionStage.ENTERPRISE
    if s.subscription_plus_managed_service:
        return PricingEvolutionStage.PLATFORM_PLUS_SERVICE
    if s.has_mrr_retainers_material:
        return PricingEvolutionStage.MANAGED_RETAINER
    if s.repeatable_sprint_catalog_live:
        return PricingEvolutionStage.REPEATABLE_SPRINT
    if s.founder_proof_engagements:
        return PricingEvolutionStage.FOUNDER_PROOF
    return PricingEvolutionStage.FOUNDER_PROOF
