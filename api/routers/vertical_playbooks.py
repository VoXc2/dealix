"""Vertical Playbooks v5 — 5 sector catalogs."""
from __future__ import annotations

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.vertical_playbooks import (
    Vertical,
    get_playbook,
    list_playbooks,
    recommend_for,
    summary,
)

router = APIRouter(prefix="/api/v1/vertical-playbooks", tags=["vertical-playbooks"])


@router.get("/status")
async def status() -> dict:
    return {"module": "vertical_playbooks", **summary()}


@router.get("/list")
async def get_list() -> dict:
    return {"verticals": list_playbooks()}


@router.get("/{vertical}")
async def get_one(vertical: str) -> dict:
    try:
        return get_playbook(vertical)
    except (KeyError, ValueError) as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/recommend")
async def recommend(payload: dict = Body(...)) -> dict:
    """Best-effort hint-to-playbook mapping.

    Body: ``{"sector_hint": "Saudi B2B SaaS"}``. Returns the matching
    playbook or the b2b_services fallback.
    """
    hint = str(payload.get("sector_hint") or "")
    return recommend_for(hint)
