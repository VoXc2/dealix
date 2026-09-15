"""Commercial map contract for the current launch-authorized buying path.

The compatibility endpoint is intentionally no longer a public fixed-price
service catalog. It exposes the canonical Free Mini Diagnostic -> qualified
discovery -> customer-specific intervention path and
must remain fail-closed on public checkout/pricing authority.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def _body() -> dict:
    resp = client.get("/api/v1/commercial-map")
    assert resp.status_code == 200, resp.text
    return resp.json()


def test_endpoint_exposes_current_launch_authority() -> None:
    body = _body()
    assert body["authority"] == "launch_commercial_truth"
    assert body["entry_offer"]["id"] == "free_mini_diagnostic"
    assert body["primary_offer"]["id"] == "revenue_command_pilot_30d"


def test_primary_offer_is_quote_only_and_customer_specific_duration() -> None:
    body = _body()
    offer = body["primary_offer"]
    assert offer["duration_days"] is None
    assert offer["duration_model"] == "customer_specific_after_qualified_discovery"
    assert offer["price_model"] == "customer_specific_quote_only"
    assert offer["public_fixed_pricing"] is False
    assert offer["public_checkout"] is False


def test_entry_offer_is_free_without_public_checkout() -> None:
    body = _body()
    entry = body["entry_offer"]
    assert entry["price_model"] == "free"
    assert entry["public_checkout"] is False


def test_buying_path_preserves_truth_order() -> None:
    body = _body()
    assert body["buying_path"] == [
        "FREE_MINI_DIAGNOSTIC",
        "QUALIFIED_DISCOVERY",
        "CUSTOMER_SPECIFIC_QUOTE",
        "CUSTOMER_SPECIFIC_INTERVENTION",
        "VERIFIED_PAYMENT",
        "DELIVERY",
        "CUSTOMER_VALIDATED_PROOF",
        "STOP_EXPAND_REDESIGN",
    ]


def test_governance_envelope_is_fail_closed() -> None:
    body = _body()
    guardrails = body["guardrails"]
    for key in (
        "no_public_fixed_price",
        "no_public_checkout",
        "quote_requires_qualified_discovery",
        "quote_requires_explicit_authority",
        "invoice_requires_approved_quote_fingerprint",
        "invoice_requires_approval_record_before_persistence",
        "invoice_draft_is_idempotent",
        "invoice_is_not_payment",
        "payment_requires_independent_evidence",
        "no_automatic_discount",
        "no_automatic_payment",
    ):
        assert guardrails[key] is True


def test_markdown_endpoint_matches_quote_only_authority() -> None:
    resp = client.get("/api/v1/commercial-map/markdown")
    assert resp.status_code == 200
    body = resp.text
    assert "Free Mini Diagnostic" in body
    assert "Qualified Discovery" in body
    assert "Customer-Specific Quote" in body
    assert "Customer-Specific Intervention" in body
    assert "Verified Payment" in body
    assert "Customer-Validated Proof" in body
    assert "Public fixed pricing: false" in body
    assert "Public checkout: false" in body
    assert "Invoice is not payment." in body


def test_compatibility_endpoint_does_not_resurrect_retired_catalog_shape() -> None:
    body = _body()
    for retired_key in ("offers", "registry_count", "service_ids", "checkout_url"):
        assert retired_key not in body
