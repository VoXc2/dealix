"""
Tests for ConversationMemory (aiosqlite-backed SQLite store).
"""
from __future__ import annotations

import pytest
import pytest_asyncio


@pytest.mark.asyncio
async def test_upsert_and_get_lead(memory):
    """Upserting a lead creates a row, subsequent upserts update it."""
    await memory.upsert_lead(
        channel="whatsapp",
        address="+966511111111",
        name="Ahmed",
        company="متجر الأفق",
        sector="ecommerce",
    )
    lead = await memory.get_lead(channel="whatsapp", address="+966511111111")
    assert lead is not None
    assert lead["name"] == "Ahmed"
    assert lead["company"] == "متجر الأفق"
    assert lead["message_count"] == 1

    # Upsert again — message_count should increment
    await memory.upsert_lead(channel="whatsapp", address="+966511111111")
    lead = await memory.get_lead(channel="whatsapp", address="+966511111111")
    assert lead["message_count"] == 2


@pytest.mark.asyncio
async def test_lead_not_found(memory):
    """get_lead returns None for unknown address."""
    lead = await memory.get_lead(channel="whatsapp", address="+9665XXXXXXXX")
    assert lead is None


@pytest.mark.asyncio
async def test_save_and_get_history(memory):
    """save_message persists messages; get_history returns them in chat format."""
    await memory.upsert_lead(channel="whatsapp", address="+966522222222")

    await memory.save_message(
        channel="whatsapp",
        address="+966522222222",
        direction="in",
        body="مرحبا",
    )
    await memory.save_message(
        channel="whatsapp",
        address="+966522222222",
        direction="out",
        body="أهلاً وسهلاً!",
    )

    history = await memory.get_history(
        channel="whatsapp", address="+966522222222"
    )
    assert len(history) == 2
    assert history[0] == {"role": "user", "content": "مرحبا"}
    assert history[1] == {"role": "assistant", "content": "أهلاً وسهلاً!"}


@pytest.mark.asyncio
async def test_get_history_limit(memory):
    """get_history respects the limit parameter."""
    await memory.upsert_lead(channel="whatsapp", address="+966533333333")
    for i in range(15):
        await memory.save_message(
            channel="whatsapp",
            address="+966533333333",
            direction="in",
            body=f"رسالة {i}",
        )

    history = await memory.get_history(
        channel="whatsapp", address="+966533333333", limit=5
    )
    assert len(history) == 5
    # Should be the last 5 messages (chronological)
    assert history[-1]["content"] == "رسالة 14"


@pytest.mark.asyncio
async def test_opt_out(memory):
    """set_opt_out marks lead as opted-out."""
    await memory.upsert_lead(channel="email", address="test@example.com")
    await memory.set_opt_out(channel="email", address="test@example.com")

    lead = await memory.get_lead(channel="email", address="test@example.com")
    assert lead["opt_in"] == 0
    assert lead["stage"] == "unsubscribed"


@pytest.mark.asyncio
async def test_update_stage(memory):
    """update_stage changes the lead's pipeline stage."""
    await memory.upsert_lead(channel="whatsapp", address="+966544444444")
    await memory.update_stage(
        channel="whatsapp", address="+966544444444", stage="qualified"
    )
    lead = await memory.get_lead(channel="whatsapp", address="+966544444444")
    assert lead["stage"] == "qualified"


@pytest.mark.asyncio
async def test_list_leads_filter(memory):
    """list_leads correctly filters by channel and stage."""
    await memory.upsert_lead(channel="whatsapp", address="+966551111111", stage="new")
    await memory.upsert_lead(channel="email",    address="a@b.com",        stage="qualified")
    await memory.upsert_lead(channel="whatsapp", address="+966552222222", stage="qualified")

    wa_leads = await memory.list_leads(channel="whatsapp")
    assert len(wa_leads) >= 2

    qualified = await memory.list_leads(stage="qualified")
    assert all(l["stage"] == "qualified" for l in qualified)


@pytest.mark.asyncio
async def test_conversation_session(memory):
    """upsert_conversation + get_conversation round-trip."""
    from datetime import datetime, timedelta, timezone

    expires = (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat()

    await memory.upsert_conversation(
        channel="whatsapp",
        address="+966560000000",
        session_active=True,
        session_expires=expires,
        intent="interested",
        sentiment="positive",
    )

    conv = await memory.get_conversation(channel="whatsapp", address="+966560000000")
    assert conv is not None
    assert conv["session_active"] == 1
    assert conv["intent"] == "interested"
    assert conv["sentiment"] == "positive"
