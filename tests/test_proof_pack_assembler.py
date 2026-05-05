"""Tests for proof_snippet_engine.render_pack + the
``POST /api/v1/self-growth/proof-pack/assemble`` endpoint (P2).
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.self_growth_os import proof_snippet_engine


_GOOD_EVENT_INTERNAL = {
    "event_type": "pilot_delivered",
    "service_id": "growth_starter",
    "outcome_metric": "qualified_opportunities",
    "outcome_value": 14,
    "sla_period_days": 7,
    "consent_for_publication": False,
    "customer_anonymized": "ACME-001",
}

_GOOD_EVENT_PUBLIC = {
    "event_type": "pilot_delivered",
    "service_id": "growth_starter",
    "outcome_metric": "drafts_approved",
    "outcome_value": 22,
    "sla_period_days": 7,
    "consent_for_publication": True,
    "customer_display_name": "ACME Saudi",
}


# ─── Pack rendering happy paths ─────────────────────────────────────


def test_pack_renders_3_events_internal_only_when_any_consent_false():
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_INTERNAL, _GOOD_EVENT_PUBLIC, _GOOD_EVENT_INTERNAL],
        customer_handle="ACME-001",
    )
    assert pack["decision"] == "allowed_draft"
    assert pack["approval_status"] == "approval_required"
    assert pack["audience"] == "internal_only"
    assert pack["customer_handle"] == "ACME-001"
    # Markdown is non-empty and contains every event
    assert pack["markdown_ar"]
    assert pack["markdown_en"]
    assert pack["markdown_ar"].count("###") == 3
    assert pack["markdown_en"].count("###") == 3


def test_pack_audience_public_when_all_consented():
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_PUBLIC, _GOOD_EVENT_PUBLIC],
        customer_handle="ACME Saudi",
    )
    assert pack["audience"] == "public_with_consent"
    # Real customer name appears in the snippets (not just the handle)
    assert "ACME Saudi" in pack["markdown_ar"]


def test_pack_includes_period_label_in_titles():
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_INTERNAL],
        customer_handle="ACME-001",
        period_label="2026-Q2 Pilot",
    )
    assert "2026-Q2 Pilot" in pack["markdown_ar"]
    assert "2026-Q2 Pilot" in pack["markdown_en"]


def test_pack_always_returns_approval_required():
    """Even a fully consented pack stays approval_required."""
    pack = proof_snippet_engine.render_pack([_GOOD_EVENT_PUBLIC])
    assert pack["approval_status"] == "approval_required"


# ─── Failure modes ──────────────────────────────────────────────────


def test_empty_events_returns_blocked():
    pack = proof_snippet_engine.render_pack([])
    assert pack["decision"] == "blocked"
    assert pack["audience"] == "invalid"


def test_pack_blocks_when_any_event_invalid():
    """An event with missing required fields blocks the entire pack."""
    bad = {"event_type": "broken"}  # missing service_id, outcome_*, consent
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_INTERNAL, bad, _GOOD_EVENT_PUBLIC]
    )
    assert pack["decision"] == "blocked"
    assert pack["audience"] == "invalid"
    assert "blocked" in pack["notes"].lower()


def test_pack_blocks_when_event_has_forbidden_token():
    """If an event's outcome_metric contains a forbidden token, the
    individual render() blocks AND the pack blocks too."""
    poisoned = dict(_GOOD_EVENT_INTERNAL)
    # 'guaranteed' triggers safe_publishing_gate
    poisoned["outcome_metric"] = "guaranteed sales"
    pack = proof_snippet_engine.render_pack([poisoned])
    assert pack["decision"] == "blocked"
    assert "guaranteed" in pack.get("forbidden_tokens_found", [])


def test_pack_summary_block_records_event_count():
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_INTERNAL, _GOOD_EVENT_PUBLIC],
        customer_handle="ACME",
    )
    assert "2" in pack["summary_ar"] or "حدثاً" in pack["summary_ar"]


def test_pack_carries_individual_event_results():
    pack = proof_snippet_engine.render_pack(
        [_GOOD_EVENT_INTERNAL, _GOOD_EVENT_PUBLIC]
    )
    assert len(pack["events"]) == 2
    # Each event's per-event audience is preserved
    assert pack["events"][0]["audience"] == "internal_only"
    assert pack["events"][1]["audience"] == "public_with_consent"


# ─── API endpoint ───────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_endpoint_returns_pack():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-pack/assemble",
            json={
                "customer_handle": "ACME-001",
                "events": [_GOOD_EVENT_INTERNAL, _GOOD_EVENT_PUBLIC],
            },
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["decision"] == "allowed_draft"
    assert payload["audience"] == "internal_only"
    assert payload["markdown_ar"]


@pytest.mark.asyncio
async def test_endpoint_400_on_missing_events():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-pack/assemble",
            json={"customer_handle": "ACME-001"},
        )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_endpoint_400_on_empty_events():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-pack/assemble",
            json={"customer_handle": "ACME-001", "events": []},
        )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_endpoint_returns_blocked_when_event_invalid():
    """Invalid event in the pack returns 200 + decision=blocked
    (caller can read the response and surface specific errors)."""
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-pack/assemble",
            json={
                "customer_handle": "ACME-001",
                "events": [{"event_type": "broken"}],
            },
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["decision"] == "blocked"
