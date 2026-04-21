"""
HUMAIN ALLaM LLM Provider — Saudi Sovereign Arabic-first LLM.
موفر نموذج ALLaM من HUMAIN — النموذج اللغوي السيادي السعودي.

ALLaM is developed by SDAIA / HUMAIN and is designed for Arabic language tasks
with KSA data residency, meeting PDPL and Saudi AI sovereignty requirements.

Status (as of mid-2025): ALLaM is available via the HUMAIN marketplace /
IBM watsonx.ai. The marketplace API is not yet publicly open — this adapter
uses an OpenAI-compatible REST interface (ChatCompletion format) which ALLaM
is expected to expose when GA.

TODO items are clearly marked where the API spec is not yet confirmed.

Docs / References:
- https://humain.ai/
- https://sdaia.gov.sa/ar/Media/Blog/Pages/BlogSingleView.aspx?ItemId=59
- IBM watsonx ALLaM: https://www.ibm.com/products/watsonx-ai/allam

Environment variables:
- ALLAM_API_KEY          — API key from HUMAIN marketplace
- ALLAM_API_BASE_URL     — Base URL (defaults to expected HUMAIN endpoint)
- ALLAM_MODEL            — Model ID (defaults to "allam-2-7b-instruct")
- ALLAM_MAX_TOKENS       — Max tokens per response (default: 2048)
- ALLAM_TEMPERATURE      — Default temperature (default: 0.7)
"""

from __future__ import annotations

import logging
import os
import time
from typing import Optional

import httpx

logger = logging.getLogger(__name__)

# TODO: Confirm final production endpoint from HUMAIN marketplace
# Expected to follow OpenAI ChatCompletion format
_DEFAULT_BASE_URL = "https://api.humain.ai/v1"  # TODO: Confirm URL
_DEFAULT_MODEL = "allam-2-7b-instruct"           # TODO: Confirm model ID


