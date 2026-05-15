"""End-to-end Revenue Intelligence → Proof Pack → Founder Summary (MVP)."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app
from api.routers.proof_pack_governed import COMPONENT_KEYS
from api.routers.revenue_intelligence import clear_revenue_intelligence_state_for_tests
from auto_client_acquisition.founder_command_summary import clear_all_for_tests


@pytest.fixture(autouse=True)
def _reset_stores() -> None:
    clear_all_for_tests()
    clear_revenue_intelligence_state_for_tests()
    yield
    clear_all_for_tests()
    clear_revenue_intelligence_state_for_tests()


def test_revenue_intelligence_pipeline_to_founder_summary() -> None:
    client = TestClient(app)
    eid = "e2e_ri_001"
    imp = client.post(
        f"/api/v1/revenue-intelligence/{eid}/import",
        json={
            "client_label": "Test Services Co",
            "source_passport": {
                "source_id": "src-1",
                "owner": "client",
                "allowed_use": ["internal_analysis"],
                "contains_pii": False,
                "relationship_status": "warm_intro",
            },
            "accounts": [
                {
                    "company_name": "Acme KSA",
                    "sector": "technology",
                    "city": "riyadh",
                    "source": "crm_export",
                    "phone": "+966501112233",
                },
                {
                    "company_name": "Beta LLC",
                    "sector": "consulting",
                    "city": "jeddah",
                    "source": "referral",
                },
            ],
        },
    )
    assert imp.status_code == 200
    assert imp.json()["governance_decision"] == "ALLOW"

    sc = client.post(f"/api/v1/revenue-intelligence/{eid}/score")
    assert sc.status_code == 200

    dr = client.post(
        f"/api/v1/revenue-intelligence/{eid}/draft-pack",
        json={"include_whatsapp_draft": True, "relationship_status": "warm_intro"},
    )
    assert dr.status_code == 200
    assert dr.json()["governance_decision"] == "DRAFT_ONLY"

    fn = client.post(f"/api/v1/revenue-intelligence/{eid}/finalize")
    assert fn.status_code == 200

    sections = fn.json()["proof_pack_v2_narrative_sections"]
    components = {k: f"evidence-{k}" for k in COMPONENT_KEYS}
    gen = client.post(
        f"/api/v1/proof-pack/{eid}/generate",
        json={"sections": sections, "components": components},
    )
    assert gen.status_code == 200
    assert gen.json()["proof_score"] >= 70

    rg = client.post(
        f"/api/v1/proof-pack/{eid}/retainer-gate",
        json={
            "client_health": 85,
            "workflow_recurring": True,
            "owner_exists": True,
            "monthly_value_clear": True,
            "stakeholder_engaged": True,
            "governance_risk_controlled": True,
        },
    )
    assert rg.status_code == 200

    fs = client.get("/api/v1/founder-summary")
    assert fs.status_code == 200
    assert fs.json()["brief"]["engagements_count"] >= 1


def test_diagnostic_intent_axes() -> None:
    client = TestClient(app)
    body = {
        "axes_0_5": {k: 3 for k in ("revenue", "data", "workflow", "knowledge", "governance", "reporting")},
    }
    r = client.post("/api/v1/diagnostic/intent", json=body)
    assert r.status_code == 200
    j = r.json()
    assert j["capability_score"] == 60.0
    assert "dtg_decision" in j


def test_draft_pack_doctrine_403() -> None:
    client = TestClient(app)
    eid = "e2e_bad"
    client.post(
        f"/api/v1/revenue-intelligence/{eid}/import",
        json={
            "source_passport": {
                "source_id": "s",
                "owner": "o",
                "allowed_use": ["x"],
                "contains_pii": False,
                "relationship_status": "unknown",
            },
            "accounts": [{"company_name": "X", "sector": "technology", "city": "riyadh", "source": "s"}],
        },
    )
    client.post(f"/api/v1/revenue-intelligence/{eid}/score")
    r = client.post(
        f"/api/v1/revenue-intelligence/{eid}/draft-pack",
        json={"request_cold_whatsapp": True},
    )
    assert r.status_code == 403
