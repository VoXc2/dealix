"""Tests for daily_growth_loop + proof_snippet_engine.

Pure unit tests — no network, no LLM, no DB.
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.self_growth_os import (
    daily_growth_loop,
    proof_snippet_engine,
)


# ─── daily_growth_loop ──────────────────────────────────────────────


def test_daily_loop_returns_typed_blocks():
    loop = daily_growth_loop.build_today()
    for key in [
        "schema_version",
        "generated_at",
        "decisions",
        "service_to_promote",
        "partner_focus",
        "seo_gap_pages",
        "perimeter_status",
        "open_loops",
        "guardrails",
    ]:
        assert key in loop, f"daily loop missing block: {key}"


def test_daily_loop_guardrails_block_is_locked():
    loop = daily_growth_loop.build_today()
    g = loop["guardrails"]
    assert g["no_live_send"] is True
    assert g["no_scraping"] is True
    assert g["no_cold_outreach"] is True
    assert g["approval_required_for_external_actions"] is True


def test_daily_loop_partner_focus_rotates_deterministically():
    """Same day-of-year → same partner category. The function reads
    today's date, so we just check it returns *some* category from
    the catalog."""
    loop = daily_growth_loop.build_today()
    pf = loop["partner_focus"]
    if pf:  # may be empty if catalog is empty (it isn't, but defensive)
        assert "category_id" in pf
        assert pf.get("warm_intro_draft_ar")


def test_daily_loop_service_to_promote_is_partial_or_pilot():
    loop = daily_growth_loop.build_today()
    svc = loop["service_to_promote"]
    if svc:
        assert svc["status"] in {"partial", "pilot"}
        assert svc["service_id"]


def test_daily_loop_seo_gap_pages_are_sorted_ascending():
    loop = daily_growth_loop.build_today()
    pages = loop["seo_gap_pages"]
    if len(pages) > 1:
        for a, b in zip(pages, pages[1:]):
            assert a["score"] <= b["score"]


def test_daily_loop_open_loops_includes_review_pending_items():
    loop = daily_growth_loop.build_today()
    text = "\n".join(loop["open_loops"])
    # B1, B2, B4 are surfaced; S5 is too.
    assert "B1" in text
    assert "B2" in text


def test_to_markdown_renders_non_empty():
    loop = daily_growth_loop.build_today()
    md = daily_growth_loop.to_markdown(loop)
    assert "# Dealix — Daily Growth Loop" in md
    assert "Hard guardrails" in md


# ─── proof_snippet_engine ───────────────────────────────────────────


_GOOD_EVENT = {
    "event_type": "pilot_delivered",
    "service_id": "growth_starter",
    "outcome_metric": "qualified_opportunities",
    "outcome_value": 14,
    "sla_period_days": 7,
    "consent_for_publication": False,
    "customer_anonymized": "ACME-001",
}


def test_proof_snippet_renders_internal_only_without_consent():
    result = proof_snippet_engine.render(_GOOD_EVENT)
    assert result.decision == "allowed_draft"
    assert result.approval_status == "approval_required"
    assert result.audience == "internal_only"
    assert result.snippet_ar
    assert result.snippet_en


def test_proof_snippet_anonymizes_customer_without_consent():
    result = proof_snippet_engine.render(_GOOD_EVENT)
    # The anonymized handle (ACME-001) is fine; the customer_display_name
    # if present must NOT leak.
    event_with_name = dict(_GOOD_EVENT, customer_display_name="Real Co Ltd")
    result2 = proof_snippet_engine.render(event_with_name)
    assert "Real Co Ltd" not in result2.snippet_ar
    assert "Real Co Ltd" not in result2.snippet_en


def test_proof_snippet_uses_real_name_when_consent_true():
    event = dict(_GOOD_EVENT, consent_for_publication=True, customer_display_name="Real Co Ltd")
    result = proof_snippet_engine.render(event)
    assert result.audience == "public_with_consent"
    assert "Real Co Ltd" in result.snippet_ar
    assert "Real Co Ltd" in result.snippet_en


def test_proof_snippet_blocks_missing_required_fields():
    incomplete = {"event_type": "pilot_delivered", "service_id": "growth_starter"}
    result = proof_snippet_engine.render(incomplete)
    assert result.decision == "blocked"
    assert result.audience == "invalid"
    assert "missing required fields" in result.notes


def test_proof_snippet_renders_default_handle_when_no_customer_field():
    event = dict(_GOOD_EVENT)
    event.pop("customer_anonymized", None)
    result = proof_snippet_engine.render(event)
    assert result.decision == "allowed_draft"
    # Default handle is generic
    assert "Saudi B2B customer" in result.snippet_ar or "Saudi B2B customer" in result.snippet_en


def test_proof_snippet_render_batch_aggregates_counts():
    events = [
        _GOOD_EVENT,
        dict(_GOOD_EVENT, consent_for_publication=True),
        {"event_type": "broken"},  # missing fields → blocked
    ]
    out = proof_snippet_engine.render_batch(events)
    assert out["summary"]["total"] == 3
    assert out["summary"]["public_with_consent"] == 1
    assert out["summary"]["internal_only"] == 1
    assert out["summary"]["blocked"] == 1


def test_proof_snippet_boundaries_advertises_safety_rules():
    b = proof_snippet_engine.boundaries()
    assert b["default_audience"] == "internal_only"
    assert b["default_approval_status"] == "approval_required"
    rules = b["rules"]
    assert rules["customer_name_anonymized_unless_consent"] is True
    assert rules["rejected_if_forbidden_vocabulary"] is True
    assert rules["always_approval_required_before_external_publish"] is True
    assert rules["no_invented_metrics"] is True


# ─── API endpoint tests ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_daily_loop_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/daily-loop")
    assert r.status_code == 200
    payload = r.json()
    assert "decisions" in payload
    assert payload["guardrails"]["no_live_send"] is True


@pytest.mark.asyncio
async def test_proof_snippet_render_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-snippet/render",
            json=_GOOD_EVENT,
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["decision"] == "allowed_draft"
    assert payload["audience"] == "internal_only"


@pytest.mark.asyncio
async def test_proof_snippet_render_batch_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-snippet/render-batch",
            json={"events": [_GOOD_EVENT, dict(_GOOD_EVENT, consent_for_publication=True)]},
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["summary"]["total"] == 2


@pytest.mark.asyncio
async def test_proof_snippet_boundaries_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/proof-snippet/boundaries")
    assert r.status_code == 200
    assert "rules" in r.json()


@pytest.mark.asyncio
async def test_proof_snippet_render_batch_400_on_invalid_payload():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/self-growth/proof-snippet/render-batch",
            json={"not_events": "x"},
        )
    assert r.status_code == 400
