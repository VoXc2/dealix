"""
Ollama Client — async chat/generate with retries, timeouts, and streaming.

Talks to an Ollama daemon (default http://localhost:11434) using Ollama's
native /api/chat endpoint. Ollama also exposes an OpenAI-compatible /v1
surface, but the native endpoint gives us better streaming primitives and
always-on model management. The client is intentionally dependency-free
beyond httpx — the same httpx version the rest of the backend already uses.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
import time
from dataclasses import dataclass, field
from typing import AsyncIterator, Optional

import httpx

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = os.environ.get("LOCAL_LLM_BASE_URL", "http://localhost:11434")
DEFAULT_TIMEOUT_S = float(os.environ.get("LOCAL_LLM_TIMEOUT_S", "120"))
DEFAULT_RETRIES = int(os.environ.get("LOCAL_LLM_RETRIES", "2"))


@dataclass
class OllamaChatResult:
    model: str
    content: str
    latency_ms: int
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    success: bool = True
    error: Optional[str] = None
    raw: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "model": self.model,
            "content": self.content,
            "latency_ms": self.latency_ms,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "success": self.success,
            "error": self.error,
        }


class OllamaClient:
    """Async client for a single Ollama daemon."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        timeout_s: float = DEFAULT_TIMEOUT_S,
        retries: int = DEFAULT_RETRIES,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout_s = timeout_s
        self.retries = max(0, retries)
        self._healthy: Optional[bool] = None
        self._last_check: float = 0.0

    # ── lifecycle ────────────────────────────────────────────────

    async def health(self, force: bool = False) -> bool:
        """Return True if the daemon responds. Caches for 30 s."""
        now = time.time()
        if not force and self._healthy is not None and now - self._last_check < 30:
            return self._healthy
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                self._healthy = resp.status_code == 200
        except Exception as e:
            logger.debug("Ollama health check failed at %s: %s", self.base_url, e)
            self._healthy = False
        self._last_check = now
        return self._healthy

    async def list_models(self) -> list[dict]:
        """Return `/api/tags` models array (may be empty)."""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                resp.raise_for_status()
                return resp.json().get("models", []) or []
        except Exception as e:
            logger.warning("Ollama list_models failed: %s", e)
            return []

    async def has_model(self, tag: str) -> bool:
        """Check if an exact model tag is available locally."""
        models = await self.list_models()
        for m in models:
            name = m.get("name") or m.get("model") or ""
            if name == tag or name.startswith(f"{tag}:"):
                return True
        return False

    # ── chat ─────────────────────────────────────────────────────

    async def chat(
        self,
        model: str,
        messages: list[dict],
        *,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
        system: Optional[str] = None,
        stop: Optional[list[str]] = None,
    ) -> OllamaChatResult:
        """
        Non-streaming chat completion. Retries on network/5xx errors.
        Falls back to a typed error result rather than raising.
        """
        payload_messages = list(messages)
        if system:
            payload_messages = [{"role": "system", "content": system}] + payload_messages

        options = {"temperature": temperature}
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        if stop:
            options["stop"] = stop

        body = {
            "model": model,
            "messages": payload_messages,
            "stream": False,
            "options": options,
        }
        if json_mode:
            body["format"] = "json"

        start = time.time()
        last_error: Optional[str] = None

        for attempt in range(self.retries + 1):
            try:
                async with httpx.AsyncClient(timeout=self.timeout_s) as client:
                    resp = await client.post(f"{self.base_url}/api/chat", json=body)
                    resp.raise_for_status()
                    data = resp.json()
                latency_ms = int((time.time() - start) * 1000)
                content = data.get("message", {}).get("content", "")
                return OllamaChatResult(
                    model=model,
                    content=content,
                    latency_ms=latency_ms,
                    prompt_tokens=data.get("prompt_eval_count", 0) or 0,
                    completion_tokens=data.get("eval_count", 0) or 0,
                    total_tokens=(data.get("prompt_eval_count", 0) or 0)
                    + (data.get("eval_count", 0) or 0),
                    raw=data,
                )
            except httpx.HTTPStatusError as e:
                last_error = f"HTTP {e.response.status_code}: {e.response.text[:200]}"
                # 4xx → do not retry (likely missing model / bad request)
                if 400 <= e.response.status_code < 500:
                    break
            except (httpx.TimeoutException, httpx.TransportError) as e:
                last_error = f"{type(e).__name__}: {e}"
            except Exception as e:
                last_error = f"{type(e).__name__}: {e}"

            if attempt < self.retries:
                backoff = 0.75 * (2 ** attempt)
                logger.info(
                    "Ollama chat retry %d/%d after %.1fs: %s",
                    attempt + 1, self.retries, backoff, last_error,
                )
                await asyncio.sleep(backoff)

        latency_ms = int((time.time() - start) * 1000)
        self._healthy = False
        return OllamaChatResult(
            model=model,
            content="",
            latency_ms=latency_ms,
            success=False,
            error=last_error or "unknown error",
        )

    async def chat_stream(
        self,
        model: str,
        messages: list[dict],
        *,
        temperature: float = 0.3,
        max_tokens: Optional[int] = None,
        system: Optional[str] = None,
    ) -> AsyncIterator[str]:
        """
        Stream tokens as they arrive. Yields text deltas (empty on done).
        Caller is responsible for handling errors — exceptions propagate.
        """
        payload_messages = list(messages)
        if system:
            payload_messages = [{"role": "system", "content": system}] + payload_messages

        options = {"temperature": temperature}
        if max_tokens is not None:
            options["num_predict"] = max_tokens

        body = {
            "model": model,
            "messages": payload_messages,
            "stream": True,
            "options": options,
        }

        async with httpx.AsyncClient(timeout=self.timeout_s) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=body) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    delta = obj.get("message", {}).get("content", "")
                    if delta:
                        yield delta
                    if obj.get("done"):
                        return

    # ── pull ─────────────────────────────────────────────────────

    async def pull_model(self, tag: str, timeout_s: float = 1800.0) -> bool:
        """
        Trigger `ollama pull` over HTTP. Long-running; default 30 min timeout.
        Returns True on success.
        """
        try:
            async with httpx.AsyncClient(timeout=timeout_s) as client:
                async with client.stream(
                    "POST", f"{self.base_url}/api/pull",
                    json={"name": tag, "stream": True},
                ) as resp:
                    resp.raise_for_status()
                    async for line in resp.aiter_lines():
                        if not line:
                            continue
                        try:
                            obj = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        status = obj.get("status", "")
                        if status == "success":
                            return True
                        if "error" in obj:
                            logger.warning("Ollama pull error for %s: %s", tag, obj["error"])
                            return False
            return True
        except Exception as e:
            logger.warning("Ollama pull_model(%s) failed: %s", tag, e)
            return False


# ── Module-level singleton ──────────────────────────────────────────

_client: Optional[OllamaClient] = None


def get_local_client() -> OllamaClient:
    global _client
    if _client is None:
        _client = OllamaClient()
    return _client
