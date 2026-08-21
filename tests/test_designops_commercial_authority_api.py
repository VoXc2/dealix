"""DesignOps HTTP surface must not teach or emit the retired commercial ladder."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import create_app
from api.routers.designops import ProposalPageRequest


def test_proposal_request_default_is_current_paid_motion() -> None:
    request = ProposalPageRequest(customer_handle="ACME")

    assert request.recommended_service == "revenue_command_pilot_30d"
    assert request.timeline_days == 30
    assert request.price_band_sar == "quote_after_discovery"


def test_designops_proposal_normalizes_legacy_price_fields() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/designops/generate/proposal-page",
        json={
            "customer_handle": "ACME",
            "recommended_service": "growth_starter",
            "scope_ar": "Workflow واحد مع baseline وowner وProof.",
            "scope_en": "One workflow with a baseline, owner, and Proof.",
            "timeline_days": 7,
            "price_band_sar": "499",
        },
    )

    assert response.status_code == 200
    body = response.json()
    manifest = body["manifest"]
    blob = body["markdown"] + "\n" + body["html"]

    assert manifest["recommended_service"] == "Revenue Command Pilot"
    assert manifest["timeline_days"] == 30
    assert manifest["price_band_sar"] == "quote_after_discovery"
    assert manifest["quote_only"] is True
    assert manifest["safe_to_send"] is False
    assert "499" not in blob
    assert "Revenue Command Pilot" in blob


def test_designops_proposal_rejects_retired_claim_inside_customer_scope() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/designops/generate/proposal-page",
        json={
            "customer_handle": "ACME",
            "scope_ar": "استخدم /ar/risk-score ثم Data Pack 1500.",
            "scope_en": "Use the retired funnel.",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"] == "proposal contains retired commercial authority"


def test_designops_pricing_endpoint_is_one_product_quote_only() -> None:
    client = TestClient(create_app())
    response = client.post(
        "/api/v1/designops/generate/pricing-page",
        json={"highlight": "growth_starter"},
    )

    assert response.status_code == 200
    body = response.json()
    manifest = body["manifest"]
    blob = body["markdown"] + "\n" + body["html"]

    assert manifest["tier_count"] == 1
    assert manifest["product_count"] == 1
    assert manifest["quote_only"] is True
    assert manifest["public_fixed_price"] is False
    assert "Revenue Command Pilot" in blob
    assert "Growth Starter" not in blob
