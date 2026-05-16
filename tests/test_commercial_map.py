"""Commercial Map — Wave 14J source of truth."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.service_catalog.registry import OFFERINGS, SERVICE_IDS

client = TestClient(app)


def test_endpoint_lists_all_offerings():
    resp = client.get("/api/v1/commercial-map")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["registry_count"] == len(OFFERINGS)
    ids = {o["service_id"] for o in body["offers"]}
    assert ids == set(SERVICE_IDS)


def test_endpoint_carries_governance_envelope():
    resp = client.get("/api/v1/commercial-map")
    assert resp.status_code == 200
    body = resp.json()
    assert body["governance_decision"] == "allow"


def test_each_offer_has_required_fields():
    body = client.get("/api/v1/commercial-map").json()
    required = {
        "service_id", "name_ar", "name_en", "price_sar", "price_unit",
        "duration_days", "kpi_commitment_ar", "kpi_commitment_en",
        "refund_policy_ar", "refund_policy_en", "deliverables",
        "action_modes_used", "non_negotiables_enforced", "wiring", "notes",
    }
    for offer in body["offers"]:
        missing = required - set(offer.keys())
        assert not missing, f"{offer['service_id']} missing fields: {missing}"


def test_each_offer_has_wiring():
    body = client.get("/api/v1/commercial-map").json()
    for offer in body["offers"]:
        wiring = offer["wiring"]
        assert "landing_url" in wiring, f"{offer['service_id']} has no landing_url"
        assert wiring["landing_url"].startswith("/"), (
            f"{offer['service_id']} landing_url must be a path"
        )


def test_paid_offers_have_checkout_or_founder_issued():
    body = client.get("/api/v1/commercial-map").json()
    for offer in body["offers"]:
        if offer["price_sar"] > 0 and offer["price_unit"] != "custom":
            wiring = offer["wiring"]
            assert wiring.get("checkout_url") or wiring.get("checkout_endpoint"), (
                f"paid offer {offer['service_id']} missing checkout"
            )


def test_every_offer_has_non_negotiables():
    body = client.get("/api/v1/commercial-map").json()
    for offer in body["offers"]:
        assert offer["non_negotiables_enforced"], (
            f"{offer['service_id']} must have non_negotiables_enforced"
        )
        # Every offer forbids cold WhatsApp + scraping + fake proof.
        joined = " ".join(offer["non_negotiables_enforced"])
        assert "no_cold_whatsapp" in joined
        assert "no_scraping" in joined
        assert "no_fake_proof" in joined


def test_markdown_endpoint_is_bilingual():
    resp = client.get("/api/v1/commercial-map/markdown")
    assert resp.status_code == 200
    body = resp.text
    # Bilingual disclaimer footer
    assert "Estimated outcomes are not guaranteed outcomes" in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body
    # Includes the section titles
    assert "Dealix Commercial Wiring Map" in body
    assert "خريطة الربط التجاري" in body
    # Includes all service_ids
    for sid in SERVICE_IDS:
        assert sid in body, f"markdown missing service_id={sid}"


def test_board_memo_offer_links_to_board_decision_os():
    body = client.get("/api/v1/commercial-map").json()
    memo = next(
        o for o in body["offers"] if o["service_id"] == "board_decision_memo"
    )
    assert "board_decision_os" in memo["wiring"]["delivery_module"]


def test_retainer_links_to_workspace_endpoint():
    body = client.get("/api/v1/commercial-map").json()
    retainer = next(
        o for o in body["offers"] if o["service_id"] == "governed_ops_retainer"
    )
    assert "workspace" in retainer["wiring"]["delivery_endpoint"]


def test_diagnostic_offer_links_to_revenue_ops_intake():
    body = client.get("/api/v1/commercial-map").json()
    diagnostic = next(
        o
        for o in body["offers"]
        if o["service_id"] == "governed_revenue_ops_diagnostic"
    )
    assert diagnostic["wiring"]["intake_endpoint"] == (
        "POST /api/v1/revenue-ops/diagnostics"
    )
    assert "decision-passport" in diagnostic["wiring"]["delivery_endpoint"]
