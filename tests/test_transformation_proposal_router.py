"""API tests — Transformation OS endpoints on the commercial router."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_transformation_proposal_generate_returns_approval_gated():
    resp = client.post(
        "/api/v1/commercial/transformation-proposal/generate",
        json={
            "company_name": "Acme Clinics",
            "sector": "healthcare_clinic",
            "selected_system_ids": ["whatsapp_revenue_os", "ai_command_center_os"],
            "stakeholders": ["CEO", "COO"],
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["approval_status"] == "approval_required"
    assert body["is_estimate"] is True
    assert len(body["line_items"]) == 2
    assert body["total_setup_sar_min"] > 0


def test_transformation_proposal_markdown_is_bilingual():
    resp = client.post(
        "/api/v1/commercial/transformation-proposal/generate/markdown",
        json={"company_name": "Beta", "selected_system_ids": ["brand_intelligence_os"]},
    )
    assert resp.status_code == 200, resp.text
    text = resp.text
    assert "Dealix Transformation Proposal" in text
    assert "عرض التحول" in text
    assert "Estimated value is not Verified value" in text


def test_transformation_proposal_rejects_guaranteed_claims():
    resp = client.post(
        "/api/v1/commercial/transformation-proposal/generate",
        json={
            "company_name": "Beta",
            "selected_system_ids": ["whatsapp_revenue_os"],
            "notes": "We guarantee +300% revenue",
        },
    )
    assert resp.status_code == 400, resp.text


def test_transformation_proposal_empty_selection_is_400():
    resp = client.post(
        "/api/v1/commercial/transformation-proposal/generate",
        json={"company_name": "Beta", "selected_system_ids": []},
    )
    assert resp.status_code == 400, resp.text


def test_roi_estimate_returns_ranges():
    resp = client.post(
        "/api/v1/commercial/roi/estimate",
        json={
            "company_name": "Acme",
            "manual_hours_per_week": 20,
            "hourly_cost_sar": 80,
            "lost_leads_per_month": 10,
            "avg_deal_value_sar": 5000,
            "recovered_conversion_pct": 15,
            "setup_cost_sar": 35000,
            "monthly_cost_sar": 8000,
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "internal_estimate_only"
    assert body["customer_value_claim"] is False
    assert body["guarantee"] is False
    result = body["result"]
    assert result["is_estimate"] is True
    assert result["gross_annual_value_sar_min"] <= result["gross_annual_value_sar_max"]
    assert result["annual_cost_sar"] == 35000 + 12 * 8000
