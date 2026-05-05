"""Phase 11 — observability_v6 trace/audit/incident tests."""
from __future__ import annotations

import threading

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.main import create_app
from auto_client_acquisition.observability_v6 import (
    AuditEvent,
    Incident,
    IncidentSeverity,
    TraceRecord,
    build_correlation_id,
    list_audit,
    list_incidents,
    record_audit,
    record_incident,
)
from auto_client_acquisition.observability_v6.audit_event import _reset_audit_buffer
from auto_client_acquisition.observability_v6.incident import _reset_incident_buffer


def _make_trace(**overrides) -> TraceRecord:
    base = {
        "correlation_id": build_correlation_id(),
        "audit_id": "aud_test_0001",
        "agent_run_id": "run_test_0001",
        "tenant_id": "tenant_anon",
        "object_id": "obj_lead_42",
        "action_mode": "draft_only",
        "approval_status": "pending",
        "risk_level": "low",
        "proof_event_id": None,
        "latency_ms": 12.5,
        "cost": None,
        "error_type": None,
    }
    base.update(overrides)
    return TraceRecord(**base)


def _make_event(summary: str, **overrides) -> AuditEvent:
    return AuditEvent(
        source_module="unit_test",
        action_summary=summary,
        trace=_make_trace(**overrides),
    )


@pytest.fixture(autouse=True)
def _clean_buffers():
    _reset_audit_buffer()
    _reset_incident_buffer()
    yield
    _reset_audit_buffer()
    _reset_incident_buffer()


def test_build_correlation_id_returns_unique_prefixed_ids():
    a = build_correlation_id()
    b = build_correlation_id()
    assert a.startswith("cor_")
    assert b.startswith("cor_")
    assert a != b
    # uuid4 hex => 32 chars after the prefix
    assert len(a) == len("cor_") + 32


def test_record_audit_and_list_audit_roundtrip():
    evt = _make_event("Built draft for tenant")
    stored = record_audit(evt)
    assert stored.id == evt.id
    rows = list_audit(limit=10)
    assert len(rows) == 1
    assert rows[0].id == evt.id
    assert rows[0].source_module == "unit_test"
    assert rows[0].trace.correlation_id == evt.trace.correlation_id


def test_pii_in_action_summary_is_redacted_at_record_time():
    raw_summary = (
        "Contacted ahmed@example.com on phone +966501234567 about lead 42"
    )
    evt = _make_event(raw_summary)
    stored = record_audit(evt)
    assert "+966501234567" not in stored.action_summary
    assert "ahmed@example.com" not in stored.action_summary
    assert "***REDACTED_PHONE***" in stored.action_summary
    # the email local part is masked: a***@example.com
    assert "@example.com" in stored.action_summary
    assert "ahmed@" not in stored.action_summary

    # And the buffer copy is also redacted (no raw PII can survive).
    [from_buffer] = list_audit(limit=10)
    assert "+966501234567" not in from_buffer.action_summary
    assert "ahmed@example.com" not in from_buffer.action_summary


def test_record_incident_and_list_incidents_roundtrip():
    inc = Incident(
        severity=IncidentSeverity.P1,
        title="draft sent to wrong customer",
        summary_ar="مسودة أُرسلت للعميل الخاطئ",
        summary_en="draft sent to wrong customer",
    )
    stored = record_incident(inc)
    assert stored.id == inc.id
    rows = list_incidents()
    assert len(rows) == 1
    assert rows[0].id == inc.id
    assert rows[0].severity == IncidentSeverity.P1


def test_list_incidents_severity_filter_only_returns_matching():
    record_incident(
        Incident(
            severity=IncidentSeverity.P0,
            title="live action without approval",
            summary_ar="إجراء مباشر بدون موافقة",
            summary_en="live action without approval",
        )
    )
    record_incident(
        Incident(
            severity=IncidentSeverity.P2,
            title="daily digest failed",
            summary_ar="فشل الملخص اليومي",
            summary_en="daily digest failed",
        )
    )
    record_incident(
        Incident(
            severity=IncidentSeverity.P3,
            title="typo in brief",
            summary_ar="خطأ مطبعي",
            summary_en="typo in brief",
        )
    )

    p0_only = list_incidents(severity_filter=IncidentSeverity.P0)
    assert len(p0_only) == 1
    assert p0_only[0].severity == IncidentSeverity.P0

    p2_only = list_incidents(severity_filter=IncidentSeverity.P2)
    assert len(p2_only) == 1
    assert p2_only[0].severity == IncidentSeverity.P2

    all_three = list_incidents()
    assert len(all_three) == 3


def test_audit_buffer_thread_safe_under_parallel_writes():
    n_threads = 16
    per_thread = 25

    def _writer(idx: int) -> None:
        for i in range(per_thread):
            record_audit(_make_event(f"thread-{idx}-event-{i}"))

    threads = [threading.Thread(target=_writer, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    rows = list_audit(limit=n_threads * per_thread + 10)
    assert len(rows) == n_threads * per_thread
    # All ids must be unique — proves no torn writes.
    ids = {r.id for r in rows}
    assert len(ids) == n_threads * per_thread


def test_router_status_returns_200_with_guardrails():
    client = TestClient(create_app())
    resp = client.get("/api/v1/observability/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "observability_v6"
    assert body["guardrails"]["no_external_telemetry"] is True
    assert body["guardrails"]["no_pii_in_audit"] is True
    assert body["guardrails"]["append_only"] is True
    assert body["guardrails"]["thread_safe"] is True


def test_router_post_incident_with_rogue_field_returns_422():
    client = TestClient(create_app())
    resp = client.post(
        "/api/v1/observability/incident",
        json={
            "severity": "P1",
            "title": "test",
            "summary_ar": "اختبار",
            "summary_en": "test",
            "rogue_field": "not allowed",
        },
    )
    assert resp.status_code == 422


def test_router_post_incident_then_list_via_endpoint():
    client = TestClient(create_app())
    payload = {
        "severity": "P0",
        "title": "PII leak",
        "summary_ar": "تسرب بيانات شخصية",
        "summary_en": "PII leak",
        "root_cause": "missing redactor in export path",
        "customer_impact": "one customer affected",
    }
    create_resp = client.post("/api/v1/observability/incident", json=payload)
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["severity"] == "P0"
    assert created["id"].startswith("inc_")

    list_resp = client.get("/api/v1/observability/incidents?severity=P0")
    assert list_resp.status_code == 200
    body = list_resp.json()
    assert body["count"] == 1
    assert body["severity_filter"] == "P0"
    assert body["incidents"][0]["id"] == created["id"]


def test_trace_record_is_frozen_and_extra_forbidden():
    trace = _make_trace()
    with pytest.raises(ValidationError):
        trace.__class__(  # extra='forbid'
            correlation_id="cor_x",
            audit_id="a",
            agent_run_id="r",
            tenant_id="t",
            object_id="o",
            action_mode="read_only",
            approval_status="none",
            risk_level="low",
            latency_ms=1.0,
            unknown_field="x",
        )
    # frozen — assignment forbidden.
    with pytest.raises(ValidationError):
        trace.latency_ms = 9999  # type: ignore[misc]
