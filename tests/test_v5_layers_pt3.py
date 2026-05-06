"""Tests for v5 layers part 3:
   customer_data_plane + finance_os + delivery_factory.

Pure unit + ASGI tests. No network, no DB writes (in-memory only).
"""
from __future__ import annotations

import os

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.customer_data_plane import (
    ChannelKind,
    ConsentRegistry,
    ContactabilityVerdict,
    contactability_check,
    redact_email,
    redact_phone,
    redact_text,
)
from auto_client_acquisition.customer_data_plane.consent_registry import (
    get_default_registry,
)
from auto_client_acquisition.customer_data_plane.pii_redactor import redact_dict
from auto_client_acquisition.customer_data_plane.schemas import ConsentSource
from auto_client_acquisition.delivery_factory import (
    build_delivery_plan,
    list_available_services,
)
from auto_client_acquisition.finance_os import (
    draft_invoice,
    finance_guardrails,
    get_pricing_tier,
    is_live_charge_allowed,
    pricing_catalog,
)


# ════════════════════ customer_data_plane ════════════════════


def _fresh_registry() -> ConsentRegistry:
    reg = ConsentRegistry()
    return reg


def test_consent_grant_and_status():
    reg = _fresh_registry()
    reg.grant(contact_id="cust-1", channel=ChannelKind.WHATSAPP_TEMPLATE)
    status, rec = reg.status_for("cust-1", ChannelKind.WHATSAPP_TEMPLATE)
    assert status.value == "granted"
    assert rec is not None and rec.is_active()


def test_consent_unknown_returns_unknown():
    reg = _fresh_registry()
    status, rec = reg.status_for("never-seen", ChannelKind.EMAIL_DRAFT)
    assert status.value == "unknown"
    assert rec is None


def test_consent_withdraw_propagates():
    reg = _fresh_registry()
    reg.grant(contact_id="cust-2", channel=ChannelKind.WHATSAPP_TEMPLATE)
    out = reg.withdraw("cust-2", ChannelKind.WHATSAPP_TEMPLATE)
    assert len(out) == 1
    assert out[0].withdrawal_timestamp is not None
    status, _ = reg.status_for("cust-2", ChannelKind.WHATSAPP_TEMPLATE)
    assert status.value == "withdrawn"


def test_consent_withdraw_all_channels():
    reg = _fresh_registry()
    reg.grant(contact_id="cust-3", channel=ChannelKind.WHATSAPP_TEMPLATE)
    reg.grant(contact_id="cust-3", channel=ChannelKind.EMAIL_DRAFT)
    out = reg.withdraw("cust-3")  # no channel = all
    assert len(out) == 2


def test_contactability_inbound_always_safe():
    reg = _fresh_registry()
    result = contactability_check("anon", ChannelKind.WHATSAPP_INBOUND, reg)
    assert result.verdict == ContactabilityVerdict.SAFE.value


def test_contactability_default_deny_unknown_consent():
    reg = _fresh_registry()
    result = contactability_check("anon", ChannelKind.WHATSAPP_TEMPLATE, reg)
    assert result.verdict == ContactabilityVerdict.BLOCKED.value
    assert "default deny" in result.reason


def test_contactability_safe_after_consent():
    reg = _fresh_registry()
    reg.grant(contact_id="cust-4", channel=ChannelKind.EMAIL_DRAFT)
    result = contactability_check("cust-4", ChannelKind.EMAIL_DRAFT, reg)
    assert result.verdict == ContactabilityVerdict.SAFE.value
    assert result.consent_known is True


def test_contactability_blocked_after_withdraw():
    reg = _fresh_registry()
    reg.grant(contact_id="cust-5", channel=ChannelKind.EMAIL_DRAFT)
    reg.withdraw("cust-5")
    result = contactability_check("cust-5", ChannelKind.EMAIL_DRAFT, reg)
    assert result.verdict == ContactabilityVerdict.BLOCKED.value


def test_contactability_blocked_channel_returns_blocked():
    reg = _fresh_registry()
    result = contactability_check("anon", ChannelKind.BLOCKED, reg)
    assert result.verdict == ContactabilityVerdict.BLOCKED.value


def test_contactability_linkedin_manual_needs_review():
    reg = _fresh_registry()
    result = contactability_check("anon", ChannelKind.LINKEDIN_MANUAL, reg)
    assert result.verdict == ContactabilityVerdict.NEEDS_REVIEW.value


