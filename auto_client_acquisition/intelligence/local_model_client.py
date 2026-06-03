"""Dealix Intelligence — Local Model Client (Ollama / vLLM adapter).

Thin HTTP client for local LLM servers. Supports two backends:
- **Ollama** (default) — http://localhost:11434/api/generate
- **vLLM**   — OpenAI-compatible: http://localhost:8000/v1/chat/completions

Hard rules (Article 4 + Article 8):
- Graceful degradation when local server is unreachable: return
  ``LocalModelUnavailable`` rather than raising — caller decides
  whether to fall back to cloud or human.
- NEVER print or log secrets / API keys / customer PII.
- NEVER auto-retry indefinitely (caps retries at 1; total wall-time
  bounded by ``timeout_seconds`` parameter).
- Default ``timeout_seconds=10`` — long enough for real classification,
  short enough to fail-fast in CI/sandbox.

Designed to be import-safe (no network call at import time).
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Literal

import httpx

LocalProvider = Literal["ollama", "vllm", "none"]


@dataclass(frozen=True, slots=True)
class LocalModelResponse:
    """Successful local-model response."""

    text: str
    model: str
    backend: LocalProvider
    latency_ms: int
    estimated_input_tokens: int
    estimated_output_tokens: int
    raw_json: dict[str, Any]


@dataclass(frozen=True, slots=True)
class LocalModelUnavailable:
    """Signal that local server isn't reachable / not configured.

    Caller (model_router) decides next step:
    - cloud_fallback (if cloud creds available + privacy allows)
    - human_handoff (if task.fallback_to_human=True)
    - skip          (if task is best-effort)
    """

    reason: str
    backend_attempted: LocalProvider
    base_url: str


def _detect_provider() -> tuple[LocalProvider, str]:
    """Read env vars to determine which local backend to use.

    Order: explicit LOCAL_LLM_PROVIDER → presence of OLLAMA_BASE_URL →
    presence of VLLM_BASE_URL → none.

    Returns ``(provider, base_url)``. ``provider="none"`` when nothing
    is configured.
    """
    explicit = os.environ.get("LOCAL_LLM_PROVIDER", "").strip().lower()
    if explicit == "ollama":
        return ("ollama", os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434"))
    if explicit == "vllm":
        return ("vllm", os.environ.get("VLLM_BASE_URL", "http://localhost:8000/v1"))
    if explicit in ("none", "off", "disabled"):
        return ("none", "")
    # Auto-detect via env vars
    if os.environ.get("OLLAMA_BASE_URL"):
        return ("ollama", os.environ["OLLAMA_BASE_URL"])
    if os.environ.get("VLLM_BASE_URL"):
        return ("vllm", os.environ["VLLM_BASE_URL"])
    # Default: try Ollama at localhost (only when caller explicitly invokes)
    return ("ollama", "http://localhost:11434")


def is_local_configured() -> bool:
    """True when env vars indicate a local backend is available.

    Does NOT make a network call — just checks env. Use ``ping_local()``
    for an actual reachability check.
    """
    explicit = os.environ.get("LOCAL_LLM_PROVIDER", "").strip().lower()
    if explicit in ("ollama", "vllm"):
        return True
    if explicit in ("none", "off", "disabled"):
        return False
    return bool(os.environ.get("OLLAMA_BASE_URL") or os.environ.get("VLLM_BASE_URL"))


def ping_local(timeout_seconds: float = 2.0) -> tuple[bool, str]:
    """Check if the configured local backend is reachable.

    Returns ``(is_up, message)``. Catches every exception and reports
    via ``message`` — never raises. Safe to call from anywhere.
    """
    provider, base_url = _detect_provider()
    if provider == "none" or not base_url:
        return (False, "no local provider configured")
    try:
        # Ollama: GET / returns "Ollama is running"
        # vLLM: GET /v1/models returns model list
        path = "/api/tags" if provider == "ollama" else "/models"
        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.get(f"{base_url}{path}")
        if response.status_code in (200, 404):
            return (True, f"{provider} reachable at {base_url}")
        return (False, f"{provider} returned status {response.status_code}")
    except (httpx.ConnectError, httpx.ConnectTimeout):
        return (False, f"{provider} unreachable at {base_url}")
    except (httpx.HTTPError, OSError, ValueError) as exc:
        # Catch-all for transport errors; never raise from this helper.
        return (False, f"{provider} ping failed: {type(exc).__name__}")


def generate(
    *,
    prompt: str,
    model: str = "",
    backend: LocalProvider | None = None,
    timeout_seconds: float = 10.0,
    json_mode: bool = False,
    max_tokens: int = 1024,
    temperature: float = 0.2,
) -> LocalModelResponse | LocalModelUnavailable:
    """Generate text from a local model.

    Args:
        prompt: User prompt (system+user combined for Ollama; chat format
            for vLLM)
        model: Model name (Ollama: ``qwen2.5:7b`` etc.; vLLM: any served
            model). When empty, picks a sensible default per backend.
        backend: Force a specific backend. When None, auto-detects via env.
        timeout_seconds: HTTP timeout (default 10s — generous for real
            classification, fail-fast in sandbox).
        json_mode: Request structured JSON output (Ollama: ``format=json``;
            vLLM: ``response_format={"type":"json_object"}``).
        max_tokens: Output cap (Ollama: ``num_predict``; vLLM:
            ``max_tokens``).
        temperature: Lower = more deterministic. Default 0.2 for
            consistency.

    Returns:
        ``LocalModelResponse`` on success, ``LocalModelUnavailable``
        on any failure (including server-down, timeout, malformed
        response).
    """
    detected_provider, base_url = _detect_provider()
    chosen = backend or detected_provider

    if chosen == "none" or not base_url:
        return LocalModelUnavailable(
            reason="no local provider configured",
            backend_attempted=chosen,
            base_url=base_url,
        )

    if chosen == "ollama":
        return _generate_ollama(
            prompt=prompt, model=model or "qwen2.5:7b",
            base_url=base_url, timeout_seconds=timeout_seconds,
            json_mode=json_mode, max_tokens=max_tokens,
            temperature=temperature,
        )
    if chosen == "vllm":
        return _generate_vllm(
            prompt=prompt, model=model or "default",
            base_url=base_url, timeout_seconds=timeout_seconds,
            json_mode=json_mode, max_tokens=max_tokens,
            temperature=temperature,
        )
    return LocalModelUnavailable(
        reason=f"unknown backend {chosen!r}",
        backend_attempted=chosen,
        base_url=base_url,
    )


def _generate_ollama(
    *, prompt: str, model: str, base_url: str, timeout_seconds: float,
    json_mode: bool, max_tokens: int, temperature: float,
) -> LocalModelResponse | LocalModelUnavailable:
    """Ollama-specific HTTP path."""
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": temperature,
            "num_predict": max_tokens,
        },
    }
    if json_mode:
        payload["format"] = "json"
    try:
        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.post(f"{base_url}/api/generate", json=payload)
            response.raise_for_status()
            data = response.json()
    except (httpx.ConnectError, httpx.ConnectTimeout):
        return LocalModelUnavailable(
            reason="ollama server unreachable",
            backend_attempted="ollama", base_url=base_url,
        )
    except httpx.HTTPStatusError as exc:
        return LocalModelUnavailable(
            reason=f"ollama HTTP {exc.response.status_code}",
            backend_attempted="ollama", base_url=base_url,
        )
    except (httpx.HTTPError, OSError, ValueError, json.JSONDecodeError) as exc:
        return LocalModelUnavailable(
            reason=f"ollama transport error: {type(exc).__name__}",
            backend_attempted="ollama", base_url=base_url,
        )

    text = str(data.get("response", "")).strip()
    if not text:
        return LocalModelUnavailable(
            reason="ollama returned empty response",
            backend_attempted="ollama", base_url=base_url,
        )

    # Token usage (Ollama provides eval_count + prompt_eval_count)
    in_tokens = int(data.get("prompt_eval_count", _approx_tokens(prompt)))
    out_tokens = int(data.get("eval_count", _approx_tokens(text)))
    latency_ms = int(data.get("total_duration", 0) / 1_000_000)  # ns → ms

    return LocalModelResponse(
        text=text, model=model, backend="ollama",
        latency_ms=latency_ms,
        estimated_input_tokens=in_tokens,
        estimated_output_tokens=out_tokens,
        raw_json=data,
    )


def _generate_vllm(
    *, prompt: str, model: str, base_url: str, timeout_seconds: float,
    json_mode: bool, max_tokens: int, temperature: float,
) -> LocalModelResponse | LocalModelUnavailable:
    """vLLM (OpenAI-compatible) HTTP path."""
    payload: dict[str, Any] = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    try:
        with httpx.Client(timeout=timeout_seconds) as client:
            response = client.post(f"{base_url}/chat/completions", json=payload)
            response.raise_for_status()
            data = response.json()
    except (httpx.ConnectError, httpx.ConnectTimeout):
        return LocalModelUnavailable(
            reason="vllm server unreachable",
            backend_attempted="vllm", base_url=base_url,
        )
    except httpx.HTTPStatusError as exc:
        return LocalModelUnavailable(
            reason=f"vllm HTTP {exc.response.status_code}",
            backend_attempted="vllm", base_url=base_url,
        )
    except (httpx.HTTPError, OSError, ValueError, json.JSONDecodeError) as exc:
        return LocalModelUnavailable(
            reason=f"vllm transport error: {type(exc).__name__}",
            backend_attempted="vllm", base_url=base_url,
        )

    try:
        text = str(data["choices"][0]["message"]["content"]).strip()
    except (KeyError, IndexError, TypeError):
        return LocalModelUnavailable(
            reason="vllm response missing choices[0].message.content",
            backend_attempted="vllm", base_url=base_url,
        )
    if not text:
        return LocalModelUnavailable(
            reason="vllm returned empty content",
            backend_attempted="vllm", base_url=base_url,
        )

    usage = data.get("usage", {})
    in_tokens = int(usage.get("prompt_tokens", _approx_tokens(prompt)))
    out_tokens = int(usage.get("completion_tokens", _approx_tokens(text)))

    return LocalModelResponse(
        text=text, model=model, backend="vllm",
        latency_ms=0,  # vLLM doesn't return latency directly
        estimated_input_tokens=in_tokens,
        estimated_output_tokens=out_tokens,
        raw_json=data,
    )


def _approx_tokens(text: str) -> int:
    """Cheap token estimate: ~4 chars per token (English; Arabic ≈ 2.5)."""
    if not text:
        return 0
    # Conservative approximation: 3.5 chars/token average
    return max(1, int(len(text) / 3.5))
