"""
Pytest fixtures & LLM mocking.
"""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator, Iterator
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# ── Force test-mode env before importing app ───────────────────
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("APP_DEBUG", "false")
os.environ.setdefault("ANTHROPIC_API_KEY", "test-anthropic-key")
os.environ.setdefault("DEEPSEEK_API_KEY", "test-deepseek-key")
os.environ.setdefault("GROQ_API_KEY", "test-groq-key")
os.environ.setdefault("GLM_API_KEY", "test-glm-key")
os.environ.setdefault("GOOGLE_API_KEY", "test-google-key")


from core.llm.base import LLMResponse  # noqa: E402


@pytest.fixture
def mock_llm_response() -> LLMResponse:
    return LLMResponse(
        content='{"ok": true, "message": "mock response"}',
        provider="mock",
        model="mock-model",
        input_tokens=10,
        output_tokens=20,
        finish_reason="end_turn",
    )


@pytest.fixture
def mock_router(mock_llm_response: LLMResponse) -> Iterator[AsyncMock]:
    """Replace the global router with an AsyncMock returning mock_llm_response."""
    with patch("core.llm.router.get_router") as mock_get, \
         patch("core.agents.base.get_router") as mock_get2:
        router_instance = AsyncMock()
        router_instance.run.return_value = mock_llm_response
        router_instance.available_providers.return_value = []
        router_instance.usage_summary.return_value = {}
        mock_get.return_value = router_instance
        mock_get2.return_value = router_instance
        yield router_instance


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """HTTPX async client against the FastAPI app."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture
def sample_lead_payload() -> dict[str, Any]:
    return {
        "company": "شركة التقنية المتقدمة",
        "name": "أحمد محمد",
        "email": "ahmed@techadvanced.sa",
        "phone": "+966501234567",
        "sector": "technology",
        "company_size": "medium",
        "region": "Saudi Arabia",
        "budget": 50000,
        "message": "نحتاج نظام AI لأتمتة إدارة المبيعات والمتابعة، المشكلة عندنا بطء في الرد على العملاء",
    }


@pytest.fixture
def sample_lead_payload_en() -> dict[str, Any]:
    return {
        "company": "Saudi Logistics Co",
        "name": "John Doe",
        "email": "john@saudilogistics.com",
        "phone": "+966501112233",
        "sector": "logistics",
        "company_size": "large",
        "region": "Saudi Arabia",
        "budget": 120000,
        "message": "We need help with route optimization — manual process is slow and expensive",
    }
