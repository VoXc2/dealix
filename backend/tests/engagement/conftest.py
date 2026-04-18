"""
Shared fixtures for engagement framework tests.
"""
from __future__ import annotations

import os
import tempfile
import asyncio
from pathlib import Path
from typing import AsyncGenerator

import pytest
import pytest_asyncio

# Point prompts to the real directory so LLMGateway can load them in tests
os.environ.setdefault(
    "PROMPTS_DIR",
    str(Path(__file__).parents[2] / "app" / "engagement" / "prompts"),
)
os.environ.setdefault("DEALIX_DB", ":memory:")  # use in-memory SQLite for tests
os.environ.setdefault("GROQ_API_KEY", "")
os.environ.setdefault("OPENAI_API_KEY", "")
os.environ.setdefault("TWILIO_ACCOUNT_SID", "")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "")


@pytest.fixture(scope="session")
def event_loop():
    """Use a single event loop for the whole test session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def settings():
    """Return a test EngagementSettings with safe defaults."""
    from app.engagement.base import EngagementSettings

    return EngagementSettings(
        groq_api_key="",
        openai_api_key="",
        twilio_account_sid="",
        twilio_auth_token="",
        twilio_whatsapp_number="whatsapp:+14155238886",
        twilio_sms_number="+14155238886",
        sendgrid_api_key="",
        dealix_db=":memory:",
        rate_limit_per_minute=100,
        rate_limit_per_hour=10000,
        max_retry_attempts=2,
        retry_base_delay=0.01,
        quiet_hours_start=23,  # effectively disabled for most tests
        quiet_hours_end=0,
    )


@pytest_asyncio.fixture
async def memory(tmp_path):
    """
    Return an initialised ConversationMemory backed by a unique temp file per test.
    Using ":memory:" would share state across tests via aiosqlite's connection pool.
    """
    from app.engagement.memory import ConversationMemory

    db_path = str(tmp_path / "test_engagement.db")
    mem = ConversationMemory(db_path=db_path)
    await mem.init()
    return mem


@pytest.fixture
def llm(settings):
    """Return an LLMGateway with no real API keys (for unit tests)."""
    from app.engagement.llm import LLMGateway

    return LLMGateway(settings=settings)


@pytest_asyncio.fixture
async def wa_agent(settings, memory, llm):
    """Return a WhatsAppAgent wired up with test settings."""
    from app.engagement.channels.whatsapp import WhatsAppAgent

    return WhatsAppAgent(settings=settings, memory=memory, llm=llm)


@pytest_asyncio.fixture
async def sms_agent(settings, memory, llm):
    """Return an SMSAgent wired up with test settings."""
    from app.engagement.channels.sms import SMSAgent

    return SMSAgent(settings=settings, memory=memory, llm=llm)


@pytest_asyncio.fixture
async def email_agent(settings, memory, llm):
    """Return an EmailAgent wired up with test settings."""
    from app.engagement.channels.email import EmailAgent

    return EmailAgent(settings=settings, memory=memory, llm=llm)
