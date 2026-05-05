"""Sector → customer-facing bundle mapping.

Returns one of the 5 customer-facing bundle ids only. Falls back to
``growth_starter`` for unknown sectors.
"""
from __future__ import annotations

from typing import Any


# The 5 customer-facing bundles. Aligned with finance_os.pricing_catalog
# tier_ids but expressed as the simpler bundle ids the customer sees.
CUSTOMER_FACING_BUNDLES: tuple[str, ...] = (
    "diagnostic",
    "growth_starter",
    "data_to_revenue",
    "executive_growth_os",
    "partnership_growth",
)


_SECTOR_BUNDLE_MAP: dict[str, str] = {
    "b2b_services": "growth_starter",
    "b2b_saas": "growth_starter",
    "agency": "partnership_growth",
    "training_consulting": "growth_starter",
    "local_services": "growth_starter",
    "ecommerce_b2c": "data_to_revenue",
    "real_estate": "growth_starter",
    "healthcare_clinic": "growth_starter",
    "enterprise": "executive_growth_os",
}


def recommend_service(brain: Any) -> str:
    """Return the recommended bundle id for the given brain.

    Accepts either a ``CompanyBrainV6`` or anything exposing ``sector``.
    Always returns one of ``CUSTOMER_FACING_BUNDLES``; unknown sectors
    fall back to ``growth_starter``.
    """
    sector = getattr(brain, "sector", None)
    bundle = _SECTOR_BUNDLE_MAP.get(str(sector or ""), "growth_starter")
    if bundle not in CUSTOMER_FACING_BUNDLES:  # defensive
        bundle = "growth_starter"
    return bundle
