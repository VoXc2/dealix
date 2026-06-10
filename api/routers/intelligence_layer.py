"""Wave 12.7 — Intelligence Layer HTTP surface.

Exposes the Wave 12 §32 Intelligence Stack via FastAPI:
- GET  /api/v1/intelligence/status        — layer health + provider config
- POST /api/v1/intelligence/route          — dispatch a task to the right model
- GET  /api/v1/intelligence/tasks          — list canonical Dealix tasks
- POST /api/v1/intelligence/confidence     — score a model output

Wraps the existing ``auto_client_acquisition.intelligence`` modules
(task_registry, local_model_client, confidence, dealix_model_router).

Hard rules surfaced via ``_HARD_GATES`` dict (parity with other Wave 4+
routers — Article 4).
"""
from __future__ import annotations

from typing import Any, Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from auto_client_acquisition.intelligence.confidence import (
    combine,
    from_text_signals,
)
from auto_client_acquisition.intelligence.dealix_model_router import (
    route_task,
    status_summary,
)
from auto_client_acquisition.intelligence.dealix_task_registry import (
    DealixTask,
    all_tasks,
    get_task_requirements,
)

router = APIRouter(prefix="/api/v1/intelligence", tags=["Intelligence Layer"])


_HARD_GATES = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_secrets_in_response": True,
    "founder_only_tasks_never_cloud": True,
    "graceful_degradation_on_failure": True,
    "approval_required_for_external_actions": True,
}


# ─────────────────────────────────────────────────────────────────────
# Status
# ─────────────────────────────────────────────────────────────────────


@router.get("/status")
async def status() -> dict[str, Any]:
    """Layer status — provider config + reachability + hard gates.

    Read-only. Safe to poll. Never returns API keys.
    """
    summary = status_summary()
    summary["hard_gates"] = _HARD_GATES
    return summary


# ─────────────────────────────────────────────────────────────────────
# Tasks
# ─────────────────────────────────────────────────────────────────────


@router.get("/tasks")
async def list_tasks() -> dict[str, Any]:
    """List all 21 canonical Dealix tasks + their requirements.

    Read-only catalog. Used by founder dashboard to show which tasks
    map to which model tier + privacy level.
    """
    tasks = all_tasks()
    catalog = []
    for task in tasks:
        try:
            req = get_task_requirements(task)
            catalog.append({
                "task": task,
                "tier": req.tier.value if hasattr(req.tier, "value") else str(req.tier),
                "privacy_level": req.privacy_level,
                "requires_arabic_quality": req.requires_arabic_quality,
                "requires_structured_output": req.requires_structured_output,
                "max_cost_usd_per_call": req.max_cost_usd_per_call,
                "fallback_to_human": req.fallback_to_human,
            })
        except KeyError:
            continue  # skip drift
    return {
        "service": "intelligence_layer_tasks",
        "tasks_registered": len(catalog),
        "tasks": catalog,
        "hard_gates": _HARD_GATES,
    }


# ─────────────────────────────────────────────────────────────────────
# Route a task
# ─────────────────────────────────────────────────────────────────────


class RouteTaskRequest(BaseModel):
    """Inbound request to dispatch a task to the model layer."""

    task: str = Field(..., description="Must be a canonical DealixTask")
    prompt: str = Field(..., min_length=1, max_length=8000)
    language: Literal["ar", "en", "bilingual"] = "ar"
    json_mode: bool = False
    customer_handle: str = ""
    cloud_fallback_enabled: bool = True


@router.post("/route")
async def route_task_endpoint(req: RouteTaskRequest) -> dict[str, Any]:
    """Dispatch a Dealix task to the right model + return the decision.

    Returns ``RouterDecision`` as a dict — caller inspects ``status``
    field to decide next step.

    Hard rules (Article 4):
    - founder_only tasks NEVER reach cloud
    - Unknown task → ``status="degraded_to_human"`` (never raises)
    - Local-first; cloud only when local low-confidence + privacy allows
    - No secrets logged
    """
    try:
        decision = route_task(
            task=req.task,  # type: ignore[arg-type]
            prompt=req.prompt,
            language=req.language,
            json_mode=req.json_mode,
            customer_handle=req.customer_handle,
            cloud_fallback_enabled=req.cloud_fallback_enabled,
        )
    except Exception as exc:
        # Article 8: never fake success — surface the error honestly
        raise HTTPException(
            status_code=500,
            detail={
                "error": "intelligence_layer_internal",
                "type": type(exc).__name__,
                # NEVER include str(exc) — could leak prompts / secrets
                "message": "router invocation failed; check server logs",
            },
        ) from exc

    return {
        "task": decision.task,
        "status": decision.status,
        "text": decision.text,
        "backend_used": decision.backend_used,
        "model_used": decision.model_used,
        "estimated_cost_usd": decision.estimated_cost_usd,
        "estimated_input_tokens": decision.estimated_input_tokens,
        "estimated_output_tokens": decision.estimated_output_tokens,
        "is_actionable": decision.is_actionable,
        "needs_human": decision.needs_human,
        "confidence": {
            "score": decision.confidence.score,
            "level": decision.confidence.level,
            "reasons": list(decision.confidence.reasons),
        },
        "fallback_reasons": list(decision.fallback_reasons),
    }


# ─────────────────────────────────────────────────────────────────────
# Confidence scoring (standalone helper)
# ─────────────────────────────────────────────────────────────────────


class ConfidenceScoreRequest(BaseModel):
    """Standalone confidence-scoring endpoint for caller-supplied text."""

    text: str = Field(..., min_length=0, max_length=8000)
    expected_json: bool = False


@router.post("/confidence")
async def confidence_score(req: ConfidenceScoreRequest) -> dict[str, Any]:
    """Compute a confidence score for a model output text.

    Pure function — no side effects, no model calls. Used by callers
    that already have a model response and want the canonical confidence
    bucket.
    """
    score = from_text_signals(req.text, expected_json=req.expected_json)
    return {
        "score": score.score,
        "level": score.level,
        "reasons": list(score.reasons),
        "is_actionable": score.is_actionable,
        "needs_human_review": score.needs_human_review,
    }
