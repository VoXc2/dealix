"""Growth Beast daily loop API — deterministic composition."""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.growth_beast.daily_loop import build_daily_growth_beast_loop

router = APIRouter(prefix="/api/v1/growth-beast", tags=["growth-beast-loop"])


class _DailyLoopBody(BaseModel):
    model_config = ConfigDict(extra="allow")

    company_profile: dict[str, Any] = Field(default_factory=dict)


@router.get("/status")
async def growth_beast_status() -> dict[str, Any]:
    return {
        "service": "growth_beast_loop",
        "status": "operational",
        "version": "v12_5",
        "endpoints": ["/daily-loop"],
        "hard_gates": {
            "no_cold_whatsapp": True,
            "no_linkedin_automation": True,
            "no_scraping": True,
            "no_live_send": True,
        },
    }


@router.post("/daily-loop")
async def daily_loop(body: _DailyLoopBody = Body(default_factory=_DailyLoopBody)) -> dict[str, Any]:
    raw = body.model_dump(exclude_unset=True)
    if raw.get("company_profile"):
        profile: dict[str, Any] = raw["company_profile"]
    else:
        profile = {k: v for k, v in raw.items() if k != "company_profile"}
    return build_daily_growth_beast_loop(profile)
