"""
Tests: Conversations, Messages, Reply (dry-run), AI Suggest
"""
from __future__ import annotations

import os
import pytest
from .conftest import auth

# Ensure no real Twilio calls in tests
os.environ.setdefault("TWILIO_ACCOUNT_SID", "")
os.environ.setdefault("TWILIO_AUTH_TOKEN", "")


@pytest.mark.asyncio
async def test_list_conversations(client, token_a):
    """Conversations list returns correct shape."""
    r = await client.get("/api/v1/conversations", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_list_conversations_channel_filter(client, token_a):
    """Channel filter narrows conversation list."""
    r = await client.get("/api/v1/conversations?channel=whatsapp", headers=auth(token_a))
    assert r.status_code == 200
    data = r.json()
    for item in data["items"]:
        assert item["channel"] == "whatsapp"


@pytest.mark.asyncio
async def test_get_messages_for_phone(client, token_a):
    """Getting messages for a phone returns message list."""
    phone = "+966501111111"
    r = await client.get(
        f"/api/v1/conversations/{phone}/messages",
        headers=auth(token_a)
    )
    assert r.status_code == 200
    data = r.json()
    assert data["phone"] == phone
    assert "messages" in data
    assert isinstance(data["messages"], list)
    # Should have at least 1 message from seed
    assert len(data["messages"]) >= 1


@pytest.mark.asyncio
async def test_reply_dry_run(client, token_a):
    """Reply endpoint works in dry-run mode (no Twilio creds)."""
    phone = "+966501111111"
    r = await client.post(
        f"/api/v1/conversations/{phone}/reply",
        json={"channel": "whatsapp", "body": "مرحباً، هذا رسالة اختبار"},
        headers=auth(token_a)
    )
    # 200 or 207 (if warning)
    assert r.status_code in (200, 207)
    data = r.json()
    assert "message" in data
    msg = data["message"]
    assert msg["direction"] == "out"
    assert msg["body"] == "مرحباً، هذا رسالة اختبار"
    assert msg["phone"] == phone


@pytest.mark.asyncio
async def test_reply_saves_to_db(client, token_a):
    """Reply is persisted and appears in message history."""
    phone = "+966501111111"
    body = "رسالة اختبار فريدة " + "unique_test_xyz"

    # Send reply
    r1 = await client.post(
        f"/api/v1/conversations/{phone}/reply",
        json={"channel": "whatsapp", "body": body},
        headers=auth(token_a)
    )
    assert r1.status_code in (200, 207)

    # Verify it appears in messages
    r2 = await client.get(
        f"/api/v1/conversations/{phone}/messages",
        headers=auth(token_a)
    )
    bodies = [m["body"] for m in r2.json()["messages"]]
    assert body in bodies, f"Sent message not found in history. Bodies: {bodies}"


@pytest.mark.asyncio
async def test_ai_suggest_no_groq(client, token_a):
    """AI suggest returns 3 suggestions (fallback when no GROQ key)."""
    os.environ["GROQ_API_KEY"] = ""
    phone = "+966501111111"
    r = await client.post(
        f"/api/v1/conversations/{phone}/ai-suggest",
        headers=auth(token_a)
    )
    assert r.status_code == 200
    data = r.json()
    assert "suggestions" in data
    assert len(data["suggestions"]) == 3
    for s in data["suggestions"]:
        assert isinstance(s, str)
        assert len(s) > 0
