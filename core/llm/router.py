"""
Model Router — intelligently routes tasks to LLM providers with fallback.
مُوجّه النماذج — يرسل كل مهمة لأفضل مزود مع احتياط عند الفشل.

v2: asyncio.Lock added to usage counters to prevent data races in
concurrent async tasks (multiple coroutines hitting the same router
simultaneously could produce corrupted token/call counts).
"""

from __future__ import annotations

import asyncio
import json
import logging
from collections import deque
from dataclasses import asdict, dataclass
from typing import Any

from core.config.models import (
    FALLBACK_CHAIN,
    TASK_ROUTING,
    Provider,
    Task,
)
from core.config.settings import Settings, get_settings
from core.llm.anthropic_client import AnthropicClient
from core.llm.base import LLMClient, LLMResponse, Message
from core.llm.gemini_client import GeminiClient
from core.llm.glm_client import GLMClient
from core.llm.model_economics import ModelUsageEvent, build_usage_event
from core.llm.openai_compat import (
    DeepSeekClient,
    GroqClient,
    OllamaCompatClient,
    OpenAIClient,
    OpenAICompatClient,
    is_http_402_error,
    openai_compat_retry_count,
    reset_openai_compat_retry_count,
)

logger = logging.getLogger(__name__)


@dataclass
class UsageRecord:
    """Tracks calls/tokens per provider | يتتبع الاستدعاءات والرموز لكل مزود."""

    calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    errors: int = 0
    fallbacks_triggered: int = 0


