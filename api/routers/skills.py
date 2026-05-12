"""
Skills catalog router — public read + per-skill execution.

Endpoints:
    GET  /api/v1/skills              — list every skill in skills/MANIFEST.yaml
    GET  /api/v1/skills/{id}         — single skill metadata
    POST /api/v1/skills/{id}/run     — execute a registered handler
    GET  /api/v1/skills/handlers     — which skill ids have Python handlers
"""

from __future__ import annotations

import time
from typing import Any

from fastapi import APIRouter, HTTPException, Path, Request
from pydantic import BaseModel, Field

from core.logging import get_logger
from dealix.agents.skills import by_id, load
from dealix.agents.skills.handlers import (
    get_handler,
    registered_ids,
)
from dealix.observability.skill_tracer import SkillTraceContext, traced_skill_run

# Importing these modules triggers the `@register(...)` side-effects
# that put the T9 handlers in the registry.
from dealix.agents.skills import handlers_llm as _t9_llm  # noqa: F401
from dealix.agents.skills import handlers_data as _t9_data  # noqa: F401

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])
log = get_logger(__name__)


@router.get("")
async def list_skills() -> dict[str, Any]:
    skills = load()
    handlers = set(registered_ids())
    return {
        "count": len(skills),
        "skills": [
            {
                "id": s.id,
                "path": s.path,
                "description": s.description,
                "inputs": s.inputs,
                "output_shape": s.output_shape,
                "executable": s.id in handlers,
            }
            for s in skills
        ],
    }


@router.get("/handlers")
async def list_handlers() -> dict[str, Any]:
    """Which skill ids have a Python handler registered today."""
    return {"handlers": registered_ids()}


@router.get("/{skill_id}")
async def get_skill(skill_id: str = Path(..., max_length=64)) -> dict[str, Any]:
    s = by_id(skill_id)
    if s is None:
        raise HTTPException(404, "skill_not_found")
    return {
        "id": s.id,
        "path": s.path,
        "description": s.description,
        "inputs": s.inputs,
        "output_shape": s.output_shape,
        "permissions": s.permissions,
        "executable": get_handler(s.id) is not None,
    }


class SkillRunIn(BaseModel):
    inputs: dict[str, Any] = Field(default_factory=dict)
    estimated_usd: float = Field(default=0.0, ge=0, le=10.0)


@router.post("/{skill_id}/run")
async def run_skill(
    payload: SkillRunIn,
    request: Request,
    skill_id: str = Path(..., max_length=64),
) -> dict[str, Any]:
    """Execute a registered skill handler. Skills without a handler
    return 501 not_implemented — at which point the BYOA path applies.

    Wraps the call with `traced_skill_run` which adds cost-cap
    enforcement (CostGuard), a Langfuse trace, and a Lago meter event
    when the corresponding env vars are set.
    """
    s = by_id(skill_id)
    if s is None:
        raise HTTPException(404, "skill_not_found")
    handler = get_handler(skill_id)
    if handler is None:
        raise HTTPException(501, "skill_handler_not_implemented")

    tenant_id = getattr(request.state, "tenant_id", None) or "anonymous"
    ctx = SkillTraceContext(
        skill_id=skill_id,
        tenant_id=tenant_id,
        locale=str(payload.inputs.get("locale") or "ar"),
    )

    t0 = time.perf_counter()
    try:
        result = await traced_skill_run(
            ctx=ctx,
            handler=handler,
            inputs=payload.inputs,
            estimated_usd=payload.estimated_usd,
        )
    except Exception as exc:  # surface the failure rather than crash.
        log.exception("skill_run_failed", skill_id=skill_id)
        raise HTTPException(500, f"skill_execution_failed:{exc!s}") from exc

    # Surface the cost-cap short-circuit as HTTP 402.
    if isinstance(result, dict) and result.get("error") == "cost_cap_exceeded":
        raise HTTPException(
            status_code=402,
            detail={"error": "cost_cap_exceeded", "reason": result.get("reason")},
        )

    elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
    log.info(
        "skill_ran",
        skill_id=skill_id,
        ms=elapsed_ms,
        tenant_id=tenant_id,
    )
    return {
        "skill_id": skill_id,
        "tenant_id": tenant_id,
        "elapsed_ms": elapsed_ms,
        "result": result,
    }
