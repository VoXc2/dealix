"""
Dealix — LLMGateway
=====================
Wraps Groq (primary) and OpenAI (fallback) with:
  - chat(messages, model, temperature, max_tokens) → str
  - stream() async generator → AsyncIterator[str]
  - Arabic system prompts loaded from prompts/ directory
  - Function calling / tool use support

Usage:
    settings = EngagementSettings()
    llm = LLMGateway(settings=settings)

    # Simple chat
    reply = await llm.chat([{"role": "user", "content": "مرحبا"}])

    # With system prompt from library
    system = llm.get_system_prompt("whatsapp_inbound_ar")
    reply = await llm.chat([
        {"role": "system", "content": system},
        {"role": "user",   "content": "أريد معرفة الأسعار"},
    ])

    # Streaming
    async for token in llm.stream([{"role": "user", "content": "اشرح..."}]):
        print(token, end="", flush=True)

    # Function / tool calling
    tools = [{
        "type": "function",
        "function": {
            "name": "book_meeting",
            "description": "Book a sales meeting",
            "parameters": {
                "type": "object",
                "properties": {
                    "datetime_iso": {"type": "string"},
                    "lead_name": {"type": "string"},
                }
            }
        }
    }]
    response = await llm.chat_with_tools(messages, tools)
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, AsyncIterator

import httpx

from .base import EngagementSettings

logger = logging.getLogger("dealix.engagement.llm")

# Prompts directory (relative to this file)
_PROMPTS_DIR = Path(__file__).parent / "prompts"

# Groq endpoint
_GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

# OpenAI endpoint
_OPENAI_URL = "https://api.openai.com/v1/chat/completions"


class LLMGateway:
    """
    Unified LLM gateway with Groq as primary and OpenAI as fallback.

    Both providers use the OpenAI-compatible Chat Completions API format,
    so the same payload works for both.
    """

    def __init__(self, settings: EngagementSettings) -> None:
        self.settings = settings
        self._prompt_cache: dict[str, str] = {}

    # ── Public chat API ──────────────────────────────────────

    async def chat(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        temperature: float = 0.6,
        max_tokens: int = 400,
    ) -> str:
        """
        Send a chat completion request.
        Tries Groq first; falls back to OpenAI on failure.

        Returns the assistant's text content.
        """
        payload = _build_payload(
            messages=messages,
            model=model or self.settings.groq_model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        # Try Groq
        if self.settings.groq_api_key:
            try:
                return await self._call(
                    url=_GROQ_URL,
                    api_key=self.settings.groq_api_key,
                    payload=payload,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Groq failed (%s) — falling back to OpenAI", exc)

        # Fallback: OpenAI
        if self.settings.openai_api_key:
            fallback_payload = {
                **payload,
                "model": model or self.settings.openai_model,
            }
            try:
                return await self._call(
                    url=_OPENAI_URL,
                    api_key=self.settings.openai_api_key,
                    payload=fallback_payload,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("OpenAI fallback also failed: %s", exc)

        # Both failed — return a safe Arabic fallback
        logger.error("No LLM available — returning static fallback")
        return "مرحباً، شكراً لتواصلك مع Dealix. سيرد عليك مختص بأقرب وقت."

    async def stream(
        self,
        messages: list[dict[str, Any]],
        model: str | None = None,
        temperature: float = 0.6,
        max_tokens: int = 400,
    ) -> AsyncIterator[str]:
        """
        Streaming chat completion via Groq (SSE).
        Yields text tokens as they arrive.
        Falls back to non-streaming if streaming fails.
        """
        if not self.settings.groq_api_key:
            full_reply = await self.chat(messages, model, temperature, max_tokens)
            yield full_reply
            return

        payload = {
            **_build_payload(messages, model or self.settings.groq_model,
                             temperature, max_tokens),
            "stream": True,
        }
        headers = {
            "Authorization": f"Bearer {self.settings.groq_api_key}",
            "Content-Type": "application/json",
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream(
                    "POST", _GROQ_URL, json=payload, headers=headers
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line.startswith("data:"):
                            continue
                        data_str = line[len("data:"):].strip()
                        if data_str == "[DONE]":
                            return
                        try:
                            data = json.loads(data_str)
                            token = (
                                data.get("choices", [{}])[0]
                                .get("delta", {})
                                .get("content", "")
                            )
                            if token:
                                yield token
                        except json.JSONDecodeError:
                            continue
        except Exception as exc:  # noqa: BLE001
            logger.error("Streaming failed: %s — falling back to non-streaming", exc)
            full_reply = await self.chat(messages, model, temperature, max_tokens)
            yield full_reply

    async def chat_with_tools(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 600,
    ) -> dict[str, Any]:
        """
        Function calling / tool use.

        Returns the raw response dict so callers can inspect:
          - response["choices"][0]["message"]["content"]          (text)
          - response["choices"][0]["message"]["tool_calls"]       (tool calls)

        Supported tools examples:
          book_meeting — schedule a calendar slot
          save_lead_attribute — update a lead field
          qualify_lead — run BANT check
        """
        payload = {
            **_build_payload(
                messages=messages,
                model=model or self.settings.groq_model,
                temperature=temperature,
                max_tokens=max_tokens,
            ),
            "tools": tools,
            "tool_choice": "auto",
        }

        if self.settings.groq_api_key:
            try:
                return await self._call_raw(
                    url=_GROQ_URL,
                    api_key=self.settings.groq_api_key,
                    payload=payload,
                )
            except Exception as exc:  # noqa: BLE001
                logger.warning("Groq tool call failed (%s) — falling back to OpenAI", exc)

        if self.settings.openai_api_key:
            fallback_payload = {**payload, "model": model or self.settings.openai_model}
            try:
                return await self._call_raw(
                    url=_OPENAI_URL,
                    api_key=self.settings.openai_api_key,
                    payload=fallback_payload,
                )
            except Exception as exc:  # noqa: BLE001
                logger.error("OpenAI tool call fallback also failed: %s", exc)

        return {"choices": [{"message": {"content": None, "tool_calls": []}}]}

    # ── Prompt library ───────────────────────────────────────

    def get_system_prompt(self, key: str) -> str:
        """
        Load a system prompt by key from the prompts/ directory.

        Key examples:
          "system_base_ar"        → prompts/system_base_ar.md
          "whatsapp_inbound_ar"   → prompts/whatsapp_inbound_ar.md
          "qualifier_ar"          → prompts/qualifier_ar.md

        Prompts are cached in memory after first load.
        Returns an empty string if the file is not found.
        """
        if key in self._prompt_cache:
            return self._prompt_cache[key]

        path = _PROMPTS_DIR / f"{key}.md"
        if not path.exists():
            logger.warning("Prompt file not found: %s", path)
            return ""

        content = path.read_text(encoding="utf-8").strip()
        self._prompt_cache[key] = content
        return content

    def compose_prompt(self, *keys: str, separator: str = "\n\n---\n\n") -> str:
        """
        Combine multiple prompt files into one system prompt.
        Example: compose_prompt("system_base_ar", "qualifier_ar")
        """
        parts = [p for k in keys if (p := self.get_system_prompt(k))]
        return separator.join(parts)

    def list_available_prompts(self) -> list[str]:
        """Return a list of all available prompt keys."""
        return [p.stem for p in _PROMPTS_DIR.glob("*.md")]

    # ── Internal helpers ─────────────────────────────────────

    async def _call(self, url: str, api_key: str, payload: dict[str, Any]) -> str:
        """POST to an OpenAI-compatible endpoint; return content string."""
        raw = await self._call_raw(url, api_key, payload)
        return raw["choices"][0]["message"]["content"].strip()

    async def _call_raw(
        self, url: str, api_key: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        """POST to an OpenAI-compatible endpoint; return full response dict."""
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload, headers=headers)
            resp.raise_for_status()
            return resp.json()


# ─────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────

def _build_payload(
    messages: list[dict[str, Any]],
    model: str,
    temperature: float,
    max_tokens: int,
) -> dict[str, Any]:
    return {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }


# ─────────────────────────────────────────────────────────────
# Built-in tool definitions (reusable across agents)
# ─────────────────────────────────────────────────────────────

TOOL_BOOK_MEETING: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "book_meeting",
        "description": "Book a sales demo meeting with the lead",
        "parameters": {
            "type": "object",
            "properties": {
                "datetime_iso": {
                    "type": "string",
                    "description": "ISO 8601 datetime for the meeting (UTC)",
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Meeting duration in minutes",
                    "default": 30,
                },
                "notes": {
                    "type": "string",
                    "description": "Notes about what to cover",
                },
            },
            "required": ["datetime_iso"],
        },
    },
}

TOOL_SAVE_LEAD_ATTRIBUTE: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "save_lead_attribute",
        "description": "Save a key-value attribute for the current lead",
        "parameters": {
            "type": "object",
            "properties": {
                "attribute": {
                    "type": "string",
                    "description": "Attribute name (e.g. budget_sar, team_size, pain_point)",
                },
                "value": {
                    "type": "string",
                    "description": "Attribute value",
                },
            },
            "required": ["attribute", "value"],
        },
    },
}

TOOL_QUALIFY_LEAD: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "qualify_lead",
        "description": "Record a BANT qualification assessment for the lead",
        "parameters": {
            "type": "object",
            "properties": {
                "budget": {
                    "type": "string",
                    "description": "Estimated budget (e.g. '5000 SAR/month')",
                },
                "authority": {
                    "type": "string",
                    "description": "Decision maker level: 'C-level' | 'VP' | 'Manager' | 'Unknown'",
                },
                "need": {
                    "type": "string",
                    "description": "Primary pain point / need",
                },
                "timeline": {
                    "type": "string",
                    "description": "Expected purchase timeline (e.g. 'within 1 month')",
                },
                "score": {
                    "type": "integer",
                    "description": "Overall qualification score 0-100",
                },
            },
        },
    },
}

DEFAULT_SALES_TOOLS = [
    TOOL_BOOK_MEETING,
    TOOL_SAVE_LEAD_ATTRIBUTE,
    TOOL_QUALIFY_LEAD,
]
