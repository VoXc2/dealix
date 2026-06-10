"""Tests for revenue learning loop (P7 intelligence)."""

from __future__ import annotations

from pathlib import Path

import pytest
from starlette.testclient import TestClient

from api.main import app
from dealix.commercial_ops.revenue_learning_loop import (
    _source_ref_is_real,
    build_weekly_learning_report,
)


def test_source_ref_placeholder_blocked():
    assert _source_ref_is_real("crm:hubspot:export:2026-W20") is True
    assert _source_ref_is_real("crm:export:not_synced_yet") is False
    assert _source_ref_is_real("") is False


def test_build_weekly_learning_report_structure(tmp_path: Path):
    csv_path = tmp_path / "evidence.csv"
    csv_path.write_text(
        "event_id,event_date,event_type,company,contact,motion,offer_id,owner,source_channel,notes\n"
        "e1,2026-05-18,scope_requested,Acme Co,,motion_a,ten_lead_audit,founder,manual,real deal\n"
        "e2,2026-05-18,demo_booked,Acme Co,,motion_a,,founder,manual,follow-up\n",
        encoding="utf-8",
    )
    report = build_weekly_learning_report(evidence_path=csv_path)
    assert report["period"].startswith("20")
    assert report["governance_decision"] == "allow_with_review"
    assert report["evidence_summary"]["real_company_events"] == 2
    assert "crm_numbers_policy" in report
    assert report["kpi_values_available"] == []


def test_weekly_filled_endpoint_requires_admin(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test-learning-admin")
    client = TestClient(app)
    denied = client.get("/api/v1/revenue-os/learning/weekly-filled")
    assert denied.status_code == 401
    ok = client.get(
        "/api/v1/revenue-os/learning/weekly-filled",
        headers={"X-Admin-API-Key": "test-learning-admin"},
    )
    assert ok.status_code == 200
    body = ok.json()
    assert body["period"]
    assert "funnel_metrics" in body
    assert "kpi_registry" in body
