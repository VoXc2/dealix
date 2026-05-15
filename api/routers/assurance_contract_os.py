"""System 28 — Assurance Contract Engine router.

Register assurance contracts and evaluate agent actions against them. No
contract means a fail-closed DENY; external/irreversible actions escalate.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.assurance_contract_os.core import (
    ContractError,
    get_contract_engine,
)
from auto_client_acquisition.assurance_contract_os.schemas import (
    AssuranceContract,
    ContractType,
)

router = APIRouter(prefix="/api/v1/assurance-contracts", tags=["assurance-contracts"])


class ContractBody(BaseModel):
    contract_type: ContractType
    agent_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    may_see: list[str] = Field(default_factory=list)
    may_propose: list[str] = Field(default_factory=list)
    may_execute: list[str] = Field(default_factory=list)
    precondition_checks: list[str] = Field(default_factory=list)
    rollback_plan: str | None = None
    is_external: bool = False
    is_irreversible: bool = False


class EvaluateBody(BaseModel):
    agent_id: str = Field(..., min_length=1)
    action_type: str = Field(..., min_length=1)
    context: dict[str, Any] = Field(default_factory=dict)


@router.post("/contracts", status_code=201)
async def register_contract(body: ContractBody) -> dict[str, Any]:
    contract = AssuranceContract(**body.model_dump())
    try:
        stored = get_contract_engine().register_contract(contract)
    except ContractError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return stored.model_dump(mode="json")


@router.get("/contracts")
async def list_contracts(agent_id: str | None = None) -> dict[str, Any]:
    contracts = get_contract_engine().list_contracts(agent_id=agent_id)
    return {
        "count": len(contracts),
        "contracts": [c.model_dump(mode="json") for c in contracts],
    }


@router.get("/contracts/{contract_id}")
async def get_contract(contract_id: str) -> dict[str, Any]:
    for contract in get_contract_engine().list_contracts():
        if contract.contract_id == contract_id:
            return contract.model_dump(mode="json")
    raise HTTPException(status_code=404, detail=f"contract not found: {contract_id}")


@router.post("/evaluate")
async def evaluate(body: EvaluateBody) -> dict[str, Any]:
    result = get_contract_engine().evaluate(
        agent_id=body.agent_id,
        action_type=body.action_type,
        context=body.context,
    )
    return result.model_dump(mode="json")
