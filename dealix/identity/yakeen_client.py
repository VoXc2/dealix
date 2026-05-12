"""
Yakeen — Saudi National Information Center identity verification.

Used to verify a Saudi national or resident's basic identity
(name, DOB, family name match) without storing the underlying data.
Per PDPL, we only hold the *result* (verified yes/no + timestamp +
request id), never the personal data itself.

Reference: https://api.elm.sa/yakeen (consumed via Saudi Business Gateway
or directly per NIC licence).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class YakeenResult:
    verified: bool
    request_id: str | None
    error: str | None = None


def is_configured() -> bool:
    return bool(os.getenv("YAKEEN_API_KEY", "").strip())


def _base() -> str:
    return os.getenv("YAKEEN_API_BASE", "https://api.elm.sa/api/v1").rstrip("/")


async def verify_identity(
    *,
    national_id: str,
    date_of_birth_hijri: str,
) -> YakeenResult:
    """Verify a national ID against the Hijri DOB on file."""
    if not is_configured():
        return YakeenResult(verified=False, request_id=None, error="yakeen_not_configured")
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.post(
                f"{_base()}/yakeen/citizen/personal-info",
                headers={
                    "ApiKey": os.getenv("YAKEEN_API_KEY", "").strip(),
                    "Content-Type": "application/json",
                },
                json={
                    "nationalId": national_id,
                    "dateOfBirthH": date_of_birth_hijri,
                },
            )
            r.raise_for_status()
            data = r.json()
    except Exception as exc:
        log.exception("yakeen_verify_failed")
        return YakeenResult(verified=False, request_id=None, error=str(exc))
    return YakeenResult(
        verified=bool(data.get("verified", False)),
        request_id=str(data.get("requestId") or ""),
    )
