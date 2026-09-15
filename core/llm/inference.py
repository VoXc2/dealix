"""Safe application-facing entry point for routed LLM inference.

Omega V3 model/provider/cost/data authority belongs to the canonical broker and
Session Factory. This compatibility adapter must never turn configured-provider
order into execution authority. Production ``ModelRouter`` therefore fails closed
until callers migrate to the governed execution fabric.
"""

from __future__ import annotations

import asyncio

from core.config.models import Provider, Task
from core.llm import router as llm_router
from core.llm.base import Message


class NoLLMProviderConfigured(RuntimeError):
    """Raised when inference has no policy-compliant configured provider."""


async def complete_with_router(
    system_prompt: str,
    user_input: str,
    *,
    task: Task = Task.ARABIC_TASKS,
    max_tokens: int = 400,
    temperature: float = 0.4,
    timeout_seconds: float = 12.0,
) -> tuple[str, str]:
    """Invoke the compatibility router without choosing a provider.

    Configured-provider order is observational only. DeepSeek and the migration
    HOLD sentinel are explicitly excluded, and this adapter never passes a
    preferred provider. The production router owns the final fail-closed guard;
    custom test/migration routers may continue to implement the same ``run`` seam.
    """

    router = llm_router.get_router()
    provider_probe = getattr(router, "available_providers", None)
    if callable(provider_probe):
        configured = provider_probe()
        policy_compliant = [
            provider
            for provider in configured
            if provider not in {Provider.DEEPSEEK, Provider.HOLD}
        ]
        if not policy_compliant:
            raise NoLLMProviderConfigured("no_policy_compliant_llm_provider_configured")

    response = await asyncio.wait_for(
        router.run(
            task=task,
            messages=[Message(role="user", content=user_input)],
            system=system_prompt,
            max_tokens=max_tokens,
            temperature=temperature,
        ),
        timeout=timeout_seconds,
    )
    return response.content, response.model


__all__ = ["NoLLMProviderConfigured", "complete_with_router"]
