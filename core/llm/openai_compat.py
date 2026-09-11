"""
OpenAI-compatible API client — used for DeepSeek, Groq, OpenAI.
عميل متوافق مع OpenAI — يُستخدم لـ DeepSeek و Groq و OpenAI.
"""

from __future__ import annotations

from contextvars import ContextVar
from typing import Any

import httpx
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from core.llm.base import LLMClient, LLMResponse, Message

LOCAL_OLLAMA_TIMEOUT_SECONDS = 180


def _is_local_ollama_base_url(base_url: str) -> bool:
    """Return True only for the loopback Ollama OpenAI-compatible endpoint."""

    normalized = base_url.strip().casefold().rstrip("/")
    return normalized in {
        "http://127.0.0.1:11434/v1",
        "http://localhost:11434/v1",
        "http://[::1]:11434/v1",
    }


def _requests_json_only(system: str | None) -> bool:
    """Detect an explicit JSON-only response contract without broad heuristics."""

    if not system:
        return False
    normalized = system.casefold()
    return (
        ("أخرج json صحيح" in normalized and "فقط" in normalized)
        or "valid json only" in normalized
        or "json only" in normalized
    )


def is_http_402_error(exc: BaseException) -> bool:
    return isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 402


_retry_attempt: ContextVar[int] = ContextVar("openai_compat_retry_attempt", default=1)


def _record_retry_attempt(retry_state: Any) -> None:
    _retry_attempt.set(max(1, int(retry_state.attempt_number)))


def reset_openai_compat_retry_count() -> None:
    _retry_attempt.set(1)


def openai_compat_retry_count() -> int:
    """Retries performed by the most recent compatible-client call in this async context."""
    return max(0, _retry_attempt.get() - 1)


def _retryable_openai_compat_error(exc: BaseException) -> bool:
    """Retry transient transport/server errors, never billing/auth/client errors.

    In particular HTTP 402 must fail immediately so the router can open its
    provider circuit/fallback path instead of spending time on doomed retries.
    """
    if isinstance(exc, httpx.TimeoutException):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        return exc.response.status_code in {408, 409, 429} or exc.response.status_code >= 500
    return False


class OpenAICompatClient(LLMClient):
    """Base OpenAI-compatible client (chat/completions endpoint)."""

    provider_name = "openai_compat"

    def __init__(
        self,
        api_key: str,
        model: str,
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 60,
    ) -> None:
        # CPU-only loopback inference can legitimately exceed the remote-API
        # default while still being healthy. Keep the larger budget scoped only
        # to the exact local Ollama endpoints and only when the caller left the
        # generic 60-second default unchanged. Explicit caller timeouts win.
        effective_timeout = (
            LOCAL_OLLAMA_TIMEOUT_SECONDS
            if timeout == 60 and _is_local_ollama_base_url(base_url)
            else timeout
        )
        super().__init__(
            api_key=api_key,
            model=model,
            base_url=base_url,
            timeout=effective_timeout,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception(_retryable_openai_compat_error),
        before=_record_retry_attempt,
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
        """Send chat completion via OpenAI-compatible endpoint."""
        full_messages: list[dict[str, str]] = []
        if system:
            full_messages.append({"role": "system", "content": system})
        full_messages.extend(m.to_dict() for m in messages)

        payload: dict[str, Any] = {
            "model": self.model,
            "messages": full_messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }

        # Structured-output overrides are deliberately scoped to loopback
        # Ollama. Remote OpenAI-compatible providers keep their existing
        # behavior until each provider is explicitly qualified.
        if _is_local_ollama_base_url(self.base_url):
            explicit_format = kwargs.get("response_format")
            if isinstance(explicit_format, dict):
                payload["response_format"] = explicit_format
            elif _requests_json_only(system):
                payload["response_format"] = {"type": "json_object"}

            if "response_format" in payload:
                payload["reasoning_effort"] = str(
                    kwargs.get("reasoning_effort") or "none"
                )

            seed = kwargs.get("seed")
            if isinstance(seed, int):
                payload["seed"] = seed

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        url = f"{self.base_url}/chat/completions"

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()

        choices = data.get("choices", [])
        if not choices:
            raise RuntimeError(f"No choices returned from {self.provider_name}")

        first_choice = choices[0]
        message = first_choice.get("message", {})
        content = message.get("content", "") or ""

        usage = data.get("usage", {})
        return LLMResponse(
            content=content,
            provider=self.provider_name,
            model=data.get("model", self.model),
            input_tokens=usage.get("prompt_tokens", 0),
            output_tokens=usage.get("completion_tokens", 0),
            cached_tokens=usage.get("prompt_cache_hit_tokens", 0),
            finish_reason=first_choice.get("finish_reason"),
            raw=data,
        )


class DeepSeekClient(OpenAICompatClient):
    """DeepSeek client (OpenAI-compatible)."""

    provider_name = "deepseek"

    def __init__(
        self,
        api_key: str,
        model: str = "deepseek-chat",
        base_url: str = "https://api.deepseek.com/v1",
        timeout: int = 60,
    ) -> None:
        super().__init__(api_key=api_key, model=model, base_url=base_url, timeout=timeout)


class GroqClient(OpenAICompatClient):
    """Groq client (OpenAI-compatible) — runs Llama 3.3 70B, ultra-fast."""

    provider_name = "groq"

    def __init__(
        self,
        api_key: str,
        model: str = "llama-3.3-70b-versatile",
        base_url: str = "https://api.groq.com/openai/v1",
        timeout: int = 60,
    ) -> None:
        super().__init__(api_key=api_key, model=model, base_url=base_url, timeout=timeout)


class OllamaCompatClient(OpenAICompatClient):
    """Loopback Ollama client for DeepSeek 402 fallback."""

    provider_name = "ollama_local"

    def __init__(
        self,
        model: str,
        base_url: str = "http://127.0.0.1:11434/v1",
        timeout: int = 60,
    ) -> None:
        if not _is_local_ollama_base_url(base_url):
            raise ValueError("Ollama fallback must use an exact loopback base URL")
        super().__init__(api_key="ollama-local", model=model, base_url=base_url, timeout=timeout)


class OpenAIClient(OpenAICompatClient):
    """OpenAI client (fallback)."""

    provider_name = "openai"

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        base_url: str = "https://api.openai.com/v1",
        timeout: int = 60,
    ) -> None:
        super().__init__(api_key=api_key, model=model, base_url=base_url, timeout=timeout)