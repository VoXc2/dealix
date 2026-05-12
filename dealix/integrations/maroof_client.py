"""
Maroof — Saudi Ministry of Commerce consumer-reputation directory.

Maroof lets a buyer look up a Saudi merchant's verification + rating
status. We surface this at two points:

1. **Enrichment** — alongside Wathq, attach the merchant's Maroof
   verification status to a lead profile.
2. **Trust signals** — show the customer a green/amber/red badge on
   their public-facing landing page when their Maroof profile is
   linked (read by the verticals / E-commerce skill).

Maroof has no documented public REST API; access is granted to
licensed partners via the Saudi Business Center. The client below
returns 503-shaped not-configured until a key is set.

Reference: https://maroof.sa
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _base() -> str:
    return os.getenv("MAROOF_API_BASE", "https://maroof.sa/api/v1").rstrip("/")


def is_configured() -> bool:
    return bool(os.getenv("MAROOF_API_KEY", "").strip())


@dataclass(frozen=True)
class MaroofProfile:
    cr_number: str
    verified: bool
    rating: float | None
    review_count: int
    badge_color: str  # green | amber | red | gray


async def lookup(cr_number: str) -> MaroofProfile | None:
    """Return Maroof profile for a CR number, or None when not configured / not found."""
    if not is_configured():
        return None
    headers = {"Authorization": f"Bearer {os.getenv('MAROOF_API_KEY', '').strip()}"}
    try:
        async with httpx.AsyncClient(timeout=10) as c:
            r = await c.get(f"{_base()}/merchants/{cr_number}", headers=headers)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("maroof_lookup_failed", cr=cr_number)
        return None
    rating = data.get("rating")
    badge = "gray"
    if data.get("verified") and rating is not None:
        if rating >= 4.0:
            badge = "green"
        elif rating >= 3.0:
            badge = "amber"
        else:
            badge = "red"
    return MaroofProfile(
        cr_number=cr_number,
        verified=bool(data.get("verified")),
        rating=rating,
        review_count=int(data.get("reviewCount") or 0),
        badge_color=badge,
    )
