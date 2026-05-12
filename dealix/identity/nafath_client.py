"""
Nafath — Saudi national identity authentication (NIC + 2FA via the
Nafath app).

We use Nafath at two key points:

1. **High-privilege admin actions** — when a tenant owner toggles a
   destructive setting, we send a Nafath request and wait for the
   approve push on their phone.
2. **Business-owner onboarding** — to assert that the human signing
   the DPA is the same person on the commercial register.

Production credentials are issued by the Saudi Data & AI Authority
(SDAIA) to licensed services. Until issued, this client returns 503
`nafath_not_configured` so the surrounding flow can degrade.

Reference: https://www.absher.sa/wps/portal/individuals/services/sc/srv90 (Nafath)
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class NafathRequest:
    request_id: str
    expires_at: str | None
    transaction_id: str


@dataclass
class NafathStatus:
    state: str  # WAITING | COMPLETED | REJECTED | EXPIRED
    national_id: str | None
    completed_at: str | None


def _base() -> str:
    return os.getenv(
        "NAFATH_API_BASE", "https://api.nafath.sa/api/v1"
    ).rstrip("/")


def _headers() -> dict[str, str]:
    return {
        "ApiKey": os.getenv("NAFATH_API_KEY", "").strip(),
        "Content-Type": "application/json",
    }


def is_configured() -> bool:
    return bool(os.getenv("NAFATH_API_KEY", "").strip())


async def create_request(*, national_id: str, service: str = "Dealix") -> NafathRequest:
    if not is_configured():
        raise RuntimeError("nafath_not_configured")
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(
            f"{_base()}/api/Nafath/Initiate",
            headers=_headers(),
            json={"nationalId": national_id, "service": service, "local": "ar"},
        )
        r.raise_for_status()
        data = r.json()
    return NafathRequest(
        request_id=str(data.get("requestId", "")),
        transaction_id=str(data.get("transId", "")),
        expires_at=data.get("expiresAt"),
    )


async def poll_status(*, request_id: str, transaction_id: str) -> NafathStatus:
    if not is_configured():
        raise RuntimeError("nafath_not_configured")
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.post(
            f"{_base()}/api/Nafath/Verify",
            headers=_headers(),
            json={"requestId": request_id, "transId": transaction_id},
        )
        r.raise_for_status()
        data = r.json()
    return NafathStatus(
        state=str(data.get("status") or "WAITING").upper(),
        national_id=data.get("nationalId"),
        completed_at=data.get("completedAt"),
    )
