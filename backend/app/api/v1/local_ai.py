"""
Local AI API — status, model catalog, and chat against the on-prem Ollama daemon.

Endpoints:
  GET  /api/v1/local-ai/status        → daemon health + detected tier + pulled models
  GET  /api/v1/local-ai/catalog       → catalogued models + recommended install plan
  POST /api/v1/local-ai/chat          → non-streaming chat against a picked model
  POST /api/v1/local-ai/health-check  → force a fresh Ollama ping
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.local_ai.catalog import (
    MODEL_CATALOG,
    TaskKind,
    detect_server_tier,
    recommended_install_plan,
    select_models_for_tier,
)
from app.services.local_ai.client import get_local_client
from app.services.local_ai.router import get_local_router


router = APIRouter(prefix="/local-ai", tags=["Local AI"])


class LocalChatRequest(BaseModel):
    task: str = Field(default="internal_drafting", description="Dealix task key (e.g. internal_drafting, fast_classify, coding, arabic_summarization).")
    prompt: str = Field(..., min_length=1)
    system: str = ""
    temperature: float = 0.3
    max_tokens: int = 1024
    json_mode: bool = False
    race: bool = False


@router.get("/status")
async def status() -> dict[str, Any]:
    client = get_local_client()
    lrouter = get_local_router()
    capacity = detect_server_tier()
    healthy = await client.health(force=True)
    pulled = await client.list_models() if healthy else []
    return {
        "enabled": lrouter.is_enabled(),
        "daemon_healthy": healthy,
        "base_url": client.base_url,
        "capacity": capacity.to_dict(),
        "pulled_models": [m.get("name") or m.get("model") for m in pulled],
        "overrides": {
            "default": lrouter.default_model,
            "router": lrouter.router_model,
            "coder": lrouter.coder_model,
            "reasoner": lrouter.reasoner_model,
        },
    }


@router.get("/catalog")
async def catalog() -> dict[str, Any]:
    capacity = detect_server_tier()
    eligible = select_models_for_tier(capacity.tier)
    plan = recommended_install_plan(capacity)
    return {
        "capacity": capacity.to_dict(),
        "all_models": [
            {
                "tag": m.ollama_tag,
                "family": m.family,
                "approx_size_gb": m.approx_size_gb,
                "min_ram_gb": m.min_ram_gb,
                "tier": m.tier.value,
                "tasks": [t.value for t in m.tasks],
                "arabic_quality": m.arabic_quality,
                "english_quality": m.english_quality,
                "notes": m.notes,
            }
            for m in MODEL_CATALOG
        ],
        "eligible_for_host": [m.ollama_tag for m in eligible],
        "recommended_install_plan": [m.ollama_tag for m in plan],
    }


@router.post("/health-check")
async def health_check() -> dict[str, Any]:
    client = get_local_client()
    return {"healthy": await client.health(force=True), "base_url": client.base_url}


@router.post("/chat")
async def chat(body: LocalChatRequest) -> dict[str, Any]:
    lrouter = get_local_router()
    if not lrouter.is_enabled():
        raise HTTPException(status_code=503, detail="Local AI disabled (LOCAL_LLM_ENABLED=0).")
    if not await lrouter.is_available():
        raise HTTPException(status_code=503, detail="Ollama daemon unreachable or no models pulled.")
    result = await lrouter.run(
        task=body.task,
        prompt=body.prompt,
        system=body.system,
        temperature=body.temperature,
        max_tokens=body.max_tokens,
        json_mode=body.json_mode,
        race=body.race,
    )
    if not result.success:
        raise HTTPException(status_code=502, detail=result.error or "Local inference failed")
    decision = lrouter.decide(lrouter.resolve_task(body.task))
    return {
        "decision": decision.to_dict(),
        "result": result.to_dict(),
    }


@router.get("/tasks")
async def tasks() -> dict[str, Any]:
    """Return the Dealix task keys the local router understands."""
    return {
        "task_kinds": [t.value for t in TaskKind],
        "mapped_task_strings": sorted(list({
            *[k for k in _all_task_strings()],
        })),
    }


def _all_task_strings() -> list[str]:
    from app.services.local_ai.router import _TASK_STRING_MAP
    return list(_TASK_STRING_MAP.keys())
