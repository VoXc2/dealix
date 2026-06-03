"""Phase 10 — Customer Portal enriched_view v2 (Wave 4 additive keys)."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_new_enriched_keys_present() -> None:
    """All 8 new Wave 4 keys must be reachable in enriched_view."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-keys-test")
    enriched = r.json()["enriched_view"]
    new_keys = [
        "full_ops_score", "weaknesses_summary", "next_3_decisions",
        "support_summary", "payment_state", "proof_summary",
        "approval_summary", "executive_command_link",
    ]
    for k in new_keys:
        assert k in enriched, f"Wave 4 enriched key missing: {k}"


@pytest.mark.asyncio
async def test_full_ops_score_in_portal() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-fos-test")
    score = r.json()["enriched_view"]["full_ops_score"]
    assert "score" in score
    assert "readiness_label" in score


@pytest.mark.asyncio
async def test_weaknesses_summary_shape() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-weak-test")
    ws = r.json()["enriched_view"]["weaknesses_summary"]
    assert "total" in ws
    assert "critical_count" in ws
    assert "top_3" in ws
    assert isinstance(ws["top_3"], list)
    assert len(ws["top_3"]) <= 3


@pytest.mark.asyncio
async def test_next_3_decisions_shape() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-decisions")
    section = r.json()["enriched_view"]["next_3_decisions"]
    assert "decisions" in section
    assert isinstance(section["decisions"], list)
    assert len(section["decisions"]) <= 3


@pytest.mark.asyncio
async def test_executive_command_link_present() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-link-test")
    link = r.json()["enriched_view"]["executive_command_link"]
    assert "url" in link
    assert "executive-command-center.html" in link["url"]
    assert "v2-link-test" in link["url"]
    assert "label_ar" in link
    assert "label_en" in link


@pytest.mark.asyncio
async def test_payment_state_no_fake_revenue() -> None:
    """Even with no payments, response shape valid + counts are 0."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-payment-empty")
    pay = r.json()["enriched_view"]["payment_state"]
    assert pay["confirmed_count"] == 0
    assert pay["total_payments"] == 0


@pytest.mark.asyncio
async def test_proof_summary_no_fake_proof() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-proof-empty")
    proof = r.json()["enriched_view"]["proof_summary"]
    assert proof["proof_events_count"] == 0


@pytest.mark.asyncio
async def test_approval_summary_shape() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-approval")
    summary = r.json()["enriched_view"]["approval_summary"]
    assert "pending_total" in summary


@pytest.mark.asyncio
async def test_support_summary_shape() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customer-portal/v2-support")
    s = r.json()["enriched_view"]["support_summary"]
    assert "open_tickets" in s
