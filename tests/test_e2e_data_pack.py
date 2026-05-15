"""End-to-end commercial proof — the 1,500 SAR Data-to-Revenue Pack.

Walks the governed delivery chain a real customer experiences, through
real in-process API endpoints:

  CSV upload  ->  Data Quality Score  ->  Source-Passport governance gate
              ->  value event (tier discipline)  ->  Monthly Value Report
              ->  Trust Pack

If this test passes, the Data Pack service is deliverable end-to-end —
not merely documented.
"""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

_CUSTOMER = "e2e_datapack_co"
_CSV = (
    "company_name,sector,city,relationship_status\n"
    "شركة الواحة,b2b_services,Riyadh,warm\n"
    "Madar Logistics,logistics,Jeddah,warm\n"
    "Tameer,real_estate,Jeddah,cold\n"
)
_PASSPORT = {
    "source_id": "SRC-E2E-1",
    "source_type": "client_upload",
    "owner": "client",
    "allowed_use": ["internal_analysis", "scoring"],
    "contains_pii": False,
    "sensitivity": "medium",
    "ai_access_allowed": True,
    "external_use_allowed": False,
    "retention_policy": "project_duration",
}


def test_step1_csv_upload_returns_dq_score() -> None:
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={"customer_handle": _CUSTOMER, "raw_csv": _CSV},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["preview"]["row_count"] == 3
    dq = body["data_quality_score"]
    assert 0 <= dq["overall"] <= 100
    # No Source Passport -> estimate only, governance must not be a clean allow.
    assert body["is_estimate"] is True
    assert body["source_passport"]["provided"] is False


def test_step2_passport_unblocks_governed_scoring() -> None:
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={
            "customer_handle": _CUSTOMER,
            "raw_csv": _CSV,
            "passport": _PASSPORT,
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["source_passport"]["valid"] is True
    assert body["governance_decision"] in {"allow", "allow_with_review"}
    assert body["next_step_recommendation"]


def test_step3_oversize_upload_is_rejected() -> None:
    big = "company_name\n" + ("x" * 5_300_000)
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={"customer_handle": _CUSTOMER, "raw_csv": big},
    )
    assert resp.status_code == 413


def test_step4_value_event_tier_discipline_enforced() -> None:
    # Estimated value is always accepted.
    ok = client.post(
        f"/api/v1/value/event/{_CUSTOMER}",
        json={"kind": "pipeline_uplift", "amount": 25000, "tier": "estimated"},
    )
    assert ok.status_code == 200, ok.text

    # Verified value WITHOUT a source ref must be refused (no fake proof).
    bad = client.post(
        f"/api/v1/value/event/{_CUSTOMER}",
        json={"kind": "revenue", "amount": 25000, "tier": "verified", "source_ref": ""},
    )
    assert bad.status_code == 422, bad.text


def test_step5_monthly_report_carries_governance_and_limitations() -> None:
    resp = client.get(f"/api/v1/value/{_CUSTOMER}/report/monthly/markdown")
    assert resp.status_code == 200, resp.text
    md = resp.text
    assert "## Limitations" in md
    assert "Estimated value is not Verified value" in md
    assert "القيمة التقديرية ليست قيمة مُتحقَّقة" in md


def test_step6_trust_pack_renders() -> None:
    resp = client.get(f"/api/v1/value/trust-pack/{_CUSTOMER}/markdown")
    assert resp.status_code == 200, resp.text
    assert len(resp.text.strip()) > 0
