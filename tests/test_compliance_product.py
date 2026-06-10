"""Smoke tests for compliance-product router (P4 Saudi moat)."""

from __future__ import annotations

from starlette.testclient import TestClient

from api.main import app
from api.routers.compliance_product import (
    build_pdpl_checklist,
    build_trust_pack_summary,
    build_zatca_readiness,
)


def test_pdpl_checklist_endpoint():
    client = TestClient(app)
    r = client.get("/api/v1/compliance-product/pdpl-checklist")
    assert r.status_code == 200
    data = r.json()
    assert data["governance_decision"] == "allow"
    assert "ropa" in data
    assert "consent" in data
    assert "dsr" in data
    assert data["ropa"]["activity_count"] >= 1
    assert "access" in data["dsr"]["types"]


def test_trust_pack_endpoint():
    client = TestClient(app)
    r = client.get("/api/v1/compliance-product/trust-pack")
    assert r.status_code == 200
    data = r.json()
    assert data["governance_decision"] == "allow_with_review"
    assert "trust_pack" in data
    assert data["trust_pack"]["sections"]
    assert len(data["enterprise_package_docs"]) >= 1


def test_zatca_readiness_endpoint():
    client = TestClient(app)
    r = client.get("/api/v1/compliance-product/zatca-readiness")
    assert r.status_code == 200
    data = r.json()
    assert data["governance_decision"] == "allow"
    assert "phase_2_e_invoice" in data
    assert data["retention_years"] == 6


def test_build_helpers_smoke():
    pdpl = build_pdpl_checklist()
    assert pdpl["consent"]["lawful_bases"]
    trust = build_trust_pack_summary()
    assert trust["non_negotiables_count"] == 11
    zatca = build_zatca_readiness()
    assert zatca["router_ref"] == "/api/v1/zatca"
