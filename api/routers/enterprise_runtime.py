"""Enterprise runtime router for governed operational workflow execution."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.enterprise_infrastructure.runtime import run_governed_workflow

router = APIRouter(prefix="/api/v1/enterprise/runtime", tags=["enterprise-runtime"])


class _LeadQualificationRunBody(BaseModel):
    tenant_id: str = Field(..., min_length=1)
    actor_role: str = Field(..., min_length=1)
    approvals: list[str] = Field(default_factory=list)
    forced_fail_steps: list[str] = Field(default_factory=list)


@router.post("/lead-qualification/run")
async def run_lead_qualification(body: _LeadQualificationRunBody) -> dict[str, Any]:
    root = Path(__file__).resolve().parents[2]
    workflow_path = root / "workflows" / "sales" / "lead_qualification.workflow.yaml"
    agent_path = root / "agents" / "sales_agent" / "agent.yaml"
    try:
        return run_governed_workflow(
            workflow_path=workflow_path,
            agent_path=agent_path,
            tenant_id=body.tenant_id,
            actor_role=body.actor_role,
            approvals=set(body.approvals),
            forced_fail_steps=set(body.forced_fail_steps),
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=f"enterprise_runtime_failed: {exc}") from exc
