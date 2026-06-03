"""Customer Brain HTTP surface.

4 endpoints:
  GET  /api/v1/customers/{handle}/brain
  POST /api/v1/customers/{handle}/brain/build
  GET  /api/v1/customers/{handle}/context-pack
  GET  /api/v1/customers/{handle}/brain/status

Hard gates: NO_PII_IN_SNAPSHOT, no internal terms in customer-facing fields.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.customer_brain import (
    build_snapshot,
    context_pack,
    get_snapshot,
    list_known_customers,
)

router = APIRouter(prefix="/api/v1/customers", tags=["customer-brain"])

_HARD_GATES: dict[str, bool] = {
    "no_pii_in_snapshot": True,
    "no_live_send": True,
    "no_scraping": True,
    "approval_required_for_external_actions": True,
}


@router.get("/{handle}/brain")
async def brain(handle: str) -> dict[str, Any]:
    snap = get_snapshot(customer_handle=handle)
    if snap is None:
        # Lazy-build on first request
        snap = build_snapshot(customer_handle=handle)
    return {
        "snapshot": snap.model_dump(mode="json"),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{handle}/brain/build")
async def brain_build(handle: str) -> dict[str, Any]:
    snap = build_snapshot(customer_handle=handle)
    return {
        "snapshot": snap.model_dump(mode="json"),
        "rebuilt": True,
        "hard_gates": _HARD_GATES,
    }


@router.get("/{handle}/context-pack")
async def context_pack_endpoint(handle: str) -> dict[str, Any]:
    snap = get_snapshot(customer_handle=handle) or build_snapshot(
        customer_handle=handle
    )
    pack = context_pack(snap)
    return {
        "context_pack": pack,
        "hard_gates": _HARD_GATES,
    }


@router.get("/brain/status")
async def status() -> dict[str, Any]:
    return {
        "service": "customer_brain",
        "version": "1.0.0",
        "known_customers": list_known_customers(),
        "hard_gates": _HARD_GATES,
    }
