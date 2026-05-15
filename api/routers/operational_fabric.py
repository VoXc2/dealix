"""Operational Fabric Router — observability surface for Systems 26-35."""

from __future__ import annotations

from fastapi import APIRouter

from auto_client_acquisition.operational_fabric_os import (
    PLATFORM_CONTRACTS,
    operational_dominance_status,
)

router = APIRouter(prefix="/api/v1/platform", tags=["platform"])


@router.get("/contracts")
async def list_platform_contracts() -> dict[str, object]:
    return {
        "contracts_total": len(PLATFORM_CONTRACTS),
        "contracts": [
            {
                "system_id": contract.system_id,
                "system_name": contract.system_name,
                "platform_path": contract.platform_path,
                "module_path": contract.module_path,
                "symbol": contract.symbol,
            }
            for contract in PLATFORM_CONTRACTS
        ],
    }


@router.get("/contracts/health")
async def platform_contract_health() -> dict[str, object]:
    return operational_dominance_status()
