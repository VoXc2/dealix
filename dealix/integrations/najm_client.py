"""
Najm — Saudi auto-insurance claims authority.

For automotive-vertical tenants (dealerships, fleet operators), Najm
exposes claim history + risk class per VIN / driver. We surface this
in the lead-scorer when the auto-vertical bundle is active.

Credentials are issued by Najm Insurance Services to authorised
brokers. Inert without `NAJM_API_KEY`.

Reference: https://najm.sa
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _base() -> str:
    return os.getenv("NAJM_API_BASE", "https://api.najm.sa/v1").rstrip("/")


def is_configured() -> bool:
    return bool(os.getenv("NAJM_API_KEY", "").strip())


@dataclass(frozen=True)
class VehicleHistory:
    vin: str
    claim_count: int
    at_fault_count: int
    risk_class: str  # A | B | C | D | unknown


async def vehicle_history(vin: str) -> VehicleHistory | None:
    if not is_configured():
        return None
    headers = {"Authorization": f"Bearer {os.getenv('NAJM_API_KEY', '').strip()}"}
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{_base()}/vehicles/{vin}/history", headers=headers)
            if r.status_code == 404:
                return VehicleHistory(vin, 0, 0, "unknown")
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("najm_history_failed", vin=vin)
        return None
    return VehicleHistory(
        vin=vin,
        claim_count=int(data.get("claimCount") or 0),
        at_fault_count=int(data.get("atFaultCount") or 0),
        risk_class=str(data.get("riskClass") or "unknown"),
    )
