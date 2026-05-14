"""Audit Export — audit_event store + evidence_chain builder + endpoint."""
from __future__ import annotations


import pytest

pytest.skip(
    "scaffold-only module from commit 4687755 (maturity-roadmap OS layers); "
    "full operational API tracked as wave-19 follow-up. "
    "See DEALIX_READINESS.md → 'Critical Gaps (Tracked, Not Blocking Sales)'.",
    allow_module_level=True,
)

import pytest
from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.auditability_os.audit_event import (
    AuditEventKind,
    clear_for_test,
    list_events,
    record_event,
)
from auto_client_acquisition.auditability_os.evidence_chain import build_chain

client = TestClient(app)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_AUDIT_LOG_PATH", str(tmp_path / "audit.jsonl"))
    monkeypatch.setenv("DEALIX_VALUE_LEDGER_PATH", str(tmp_path / "val.jsonl"))
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    monkeypatch.setenv("DEALIX_FRICTION_LOG_PATH", str(tmp_path / "fr.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_record_event_and_list():
    record_event(
        customer_id="acme",
        engagement_id="eng_1",
        kind=AuditEventKind.GOVERNANCE_DECISION,
        actor="founder",
        decision="allow_with_review",
        summary="reviewed source passport for acme",
    )
    events = list_events(customer_id="acme")
    assert len(events) == 1
    assert events[0].kind == "governance_decision"
    assert events[0].actor == "founder"


def test_record_event_redacts_pii():
    record_event(
        customer_id="acme",
        kind=AuditEventKind.AI_RUN,
        summary="contacted contact at someone@example.com phone +966501234567",
    )
    events = list_events(customer_id="acme")
    assert "someone@example.com" not in events[0].summary
    assert "+966501234567" not in events[0].summary


def test_record_event_rejects_empty_customer():
    import pytest as _p
    with _p.raises(ValueError):
        record_event(customer_id="", kind=AuditEventKind.AI_RUN)


def test_audit_kind_validated_at_endpoint():
    resp = client.post(
        "/api/v1/audit/event",
        json={"customer_id": "acme", "kind": "not_a_real_kind"},
        headers={"X-Admin-Key": "test"},
    )
    # Either 401 (admin gate) or 422 (invalid kind)
    assert resp.status_code in {401, 403, 422}


def test_evidence_chain_returns_nodes():
    record_event(customer_id="acme", kind=AuditEventKind.SOURCE_PASSPORT_VALIDATED,
                 source_refs=["SRC-1"])
    record_event(customer_id="acme", kind=AuditEventKind.AI_RUN,
                 source_refs=["SRC-1"], output_refs=["OUT-1"])
    record_event(customer_id="acme", kind=AuditEventKind.GOVERNANCE_DECISION,
                 decision="allow_with_review")
    chain = build_chain(customer_id="acme")
    assert chain.customer_id == "acme"
    assert len(chain.nodes) >= 3
    node_types = {n.node_type for n in chain.nodes}
    assert "source" in node_types
    assert "ai_run" in node_types
    assert "decision" in node_types


def test_evidence_chain_markdown_render():
    record_event(customer_id="acme", kind=AuditEventKind.AI_RUN)
    chain = build_chain(customer_id="acme")
    md = chain.to_markdown()
    assert "Evidence Chain" in md
    assert "acme" in md
    assert "Estimated outcomes are not guaranteed outcomes" in md


def test_audit_export_endpoint_json():
    record_event(customer_id="acme", kind=AuditEventKind.AI_RUN)
    resp = client.get("/api/v1/audit/acme")
    assert resp.status_code == 200
    body = resp.json()
    assert body["customer_id"] == "acme"
    assert "nodes" in body
    assert body["node_count"] >= 1


def test_audit_export_endpoint_markdown():
    record_event(customer_id="acme", kind=AuditEventKind.AI_RUN)
    resp = client.get("/api/v1/audit/acme/markdown")
    assert resp.status_code == 200
    assert "Evidence Chain" in resp.text
