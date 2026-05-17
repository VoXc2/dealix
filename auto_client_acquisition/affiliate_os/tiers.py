"""Affiliate commission tiers — Dealix Full Ops Affiliate Network.

Four tiers per the Full Ops spec §8. The commission rate applies to the
FIRST paid deal a referral produces. Tier 4 (implementation partner) has
no percentage commission — it is a negotiated handoff fee.

Non-negotiables honoured: a computed commission is a DRAFT number only.
No payout happens without an approved ApprovalRequest (Article 8 — no
external action without approval).
"""
from __future__ import annotations

from enum import StrEnum
from typing import Any


class AffiliateTier(StrEnum):
    TIER_1_AFFILIATE_LEAD = "tier_1_affiliate_lead"
    TIER_2_QUALIFIED_REFERRAL = "tier_2_qualified_referral"
    TIER_3_STRATEGIC_PARTNER = "tier_3_strategic_partner"
    TIER_4_IMPLEMENTATION_PARTNER = "tier_4_implementation_partner"


# Tier 3 spec range is 15–20%; 17.5% is the canonical mid-point used for
# the draft commission. The final number is confirmed at payout approval.
_RATES: dict[AffiliateTier, float] = {
    AffiliateTier.TIER_1_AFFILIATE_LEAD: 0.05,
    AffiliateTier.TIER_2_QUALIFIED_REFERRAL: 0.10,
    AffiliateTier.TIER_3_STRATEGIC_PARTNER: 0.175,
    AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER: 0.0,
}

TIER_LABELS_AR: dict[AffiliateTier, str] = {
    AffiliateTier.TIER_1_AFFILIATE_LEAD: "المستوى 1 — مُحيل أفلييت",
    AffiliateTier.TIER_2_QUALIFIED_REFERRAL: "المستوى 2 — إحالة مؤهَّلة",
    AffiliateTier.TIER_3_STRATEGIC_PARTNER: "المستوى 3 — شريك استراتيجي",
    AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER: "المستوى 4 — شريك تنفيذ",
}

TIER_LABELS_EN: dict[AffiliateTier, str] = {
    AffiliateTier.TIER_1_AFFILIATE_LEAD: "Tier 1 — Affiliate Lead",
    AffiliateTier.TIER_2_QUALIFIED_REFERRAL: "Tier 2 — Qualified Referral",
    AffiliateTier.TIER_3_STRATEGIC_PARTNER: "Tier 3 — Strategic Partner",
    AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER: "Tier 4 — Implementation Partner",
}

TIER_EARNS_EN: dict[AffiliateTier, str] = {
    AffiliateTier.TIER_1_AFFILIATE_LEAD: (
        "Brings a lead via a referral link/code. 5% of the first paid Diagnostic."
    ),
    AffiliateTier.TIER_2_QUALIFIED_REFERRAL: (
        "Introduces a decision maker and books a meeting. 10% of the first paid deal."
    ),
    AffiliateTier.TIER_3_STRATEGIC_PARTNER: (
        "A CRM/AI/GRC consultant who brings a fit customer. 15–20% of the "
        "first paid deal (17.5% draft mid-point)."
    ),
    AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER: (
        "Dealix runs the Diagnostic, partner implements. Negotiated handoff "
        "fee — no percentage commission."
    ),
}


def commission_rate(tier: AffiliateTier | str) -> float:
    """Return the percentage rate (0.0–1.0) for a tier."""
    return _RATES[AffiliateTier(tier)]


def is_handoff_tier(tier: AffiliateTier | str) -> bool:
    """Tier 4 is a negotiated handoff fee, not a percentage commission."""
    return AffiliateTier(tier) == AffiliateTier.TIER_4_IMPLEMENTATION_PARTNER


def tier_table() -> list[dict[str, Any]]:
    """Public tier table for the affiliate program-terms endpoint."""
    rows: list[dict[str, Any]] = []
    for tier in AffiliateTier:
        rows.append(
            {
                "tier": tier.value,
                "label_ar": TIER_LABELS_AR[tier],
                "label_en": TIER_LABELS_EN[tier],
                "rate_pct": round(_RATES[tier] * 100, 1),
                "is_handoff": is_handoff_tier(tier),
                "earns_en": TIER_EARNS_EN[tier],
            }
        )
    return rows


__all__ = [
    "TIER_EARNS_EN",
    "TIER_LABELS_AR",
    "TIER_LABELS_EN",
    "AffiliateTier",
    "commission_rate",
    "is_handoff_tier",
    "tier_table",
]
