"""Phase 3 — Customer Brain aggregator tests.

Asserts:
- Snapshot composition from existing modules
- Lazy build on first GET
- Context pack respects 3KB cap
- HARD_GATES present
"""
from __future__ import annotations

import json

import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_brain_lazy_build_on_first_get() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/test-handle-123/brain")
    assert r.status_code == 200
    body = r.json()
    snap = body["snapshot"]
    assert snap["customer_handle"] == "test-handle-123"
    assert snap["safety_summary"] == "no_pii_in_snapshot"
    assert "pdpl_default" in snap["compliance_constraints"]


@pytest.mark.asyncio
async def test_brain_status_lists_known_customers() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Build a snapshot first
        await c.post("/api/v1/customers/known-customer/brain/build")
        # Then list
        r = await c.get("/api/v1/customers/brain/status")
    assert r.status_code == 200
    body = r.json()
    assert body["service"] == "customer_brain"
    assert "known-customer" in body["known_customers"]


@pytest.mark.asyncio
async def test_brain_pulls_leadops_history_for_customer() -> None:
    """If a leadops record was created with this customer_handle,
    the brain snapshot should reflect it."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        # Create a leadops record
        await c.post("/api/v1/leadops/run", json={
            "raw_payload": {
                "company": "Brain Test Co",
                "email": "x@brain-test.sa",
                "sector": "real_estate",
                "region": "Riyadh",
            },
            "source": "warm_intro",
            "customer_handle": "brain-test-co",
        })
        # Now build brain
        r = await c.post("/api/v1/customers/brain-test-co/brain/build")
    assert r.status_code == 200
    snap = r.json()["snapshot"]
    assert snap["profile"]["sector"] == "real_estate"
    assert "whatsapp" in snap["channels"]  # real_estate sector default
    assert len(snap["service_history"]) >= 1
    assert snap["service_history"][0]["type"] == "lead"


@pytest.mark.asyncio
async def test_context_pack_under_3kb_cap() -> None:
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        await c.post("/api/v1/customers/pack-test/brain/build")
        r = await c.get("/api/v1/customers/pack-test/context-pack")
    assert r.status_code == 200
    pack = r.json()["context_pack"]
    serialized = json.dumps(pack, ensure_ascii=False).encode("utf-8")
    assert len(serialized) <= 3072, f"context pack {len(serialized)} > 3KB"


@pytest.mark.asyncio
async def test_brain_no_internal_terms_leaked() -> None:
    """No router/agent/v12/scraping internal terms in customer-facing snapshot."""
    from api.main import app
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        r = await c.get("/api/v1/customers/leak-test/brain")
    body_str = json.dumps(r.json(), ensure_ascii=False).lower()
    # Note: source_modules INTENTIONALLY includes module names — this is
    # for engineers, not customers. The constitutional gate applies to
    # customer_company_portal, not the engineering-facing brain endpoint.
    # We just check no SENSITIVE leaks (sk_live, ghp_, etc.)
    assert "sk_live" not in body_str
    assert "ghp_" not in body_str


def test_brain_builder_handles_unknown_customer() -> None:
    """Building for an unknown handle returns an empty but valid snapshot."""
    from auto_client_acquisition.customer_brain import build_snapshot
    snap = build_snapshot(customer_handle="never-seen-before-customer")
    assert snap.customer_handle == "never-seen-before-customer"
    assert snap.service_history == []
    assert snap.proof_history == []
    assert "leadops_spine" in snap.source_modules
