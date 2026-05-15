"""Gross margin targets by monetization offer kind."""

from __future__ import annotations

from enum import StrEnum


class MonetizationOfferKind(StrEnum):
    DIAGNOSTIC = "diagnostic"
    SPRINT = "sprint"
    PILOT = "pilot"
    RETAINER = "retainer"
    ENTERPRISE = "enterprise"
    ACADEMY = "academy"
    PLATFORM_MATURE = "platform_mature"


_MIN_GROSS_MARGIN_PCT: dict[MonetizationOfferKind, float] = {
    MonetizationOfferKind.DIAGNOSTIC: 75.0,
    MonetizationOfferKind.SPRINT: 65.0,
    MonetizationOfferKind.PILOT: 55.0,
    MonetizationOfferKind.RETAINER: 65.0,
    MonetizationOfferKind.ENTERPRISE: 50.0,
    MonetizationOfferKind.ACADEMY: 80.0,
    MonetizationOfferKind.PLATFORM_MATURE: 80.0,
}


def gross_margin_meets_target(kind: MonetizationOfferKind, gross_margin_pct: float) -> bool:
    """Minimum gross margin floor for the offer class (upper bands are operational guidance)."""
    return gross_margin_pct + 1e-9 >= _MIN_GROSS_MARGIN_PCT[kind]
