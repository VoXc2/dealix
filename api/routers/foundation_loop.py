"""Foundation Core router: one complete governed enterprise loop."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.foundation_core import (
    EnterpriseLoopRequest,
    LeadInput,
    run_smallest_governed_loop,
)

router = APIRouter(prefix="/api/v1/foundation", tags=["foundation-core"])

_HARD_GATES = {
    "no_unrestricted_access": True,
    "tenant_isolation_required": True,
    "approval_required_for_external_actions": True,
    "audit_logging_required": True,
}


class _LeadPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    company: str
    name: str
    email: str
    phone: str | None = None
    sector: str | None = None
    region: str | None = None
    message: str | None = None
    budget: float | None = Field(default=None, ge=0)


class _EnterpriseLoopPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tenant_id: str = Field(min_length=1)
    user_id: str = Field(min_length=1)
    user_role: str = Field(min_length=1)
    approval_granted: bool = False
    users_in_tenant: int = Field(default=3, ge=1)
    roles_configured: list[str] = Field(default_factory=lambda: ["tenant_admin", "sales_manager"])
    crm_integration: str = "simulated_crm"
    lead: _LeadPayload


@router.get("/status")
async def foundation_status() -> dict[str, Any]:
    return {
        "service": "foundation_core",
        "status": "operational",
        "workflow": "ai_revenue_os_enterprise_loop_v1",
        "hard_gates": _HARD_GATES,
        "next_action_ar": "شغّل /enterprise-loop/run لبدء الحلقة المؤسسية الواحدة",
        "next_action_en": "Run /enterprise-loop/run to execute the single enterprise loop.",
    }


@router.post("/enterprise-loop/run")
async def run_enterprise_loop(payload: _EnterpriseLoopPayload) -> dict[str, Any]:
    try:
        result = run_smallest_governed_loop(
            EnterpriseLoopRequest(
                tenant_id=payload.tenant_id,
                user_id=payload.user_id,
                user_role=payload.user_role,
                approval_granted=payload.approval_granted,
                users_in_tenant=payload.users_in_tenant,
                roles_configured=payload.roles_configured,
                crm_integration=payload.crm_integration,
                lead=LeadInput(**payload.lead.model_dump()),
            )
        )
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"hard_gates": _HARD_GATES, **result}
