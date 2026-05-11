"""Wave 13 Phase 10 — Integration Capability HTTP surface.

- GET /api/v1/integrations/capabilities  → all 12
- GET /api/v1/integrations/{integration_id}
- GET /api/v1/integrations/status

Wraps ``auto_client_acquisition.integration_capability``.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.integration_capability import (
    IntegrationCapability,
    get_integration,
    list_integrations,
)

router = APIRouter(prefix="/api/v1/integrations", tags=["Integration Capability"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_scraping": True,
    "no_cold_whatsapp": True,
    "L3_requires_5_plus_customers_proof": True,
}


def _serialize(i: IntegrationCapability) -> dict[str, Any]:
    return i.model_dump()


@router.get("/status")
async def integrations_status() -> dict[str, Any]:
    integrations = list_integrations()
    return {
        "status": "ok",
        "wave": "wave13_phase_10_integration_capability",
        "integrations_count": len(integrations),
        "by_level": {
            "level_1_manual_csv": sum(1 for i in integrations if i.current_level == 1),
            "level_2_read_only": sum(1 for i in integrations if i.current_level == 2),
            "level_3_controlled_write": sum(1 for i in integrations if i.current_level == 3),
        },
        "hard_gates": _HARD_GATES,
    }


@router.get("/capabilities")
async def integrations_list() -> dict[str, Any]:
    return {
        "integrations": [_serialize(i) for i in list_integrations()],
        "count": len(list_integrations()),
        "hard_gates": _HARD_GATES,
    }


@router.get("/{integration_id}")
async def integration_detail(integration_id: str) -> dict[str, Any]:
    rec = get_integration(integration_id)
    if rec is None:
        raise HTTPException(
            status_code=404, detail=f"unknown_integration_id: {integration_id}"
        )
    return {
        "integration": _serialize(rec),
        "hard_gates": _HARD_GATES,
    }
