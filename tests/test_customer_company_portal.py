"""Customer portal — eight fields, zero internal leakage."""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app


@pytest.mark.asyncio
async def test_customer_portal_200() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-portal/Slot-A")
        assert r.status_code == 200


@pytest.mark.asyncio
async def test_customer_portal_no_internal_leakage() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-portal/Slot-A")
        body = r.json()
        forbidden = [
            "v11",
            "v12",
            "v12.5",
            "agent",
            "router",
            "verifier",
            "growth_beast",
            "revops",
            "compliance_os_v12",
        ]
        serialized = json.dumps(body, ensure_ascii=False).lower()
        for f in forbidden:
            assert f.lower() not in serialized, f"leaked {f}"


@pytest.mark.asyncio
async def test_eight_top_level_customer_fields() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-portal/test-handle")
        keys = set(r.json().keys()) - {"schema_version", "experience_layer"}
        expected = {
            "start_diagnostic",
            "seven_day_plan",
            "messages_and_followups",
            "support_tickets",
            "deliverables",
            "proof_pack",
            "weekly_report",
            "next_decision",
        }
        assert expected <= keys


@pytest.mark.asyncio
async def test_seven_day_plan_length_when_consent() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/customer-portal/Slot-A")
        plan = r.json()["seven_day_plan"]
        assert len(plan) == 7


@pytest.mark.asyncio
async def test_messages_followups_has_approval_mode() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        msg = (await client.get("/api/v1/customer-portal/x")).json()[
            "messages_and_followups"
        ]
        assert msg.get("action_mode") == "approval_required"