class ModelRouter:
    """
    Routes a Task to the appropriate LLM client with fallback chain.
    يوجّه المهمة إلى عميل النموذج المناسب مع سلسلة احتياط.

    Thread safety: all mutations to usage counters are protected by an
    asyncio.Lock so concurrent coroutines don't race on shared state.
    """

    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._clients: dict[Provider, LLMClient | None] = {}
        self.usage: dict[Provider, UsageRecord] = {p: UsageRecord() for p in Provider}
        # asyncio.Lock — protects usage counter mutations under concurrency
        self._usage_lock: asyncio.Lock = asyncio.Lock()
        self._provider_circuits: dict[Provider, str] = {}
        self._usage_events: deque[ModelUsageEvent] = deque(maxlen=500)
        self._deepseek_local_fallback: LLMClient | None = None
        self._build_clients()
        self._build_deepseek_local_fallback()

    # ── Client construction ─────────────────────────────────────
    def _build_clients(self) -> None:
        """Instantiate clients only for providers that have API keys set."""
        s = self.settings

        if s.anthropic_api_key:
            self._clients[Provider.ANTHROPIC] = AnthropicClient(
                api_key=s.anthropic_api_key.get_secret_value(),
                model=s.anthropic_model,
                timeout=s.anthropic_timeout,
            )

        if s.deepseek_api_key:
            self._clients[Provider.DEEPSEEK] = DeepSeekClient(
                api_key=s.deepseek_api_key.get_secret_value(),
                model=s.deepseek_model,
                base_url=s.deepseek_base_url,
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

        configured = [p.value for p in self._clients]
        logger.info("ModelRouter initialized with providers: %s", configured)

    def _build_deepseek_local_fallback(self) -> None:
        """Prepare an opt-in loopback Ollama fallback for DeepSeek billing failures."""
        s = self.settings
        if getattr(s, "deepseek_402_ollama_fallback_enabled", False) is not True:
            return
        try:
            self._deepseek_local_fallback = OllamaCompatClient(
                model=str(s.deepseek_ollama_model),
                base_url=str(s.deepseek_ollama_base_url),
                timeout=int(s.deepseek_ollama_timeout),
            )
        except (TypeError, ValueError):
            self._deepseek_local_fallback = None
            logger.error("DeepSeek 402 local fallback disabled: invalid or non-loopback config")

    # ── Public API ──────────────────────────────────────────────
    def available_providers(self) -> list[Provider]:
        """List providers that are actually configured."""
        return list(self._clients.keys())

    def get_client(self, provider: Provider) -> LLMClient | None:
        return self._clients.get(provider)

    def circuit_status(self) -> dict[str, str]:
        """Return only provider/reason circuit state; never credentials."""
        return {provider.value: reason for provider, reason in self._provider_circuits.items()}

    def reset_provider_circuit(self, provider: Provider) -> None:
        """Explicit in-process reset after the underlying provider condition is repaired."""
        self._provider_circuits.pop(provider, None)

    def recent_usage_events(self, limit: int = 50) -> list[dict[str, Any]]:
        if limit <= 0:
            return []
        events = list(self._usage_events)[-limit:]
        rows: list[dict[str, Any]] = []
        for event in events:
            row = asdict(event)
            row["cost_per_accepted_result_usd"] = event.cost_per_accepted_result_usd
            rows.append(row)
        return rows

    @staticmethod
    def _retry_count(client: LLMClient) -> int:
        return openai_compat_retry_count() if isinstance(client, OpenAICompatClient) else 0

    @staticmethod
    def _cache_status(provider: Provider | None, response: LLMResponse) -> str:
        if provider == Provider.DEEPSEEK:
            usage = response.raw.get("usage", {}) if isinstance(response.raw, dict) else {}
            if int(usage.get("prompt_cache_hit_tokens", 0) or 0) > 0:
                return "hit"
            if int(usage.get("prompt_cache_miss_tokens", 0) or 0) > 0:
                return "miss"
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

    async def _try_deepseek_local_fallback(
        self,
        *,
        task: Task,
        messages: list[Message],
        system: str | None,
        max_tokens: int,
        temperature: float,
        requested_model: str,
    ) -> LLMResponse | None:
        client = self._deepseek_local_fallback
        if client is None:
            return None
        async with self._usage_lock:
            self.usage[Provider.DEEPSEEK].fallbacks_triggered += 1
        try:
            if isinstance(client, OpenAICompatClient):
                reset_openai_compat_retry_count()
            response = await client.chat(
                messages=messages,
                system=system,
                max_tokens=max_tokens,
                temperature=temperature,
            )
        except Exception as exc:
            self._record_usage_event(
                task=task,
                requested_model=requested_model,
                effective_model=str(getattr(client, "model", "ollama_local")),
                input_tokens=0,
                output_tokens=0,
                cache_status="unknown",
                retries=self._retry_count(client),
                accepted=False,
            )
            logger.warning(
                "DeepSeek 402 local fallback failed task=%s error_type=%s",
                task.value,
                type(exc).__name__,
            )
            return None
        self._record_usage_event(
            task=task,
            requested_model=requested_model,
            effective_model=response.model,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            cache_status=self._cache_status(None, response),
            retries=self._retry_count(client),
            accepted=True,
        )
        logger.warning("DeepSeek circuit served by loopback Ollama task=%s", task.value)
        return response

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
        """
        Execute a task through the routing + fallback chain.
        نفّذ المهمة عبر سلسلة التوجيه والاحتياط.

        Usage counters are mutated under asyncio.Lock to prevent races
        when multiple coroutines share the same router instance.
        """
        # Normalize input
        if isinstance(messages, str):
            messages = [Message(role="user", content=messages)]

        primary = preferred_provider or TASK_ROUTING.get(task, Provider.ANTHROPIC)
        chain = [primary] + [p for p in FALLBACK_CHAIN.get(primary, []) if p != primary]

        last_error: Exception | None = None
        for idx, provider in enumerate(chain):
            client = self._clients.get(provider)
            requested_model = str(getattr(client, "model", provider.value))

            if provider in self._provider_circuits:
                logger.warning(
                    "Skipping provider=%s open_circuit=%s",
                    provider.value,
                    self._provider_circuits[provider],
                )
                if provider == Provider.DEEPSEEK:
                    local_response = await self._try_deepseek_local_fallback(
                        task=task,
                        messages=messages,
                        system=system,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        requested_model=requested_model,
                    )
                    if local_response is not None:
                        return local_response
                continue

            if client is None:
                logger.debug("Skipping unconfigured provider: %s", provider)
                continue

            try:
                # ── Increment call counter (thread-safe) ──────────
                async with self._usage_lock:
                    self.usage[provider].calls += 1
                    if idx > 0:
                        self.usage[primary].fallbacks_triggered += 1

                if idx > 0:
                    logger.warning(
                        "Task=%s fallback to provider=%s (primary=%s)",
                        task.value,
                        provider.value,
                        primary.value,
                    )

                if isinstance(client, OpenAICompatClient):
                    reset_openai_compat_retry_count()
                response = await client.chat(
                    messages=messages,
                    system=system,
                    max_tokens=max_tokens,
                    temperature=temperature,
                )

                # ── Accumulate token counts (thread-safe) ─────────
                async with self._usage_lock:
                    self.usage[provider].input_tokens += response.input_tokens
                    self.usage[provider].output_tokens += response.output_tokens

                self._record_usage_event(
                    task=task,
                    requested_model=requested_model,
                    effective_model=response.model,
                    input_tokens=response.input_tokens,
                    output_tokens=response.output_tokens,
                    cache_status=self._cache_status(provider, response),
                    retries=self._retry_count(client),
                    accepted=True,
                )
                return response

            except Exception as e:
                async with self._usage_lock:
                    self.usage[provider].errors += 1
                last_error = e
                if provider == Provider.DEEPSEEK and is_http_402_error(e):
                    self._provider_circuits[Provider.DEEPSEEK] = "billing_402"
                    self._record_usage_event(
                        task=task,
                        requested_model=requested_model,
                        effective_model=requested_model,
                        input_tokens=0,
                        output_tokens=0,
                        cache_status="unknown",
                        retries=self._retry_count(client),
                        accepted=False,
                    )
                    logger.warning("DeepSeek billing circuit opened task=%s", task.value)
                    local_response = await self._try_deepseek_local_fallback(
                        task=task,
                        messages=messages,
                        system=system,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        requested_model=requested_model,
                    )
                    if local_response is not None:
                        return local_response
                    continue
                logger.exception(
                    "Provider=%s failed for task=%s: %s", provider.value, task.value, e
                )
                continue

        raise RuntimeError(f"All providers failed for task {task.value}. Last error: {last_error}")

    def usage_summary(self) -> dict[str, Any]:
        """Human-readable usage summary."""
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


# ── Singleton ───────────────────────────────────────────────────
_router_instance: ModelRouter | None = None


def get_router() -> ModelRouter:
    """Global router singleton."""
    global _router_instance
    if _router_instance is None:
        _router_instance = ModelRouter()
    return _router_instance
