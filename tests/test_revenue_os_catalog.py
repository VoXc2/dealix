"""API tests for Revenue OS catalog router."""

from __future__ import annotations

from starlette.testclient import TestClient

from api.main import app


def test_revenue_os_catalog_endpoint():
    client = TestClient(app)
    r = client.get("/api/v1/revenue-os/catalog")
    assert r.status_code == 200
    data = r.json()
    assert "source_registry" in data
    assert "cold_whatsapp" in data["forbidden_sources"]
    assert "enrichment_waterfall_order" in data
    assert data["factory_blueprint_endpoint"] == "/api/v1/revenue-os/factory/blueprint"


def test_factory_blueprint_endpoint_shape():
    client = TestClient(app)
    r = client.get("/api/v1/revenue-os/factory/blueprint")
    assert r.status_code == 200
    data = r.json()
    assert data["primary_offer"]["name"] == "7-Day Governed Revenue & AI Ops Diagnostic"
    assert len(data["layers"]) == 7
    assert len(data["automation_workflows"]) == 18
    assert data["execution_targets"]["day_30_targets"]["paid_diagnostics"] == 1
    assert data["execution_targets"]["day_90_targets"]["diagnostics_range"] == [3, 5]


def test_factory_blueprint_governance_guards_present():
    client = TestClient(app)
    data = client.get("/api/v1/revenue-os/factory/blueprint").json()
    guards = set(data["non_negotiables"])
    assert "no_external_send_without_founder_approval" in guards
    assert "no_revenue_mark_before_payment_proof" in guards

    approval_rows = {row["action"]: row for row in data["approval_matrix"]}
    assert approval_rows["send_invoice"]["needs_founder"] is True
    assert approval_rows["create_crm_contact"]["needs_founder"] is False

    levels = data["automation_levels"]
    assert "send_external_message" in levels["founder_approval"]
    assert "score_lead" in levels["autopilot"]


def test_normalize_signals_endpoint():
    client = TestClient(app)
    body = {
        "signals": [
            {
                "source_type": "founder_observation",
                "sector_hint": "real_estate",
                "company_placeholder": "Slot-X",
                "signal_type": "hiring_sales_team",
                "signal_text_redacted": "Public note redacted",
                "confidence": 0.8,
                "why_now": "",
                "public_only": True,
                "contains_personal_data": False,
                "risk_flags": [],
            }
        ]
    }
    r = client.post("/api/v1/revenue-os/signals/normalize", json=body)
    assert r.status_code == 200
    out = r.json()
    assert len(out["signals"]) == 1
    assert out["signals"][0]["proof_target"]
    assert "cold_whatsapp" in out["signals"][0]["blocked_actions"]
    assert out["rollup"]["total"] == 1


def test_anti_waste_blocks_external_without_passport():
    client = TestClient(app)
    r = client.post(
        "/api/v1/revenue-os/anti-waste/check",
        json={
            "has_decision_passport": False,
            "lead_source": "website_inquiry",
            "action_external": True,
            "upsell_attempt": False,
            "proof_event_count": 0,
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert any(v["code"] == "no_passport_no_action" for v in data["violations"])


def test_expansion_gated_without_proof():
    client = TestClient(app)
    r = client.post(
        "/api/v1/revenue-os/expansion/next-offer",
        json={
            "primary_pain_keyword": "data crm",
            "sector": "consulting",
            "max_proof_level": 0,
            "proof_event_count": 0,
        },
    )
    assert r.status_code == 200
    assert r.json()["gated"] is True


def test_dedupe_hint_json():
    client = TestClient(app)
    r = client.post(
        "/api/v1/revenue-os/dedupe/hint",
        json={
            "company_name": "شركة التقنية المتقدمة",
            "domain": "https://www.example.sa/contact",
            "phone": "+966501112233",
        },
    )
    assert r.status_code == 200
    assert "fingerprint_key" in r.json()


def test_pricing_power_demo():
    client = TestClient(app)
    r = client.get("/api/v1/revenue-os/scores/pricing-power-demo")
    assert r.status_code == 200
    assert "pricing_power_score" in r.json()


def test_learning_weekly_template():
    client = TestClient(app)
    r = client.get("/api/v1/revenue-os/learning/weekly-template")
    assert r.status_code == 200
    assert "what_worked_ar" in r.json()