class ALLaMProvider:
    """
    HUMAIN ALLaM language model provider.
    موفر نموذج ALLaM اللغوي من HUMAIN.

    Follows the same interface contract as LLMProvider._call_provider().
    يتبع نفس واجهة LLMProvider._call_provider().

    Returns the standard Dealix LLM response shape:
    {
        "content": str,
        "provider": "allam",
        "model": str,
        "tokens": {"prompt": int, "completion": int, "total": int},
        "latency_ms": int,
        "cached": bool,
    }

    Usage:
        provider = ALLaMProvider()
        result = await provider.chat(
            system_prompt="أنت مساعد مبيعات ذكي",
            user_message="مرحباً، ما هي خدماتكم؟"
        )
        print(result["content"])
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        max_tokens: int = 2048,
        temperature: float = 0.7,
        timeout: float = 60.0,
    ) -> None:
        self.api_key = api_key or os.getenv("ALLAM_API_KEY", "")
        self.base_url = (
            base_url
            or os.getenv("ALLAM_API_BASE_URL", _DEFAULT_BASE_URL)
        ).rstrip("/")
        self.model = model or os.getenv("ALLAM_MODEL", _DEFAULT_MODEL)
        self.max_tokens = int(os.getenv("ALLAM_MAX_TOKENS", max_tokens))
        self.temperature = float(os.getenv("ALLAM_TEMPERATURE", temperature))
        self.timeout = timeout

        if not self.api_key:
            logger.warning(
                "ALLAM_API_KEY not set — ALLaM calls will fail. "
                "Register at https://humain.ai/ to obtain an API key."
            )

    # ── Public interface ──────────────────────────────────

    async def chat(
        self,
        system_prompt: str,
        user_message: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        json_mode: bool = False,
        history: Optional[list[dict]] = None,
    ) -> dict:
        """
        Send a chat completion request to ALLaM.
        إرسال طلب إكمال محادثة إلى ALLaM.

        Args:
            system_prompt: System/instruction prompt (Arabic preferred for ALLaM)
            user_message: User message
            model: Override model ID
            temperature: Override temperature (0.0–2.0)
            max_tokens: Override max output tokens
            json_mode: Request JSON-formatted output (if supported)
            history: Prior conversation turns [{"role": "user"|"assistant", "content": str}]

        Returns:
            Standard Dealix LLM response dict
        """
        messages = [{"role": "system", "content": system_prompt}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        return await self._call_chat_completion(
            messages=messages,
            model=model or self.model,
            temperature=temperature if temperature is not None else self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            json_mode=json_mode,
        )

    async def complete(
        self,
        prompt: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> dict:
        """
        Legacy completion (non-chat) endpoint wrapper.
        غلاف نقطة النهاية القديمة للإكمال (غير دردشة).

        Maps to chat format with an empty system prompt.

        TODO: Verify if ALLaM exposes a /completions endpoint or only /chat/completions.
        """
        return await self.chat(
            system_prompt="",
            user_message=prompt,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )

    async def embed(self, text: str, model: Optional[str] = None) -> list[float]:
        """
        Generate text embeddings using ALLaM.
        إنتاج تضمينات نصية باستخدام ALLaM.

        TODO: Confirm ALLaM embedding model ID and endpoint.
              Endpoint expected: POST /embeddings (OpenAI-compatible)
        """
        embed_model = model or os.getenv("ALLAM_EMBED_MODEL", "allam-embedding")  # TODO: Confirm
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.base_url}/embeddings",
                json={"input": text, "model": embed_model},
                headers=self._headers(),
            )
            resp.raise_for_status()
            data = resp.json()
            return data["data"][0]["embedding"]

    # ── Internal implementation ───────────────────────────

    async def _call_chat_completion(
        self,
        messages: list[dict],
        model: str,
        temperature: float,
        max_tokens: int,
        json_mode: bool = False,
    ) -> dict:
        """
        Call the ALLaM /chat/completions endpoint (OpenAI-compatible format).
        استدعاء نقطة نهاية /chat/completions (تنسيق متوافق مع OpenAI).

        ALLaM is expected to expose an OpenAI-compatible API.
        TODO: Verify request/response format from HUMAIN API docs once GA.
        """
        start = time.time()

        body: dict = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }

        if json_mode:
            # OpenAI-compatible JSON mode
            # TODO: Verify ALLaM supports response_format
            body["response_format"] = {"type": "json_object"}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions",
                    json=body,
                    headers=self._headers(),
                )
                resp.raise_for_status()
                data = resp.json()
        except httpx.HTTPStatusError as exc:
            logger.error(
                f"ALLaM API HTTP error {exc.response.status_code}: {exc.response.text}"
            )
            raise
        except httpx.TimeoutException:
            logger.error("ALLaM API request timed out")
            raise

        latency_ms = int((time.time() - start) * 1000)

        # Parse OpenAI-compatible response structure
        choice = data.get("choices", [{}])[0]
        content = (
            choice.get("message", {}).get("content", "")
            or choice.get("text", "")
        )

        usage = data.get("usage", {})
        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        return {
            "content": content,
            "provider": "allam",
            "model": data.get("model", model),
            "tokens": {
                "prompt": prompt_tokens,
                "completion": completion_tokens,
                "total": usage.get("total_tokens", prompt_tokens + completion_tokens),
            },
            "latency_ms": latency_ms,
            "cached": False,
        }

    def _headers(self) -> dict[str, str]:
        """
        Build HTTP headers for ALLaM API requests.
        بناء رؤوس HTTP لطلبات ALLaM API.

        TODO: Confirm auth header format (Bearer token vs API-Key header)
        from HUMAIN marketplace documentation.
        """
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            # TODO: Add any HUMAIN-specific required headers once docs are public
        }

    # ── Health check ──────────────────────────────────────

    async def health_check(self) -> dict:
        """
        Check ALLaM API availability.
        التحقق من توفر ALLaM API.

        Returns:
            {"status": "ok"|"error", "latency_ms": int, "model": str}
        """
        try:
            result = await self.chat(
                system_prompt="أنت مساعد مفيد.",
                user_message="مرحبا",
                max_tokens=10,
            )
            return {
                "status": "ok",
                "latency_ms": result["latency_ms"],
                "model": result["model"],
                "provider": "allam",
            }
        except Exception as exc:
            return {
                "status": "error",
                "error": str(exc),
                "provider": "allam",
                "model": self.model,
            }

    def __repr__(self) -> str:
        return f"ALLaMProvider(model={self.model!r}, base_url={self.base_url!r})"
