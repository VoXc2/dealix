"""
Local AI Module — Dealix AI Revenue OS
═════════════════════════════════════════════════════════════════
On-premise / self-hosted LLM integration for Dealix.

Runs open-weight models locally via Ollama (OpenAI-compatible API)
so the server can think and execute tasks without paid cloud keys.

NOTE: Claude, GPT, Gemini, and Grok are *API-hosted* and cannot be
downloaded. The models included here are genuinely runnable on a
modest Ubuntu server (CPU or small GPU): Qwen2.5, Llama 3.x, Gemma 2,
Phi-3, DeepSeek-Coder.
"""

from app.services.local_ai.catalog import (
    LocalModelSpec,
    ServerTier,
    TaskKind,
    MODEL_CATALOG,
    detect_server_tier,
    select_models_for_tier,
    pick_model_for_task,
)
from app.services.local_ai.client import (
    OllamaClient,
    OllamaChatResult,
    get_local_client,
)
from app.services.local_ai.router import (
    LocalModelRouter,
    RouteDecision,
    get_local_router,
)

__all__ = [
    "LocalModelSpec",
    "ServerTier",
    "TaskKind",
    "MODEL_CATALOG",
    "detect_server_tier",
    "select_models_for_tier",
    "pick_model_for_task",
    "OllamaClient",
    "OllamaChatResult",
    "get_local_client",
    "LocalModelRouter",
    "RouteDecision",
    "get_local_router",
]
