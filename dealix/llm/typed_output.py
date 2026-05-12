"""
Typed-output adapter — Instructor / Outlines style.

For new agents that return structured data, callers prefer typed
Pydantic responses over the JSON-as-string approach in
core/llm/guardrails. This module exposes a small adapter that picks
the available backend (Instructor → Outlines → naive json.loads).

Usage:
    from pydantic import BaseModel
    from dealix.llm.typed_output import typed_complete

    class Proposal(BaseModel):
        subject: str
        body_ar: str
        next_steps: list[str]

    result = await typed_complete(
        model="claude-3-5-sonnet-latest",
        messages=[...],
        response_model=Proposal,
    )
"""

from __future__ import annotations

import json
from typing import Any, TypeVar

from pydantic import BaseModel

from core.logging import get_logger

log = get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


async def typed_complete(
    *,
    model: str,
    messages: list[dict[str, str]],
    response_model: type[T],
    tenant_id: str | None = None,
    **kwargs: Any,
) -> T | None:
    """Return an instance of `response_model` or None on failure."""
    try:
        import instructor  # type: ignore
        from anthropic import AsyncAnthropic  # type: ignore
    except ImportError:
        return await _naive_json_path(model, messages, response_model, tenant_id, **kwargs)
    try:
        client = instructor.from_anthropic(AsyncAnthropic())
        result = await client.messages.create(
            model=model,
            messages=messages,
            response_model=response_model,
            max_tokens=kwargs.get("max_tokens", 1024),
        )
        return result  # type: ignore[return-value]
    except Exception:
        log.exception("instructor_path_failed", model=model)
        return await _naive_json_path(model, messages, response_model, tenant_id, **kwargs)


async def _naive_json_path(
    model: str,
    messages: list[dict[str, str]],
    response_model: type[T],
    tenant_id: str | None,
    **kwargs: Any,
) -> T | None:
    """Fall back to LiteLLM + json.loads."""
    from dealix.llm.litellm_gateway import complete

    text = await complete(
        model=model, messages=messages, tenant_id=tenant_id, **kwargs
    )
    if not text:
        return None
    try:
        return response_model.model_validate_json(text)
    except Exception:
        try:
            return response_model.model_validate(json.loads(text))
        except Exception:
            log.warning(
                "typed_output_parse_failed",
                model=model,
                response_model=response_model.__name__,
            )
            return None
