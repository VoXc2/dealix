"""Risks that erode compound moat — mirror docs/moat/ANTI_MOAT_RISKS.md."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class AntiMoatRisk(StrEnum):
    OVER_CUSTOMIZATION = "over_customization"
    WEAK_PROOF = "weak_proof"
    GOVERNANCE_SHORTCUT = "governance_shortcut"
    BAD_ARABIC = "bad_arabic"
    CHEAP_POSITIONING = "cheap_positioning"
    PREMATURE_SAAS = "premature_saas"


@dataclass(frozen=True, slots=True)
class AntiMoatHit:
    risk: AntiMoatRisk
    remedy_key: str


def detect_anti_moat_risks(
    *,
    every_engagement_custom_scope: bool = False,
    delivery_without_proof_pack: bool = False,
    output_without_governance_status: bool = False,
    arabic_quality_fail: bool = False,
    priced_as_commodity_task: bool = False,
    shipped_public_saas_before_internal_use: bool = False,
) -> tuple[AntiMoatHit, ...]:
    hits: list[AntiMoatHit] = []
    if every_engagement_custom_scope:
        hits.append(
            AntiMoatHit(AntiMoatRisk.OVER_CUSTOMIZATION, "service_catalog_scope_productization_ledger"),
        )
    if delivery_without_proof_pack:
        hits.append(AntiMoatHit(AntiMoatRisk.WEAK_PROOF, "proof_pack_mandatory"))
    if output_without_governance_status:
        hits.append(
            AntiMoatHit(AntiMoatRisk.GOVERNANCE_SHORTCUT, "no_output_without_governance_status"),
        )
    if arabic_quality_fail:
        hits.append(AntiMoatHit(AntiMoatRisk.BAD_ARABIC, "arabic_business_qa"))
    if priced_as_commodity_task:
        hits.append(AntiMoatHit(AntiMoatRisk.CHEAP_POSITIONING, "sell_capability_proof_trust"))
    if shipped_public_saas_before_internal_use:
        hits.append(AntiMoatHit(AntiMoatRisk.PREMATURE_SAAS, "internal_use_first_productization_gate"))
    return tuple(hits)
