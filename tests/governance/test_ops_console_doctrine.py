"""Doctrine assertions for the Ops Console domain (/api/v1/ops/*).

حوكمة غرفة التشغيل — التحقق من الالتزام بالعقيدة.

Asserts:
  * every surface emits a `governance_decision`;
  * projected/computed numbers carry `is_estimate` (only confirmed paid
    revenue may be `is_estimate: False`);
  * the evidence ledger never leaks raw (un-redacted) PII;
  * a missing module degrades a sub-section to 200 + `note`, never a 500.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import app

ADMIN_KEY = "test-ops-admin-key"
HEADERS = {"X-Admin-API-Key": ADMIN_KEY}

GET_SURFACES = [
    "/api/v1/ops/command-center",
    "/api/v1/ops/catalog",
    "/api/v1/ops/market-proof",
    "/api/v1/ops/revenue",
    "/api/v1/ops/evidence",
    "/api/v1/ops/evidence/levels",
    "/api/v1/ops/billing",
    "/api/v1/ops/board",
    "/api/v1/ops/proof-pack/template",
]


@pytest.fixture()
def client(monkeypatch, tmp_path):
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "friction.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "value.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "capital.jsonl"))
    return TestClient(app)


def test_every_surface_emits_governance_decision(client):
    for path in GET_SURFACES:
        body = client.get(path, headers=HEADERS).json()
        assert body.get("governance_decision") == "allow", path
        assert "is_estimate" in body, path


def test_billing_numbers_carry_is_estimate(client):
    body = client.get("/api/v1/ops/billing", headers=HEADERS).json()
    # Confirmed paid revenue is ground truth.
    assert body["confirmed_revenue_sar"]["is_estimate"] is False
    # Drafted-invoice intent and unit economics are estimates.
    assert body["invoice_intent_total_sar"]["is_estimate"] is True
    assert body["unit_economics"]["is_estimate"] is True


def test_revenue_conversion_is_estimate(client):
    body = client.get("/api/v1/ops/revenue", headers=HEADERS).json()
    assert body["conversion_rates"]["is_estimate"] is True


def test_proof_pack_preview_is_governed(client):
    body = client.post(
        "/api/v1/ops/proof-pack/preview",
        json={"company": "Doctrine Co", "sector": "b2b_services"},
        headers=HEADERS,
    ).json()
    assert body["governance_decision"] == "allow"
    assert "is_estimate" in body
    # Proof-pack sections are never auto-filled from fabricated content.
    assert "never auto-generated" in body["note"]


def test_evidence_ledger_redacts_pii(client, monkeypatch, tmp_path):
    """A proof event containing an email must not leak that email."""
    pii_email = "private.lead@pii-example-domain.com"
    try:
        from auto_client_acquisition.proof_ledger import file_backend
        from auto_client_acquisition.proof_ledger.schemas import (
            ProofEvent,
            ProofEventType,
        )

        isolated = file_backend.FileProofLedger(base_dir=str(tmp_path / "proof"))
        monkeypatch.setattr(file_backend, "_DEFAULT", isolated)
        isolated.record(
            ProofEvent(
                event_type=ProofEventType.LEAD_INTAKE,
                customer_handle="DoctrineTest",
                summary_en=f"Follow up with the lead at {pii_email} this week.",
                summary_ar=f"تابع مع العميل عبر {pii_email} هذا الأسبوع.",
            )
        )
    except Exception:  # noqa: BLE001
        pytest.skip("proof ledger unavailable in this environment")

    body = client.get("/api/v1/ops/evidence", headers=HEADERS).json()
    assert pii_email not in repr(body)
    assert body["proof_events"]["count"] >= 1


def test_command_center_degrades_when_module_unavailable(client, monkeypatch):
    """A failing dependency degrades a sub-section, not the whole response."""
    import auto_client_acquisition.revenue_pipeline.pipeline as pipeline_mod

    def _boom(*_args, **_kwargs):
        raise RuntimeError("simulated outage")

    monkeypatch.setattr(pipeline_mod, "get_default_pipeline", _boom)
    resp = client.get("/api/v1/ops/command-center", headers=HEADERS)
    assert resp.status_code == 200
    assert resp.json()["pipeline"].get("note") == "revenue_pipeline_unavailable"
