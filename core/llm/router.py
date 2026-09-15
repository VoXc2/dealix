"""Legacy application LLM router compatibility surface.

Omega V3 moved automatic model/provider/cost/data authority to the canonical
Dealix broker and Session Factory.  This module remains import-compatible for
application code and observability, but it no longer executes model requests or
accepts caller-selected providers.  Callers must migrate to the governed
Company Operator -> Session Factory path; until then model inference fails
closed instead of silently spending or selecting a provider.
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections import deque
from dataclasses import asdict, dataclass
from typing import Any

from core.config.models import Provider, Task
from core.config.settings import Settings, get_settings
from core.llm.anthropic_client import AnthropicClient
from core.llm.base import LLMClient, LLMResponse, Message
from core.llm.gemini_client import GeminiClient
from core.llm.glm_client import GLMClient
from core.llm.model_economics import ModelUsageEvent, build_usage_event
from core.llm.openai_compat import (
    GroqClient,
    OpenAIClient,
    OpenAICompatClient,
    openai_compat_retry_count,
)

logger = logging.getLogger(__name__)


class LegacyModelAuthorityHold(RuntimeError):
    """Legacy router attempted model execution outside canonical authority."""


@dataclass
class UsageRecord:
    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    errors: int = 0
    fallbacks_triggered: int = 0


class ModelRouter:
    """Compatibility/observability router; automatic execution is disabled."""

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._clients: dict[Provider, LLMClient | None] = {}
        self.usage: dict[Provider, UsageRecord] = {p: UsageRecord() for p in Provider}
        self._usage_lock: asyncio.Lock = asyncio.Lock()
        self._provider_circuits: dict[Provider, str] = {}
        self._usage_events: deque[ModelUsageEvent] = deque(maxlen=500)
        self._build_clients()

    def _build_clients(self) -> None:
        """Build only non-DeepSeek clients for compatibility/status inspection.

        Presence of a configured client is not authority to execute it.  The
        ``run`` method below always fails closed until callers migrate to the
        canonical broker/Session Factory execution fabric.
        """

        s = self.settings
        if s.anthropic_api_key:
            self._clients[Provider.ANTHROPIC] = AnthropicClient(
                api_key=s.anthropic_api_key.get_secret_value(),
                model=s.anthropic_model,
                timeout=s.anthropic_timeout,
            )
        if s.glm_api_key:
            self._clients[Provider.GLM] = GLMClient(
                api_key=s.glm_api_key.get_secret_value(),
                model=s.glm_model,
                base_url=s.glm_base_url,
            )
        if s.google_api_key:
            self._clients[Provider.GEMINI] = GeminiClient(
                api_key=s.google_api_key.get_secret_value(),
                model=s.gemini_model,
            )
        if s.groq_api_key:
            self._clients[Provider.GROQ] = GroqClient(
                api_key=s.groq_api_key.get_secret_value(),
                model=s.groq_model,
                base_url=s.groq_base_url,
            )
        if s.openai_api_key:
            self._clients[Provider.OPENAI] = OpenAIClient(
                api_key=s.openai_api_key.get_secret_value(),
                model=s.openai_model,
                base_url=s.openai_base_url,
            )
        logger.info(
            "Legacy ModelRouter compatibility providers (execution disabled): %s",
            [p.value for p in self._clients],
        )

    def available_providers(self) -> list[Provider]:
        """Configured non-DeepSeek providers for migration/status only."""

        return list(self._clients.keys())

    def get_client(self, provider: Provider) -> LLMClient | None:
        """Compatibility accessor; DeepSeek is never exposed as an executable client."""

        if provider in {Provider.DEEPSEEK, Provider.HOLD}:
            return None
        return self._clients.get(provider)

    def circuit_status(self) -> dict[str, str]:
        return {provider.value: reason for provider, reason in self._provider_circuits.items()}

    def reset_provider_circuit(self, provider: Provider) -> None:
        self._provider_circuits.pop(provider, None)

    def recent_usage_events(self, limit: int = 50) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        rows: list[dict[str, Any]] = []
        for event in list(self._usage_events)[-limit:]:
            row = asdict(event)
            row["cost_per_accepted_result_usd"] = event.cost_per_accepted_result_usd
            rows.append(row)
        return rows

    @staticmethod
    def _retry_count(client: LLMClient) -> int:
        return openai_compat_retry_count() if isinstance(client, OpenAICompatClient) else 0

    @staticmethod
    def _cache_status(provider: Provider | None, response: LLMResponse) -> str:
        _ = provider
        return "hit" if response.cached_tokens > 0 else "unknown"

    def _record_usage_event(
        self,
        *,
        task: Task,
        requested_model: str,
        effective_model: str,
        input_tokens: int,
        output_tokens: int,
        cache_status: str,
        retries: int,
        accepted: bool,
    ) -> None:
        event = build_usage_event(
            logical_route=task.value,
            requested_model=requested_model,
            effective_model=effective_model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cache_status=cache_status,  # type: ignore[arg-type]
            retries=retries,
            accepted=accepted,
        )
        self._usage_events.append(event)
        logger.info("llm_usage_event=%s", json.dumps(asdict(event), sort_keys=True))

    async def run(
        self,
        task: Task,
        messages: list[Message] | str,
        *,
        system: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        preferred_provider: Provider | None = None,
    ) -> LLMResponse:
        """Fail closed instead of selecting any provider in the legacy router."""

        _ = messages, system, max_tokens, temperature
        if preferred_provider is not None:
            raise LegacyModelAuthorityHold(
                f"legacy_preferred_provider_rejected:{preferred_provider.value}; "
                "use canonical Session Factory/broker"
            )
        raise LegacyModelAuthorityHold(
            f"legacy_automatic_router_disabled:task={task.value}; "
            "use canonical Session Factory/broker"
        )

    def usage_summary(self) -> dict[str, Any]:
        return {
            provider.value: {
                "calls": record.calls,
                "input_tokens": record.input_tokens,
                "output_tokens": record.output_tokens,
                "total_tokens": record.input_tokens + record.output_tokens,
                "errors": record.errors,
                "fallbacks_triggered": record.fallbacks_triggered,
            }
            for provider, record in self.usage.items()
        }


_router_instance: ModelRouter | None = None


def get_router() -> ModelRouter:
    global _router_instance
    if _router_instance is None:
        _router_instance = ModelRouter()
    return _router_instance


__all__ = [
    "LegacyModelAuthorityHold",
    "UsageRecord",
    "ModelRouter",
    "get_router",
]
