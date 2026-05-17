"""Tests for the Public Diagnostic Funnel APIs (PR4).

All endpoints must be reachable with no Authorization header, must not
fabricate persisted data, and the risk score must always be tagged as
an estimate.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.evidence_control_plane_os.event_store import (
    reset_default_evidence_ledger,
)
from auto_client_acquisition.knowledge.article_store import reset_default_article_store
from auto_client_acquisition.knowledge.gaps import reset_default_gap_store
from auto_client_acquisition.support.ticket_store import reset_default_ticket_store


@pytest.fixture
def funnel_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path / "ev"))
    monkeypatch.setenv("DEALIX_SUPPORT_DIR", str(tmp_path / "support"))
    monkeypatch.setenv("DEALIX_KNOWLEDGE_DIR", str(tmp_path / "kb"))
    reset_default_evidence_ledger()
    reset_default_ticket_store()
    reset_default_article_store()
    reset_default_gap_store()
    yield
    reset_default_evidence_ledger()
    reset_default_ticket_store()
    reset_default_article_store()
    reset_default_gap_store()


_LEAD = {
    "name": "Sami Test",
    "company": "Test Co",
    "email": "sami@testco.sa",
    "consent": True,
}


async def test_lead_endpoint_needs_no_auth(async_client, funnel_env):
    resp = await async_client.post("/api/v1/public/leads", json=_LEAD)
    assert resp.status_code == 200  # no Authorization header sent
    assert resp.json()["ok"] is True


async def test_lead_requires_consent(async_client, funnel_env):
    payload = {**_LEAD}
    payload["consent"] = False
    resp = await async_client.post("/api/v1/public/leads", json=payload)
    assert resp.status_code == 422
    assert resp.json()["detail"] == "consent_required"


async def test_lead_requires_core_fields(async_client, funnel_env):
    resp = await async_client.post("/api/v1/public/leads", json={"consent": True})
    assert resp.status_code == 422


async def test_lead_honeypot_silently_drops(async_client, funnel_env):
    resp = await async_client.post(
        "/api/v1/public/leads", json={**_LEAD, "website": "spam"}
    )
    assert resp.status_code == 200
    assert "lead_id" not in resp.json()


async def test_risk_score_is_always_an_estimate(async_client, funnel_env):
    resp = await async_client.post(
        "/api/v1/public/risk-score",
        json={"company": "Test Co", "role": "CEO", "has_crm": True,
              "uses_ai": True, "region": "Saudi Arabia", "budget": "10000"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["is_estimate"] is True
    assert body["source"] == "public_diagnostic_estimate"
    assert 0 <= body["score"] <= 100
    assert body["band"] in {"low", "medium", "high"}


async def test_proof_pack_sample_is_synthetic(async_client, funnel_env):
    resp = await async_client.get("/api/v1/public/proof-pack/sample")
    assert resp.status_code == 200
    body = resp.json()
    assert body["sample"] is True
    assert body["source"] == "synthetic_sample"
    assert body["sections"]


async def test_public_support_opens_ticket(async_client, funnel_env):
    resp = await async_client.post(
        "/api/v1/public/support",
        json={"subject": "question", "message": "how do I get started onboarding",
              "email": "sami@testco.sa"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["ok"] is True
    assert body["ticket_id"].startswith("tkt_")


async def test_public_support_requires_message(async_client, funnel_env):
    resp = await async_client.post("/api/v1/public/support", json={"subject": "x"})
    assert resp.status_code == 422


async def test_public_services_lists_priced_offerings(async_client, funnel_env):
    resp = await async_client.get("/api/v1/public/services")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 1
    assert all("price_sar" in s for s in body["services"])
