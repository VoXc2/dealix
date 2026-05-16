"""Wave 13 Phase 2 — Service Catalog HTTP surface.

Exposes the 7 canonical Dealix offerings via FastAPI:
- GET /api/v1/services/catalog        — list all 7 offerings
- GET /api/v1/services/{service_id}    — one offering detail
- GET /api/v1/services/status          — layer health + hard gates

Wraps ``auto_client_acquisition.service_catalog.registry``.

Hard rules (Article 4): catalog is read-only, never returns
fake-revenue numbers, never lists "live_send" or "live_charge"
in any offering's action_modes_used.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.service_catalog import (
    ServiceOffering,
    get_offering,
    list_governed_services,
    list_headline_services,
    list_offerings,
)

router = APIRouter(prefix="/api/v1/services", tags=["Service Catalog"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "no_guaranteed_claims": True,  # Article 8 forbids "guaranteed"/"نضمن"
}


def _serialize(offering: ServiceOffering) -> dict[str, Any]:
    return offering.model_dump()


@router.get("/status")
async def service_catalog_status() -> dict[str, Any]:
    """Layer health, count, hard gates."""
    offerings = list_offerings()
    return {
        "status": "ok",
        "offerings_count": len(offerings),
        "service_ids": [o.id for o in offerings],
        "hard_gates": _HARD_GATES,
        "wave": "wave13_phase_2_service_catalog",
        "is_estimate": True,
    }


@router.get("/catalog")
async def service_catalog() -> dict[str, Any]:
    """All 7 offerings in display order."""
    return {
        "offerings": [_serialize(o) for o in list_offerings()],
        "count": len(list_offerings()),
        "hard_gates": _HARD_GATES,
    }


@router.get("/governed")
async def governed_service_catalog() -> dict[str, Any]:
    """The 7 governed-tier services (Governed Revenue & AI Operations).

    Added alongside the 7 canonical offerings — does not replace them.
    """
    governed = list_governed_services()
    return {
        "governed_services": [s.model_dump() for s in governed],
        "headline_services": [s.id for s in list_headline_services()],
        "count": len(governed),
        "hard_gates": _HARD_GATES,
        "is_estimate": True,
    }


@router.get("/{service_id}")
async def service_offering_detail(service_id: str) -> dict[str, Any]:
    """One offering by id."""
    offering = get_offering(service_id)
    if offering is None:
        raise HTTPException(status_code=404, detail=f"unknown_service_id: {service_id}")
    return {
        "offering": _serialize(offering),
        "hard_gates": _HARD_GATES,
    }
