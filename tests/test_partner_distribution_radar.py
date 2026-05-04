"""Tests for self_growth_os.partner_distribution_radar.

The module is a STATIC catalog — no network, no LLM, no DB. Tests
validate:
  - catalog has all required Saudi partner categories per the
    strategic master plan
  - every draft passes the safe-publishing gate (no forbidden claims)
  - every category has both Arabic and English copy
  - approval-required defaults are enforced via summary()
"""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.self_growth_os import partner_distribution_radar
from auto_client_acquisition.self_growth_os.partner_distribution_radar import CATALOG


REQUIRED_CATEGORIES = {
    "b2b_marketing_agency",
    "performance_marketing_agency",
    "sales_consultant",
    "crm_implementer",
    "software_house",
    "accounting_firm",
    "founder_community",
    "hr_recruitment",
}


def test_catalog_has_required_categories():
    ids = {c.category_id for c in CATALOG}
    missing = REQUIRED_CATEGORIES - ids
    assert not missing, f"missing partner categories: {missing}"


def test_every_category_has_arabic_and_english_text():
    for c in CATALOG:
        for field in (c.name_ar, c.fit_reason_ar, c.recommended_offer_ar,
                       c.warm_intro_draft_ar):
            assert field, f"{c.category_id}: missing Arabic field"
        for field in (c.name_en, c.fit_reason_en, c.recommended_offer_en,
                       c.warm_intro_draft_en):
            assert field, f"{c.category_id}: missing English field"


def test_every_warm_intro_draft_passes_safe_publishing_gate():
    """A draft that contains a forbidden token (نضمن, blast, scrape,
    cold outreach, …) must NOT ship in the catalog."""
    result = partner_distribution_radar.safe_drafts()
    assert result["all_safe"] is True, (
        "some catalog warm-intro drafts contain forbidden vocabulary:\n  "
        + "\n  ".join(
            f"{r['category_id']}: ar={r['ar_forbidden_tokens']} "
            f"en={r['en_forbidden_tokens']}"
            for r in result["results"]
            if r["ar_decision"] != "allowed_draft" or r["en_decision"] != "allowed_draft"
        )
    )


def test_summary_records_safety_boundary():
    s = partner_distribution_radar.summary()
    boundary = s["boundary"]
    assert boundary["no_scraping"] is True
    assert boundary["no_auto_dm"] is True
    assert boundary["no_cold_outreach"] is True
    assert boundary["approval_required_for_external_send"] is True
    assert boundary["drafts_only_until_founder_approves"] is True


def test_summary_lists_all_categories():
    s = partner_distribution_radar.summary()
    ids = {c["category_id"] for c in s["categories"]}
    assert ids == REQUIRED_CATEGORIES
    assert s["categories_total"] == len(REQUIRED_CATEGORIES)


def test_get_category_returns_dict():
    cat = partner_distribution_radar.get_category("b2b_marketing_agency")
    assert cat["category_id"] == "b2b_marketing_agency"
    assert cat["service_bundle"] == "partnership_growth"


def test_get_category_unknown_raises():
    with pytest.raises(KeyError):
        partner_distribution_radar.get_category("__not_a_real_category__")


def test_no_category_recommends_unsafe_action():
    """Defensive — every recommended_offer / next_step / risk_notes
    field must NOT contain forbidden vocabulary either."""
    forbidden_tokens = ["scrape", "blast", "guaranteed", "cold whatsapp",
                         "auto-dm", "auto dm"]
    for c in CATALOG:
        text = " ".join([
            c.recommended_offer_ar, c.recommended_offer_en,
            c.next_step, c.risk_notes,
        ]).lower()
        for tok in forbidden_tokens:
            assert tok not in text, (
                f"{c.category_id} recommended/risk field contains "
                f"unsafe token {tok!r}"
            )


# ─── API endpoint tests ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_partner_radar_summary_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/partner-radar")
    assert r.status_code == 200
    payload = r.json()
    assert payload["categories_total"] == 8
    ids = {c["category_id"] for c in payload["categories"]}
    assert ids == REQUIRED_CATEGORIES


@pytest.mark.asyncio
async def test_partner_radar_one_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/partner-radar/sales_consultant")
    assert r.status_code == 200
    payload = r.json()
    assert payload["category_id"] == "sales_consultant"
    assert payload["warm_intro_draft_ar"]
    assert payload["warm_intro_draft_en"]


@pytest.mark.asyncio
async def test_partner_radar_one_404_for_unknown():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/partner-radar/__nope__")
    assert r.status_code == 404


@pytest.mark.asyncio
async def test_partner_radar_safety_check_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/self-growth/partner-radar/drafts/safety-check")
    assert r.status_code == 200
    payload = r.json()
    assert payload["all_safe"] is True
    assert payload["total"] == 8
    assert payload["safe_count"] == 8
