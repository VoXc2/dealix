"""System 26 — Organizational Control Plane router.

Register / monitor / pause / resume / rollback / trace / re-route workflow
runs, and live-edit attached policies. Rollback and policy-edit return an
approval ticket (HTTP 202) — the state change applies only after a grant.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.control_plane_os.approval_gate import ApprovalGateError
from auto_client_acquisition.control_plane_os.core import (
    ControlPlaneError,
    get_control_plane,
)
from auto_client_acquisition.control_plane_os.schemas import PolicyEdit

router = APIRouter(prefix="/api/v1/control-plane", tags=["control-plane"])


class RegisterRunBody(BaseModel):
    workflow_id: str = Field(..., min_length=1)
    customer_id: str = Field(..., min_length=1)
    correlation_id: str | None = None
    actor: str = "system"
    attached_policy_ids: list[str] = Field(default_factory=list)


class ActorBody(BaseModel):
    actor: str = "system"
    reason: str = ""


class RerouteBody(BaseModel):
    new_workflow_id: str = Field(..., min_length=1)
    actor: str = "system"


class PolicyEditBody(BaseModel):
    policy_id: str = Field(..., min_length=1)
    change: dict[str, Any] = Field(default_factory=dict)
    editor: str = "system"


class FinalizeBody(BaseModel):
    ticket_id: str = Field(..., min_length=1)
    actor: str = "system"


def _not_found(exc: ControlPlaneError) -> HTTPException:
    return HTTPException(status_code=404, detail=str(exc))


@router.post("/runs", status_code=201)
async def register_run(body: RegisterRunBody) -> dict[str, Any]:
    run = get_control_plane().register_run(
        workflow_id=body.workflow_id,
        customer_id=body.customer_id,
        correlation_id=body.correlation_id,
        actor=body.actor,
        attached_policy_ids=body.attached_policy_ids,
    )
    return run.model_dump(mode="json")


@router.get("/runs")
async def list_runs(state: str | None = None) -> dict[str, Any]:
    runs = get_control_plane().list_runs(state=state)
    return {"count": len(runs), "runs": [r.model_dump(mode="json") for r in runs]}


@router.get("/runs/{run_id}")
async def monitor_run(run_id: str) -> dict[str, Any]:
    try:
        return get_control_plane().monitor(run_id).model_dump(mode="json")
    except ControlPlaneError as exc:
        raise _not_found(exc) from exc


@router.get("/runs/{run_id}/trace")
async def trace_run(run_id: str) -> dict[str, Any]:
    try:
        return get_control_plane().trace(run_id).model_dump(mode="json")
    except ControlPlaneError as exc:
        raise _not_found(exc) from exc


@router.post("/runs/{run_id}/pause")
async def pause_run(run_id: str, body: ActorBody) -> dict[str, Any]:
    try:
        return get_control_plane().pause(run_id, actor=body.actor).model_dump(mode="json")
    except ControlPlaneError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/runs/{run_id}/resume")
async def resume_run(run_id: str, body: ActorBody) -> dict[str, Any]:
    try:
        return get_control_plane().resume(run_id, actor=body.actor).model_dump(mode="json")
    except ControlPlaneError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.post("/runs/{run_id}/rollback", status_code=202)
async def rollback_run(run_id: str, body: ActorBody) -> dict[str, Any]:
    try:
        ticket = get_control_plane().rollback(run_id, actor=body.actor, reason=body.reason)
    except ControlPlaneError as exc:
        raise _not_found(exc) from exc
    return {"status": "approval_required", "ticket": ticket.model_dump(mode="json")}


@router.post("/runs/{run_id}/rollback/finalize")
async def finalize_rollback(run_id: str, body: FinalizeBody) -> dict[str, Any]:
    try:
        run = get_control_plane().finalize_rollback(
            run_id, body.ticket_id, actor=body.actor
        )
    except ControlPlaneError as exc:
        raise _not_found(exc) from exc
    except ApprovalGateError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return run.model_dump(mode="json")


@router.post("/runs/{run_id}/reroute")
async def reroute_run(run_id: str, body: RerouteBody) -> dict[str, Any]:
    try:
        child = get_control_plane().reroute(
            run_id, new_workflow_id=body.new_workflow_id, actor=body.actor
        )
    except ControlPlaneError as exc:
        raise _not_found(exc) from exc
    return child.model_dump(mode="json")


@router.post("/runs/{run_id}/policy-edit", status_code=202)
async def edit_policy(run_id: str, body: PolicyEditBody) -> dict[str, Any]:
    edit = PolicyEdit(
        run_id=run_id, policy_id=body.policy_id, change=body.change, editor=body.editor
    )
    try:
        ticket = get_control_plane().edit_policy(edit, actor=body.editor)
    except ControlPlaneError as exc:
        raise _not_found(exc) from exc
    return {"status": "approval_required", "ticket": ticket.model_dump(mode="json")}
