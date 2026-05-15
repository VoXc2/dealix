"""System 31 — Enterprise Safety Engine router.

Runtime safety checks, kill switches, circuit breakers and execution limits.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.runtime_safety_os.core import (
    SafetyError,
    get_safety_engine,
)
from auto_client_acquisition.runtime_safety_os.schemas import ExecutionLimit

router = APIRouter(prefix="/api/v1/runtime-safety", tags=["runtime-safety"])


class CheckBody(BaseModel):
    target: str = Field(..., min_length=1)
    action_type: str = ""


class KillSwitchBody(BaseModel):
    target: str = Field(..., min_length=1)
    actor: str = "system"
    reason: str = ""


class ExecutionLimitBody(BaseModel):
    target: str = Field(..., min_length=1)
    max_actions_per_hour: int = Field(default=1000, ge=0)
    max_concurrency: int = Field(default=10, ge=0)


@router.post("/check")
async def safety_check(body: CheckBody) -> dict[str, Any]:
    try:
        verdict = get_safety_engine().check(
            target=body.target, action_type=body.action_type
        )
    except SafetyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return verdict.model_dump(mode="json")


@router.post("/kill-switch", status_code=201)
async def engage_kill_switch(body: KillSwitchBody) -> dict[str, Any]:
    try:
        switch = get_safety_engine().engage_kill_switch(
            target=body.target, actor=body.actor, reason=body.reason
        )
    except SafetyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return switch.model_dump(mode="json")


@router.delete("/kill-switch/{switch_id}")
async def release_kill_switch(switch_id: str, actor: str = "system") -> dict[str, Any]:
    try:
        switch = get_safety_engine().release_kill_switch(switch_id, actor=actor)
    except SafetyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return switch.model_dump(mode="json")


@router.get("/circuit-breakers")
async def list_circuit_breakers() -> dict[str, Any]:
    breakers = get_safety_engine().list_breakers()
    return {
        "count": len(breakers),
        "breakers": [b.model_dump(mode="json") for b in breakers],
    }


@router.put("/execution-limits")
async def set_execution_limit(body: ExecutionLimitBody) -> dict[str, Any]:
    limit = get_safety_engine().set_execution_limit(ExecutionLimit(**body.model_dump()))
    return limit.model_dump(mode="json")


@router.get("/status/{target}")
async def safety_status(target: str) -> dict[str, Any]:
    try:
        return get_safety_engine().status(target)
    except SafetyError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
