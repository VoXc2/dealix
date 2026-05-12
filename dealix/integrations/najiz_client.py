"""
Najiz — Saudi Ministry of Justice judicial-services portal.

We use Najiz to surface a lightweight commercial-risk signal:

- count of open commercial disputes against a CR number
- count of bankruptcy / restructuring filings
- presence of execution orders (احكام تنفيذية)

Wired into the lead-scorer and renewal-forecaster skills so a tenant
can flag accounts whose principal has active judicial exposure.

Najiz access requires a SDAIA-issued client credential. Returns
503-shaped not-configured otherwise.

Reference: https://najiz.sa
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from core.logging import get_logger

log = get_logger(__name__)


def _base() -> str:
    return os.getenv("NAJIZ_API_BASE", "https://api.najiz.sa/v1").rstrip("/")


def is_configured() -> bool:
    return bool(os.getenv("NAJIZ_API_KEY", "").strip())


@dataclass(frozen=True)
class JudicialSnapshot:
    cr_number: str
    open_disputes: int
    bankruptcy_filings: int
    execution_orders: int
    risk_score: float  # 0.0 (clean) — 1.0 (high risk)


async def snapshot(cr_number: str) -> JudicialSnapshot | None:
    if not is_configured():
        return None
    headers = {"Authorization": f"Bearer {os.getenv('NAJIZ_API_KEY', '').strip()}"}
    try:
        async with httpx.AsyncClient(timeout=15) as c:
            r = await c.get(f"{_base()}/commercial-risk/{cr_number}", headers=headers)
            if r.status_code == 404:
                return JudicialSnapshot(cr_number, 0, 0, 0, 0.0)
            r.raise_for_status()
            data = r.json()
    except Exception:
        log.exception("najiz_snapshot_failed", cr=cr_number)
        return None
    od = int(data.get("openDisputes") or 0)
    bf = int(data.get("bankruptcyFilings") or 0)
    eo = int(data.get("executionOrders") or 0)
    # Risk score: bankruptcy weighs 3×, execution orders 2×, disputes 1×.
    raw = min(1.0, (3 * bf + 2 * eo + od) / 10.0)
    return JudicialSnapshot(cr_number, od, bf, eo, raw)
