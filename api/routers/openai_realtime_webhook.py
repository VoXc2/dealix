"""Verified OpenAI Realtime SIP webhook for the Dealix Voice Front Desk."""

from __future__ import annotations

import asyncio
import logging

from fastapi import APIRouter, HTTPException, Request

from dealix.voice_ai.front_desk import (
    VoiceAIConfig,
    get_voice_readiness,
    handle_openai_realtime_webhook,
    run_voice_sideband,
)

router = APIRouter(prefix="/api/v1/webhooks/openai", tags=["Webhooks", "Voice AI"])
logger = logging.getLogger(__name__)
_SIDE_BAND_TASKS: set[asyncio.Task[None]] = set()


def _retain_task(task: asyncio.Task[None]) -> None:
    _SIDE_BAND_TASKS.add(task)

    def _done(completed: asyncio.Task[None]) -> None:
        _SIDE_BAND_TASKS.discard(completed)
        if completed.cancelled():
            return
        try:
            completed.exception()
        except Exception as exc:
            logger.warning("voice sideband task finalizer failed: %s", type(exc).__name__)

    task.add_done_callback(_done)


@router.get("/voice-readiness")
async def voice_readiness() -> dict[str, object]:
    """Return non-secret Voice AI readiness state."""

    return get_voice_readiness()


@router.post("/realtime")
async def openai_realtime_webhook(request: Request) -> dict[str, object]:
    """Verify and process `realtime.call.incoming` without exposing webhook data."""

    raw_bytes = await request.body()
    try:
        raw_body = raw_bytes.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="invalid_webhook_encoding") from exc

    config = VoiceAIConfig.from_env()
    if not config.openai_api_key or not config.webhook_secret:
        # Do not accept unsigned events or attempt to infer a key from another runtime.
        raise HTTPException(status_code=503, detail="voice_ai_credentials_not_configured")

    try:
        result = await asyncio.to_thread(
            handle_openai_realtime_webhook,
            raw_body,
            request.headers,
            config,
        )
    except Exception as exc:
        # Signature failures and malformed provider events are deliberately opaque.
        logger.warning("OpenAI Realtime webhook rejected: %s", type(exc).__name__)
        raise HTTPException(status_code=400, detail="invalid_openai_webhook") from exc

    if result.start_sideband and result.call_id:
        task = asyncio.create_task(run_voice_sideband(result.call_id, config))
        _retain_task(task)

    return {
        "ok": True,
        "event_type": result.event_type,
        "action": result.action,
        "sideband_started": bool(result.start_sideband and result.call_id),
    }
