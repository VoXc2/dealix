"""
Server-Sent Events (SSE) stream for the customer dashboard.

Why SSE over WebSockets: SSE is one-way (server → client) which matches
our update model exactly; it runs on plain HTTP/1.1 so Railway/Cloudflare
work without WS tunneling; and it auto-reconnects via the browser's
`EventSource` for free.

Endpoint:
    GET /api/v1/realtime/stream   (text/event-stream)

Behaviour:
- Sends a `hello` event on connect with the resolved tenant_id.
- Sends a `heartbeat` event every 30 s so intermediate proxies don't
  drop the connection.
- If Redis is configured, subscribes to `dealix:rt:{tenant_id}` and
  forwards published events as `update` events.
- If Redis is unavailable, the heartbeat loop is sufficient — the
  stream stays open so the FE keeps an EventSource ready.
"""

from __future__ import annotations

import asyncio
import json
import os
from typing import Any, AsyncIterator

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse

from core.logging import get_logger

router = APIRouter(prefix="/api/v1/realtime", tags=["realtime"])
log = get_logger(__name__)

_HEARTBEAT_S = 30


def _format_sse(event: str, data: Any) -> bytes:
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f"event: {event}\ndata: {body}\n\n".encode("utf-8")


async def _heartbeat_only(tenant_id: str) -> AsyncIterator[bytes]:
    yield _format_sse("hello", {"tenant_id": tenant_id})
    try:
        while True:
            yield _format_sse("heartbeat", {"ts": _now_iso()})
            await asyncio.sleep(_HEARTBEAT_S)
    except asyncio.CancelledError:
        return


def _now_iso() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).isoformat()


async def _redis_subscribe(tenant_id: str) -> AsyncIterator[bytes]:
    """Try to attach to Redis pub/sub; fall back to heartbeat-only on error."""
    try:
        import redis.asyncio as redis  # type: ignore
    except Exception:
        async for chunk in _heartbeat_only(tenant_id):
            yield chunk
        return
    url = os.getenv("REDIS_URL", "").strip()
    if not url:
        async for chunk in _heartbeat_only(tenant_id):
            yield chunk
        return
    client = redis.from_url(url, decode_responses=True)
    pubsub = client.pubsub()
    channel = f"dealix:rt:{tenant_id}"
    try:
        await pubsub.subscribe(channel)
    except Exception:
        log.warning("realtime_redis_subscribe_failed", tenant=tenant_id)
        async for chunk in _heartbeat_only(tenant_id):
            yield chunk
        return

    yield _format_sse("hello", {"tenant_id": tenant_id, "transport": "redis_pubsub"})
    last_beat = asyncio.get_event_loop().time()
    try:
        while True:
            msg = await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=1.0
            )
            now = asyncio.get_event_loop().time()
            if msg:
                payload_raw = msg.get("data")
                try:
                    payload = (
                        json.loads(payload_raw)
                        if isinstance(payload_raw, str)
                        else payload_raw
                    )
                except json.JSONDecodeError:
                    payload = {"raw": payload_raw}
                yield _format_sse("update", payload)
                last_beat = now
            elif now - last_beat >= _HEARTBEAT_S:
                yield _format_sse("heartbeat", {"ts": _now_iso()})
                last_beat = now
    except asyncio.CancelledError:
        return
    finally:
        try:
            await pubsub.unsubscribe(channel)
            await pubsub.close()
            await client.aclose()
        except Exception:
            pass


@router.get("/stream")
async def realtime_stream(request: Request) -> StreamingResponse:
    """One stream per tenant. Caller is expected to be authenticated."""
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        # Allow unauthenticated probe — useful for health checks — but
        # never leak data. Use a sentinel tenant key.
        tenant_id = "anonymous"
    log.info("realtime_stream_opened", tenant_id=tenant_id)
    return StreamingResponse(
        _redis_subscribe(tenant_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache, no-transform",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
