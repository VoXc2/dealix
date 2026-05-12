"""
MISA — Saudi Ministry of Investment.

MISA issues the foreign-investment licence (Investment Licence) that
non-Saudi entities need to incorporate or invest in the Kingdom. The
client below supports two flows:

1. **Licence status check** by licence number — used at onboarding to
   recognise foreign-owned tenants and route them onto the MISA-aware
   billing path (e.g. fee waivers, certain disclosures).
2. **Foreign-investor lead-source tag** — when a lead pushes through
   our public site from a non-Saudi IP, we offer a "foreign-investor
   pilot" CTA; the MISA licence number captured there becomes the
   account anchor.

Inert without `MISA_API_KEY`.

Reference: https://misa.gov.sa
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _base() -> str:
    return os.getenv("MISA_API_BASE", "https://api.misa.gov.sa/v1").rstrip("/")


def is_configured() -> bool:
    return bool(os.getenv("MISA_API_KEY", "").strip())


@dataclass(frozen=True)
class InvestmentLicence:
    licence_number: str
    active: bool
    issued_at: str | None
    expires_at: str | None
    country_of_origin: str | None
    activity: str | None


async def licence_status(licence_number: str) -> InvestmentLicence | None:
    if not is_configured():
        return None
    headers = {"Authorization": f"Bearer {os.getenv('MISA_API_KEY', '').strip()}"}
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(
                f"{_base()}/licences/{licence_number}", headers=headers
            )
            if r.status_code == 404:
                return None
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("misa_licence_check_failed", licence=licence_number)
        return None
    return InvestmentLicence(
        licence_number=licence_number,
        active=bool(data.get("active")),
        issued_at=data.get("issuedAt"),
        expires_at=data.get("expiresAt"),
        country_of_origin=data.get("countryOfOrigin"),
        activity=data.get("activity"),
    )
