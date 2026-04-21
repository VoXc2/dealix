"""
Anthropic Claude client.
عميل Claude.
"""

from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from core.llm.base import LLMClient, LLMResponse, Message


class AnthropicClient(LLMClient):
    """Anthropic Claude API client."""

    provider_name = "anthropic"
    API_URL = "https://api.anthropic.com/v1/messages"
    API_VERSION = "2023-06-01"

    def __init__(
        self,
        api_key: str,
        model: str = "claude-sonnet-4-5-20250929",
        base_url: str | None = None,
        timeout: int = 60,
    ) -> None:
        super().__init__(api_key=api_key, model=model, base_url=base_url, timeout=timeout)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((httpx.TimeoutException, httpx.HTTPStatusError)),
        reraise=True,
    )
    async def chat(
        self,
        messages: list[Message],
        *,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        system: str | None = None,
        **kwargs: Any,
    ) -> LLMResponse:
        """Send chat completion to Anthropic API."""
        # Separate system from messages (Anthropic API convention)
        clean_messages: list[dict[str, str]] = []
        extracted_system: str | None = system

        for msg in messages:
            if msg.role == "system" and extracted_system is None:
                extracted_system = msg.content
            else:
                clean_messages.append(msg.to_dict())

        payload: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": clean_messages,
        }
        if extracted_system:
            payload["system"] = extracted_system

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": self.API_VERSION,
            "content-type": "application/json",
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(self.API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        # Extract text from content blocks
        content_blocks = data.get("content", [])
        text = "".join(
            block.get("text", "") for block in content_blocks if block.get("type") == "text"
        )

        usage = data.get("usage", {})
        return LLMResponse(
            content=text,
            provider=self.provider_name,
            model=data.get("model", self.model),
            input_tokens=usage.get("input_tokens", 0),
            output_tokens=usage.get("output_tokens", 0),
            finish_reason=data.get("stop_reason"),
            raw=data,
        )
