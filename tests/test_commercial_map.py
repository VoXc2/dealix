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


def test_retainer_offer_links_to_workspace_endpoint():
    body = client.get("/api/v1/commercial-map").json()
    retainer = next(
        o for o in body["offers"] if o["service_id"] == "governed_ops_retainer"
    )
    assert "workspace" in retainer["wiring"]["delivery_endpoint"]


def test_diagnostic_offer_links_to_sample_preview():
    body = client.get("/api/v1/commercial-map").json()
    diagnostic = next(
        o for o in body["offers"] if o["service_id"] == "diagnostic_starter"
    )
    assert diagnostic["wiring"]["sample_endpoint"] == "GET /api/v1/sprint/sample"
    assert diagnostic["wiring"]["preview_url"] == "/sprint-sample.html"


def test_offer_notes_reflect_governed_revenue_ladder():
    """Notes describe the Governed Revenue & AI Ops ladder (Rung 0 -> Retainer)."""
    body = client.get("/api/v1/commercial-map").json()
    notes_by_id = {o["service_id"]: o["notes"] for o in body["offers"]}

    free = notes_by_id["governed_revenue_risk_score"]
    assert "Rung 0" in free
    assert "Risk Score" in free
    assert "Sample Proof Pack" in free

    diagnostic = notes_by_id["diagnostic_starter"]
    assert "7-Day Governed Revenue & AI Ops Diagnostic" in diagnostic
    for tier in ("4,999", "9,999", "15,000", "25,000"):
        assert tier in diagnostic

    sprint = notes_by_id["revenue_intelligence_sprint"]
    assert "Revenue Intelligence Sprint" in sprint

    retainer = notes_by_id["governed_ops_retainer"]
    assert "Governed Ops Retainer" in retainer
    assert "4,999" in retainer
    assert "35,000" in retainer


def test_every_offer_keeps_non_negotiables_after_ladder_update():
    """The ladder narrative update must not strip any offer's hard gates."""
    body = client.get("/api/v1/commercial-map").json()
    for offer in body["offers"]:
        assert offer["non_negotiables_enforced"], (
            f"{offer['service_id']} lost non_negotiables_enforced"
        )
