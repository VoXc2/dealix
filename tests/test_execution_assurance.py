"""Execution assurance — support red-team, invoice scope gate, health ledger."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from dealix.execution_assurance.health import compute_full_ops_health
from dealix.revenue_ops_autopilot.schemas import EvidenceEvent, FunnelLeadRecord
from dealix.revenue_ops_autopilot.store import reset_autopilot_store_for_tests, uid


@pytest.fixture(autouse=True)
def _isolated_autopilot_store() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        p = Path(fh.name)
    store = reset_autopilot_store_for_tests(path=p)
    yield
    store._path.unlink(missing_ok=True)


_ADMIN = {"X-Admin-API-Key": "dev"}


def test_support_blocks_financial_guarantee_ar():
    from dealix.revenue_ops_autopilot.support_pipeline import analyze_support

    s = analyze_support("هل تضمنون لنا زيادة الإيراد 30٪ العام القادم؟")
    assert s.intent == "unsupported_financial_claim"
    assert s.risk_level == "critical"
    assert s.approval_need == "blocked_escalation"
    assert s.kb_auto_allow is False
    assert "وعداً" in s.suggested_response_ar or "ضماناً" in s.suggested_response_ar


def test_support_faq_diagnostic_kb_auto_allowed():
    from dealix.revenue_ops_autopilot.support_pipeline import analyze_support

    s = analyze_support("ما هي خدمة Diagnostic التي تقدمونها؟")
    assert s.intent == "faq_general"
    assert s.risk_level == "low"
    assert s.approval_need == "founder_review"
    assert s.kb_auto_allow is True
    assert s.kb_source_ids


def test_support_affiliate_misleading_claim_blocked():
    from dealix.revenue_ops_autopilot.support_pipeline import analyze_support

    msg = (
        "Dealix تضمن لك نمو الإيراد وتؤتمت كل مبيعاتك تلقائياً بدون تدخل."
    )
    s = analyze_support(msg)
    assert s.intent == "unsupported_financial_claim"
    assert s.kb_auto_allow is False


def test_invoice_draft_blocked_before_scope_sent_api():
    from api.main import app
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    st = get_autopilot_store()
    st.upsert_lead(
        FunnelLeadRecord(
            id="lea_pre_scope",
            email="founder@example.com",
            company="Acme",
            stage="qualified_A",
        ),
    )
    cli = TestClient(app)
    r = cli.post(
        "/api/v1/invoices/draft",
        headers=_ADMIN,
        json={"lead_id": "lea_pre_scope", "tier": "starter"},
    )
    assert r.status_code == 422, r.text
    body = r.json()
    assert body["detail"]["reason"] == "invoice_draft_blocked_until_scope_sent"


def test_invoice_draft_ok_when_scope_sent():
    from api.main import app
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    st = get_autopilot_store()
    st.upsert_lead(
        FunnelLeadRecord(
            id="lea_scoped",
            email="ops@example.com",
            company="Beta",
            stage="scope_sent",
        ),
    )
    cli = TestClient(app)
    r = cli.post(
        "/api/v1/invoices/draft",
        headers=_ADMIN,
        json={"lead_id": "lea_scoped", "tier": "starter"},
    )
    assert r.status_code == 200, r.text
    assert r.json()["item"]["lead_id"] == "lea_scoped"


def test_full_ops_health_endpoint():
    from api.main import app

    cli = TestClient(app)
    r = cli.get("/api/v1/ops-autopilot/full-ops-health", headers=_ADMIN)
    assert r.status_code == 200, r.text
    data = r.json()
    assert "registry_version" in data
    assert "kpis" in data
    assert data["policy_en"]


def test_compute_full_ops_health_evidence_completeness():
    from dealix.revenue_ops_autopilot.store import get_autopilot_store

    st = get_autopilot_store()
    st.upsert_lead(FunnelLeadRecord(id="l1", email="a@b.co"))
    st.append_evidence(
        EvidenceEvent(
            id=uid("ev"),
            event_type="lead_captured",
            entity_type="funnel_lead",
            entity_id="l1",
            summary="seed",
        ),
    )
    st.upsert_lead(FunnelLeadRecord(id="l2", email="c@d.co"))

    blob = compute_full_ops_health(store=st)
    keys = {k["key"]: k["value"] for k in blob["kpis"]}
    assert keys["evidence_lead_capture_completeness_pct"] == 50.0