# ─── Redactor ─────────────────────────────────────────────────────


def test_redact_email():
    out = redact_email("contact me at ahmad@example.sa today")
    assert "ahmad@example.sa" not in out
    assert "@example.sa" in out


def test_redact_phone_saudi_formats():
    cases = ["+966501234567", "00966501234567", "0501234567"]
    for c in cases:
        assert "REDACTED_PHONE" in redact_phone(f"call {c} now")


def test_redact_text_combines_all():
    raw = "Email a@b.sa, phone +966501234567, ID 1234567890"
    out = redact_text(raw)
    assert "a@b.sa" not in out
    assert "+966501234567" not in out
    assert "1234567890" not in out


def test_redact_dict_recurses():
    raw = {
        "name": "Ahmad",
        "email": "ahmad@example.sa",
        "nested": {"phone": "+966501234567"},
        "list": ["+966501234567", "safe text"],
    }
    out = redact_dict(raw)
    assert "ahmad@example.sa" not in str(out)
    assert "+966501234567" not in str(out)
    assert out["name"] == "Ahmad"  # name regex doesn't match plain words


# ════════════════════ finance_os ════════════════════


def test_pricing_catalog_returns_5_tiers():
    cat = pricing_catalog()
    ids = {t["tier_id"] for t in cat}
    assert ids == {
        "diagnostic", "growth_starter_pilot", "data_to_revenue",
        "executive_growth_os", "partnership_growth",
    }


def test_pilot_price_is_499():
    tier = get_pricing_tier("growth_starter_pilot")
    assert tier["price_sar"] == 499.0
    assert tier["pricing_basis"] == "one_shot"


def test_diagnostic_is_free():
    tier = get_pricing_tier("diagnostic")
    assert tier["price_sar"] == 0.0
    assert tier["pricing_basis"] == "free"


def test_executive_growth_os_is_recurring():
    tier = get_pricing_tier("executive_growth_os")
    assert tier["pricing_basis"] == "recurring_monthly"
    assert tier["price_sar"] == 2999.0


def test_unknown_tier_raises():
    with pytest.raises(KeyError):
        get_pricing_tier("__not_real__")


def test_draft_invoice_uses_catalog_price():
    draft = draft_invoice(
        tier_id="growth_starter_pilot",
        customer_email="ahmad@example.sa",
        customer_handle="ACME-001",
    )
    assert draft.amount_sar == 499.0
    assert draft.tier_id == "growth_starter_pilot"
    assert draft.approval_status == "approval_required"
    args = draft.to_cli_args()
    assert "--amount-sar" in args
    assert "499" in args


def test_draft_invoice_refuses_free_tier():
    with pytest.raises(ValueError):
        draft_invoice(tier_id="diagnostic", customer_email="x@y.sa")


def test_finance_guardrails_documents_the_rules():
    g = finance_guardrails()
    rules = g["rules"]
    assert rules["no_moyasar_allow_live_charge_env"] is True
    assert rules["cli_refuses_live_key_without_allow_live"] is True
    assert rules["no_auto_charge"] is True
    assert rules["amount_cap_per_invoice_sar"] == 50000


def test_is_live_charge_allowed_returns_false_no_matter_what(monkeypatch):
    """Even with sk_live_ + DEALIX_ALLOW_LIVE_CHARGE=1, the helper
    returns allowed=False — there is no env flag for auto-charge."""
    monkeypatch.setenv("MOYASAR_SECRET_KEY", "sk_live_dangerous")
    monkeypatch.setenv("DEALIX_ALLOW_LIVE_CHARGE", "1")
    res = is_live_charge_allowed()
    assert res["allowed"] is False
    assert res["key_mode"] == "live"


# ════════════════════ delivery_factory ════════════════════


def test_list_available_services_returns_32():
    services = list_available_services()
    assert len(services) == 32


def test_build_delivery_plan_for_partial_service():
    """Verify build_delivery_plan against a service that is still
    in development. After PR #166 (Phase K1), `lead_intake_whatsapp`
    flipped to `live`, so this test now uses `enrichment` — which
    remains `partial` until PR #168 lands the provider abstraction
    + confidence-score test.
    """
    plan = build_delivery_plan("enrichment").to_dict()
    assert plan["service_id"] == "enrichment"
    assert plan["status"] == "partial"
    # YAML lists required_inputs for this service → intake checklist items.
    assert len(plan["intake_checklist"]) >= 1
    # workflow_steps lists steps → bilingual rows.
    assert len(plan["workflow_plan_ar"]) >= 1
    assert len(plan["workflow_plan_en"]) >= 1


def test_build_delivery_plan_for_lead_intake_whatsapp_now_live():
    """Verify the LIVE-flipped lead_intake_whatsapp still produces a
    valid delivery plan with status=live and that blocked_actions
    propagate (cold_outreach_whatsapp must remain blocked even when
    the service is live)."""
    plan = build_delivery_plan("lead_intake_whatsapp").to_dict()
    assert plan["service_id"] == "lead_intake_whatsapp"
    assert plan["status"] == "live"
    assert "cold_outreach_whatsapp" in plan["blocked_actions"]


def test_delivery_plan_carries_safety_notes():
    plan = build_delivery_plan("qualification").to_dict()
    notes = plan["safety_notes"]
    assert "no_cold_outreach" in notes
    assert "no_scraping" in notes


def test_delivery_plan_qa_checklist_includes_proof_metric_check():
    plan = build_delivery_plan("lead_intake_whatsapp").to_dict()
    qa_text = "\n".join(plan["qa_checklist"])
    assert "proof_metrics" in qa_text or "proof" in qa_text.lower()


def test_unknown_service_raises():
    with pytest.raises(KeyError):
        build_delivery_plan("__not_a_service__")


def test_delivery_plan_has_bilingual_workflow_rows():
    plan = build_delivery_plan("close").to_dict()
    if plan["workflow_plan_ar"]:
        assert plan["workflow_plan_ar"][0].startswith("1.")
    if plan["workflow_plan_en"]:
        assert plan["workflow_plan_en"][0].startswith("1.")


# ════════════════════ API endpoint tests ════════════════════


@pytest.fixture(autouse=True)
def _clear_default_registry():
    """Ensure each endpoint test starts with an empty default registry."""
    get_default_registry().clear()
    yield
    get_default_registry().clear()


@pytest.mark.asyncio
async def test_consent_grant_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-data/consent/grant",
            json={
                "contact_id": "test-1",
                "channel": "email_draft",
                "source": "website_form",
            },
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["consent_status"] == "granted"


@pytest.mark.asyncio
async def test_contactability_endpoint_blocks_unknown():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-data/contactability/check",
            json={"contact_id": "anon", "channel": "whatsapp_template"},
        )
    assert r.status_code == 200
    assert r.json()["verdict"] == "blocked"


@pytest.mark.asyncio
async def test_redact_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/customer-data/redact",
            json={"text": "email a@b.sa phone +966501234567"},
        )
    assert r.status_code == 200
    out = r.json()["redacted"]
    assert "a@b.sa" not in out
    assert "+966501234567" not in out


@pytest.mark.asyncio
async def test_finance_pricing_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/finance/pricing")
    assert r.status_code == 200
    payload = r.json()
    assert payload["count"] == 5


@pytest.mark.asyncio
async def test_finance_invoice_draft_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/finance/invoice/draft",
            json={
                "tier_id": "growth_starter_pilot",
                "customer_email": "x@y.sa",
                "customer_handle": "ACME-001",
            },
        )
    assert r.status_code == 200
    payload = r.json()
    assert payload["amount_sar"] == 499.0
    assert payload["approval_status"] == "approval_required"


@pytest.mark.asyncio
async def test_finance_invoice_draft_400_on_free_tier():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.post(
            "/api/v1/finance/invoice/draft",
            json={"tier_id": "diagnostic", "customer_email": "x@y.sa"},
        )
    assert r.status_code == 400


@pytest.mark.asyncio
async def test_delivery_factory_plan_endpoint():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/delivery-factory/plan/lead_intake_whatsapp")
    assert r.status_code == 200
    payload = r.json()
    assert payload["service_id"] == "lead_intake_whatsapp"
    assert payload["safety_notes"]


@pytest.mark.asyncio
async def test_delivery_factory_404_unknown():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/delivery-factory/plan/__nope__")
    assert r.status_code == 404
