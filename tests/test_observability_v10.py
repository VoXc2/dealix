"""Observability v10 — trace schema + buffer tests (Phase B v10)."""
from __future__ import annotations

import threading

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from api.main import create_app
from auto_client_acquisition.observability_v10 import (
    SpanRecord,
    TraceRecordV10,
    _reset_v10_buffer,
    list_v10_traces,
    record_v10_trace,
    summarize_traces,
    validate_trace,
)


def _make_record(**overrides) -> dict:
    base = {
        "correlation_id": "cor_unit_test_0001",
        "customer_id": "cust_anon_42",
        "agent_id": "agent_drafter",
        "workflow_id": "wf_outreach",
        "action_mode": "draft_only",
        "approval_status": "pending",
        "risk_level": "low",
        "model_name": "balanced-drafter-bi",
        "prompt_version": "v1",
        "input_tokens": 100,
        "output_tokens": 50,
        "estimated_cost_usd": 0.002,
        "latency_ms": 12.5,
        "risk_score": 0.10,
        "proof_event_id": "",
        "redacted_payload": {"summary": "lead intake"},
    }
    base.update(overrides)
    return base


@pytest.fixture(autouse=True)
def _clean_buffer():
    _reset_v10_buffer()
    yield
    _reset_v10_buffer()


def _client() -> TestClient:
    return TestClient(create_app())


def test_trace_record_v10_has_all_required_fields():
    rec = TraceRecordV10(correlation_id="cor_x")
    fields = set(rec.model_fields.keys())
    expected = {
        "trace_id",
        "correlation_id",
        "customer_id",
        "agent_id",
        "workflow_id",
        "action_mode",
        "approval_status",
        "risk_level",
        "model_name",
        "prompt_version",
        "input_tokens",
        "output_tokens",
        "estimated_cost_usd",
        "latency_ms",
        "risk_score",
        "proof_event_id",
        "redacted_payload",
        "created_at",
    }
    assert expected <= fields
    assert rec.trace_id.startswith("trc_")


def test_validate_trace_redacts_pii_in_redacted_payload():
    rec = validate_trace(
        _make_record(
            redacted_payload={
                "note": "Contact ahmed@example.com on +966501234567 about lead 42",
            }
        )
    )
    note = rec.redacted_payload["note"]
    assert "+966501234567" not in note
    assert "ahmed@example.com" not in note
    assert "***REDACTED_PHONE***" in note


def test_validate_trace_rejects_unknown_fields():
    with pytest.raises(ValidationError):
        validate_trace(_make_record(rogue_field="not allowed"))


def test_record_and_list_roundtrip():
    stored = record_v10_trace(_make_record())
    rows = list_v10_traces(limit=10)
    assert len(rows) == 1
    assert rows[0].trace_id == stored.trace_id
    assert rows[0].correlation_id == "cor_unit_test_0001"


def test_record_v10_trace_redacts_pii_on_insert():
    stored = record_v10_trace(
        _make_record(
            redacted_payload={
                "raw": "phone +966501234567 / email user@example.com",
            }
        )
    )
    raw = stored.redacted_payload["raw"]
    assert "+966501234567" not in raw
    assert "user@example.com" not in raw


def test_summarize_traces_returns_counts_by_action_mode():
    record_v10_trace(_make_record(action_mode="draft_only"))
    record_v10_trace(_make_record(action_mode="draft_only", correlation_id="cor_2"))
    record_v10_trace(_make_record(action_mode="propose_action", correlation_id="cor_3"))

    rows = list_v10_traces(limit=10)
    summary = summarize_traces(rows)
    assert summary["trace_count"] == 3
    assert summary["by_action_mode"]["draft_only"] == 2
    assert summary["by_action_mode"]["propose_action"] == 1
    assert summary["total_cost_usd"] >= 0.0
    assert summary["avg_latency_ms"] >= 0.0


def test_summarize_traces_handles_empty_list():
    summary = summarize_traces([])
    assert summary["trace_count"] == 0
    assert summary["total_cost_usd"] == 0.0
    assert summary["avg_latency_ms"] == 0.0


def test_buffer_is_thread_safe_under_parallel_writes():
    n_threads = 12
    per_thread = 20

    def _writer(idx: int) -> None:
        for i in range(per_thread):
            record_v10_trace(
                _make_record(correlation_id=f"cor_t{idx}_e{i}")
            )

    threads = [threading.Thread(target=_writer, args=(t,)) for t in range(n_threads)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    rows = list_v10_traces(limit=n_threads * per_thread + 10)
    assert len(rows) == n_threads * per_thread
    ids = {r.trace_id for r in rows}
    assert len(ids) == n_threads * per_thread


def test_span_record_validates_status_literal():
    span = SpanRecord(
        trace_id="trc_abc",
        name="route",
        start_ms=0.0,
        end_ms=5.0,
        attributes={"tier": "cheap"},
        status="ok",
    )
    assert span.status == "ok"
    with pytest.raises(ValidationError):
        SpanRecord(
            trace_id="trc_abc",
            name="route",
            start_ms=0.0,
            end_ms=5.0,
            status="bogus",  # type: ignore[arg-type]
        )


def test_router_status_advertises_pii_redacted_on_insert():
    resp = _client().get("/api/v1/observability-v10/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "observability_v10"
    assert body["guardrails"]["pii_redacted_on_insert"] is True
    assert body["guardrails"]["no_external_http"] is True
    assert body["guardrails"]["otel_aligned"] is True


def test_router_post_validate_with_valid_body_returns_200():
    resp = _client().post(
        "/api/v1/observability-v10/trace/validate",
        json=_make_record(),
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["correlation_id"] == "cor_unit_test_0001"


def test_router_post_validate_with_extra_field_returns_422():
    resp = _client().post(
        "/api/v1/observability-v10/trace/validate",
        json=_make_record(rogue="bad"),
    )
    assert resp.status_code == 422


def test_router_post_record_redacts_pii_on_insert():
    resp = _client().post(
        "/api/v1/observability-v10/trace/record",
        json=_make_record(
            redacted_payload={"raw": "email user@example.com phone +966501234567"},
        ),
    )
    assert resp.status_code == 200
    body = resp.json()
    raw = body["redacted_payload"]["raw"]
    assert "+966501234567" not in raw
    assert "user@example.com" not in raw


def test_router_get_schema_returns_valid_json_schema():
    resp = _client().get("/api/v1/observability-v10/schema")
    assert resp.status_code == 200
    body = resp.json()
    # Pydantic v2 emits a JSON-schema-style object with type+properties.
    assert "properties" in body
    assert "correlation_id" in body["properties"]
    assert "estimated_cost_usd" in body["properties"]


def test_router_get_traces_returns_recent():
    record_v10_trace(_make_record())
    record_v10_trace(_make_record(correlation_id="cor_2"))
    resp = _client().get("/api/v1/observability-v10/traces?limit=10")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] == 2
