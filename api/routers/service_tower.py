"""Service Tower router — contracts + excellence scoring."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.service_tower.contracts import (
    all_contracts, contract_to_dict, get_contract,
)
from auto_client_acquisition.service_tower.excellence_score import (
    all_excellence, compute_excellence,
)

router = APIRouter(prefix="/api/v1/service-tower", tags=["service-tower"])


@router.get("/contracts")
async def list_contracts() -> dict[str, Any]:
    return {
        "count": len(all_contracts()),
        "contracts": [contract_to_dict(c) for c in all_contracts()],
    }


@router.get("/contracts/{service_id}")
async def get_one(service_id: str) -> dict[str, Any]:
    c = get_contract(service_id)
    if c is None:
        raise HTTPException(status_code=404, detail="contract_not_found")
    return contract_to_dict(c)


@router.get("/excellence")
async def excellence_overview() -> dict[str, Any]:
    return all_excellence()


@router.get("/excellence/{service_id}")
async def excellence_one(service_id: str) -> dict[str, Any]:
    c = get_contract(service_id)
    if c is None:
        raise HTTPException(status_code=404, detail="contract_not_found")
    return compute_excellence(c)
