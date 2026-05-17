"""Unified 4-tier affiliate/partner commission ladder.

Reconciles the playbook's 4-tier affiliate ladder with the agency
program's tiers into one ladder. The ladder is the single source of
truth for commission rates used by ``commission_engine``.

Hard money doctrine (see ``commission_engine``):
  - a commission line exists only after the deal invoice is paid;
  - tiers 1-3 are one-time on the first paid deal;
  - tier 4 (implementation) is recurring and approval-required.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Tier:
    """One rung of the commission ladder."""

    key: str
    rank: int
    name_en: str
    name_ar: str
    rate: float
    recurring: bool
    approval_required: bool
    basis: str


# Tiers 1-3 carry a single commission rate. Tier 4 is per-agreement; its
# `rate` is the conservative default share used when no agreement override
# is supplied, and it always routes through approval.
TIER_AFFILIATE_LEAD = Tier(
    key="affiliate_lead",
    rank=1,
    name_en="Affiliate Lead",
    name_ar="مُحيل",
    rate=0.05,
    recurring=False,
    approval_required=False,
    basis="first paid Diagnostic, one-time",
)
TIER_QUALIFIED_REFERRAL = Tier(
    key="qualified_referral",
    rank=2,
    name_en="Qualified Referral",
    name_ar="إحالة مؤهلة",
    rate=0.10,
    recurring=False,
    approval_required=False,
    basis="first paid deal, one-time",
)
TIER_STRATEGIC_PARTNER = Tier(
    key="strategic_partner",
    rank=3,
    name_en="Strategic Partner",
    name_ar="شريك استراتيجي",
    rate=0.175,
    recurring=False,
    approval_required=False,
    basis="first paid Diagnostic, one-time (15-20% band)",
)
TIER_IMPLEMENTATION_PARTNER = Tier(
    key="implementation_partner",
    rank=4,
    name_en="Implementation Partner",
    name_ar="شريك تنفيذ",
    rate=0.20,
    recurring=True,
    approval_required=True,
    basis="per-agreement / MRR share, recurring, approval-required",
)

_LADDER: dict[str, Tier] = {
    t.key: t
    for t in (
        TIER_AFFILIATE_LEAD,
        TIER_QUALIFIED_REFERRAL,
        TIER_STRATEGIC_PARTNER,
        TIER_IMPLEMENTATION_PARTNER,
    )
}

VALID_TIERS: tuple[str, ...] = tuple(_LADDER.keys())


def get_tier(tier_key: str) -> Tier:
    """Return the ``Tier`` for ``tier_key``.

    Raises ``ValueError`` for an unknown tier so callers cannot
    silently compute a commission against a non-existent rung.
    """
    try:
        return _LADDER[tier_key]
    except KeyError as exc:
        raise ValueError(f"unknown commission tier: {tier_key!r}") from exc


def rate_for(tier_key: str) -> float:
    """Return the commission rate (fraction of basis) for ``tier_key``."""
    return get_tier(tier_key).rate


def ladder() -> list[Tier]:
    """Return the full ladder ordered by rank."""
    return sorted(_LADDER.values(), key=lambda t: t.rank)


def ladder_summary() -> list[dict[str, object]]:
    """Return a JSON-serialisable ladder summary for API responses."""
    return [
        {
            "key": t.key,
            "rank": t.rank,
            "name_en": t.name_en,
            "name_ar": t.name_ar,
            "rate": t.rate,
            "rate_pct": round(t.rate * 100, 1),
            "recurring": t.recurring,
            "approval_required": t.approval_required,
            "basis": t.basis,
        }
        for t in ladder()
    ]


__all__ = [
    "Tier",
    "TIER_AFFILIATE_LEAD",
    "TIER_QUALIFIED_REFERRAL",
    "TIER_STRATEGIC_PARTNER",
    "TIER_IMPLEMENTATION_PARTNER",
    "VALID_TIERS",
    "get_tier",
    "rate_for",
    "ladder",
    "ladder_summary",
]
