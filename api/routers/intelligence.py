"""
Intelligence router — surfaces SmartDrafter + ChannelOrchestrator + LLM router.

Endpoints:
    POST /api/v1/intelligence/draft
        body: {kind: "outreach"|"followup"|"objection"|"clarify",
               brain: {...}, context: {...}, fallback: "..."}
        Returns LLM-generated text (or fallback) + audit fields.

    POST /api/v1/intelligence/channel-recommend
        body: {prospect: {...}, brain: {...}}
        Returns ranked channel list with reasoning.

    GET  /api/v1/intelligence/llm-status
        Returns which LLM providers are currently configured.

    GET  /api/v1/intelligence/usage
        Returns LLM usage summary (tokens, fallbacks, errors per provider).
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.intelligence.channel_orchestrator import recommend
from auto_client_acquisition.intelligence.smart_drafter import get_drafter
from core.config.settings import get_settings

router = APIRouter(prefix="/api/v1/intelligence", tags=["intelligence"])


_GATE_KEYS = (
    "whatsapp_allow_live_send",
    "whatsapp_allow_internal_send",
    "whatsapp_allow_customer_send",
    "moyasar_allow_live_charge",
    "linkedin_allow_auto_dm",
    "gmail_allow_live_send",
    "resend_allow_live_send",
    "calls_allow_live_dial",
)


def _gates_dict() -> dict[str, bool]:
    s = get_settings()
    return {g: bool(getattr(s, g, False)) for g in _GATE_KEYS}


@router.get("/llm-status")
async def llm_status() -> dict[str, Any]:
    """Show which LLM providers are configured (without leaking keys)."""
    try:
        from core.llm.router import get_router
        r = get_router()
        providers = [p.value for p in r.available_providers()]
        usage = r.usage_summary()
    except Exception as exc:  # noqa: BLE001
        return {
            "available_providers": [],
            "error": f"{type(exc).__name__}: {str(exc)[:200]}",
            "fallback_active": True,
        }
    return {
        "available_providers": providers,
        "providers_count": len(providers),
        "fallback_active": len(providers) == 0,
        "usage_summary": usage,
    }


@router.get("/usage")
async def usage() -> dict[str, Any]:
    """Return LLM usage summary."""
    try:
        from core.llm.router import get_router
        return get_router().usage_summary()
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)[:200]}


@router.post("/draft")
async def draft(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Generate a smart draft (outreach / followup / objection / clarify).

    Always returns 200 — fallback used if LLM unavailable.
    """
    kind = str(body.get("kind") or "outreach").lower()
    brain = dict(body.get("brain") or {})
    context = dict(body.get("context") or {})
    fallback = str(body.get("fallback") or "")

    drafter = get_drafter()

    if kind == "outreach":
        result = await drafter.draft_outreach_message(
            brain,
            prospect_hint=str(context.get("prospect_hint", "")),
            prospect_recent_signal=str(context.get("recent_signal", "")),
            fallback=fallback,
        )
    elif kind == "followup":
        result = await drafter.draft_followup(
            brain,
            days_since_last=int(context.get("days_since_last", 5)),
            fallback=fallback,
        )
    elif kind == "objection":
        objection_text = str(context.get("objection_text", "السعر مرتفع"))
        result = await drafter.draft_objection_response(
            brain,
            objection_text=objection_text,
            fallback=fallback,
        )
    elif kind == "clarify":
        user_message = str(context.get("user_message", body.get("user_message", "")))
        if not user_message:
            raise HTTPException(status_code=400, detail="context.user_message_required")
        result = await drafter.clarify_intent(
            user_message,
            fallback=fallback,
        )
    else:
        raise HTTPException(status_code=400, detail=f"unknown_kind:{kind}")

    return {
        "kind": kind,
        "text": result.text,
        "used_llm": result.used_llm,
        "provider": result.provider,
        "fallback_used": result.fallback_used,
        "fallback_reason": result.fallback_reason,
        "safety_passed": result.safety_passed,
        "tokens": {
            "input": result.input_tokens,
            "output": result.output_tokens,
        },
    }


@router.post("/channel-recommend")
async def channel_recommend(body: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """Return ranked allowed-vs-blocked channels for a prospect.

    Body: {prospect: {...}, brain: {...}}
    Both optional — empty inputs return the default channel ranking.
    """
    prospect = dict(body.get("prospect") or {})
    brain = dict(body.get("brain") or {})
    gates = _gates_dict()

    recs = recommend(prospect=prospect, brain=brain, gates=gates)
    return {
        "as_of_gates": gates,
        "count": len(recs),
        "recommendations": [
            {
                "channel": r.channel,
                "allowed": r.allowed,
                "score": r.score,
                "reason_ar": r.reason_ar,
            }
            for r in recs
        ],
        "best_allowed": next(
            ({"channel": r.channel, "score": r.score, "reason_ar": r.reason_ar}
             for r in recs if r.allowed),
            None,
        ),
    }
