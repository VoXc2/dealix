"""Governed Revenue & AI Operations blueprint endpoints."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.governed_ops import (
    get_blueprint,
    get_gates,
    get_market_segments,
    get_north_star,
    get_offers,
    get_positioning,
    get_state_machine,
)

router = APIRouter(prefix="/api/v1/governed-ops", tags=["governed-ops"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "governed_revenue_ai_ops",
        "positioning": "Governed Revenue & AI Operations Company",
        "guardrails": {
            "no_autonomous_external_send": True,
            "approval_first": True,
            "evidence_first": True,
        },
    }


@router.get("/positioning")
async def positioning() -> dict[str, Any]:
    return get_positioning()


@router.get("/north-star")
async def north_star() -> dict[str, Any]:
    return get_north_star()


@router.get("/offers")
async def offers() -> dict[str, Any]:
    return get_offers()


@router.get("/state-machine")
async def state_machine() -> dict[str, Any]:
    return get_state_machine()


@router.get("/gates")
async def gates() -> dict[str, Any]:
    return get_gates()


@router.get("/market-segments")
async def market_segments() -> dict[str, Any]:
    return get_market_segments()


@router.get("/blueprint")
async def blueprint() -> dict[str, Any]:
    return get_blueprint()
