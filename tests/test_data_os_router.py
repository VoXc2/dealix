"""Data OS router — CSV upload + DQ score endpoint."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

_DEMO_CSV = (
    "company_name,sector,city,relationship_status\n"
    "شركة الواحة,b2b_services,Riyadh,warm\n"
    "Madar Logistics,logistics,Jeddah,warm\n"
    "Tameer,real_estate,Jeddah,cold\n"
)


def test_import_preview_raw_csv_no_passport_blocks_or_returns_warning():
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={"customer_handle": "demo", "raw_csv": _DEMO_CSV},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["customer_handle"] == "demo"
    assert body["preview"]["row_count"] == 3
    assert "company_name" in body["preview"]["columns"]
    assert body["governance_decision"] in {"BLOCK", "REQUIRE_APPROVAL", "ALLOW_WITH_REVIEW", "ALLOW"}
    assert body["source_passport"]["provided"] is False
    assert body["is_estimate"] is True


def test_import_preview_with_passport_unblocks():
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={
            "customer_handle": "demo",
            "raw_csv": _DEMO_CSV,
            "passport": {
                "source_id": "SRC-001",
                "source_type": "client_upload",
                "owner": "client",
                "allowed_use": ["internal_analysis", "scoring"],
                "contains_pii": False,
                "sensitivity": "medium",
                "ai_access_allowed": True,
                "external_use_allowed": False,
                "retention_policy": "project_duration",
            },
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["source_passport"]["valid"] is True
    assert body["governance_decision"] in {"ALLOW", "ALLOW_WITH_REVIEW", "DRAFT_ONLY", "REQUIRE_APPROVAL"}


def test_import_preview_oversize_rejected():
    big = "company_name\n" + ("x" * 5_300_000)
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={"customer_handle": "demo", "raw_csv": big},
    )
    assert resp.status_code == 413


def test_import_preview_returns_dq_score():
    resp = client.post(
        "/api/v1/data-os/import-preview",
        json={"customer_handle": "demo", "raw_csv": _DEMO_CSV},
    )
    assert resp.status_code == 200
    body = resp.json()
    dq = body["data_quality_score"]
    assert 0 <= dq["overall"] <= 100
    assert "completeness" in dq
    assert "duplicate_inverse" in dq
