"""Authenticated operational controls/readiness for the Dealix Voice AI channel."""

from __future__ import annotations

from fastapi import APIRouter

from dealix.voice_ai.front_desk import get_voice_readiness
from dealix.voice_ai.sip_runtime import VOICE_OUTPUT_VOICE

router = APIRouter(prefix="/api/v1/ops/voice-ai", tags=["Operations", "Voice AI"])


@router.get("/readiness")
async def voice_readiness() -> dict[str, object]:
    """Return non-secret Voice AI readiness on an authenticated API surface."""

    state = get_voice_readiness()
    state["raw_recording_persistence"] = False
    state["live_voice"] = VOICE_OUTPUT_VOICE
    state["model_locked"] = True
    return state
