"""Per-customer Executive Pack endpoints.

  GET /api/v1/customers/{handle}/executive-pack/today
  GET /api/v1/customers/{handle}/executive-pack/week

These wrap auto_client_acquisition.executive_pack_v2 — extending
existing executive_os/role_command_os without modifying them.

Hard gates: NO_FAKE_REVENUE, NO_FAKE_FORECAST.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.executive_pack_v2 import (
    build_daily_pack,
    build_weekly_pack,
)

router = APIRouter(
    prefix="/api/v1/customers", tags=["executive-pack-per-customer"]
)

_HARD_GATES: dict[str, bool] = {
    "no_fake_revenue": True,
    "no_fake_forecast": True,
    "no_live_send": True,
    "no_pii_in_report": True,
}


@router.get("/{handle}/executive-pack/today")
async def today(handle: str) -> dict[str, Any]:
    pack = build_daily_pack(customer_handle=handle)
    return {
        "pack": pack.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.get("/{handle}/executive-pack/week")
async def week(handle: str) -> dict[str, Any]:
    pack = build_weekly_pack(customer_handle=handle)
    return {
        "pack": pack.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }
