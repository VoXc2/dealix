"""Proposal renderer + service-setup endpoint."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext,
    render_proposal,
)

client = TestClient(app)


def test_render_proposal_bilingual_with_disclaimer():
    md = render_proposal(
        ProposalContext(
            customer_name="شركة الواحة",
            customer_handle="alwaha",
            sector="b2b_services",
            city="Riyadh",
            engagement_id="eng_001",
            price_sar=499,
        )
    )
    assert "Revenue Intelligence" in md or "ذكاء الإيراد" in md
    assert "499" in md
    # Bilingual disclaimer
    assert "Estimated outcomes are not guaranteed outcomes" in md
    assert "النتائج التقديرية" in md
    # Non-negotiables present (either by exact var-name OR by descriptive text)
    md_low = md.lower()
    assert "scraping" in md_low
    assert "whatsapp" in md_low
    assert "linkedin" in md_low
    assert "guarantee" in md_low or "guaranteed" in md_low


def test_render_proposal_includes_retainer_path():
    md = render_proposal(
        ProposalContext(
            customer_name="Alwaha",
            customer_handle="alwaha",
            sector="b2b_services",
            city="Riyadh",
            engagement_id="eng_001",
        )
    )
    md_low = md.lower()
    assert ("managed revenue ops" in md_low) or ("managed_revenue_ops" in md_low) or ("retainer" in md_low)


def test_proposal_endpoint_returns_bilingual_markdown():
    resp = client.post(
        "/api/v1/service-setup/proposal/alwaha",
        json={
            "customer_name": "Alwaha Consulting",
            "customer_handle": "alwaha",
            "sector": "b2b_services",
            "city": "Riyadh",
            "engagement_id": "eng_001",
            "price_sar": 499,
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["customer_id"] == "alwaha"
    assert "Revenue Intelligence" in body["proposal_markdown"]
    assert body["governance_decision"] == "allow_with_review"


def test_proposal_endpoint_rejects_mismatched_handle():
    resp = client.post(
        "/api/v1/service-setup/proposal/alwaha",
        json={
            "customer_name": "X",
            "customer_handle": "different",
            "sector": "b2b_services",
            "city": "Riyadh",
            "engagement_id": "eng_002",
        },
    )
    assert resp.status_code == 400


def test_qualify_endpoint_rejects_cold_whatsapp():
    resp = client.post(
        "/api/v1/service-setup/qualify",
        json={
            "pain_clear": True, "owner_present": True, "data_available": True,
            "accepts_governance": True, "has_budget": True,
            "wants_safe_methods": True, "proof_path_visible": True,
            "retainer_path_visible": True,
            "raw_request_text": "We want cold WhatsApp automation",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["decision"] == "reject"
    assert any("whatsapp" in v for v in body["doctrine_violations"])
