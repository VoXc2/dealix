"""Support OS — lightweight classify endpoint (draft-only, escalation rules)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

from auto_client_acquisition.support_os_mode import classify_support_message

router = APIRouter(prefix="/api/v1/support-os", tags=["support-os"])


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "support_os_mode",
        "guardrails": {
            "no_llm": True,
            "no_live_send": True,
            "draft_only_default": True,
            "escalation_on_refund_privacy_security": True,
        },
    }


@router.post("/classify")
async def classify_endpoint(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    body = str(payload.get("message", "") or "")
    result = classify_support_message(body)
    return {"input_length": len(body), "classification": result}
