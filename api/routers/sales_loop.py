"""Sales Loop router — end-to-end lead-to-paid orchestration endpoints.

Wraps :mod:`auto_client_acquisition.sales_os.sales_loop_orchestrator`. The
orchestrator never sends externally and never auto-confirms payment; every
external-facing transition opens an approval-center gate.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.revenue_pipeline.stage_policy import PipelineStage
from auto_client_acquisition.sales_os.sales_loop_orchestrator import (
    SalesLoopGateError,
    get_default_sales_loop_orchestrator,
)

router = APIRouter(prefix="/api/v1/sales-loop", tags=["sales-loop"])

_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_fake_revenue": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
    "no_project_without_proof_pack": True,
    "no_project_without_capital_asset": True,
}


class _StartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    raw_payload: dict[str, Any] = Field(default_factory=dict)
    source: str = "manual"
    customer_handle: str = Field(min_length=1, max_length=64)


class _AdvanceRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    loop_id: str
    target_stage: PipelineStage
    actor: str = Field(min_length=1, max_length=64)
    commitment_evidence: str = ""
    payment_evidence: str = ""
    actual_amount_sar: int | None = None
    meeting_minutes: int = 30
    invoice_method: str = "bank_transfer"
    reason: str = ""


class _ResolveRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    approval_id: str
    decision: str = Field(pattern="^(approve|reject)$")
    who: str = Field(min_length=1, max_length=64)
    reason: str = ""


@router.get("/status")
async def sales_loop_status() -> dict[str, Any]:
    orch = get_default_sales_loop_orchestrator()
    return {
        "service": "sales_loop",
        "module": "sales_loop_orchestrator",
        "status": "operational",
        "version": "sl-v1",
        "degraded": False,
        "active_loops": len(orch.list_loops(limit=10_000)),
        "hard_gates": _HARD_GATES,
        "next_action_en": "POST /start, then POST /advance per stage_policy.",
        "next_action_ar": "ابدأ عبر /start ثم تقدّم عبر /advance حسب stage_policy.",
    }


@router.post("/start")
async def start_loop(req: _StartRequest) -> dict[str, Any]:
    orch = get_default_sales_loop_orchestrator()
    try:
        record = orch.start_loop(
            raw_payload=req.raw_payload,
            source=req.source,
            customer_handle=req.customer_handle,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"loop": record.model_dump(mode="json"), "hard_gates": _HARD_GATES}


@router.post("/advance")
async def advance_loop(req: _AdvanceRequest) -> dict[str, Any]:
    orch = get_default_sales_loop_orchestrator()
    try:
        record = await orch.advance(
            loop_id=req.loop_id,
            target_stage=req.target_stage,
            actor=req.actor,
            commitment_evidence=req.commitment_evidence,
            payment_evidence=req.payment_evidence,
            actual_amount_sar=req.actual_amount_sar,
            meeting_minutes=req.meeting_minutes,
            invoice_method=req.invoice_method,
            reason=req.reason,
        )
    except SalesLoopGateError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "approval_gate_open",
                "approval_id": exc.approval_id,
                "approval_status": exc.status,
                "message": str(exc),
            },
        ) from exc
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "loop": record.model_dump(mode="json"),
        "next_actions": orch.next_actions(record.loop_id),
        "hard_gates": _HARD_GATES,
    }


@router.post("/{loop_id}/resolve-approval")
async def resolve_approval(loop_id: str, req: _ResolveRequest) -> dict[str, Any]:
    orch = get_default_sales_loop_orchestrator()
    try:
        record = orch.resolve_approval(
            loop_id=loop_id,
            approval_id=req.approval_id,
            decision=req.decision,
            who=req.who,
            reason=req.reason,
        )
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "loop": record.model_dump(mode="json"),
        "next_actions": orch.next_actions(loop_id),
        "hard_gates": _HARD_GATES,
    }


@router.get("")
async def list_loops(limit: int = 50) -> dict[str, Any]:
    orch = get_default_sales_loop_orchestrator()
    return {
        "loops": [r.model_dump(mode="json") for r in orch.list_loops(limit=limit)],
        "hard_gates": _HARD_GATES,
    }


@router.get("/{loop_id}")
async def get_loop(loop_id: str) -> dict[str, Any]:
    orch = get_default_sales_loop_orchestrator()
    record = orch.get_loop(loop_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"unknown sales loop: {loop_id}")
    return {
        "loop": record.model_dump(mode="json"),
        "next_actions": orch.next_actions(loop_id),
        "audit_events": orch.audit_trail(loop_id),
        "hard_gates": _HARD_GATES,
    }
