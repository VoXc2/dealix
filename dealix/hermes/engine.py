"""HermesEngine — Anthropic SDK native tool-use engine.

Uses anthropic.AsyncAnthropic directly for real agentic loops with native
tool_use / tool_result blocks. Falls back to mock responses when the API
key is absent so offline tests and CI still pass.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from typing import Any

import structlog

try:
    import anthropic
    _ANTHROPIC_AVAILABLE = True
except ImportError:  # pragma: no cover
    _ANTHROPIC_AVAILABLE = False

try:
    from tenacity import retry, stop_after_attempt, wait_exponential
    _TENACITY_AVAILABLE = True
except ImportError:  # pragma: no cover
    _TENACITY_AVAILABLE = False

from dealix.hermes.config import HermesConfig, get_hermes_config

logger = structlog.get_logger(__name__)


@dataclass
class TokenUsage:
    """Accumulated token counts for a single engine run."""

    input_tokens: int = 0
    output_tokens: int = 0
    tool_rounds: int = 0

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def to_dict(self) -> dict[str, int]:
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "tool_rounds": self.tool_rounds,
        }


def build_tool_schema(
    name: str,
    description: str,
    properties: dict[str, Any],
    required: list[str],
) -> dict[str, Any]:
    """Return an Anthropic-compatible tool definition dict.

    Parameters
    ----------
    name:
        Snake_case tool identifier.
    description:
        Plain-English description of what the tool does.
    properties:
        JSON-Schema properties dict (each key maps to a type descriptor).
    required:
        List of required property names.
    """
    return {
        "name": name,
        "description": description,
        "input_schema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }


class HermesEngine:
    """Anthropic SDK native tool-use loop engine.

    When the API key is absent, all LLM calls log a warning and return
    mock data so that non-LLM functionality (tool functions, orchestration
    logic) remains testable without network access.
    """

    def __init__(self, config: HermesConfig | None = None) -> None:
        self._config = config or get_hermes_config()
        self._api_key = self._config.effective_api_key()
        self._client: Any = None
        self._usage = TokenUsage()

        if _ANTHROPIC_AVAILABLE and self._api_key:
            self._client = anthropic.AsyncAnthropic(api_key=self._api_key)
            logger.info("hermes_engine_initialized", model=self._config.hermes_model)
        else:
            logger.warning(
                "hermes_engine_no_api_key",
                hint="Set ANTHROPIC_API_KEY or HERMES_API_KEY. LLM calls will return mock data.",
            )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def run_agent_loop(
        self,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_rounds: int | None = None,
        tool_dispatcher: Any | None = None,
    ) -> tuple[str, list[dict[str, Any]]]:
        """Run the agentic tool-use loop.

        Parameters
        ----------
        system:
            System prompt string.
        messages:
            Initial messages list in Anthropic format.
        tools:
            List of tool schema dicts (from :func:`build_tool_schema`).
        max_rounds:
            Maximum number of tool-call / tool-result cycles.
        tool_dispatcher:
            Async callable ``(tool_name, tool_input) -> str``.
            If None, tools are reported as unavailable.

        Returns
        -------
        tuple[str, list]
            Final text response and the full message history.
        """
        max_rounds = max_rounds or self._config.hermes_max_tool_rounds
        self._usage = TokenUsage()
        history = list(messages)

        if self._client is None:
            return self._mock_response(system, history), history

        return await self._loop(system, history, tools, max_rounds, tool_dispatcher)

    @property
    def last_usage(self) -> TokenUsage:
        """Token usage from the most recent :meth:`run_agent_loop` call."""
        return self._usage

    # ------------------------------------------------------------------
    # Internal loop implementation
    # ------------------------------------------------------------------

    async def _loop(
        self,
        system: str,
        history: list[dict[str, Any]],
        tools: list[dict[str, Any]],
        max_rounds: int,
        tool_dispatcher: Any | None,
    ) -> tuple[str, list[dict[str, Any]]]:
        final_text = ""

        for round_num in range(1, max_rounds + 1):
            response = await self._call_api(system, history, tools)

            usage = getattr(response, "usage", None)
            if usage:
                self._usage.input_tokens += getattr(usage, "input_tokens", 0)
                self._usage.output_tokens += getattr(usage, "output_tokens", 0)

            stop_reason = getattr(response, "stop_reason", "end_turn")
            content_blocks = getattr(response, "content", [])

            # Build the assistant turn from the full content block list
            assistant_turn: dict[str, Any] = {
                "role": "assistant",
                "content": content_blocks,
            }
            history.append(assistant_turn)

            if stop_reason == "end_turn":
                # Extract final text from content blocks
                text_parts: list[str] = []
                for block in content_blocks:
                    if hasattr(block, "type") and block.type == "text":
                        text_parts.append(block.text)
                    elif isinstance(block, dict) and block.get("type") == "text":
                        text_parts.append(block.get("text", ""))
                final_text = "\n".join(text_parts).strip()
                break

            if stop_reason == "tool_use":
                self._usage.tool_rounds += 1
                tool_results: list[dict[str, Any]] = []

                for block in content_blocks:
                    block_type = (
                        block.type if hasattr(block, "type") else block.get("type")
                    )
                    if block_type != "tool_use":
                        continue

                    tool_id = block.id if hasattr(block, "id") else block.get("id", "")
                    tool_name = (
                        block.name if hasattr(block, "name") else block.get("name", "")
                    )
                    tool_input = (
                        block.input if hasattr(block, "input") else block.get("input", {})
                    )

                    logger.info(
                        "hermes_tool_call",
                        tool=tool_name,
                        round=round_num,
                    )

                    if tool_dispatcher is not None:
                        try:
                            result_str = await tool_dispatcher(tool_name, tool_input)
                        except Exception as exc:
                            result_str = json.dumps({"error": str(exc), "tool": tool_name})
                    else:
                        result_str = json.dumps({"error": "no_dispatcher", "tool": tool_name})

                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": result_str,
                        }
                    )

                history.append({"role": "user", "content": tool_results})
                continue

            # Unexpected stop_reason — treat as end_turn
            logger.warning("hermes_unexpected_stop_reason", stop_reason=stop_reason)
            break

        else:
            logger.warning("hermes_max_tool_rounds_reached", max_rounds=max_rounds)

        return final_text, history

    async def _call_api(
        self,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]],
    ) -> Any:
        """Call the Anthropic messages API with retry on transient errors."""
        create_kwargs: dict[str, Any] = {
            "model": self._config.hermes_model,
            "max_tokens": self._config.hermes_max_tokens,
            "system": system,
            "messages": messages,
        }
        if tools:
            create_kwargs["tools"] = tools

        # Inline retry logic (compatible whether tenacity is installed or not)
        last_exc: Exception | None = None
        for attempt in range(3):
            try:
                return await self._client.messages.create(**create_kwargs)
            except Exception as exc:
                last_exc = exc
                wait = 2 ** attempt
                logger.warning(
                    "hermes_api_retry",
                    attempt=attempt + 1,
                    wait_seconds=wait,
                    error=str(exc),
                )
                import asyncio
                await asyncio.sleep(wait)

        raise RuntimeError(f"Anthropic API failed after 3 attempts: {last_exc}") from last_exc

    # ------------------------------------------------------------------
    # Mock fallback
    # ------------------------------------------------------------------

    @staticmethod
    def _mock_response(system: str, history: list[dict[str, Any]]) -> str:
        """Return a deterministic mock response when no API key is configured."""
        return json.dumps(
            {
                "mock": True,
                "note": "No ANTHROPIC_API_KEY set. Configure key for real responses.",
                "system_preview": system[:80] if system else "",
                "message_count": len(history),
            }
        )


__all__ = ["HermesEngine", "TokenUsage", "build_tool_schema"]
