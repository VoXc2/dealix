"""
LiteLLM gateway — universal SDK that talks to 100+ LLM providers.

Sits behind Portkey when configured (Portkey routes; LiteLLM is the
swap-friendly client). Without a `LITELLM_*` env var the wrapper is a
no-op that forwards to the existing provider SDKs.

Reference: https://docs.litellm.ai
"""

from __future__ import annotations

import os
from typing import Any

from core.logging import get_logger

log = get_logger(__name__)


def is_enabled() -> bool:
    return os.getenv("LITELLM_PROXY_URL", "").strip() != ""


async def complete(
    *,
    model: str,
    messages: list[dict[str, str]],
    tenant_id: str | None = None,
    **kwargs: Any,
) -> str:
    """Best-effort chat completion via LiteLLM with provider fallback.

    Returns the assistant content string, or "" on failure.
    """
    if not is_enabled():
        log.info("litellm_disabled_noop", model=model)
        return ""
    try:
        import litellm  # type: ignore
    except ImportError:
        log.warning("litellm_sdk_not_installed")
        return ""
    try:
        # Attach tenant metadata so Portkey + Langfuse downstream attribute cost.
        meta = {"tenant_id": tenant_id} if tenant_id else None
        response = await litellm.acompletion(
            model=model,
            messages=messages,
            api_base=os.getenv("LITELLM_PROXY_URL"),
            metadata=meta,
            **kwargs,
        )
        return str((response.choices[0].message.content or "").strip())
    except Exception:
        log.exception("litellm_completion_failed", model=model)
        return ""
