"""MiniMax LLM provider — OpenAI-compatible, used for high-volume daily tasks."""
from __future__ import annotations
import json, os
from typing import Any
import structlog

logger = structlog.get_logger(__name__)

_MINIMAX_BASE_URL = "https://api.minimaxi.chat/v1"
_DEFAULT_MODEL = "MiniMax-Text-01"


class MiniMaxProvider:
    """Async OpenAI-compatible client pointing at MiniMax's API."""

    def __init__(self, api_key: str = "", model: str = _DEFAULT_MODEL, base_url: str = _MINIMAX_BASE_URL) -> None:
        self._api_key = api_key or os.environ.get("MINIMAX_API_KEY", "")
        self._model = model
        self._base_url = base_url
        self._client: Any = None

        if self._api_key:
            try:
                import openai
                self._client = openai.AsyncOpenAI(api_key=self._api_key, base_url=self._base_url)
                logger.info("minimax_provider_initialized", model=self._model)
            except ImportError:
                logger.warning("minimax_provider_openai_missing", hint="pip install openai")
        else:
            logger.warning("minimax_provider_no_api_key", hint="Set MINIMAX_API_KEY")

    async def chat(
        self,
        system: str,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int = 4096,
    ) -> dict[str, Any]:
        """Send a chat completion request. Returns {text, tool_calls, usage}."""
        if not self._client:
            return self._mock_response(system, messages)

        # Convert messages: prepend system as first user/system message
        oai_messages = [{"role": "system", "content": system}] + messages

        kwargs: dict[str, Any] = {
            "model": self._model,
            "messages": oai_messages,
            "max_tokens": max_tokens,
        }
        # Convert Anthropic tool schema -> OpenAI function schema
        if tools:
            kwargs["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": t["name"],
                        "description": t["description"],
                        "parameters": t["input_schema"],
                    },
                }
                for t in tools
            ]

        try:
            resp = await self._client.chat.completions.create(**kwargs)
            msg = resp.choices[0].message
            text = msg.content or ""
            tool_calls = []
            if msg.tool_calls:
                for tc in msg.tool_calls:
                    tool_calls.append({
                        "id": tc.id,
                        "name": tc.function.name,
                        "input": json.loads(tc.function.arguments),
                    })
            usage = {"input_tokens": resp.usage.prompt_tokens, "output_tokens": resp.usage.completion_tokens}
            logger.info("minimax_chat_complete", model=self._model, tokens=resp.usage.total_tokens)
            return {"text": text, "tool_calls": tool_calls, "usage": usage}
        except Exception as exc:
            logger.error("minimax_chat_error", error=str(exc))
            return {"text": "", "tool_calls": [], "usage": {}, "error": str(exc)}

    async def run_agentic_loop(
        self,
        system: str,
        user_msg: str,
        tools: list[dict[str, Any]],
        tool_dispatcher: Any,
        max_rounds: int = 10,
    ) -> tuple[str, dict[str, Any]]:
        """Run a full tool-use agentic loop. Returns (final_text, usage_dict)."""
        messages = [{"role": "user", "content": user_msg}]
        total_usage = {"input_tokens": 0, "output_tokens": 0}

        for _ in range(max_rounds):
            result = await self.chat(system=system, messages=messages, tools=tools)
            # accumulate usage
            total_usage["input_tokens"] += result.get("usage", {}).get("input_tokens", 0)
            total_usage["output_tokens"] += result.get("usage", {}).get("output_tokens", 0)

            if result.get("tool_calls"):
                # add assistant turn
                messages.append({"role": "assistant", "content": result.get("text") or "", "tool_calls": [
                    {"id": tc["id"], "type": "function", "function": {"name": tc["name"], "arguments": json.dumps(tc["input"])}}
                    for tc in result["tool_calls"]
                ]})
                # dispatch each tool call and add results
                tool_results = []
                for tc in result["tool_calls"]:
                    try:
                        res = await tool_dispatcher(tc["name"], tc["input"])
                    except Exception as exc:
                        res = json.dumps({"error": str(exc)})
                    tool_results.append({"role": "tool", "tool_call_id": tc["id"], "content": res})
                messages.extend(tool_results)
            else:
                # no tool calls -> done
                total_usage["total_tokens"] = total_usage["input_tokens"] + total_usage["output_tokens"]
                return result.get("text", ""), total_usage

        return "", total_usage

    @staticmethod
    def _mock_response(system: str, messages: list) -> dict[str, Any]:
        return {
            "text": json.dumps({"mock": True, "note": "No MINIMAX_API_KEY set.", "system_preview": system[:80]}),
            "tool_calls": [],
            "usage": {"input_tokens": 0, "output_tokens": 0},
        }

    @property
    def is_available(self) -> bool:
        return self._client is not None


__all__ = ["MiniMaxProvider"]
