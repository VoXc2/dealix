"""Postgres ↔ autopilot bridge + marketing factory."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from dealix.execution_assurance.health import compute_full_ops_health
from dealix.marketing_factory.store import reset_marketing_store_for_tests
from dealix.marketing_factory.utm import build_utm_url
from dealix.marketing_factory.weekly_pack import generate_weekly_pack
from dealix.revenue_ops_autopilot.external_ingest import (
    autopilot_id_for_pg_lead,
    ingest_postgres_lead_fields,
    postgres_row_to_capture_payload,
)
from dealix.revenue_ops_autopilot.store import get_autopilot_store, reset_autopilot_store_for_tests


@pytest.fixture(autouse=True)
def _isolated_stores() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        ap = Path(fh.name)
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh2:
        mk = Path(fh2.name)
    reset_autopilot_store_for_tests(path=ap)
    reset_marketing_store_for_tests(path=mk)
    yield
    ap.unlink(missing_ok=True)
    mk.unlink(missing_ok=True)


def test_autopilot_id_stable():
    assert autopilot_id_for_pg_lead("lead_gads_abc") == "lea_ext_lead_gads_abc"


def test_postgres_payload_includes_utm_in_pain():
    p = postgres_row_to_capture_payload(
        pg_lead_id="x1",
        source="meta_lead_ads",
        contact_name="Sami",
        contact_email="s@example.com",
        company_name="Co",
        message="hello",
        utm_source="meta",
        utm_campaign="lead_ads",
    )
    assert p["id"] == "lea_ext_x1"
    assert "utm_source=meta" in p["pain"]


def test_ingest_idempotent():
    st = get_autopilot_store()
    a = ingest_postgres_lead_fields(
        pg_lead_id="pg99",
        source="google_ads",
        contact_name="Layla",
        contact_email="l@example.com",
        company_name="Acme",
        message="inbound",
        store=st,
    )
    b = ingest_postgres_lead_fields(
        pg_lead_id="pg99",
        source="google_ads",
        contact_name="Layla",
        contact_email="l@example.com",
        company_name="Acme",
        message="inbound",
        store=st,
    )
    assert a.id == b.id
    assert len(st.list_leads(limit=50)) == 1


def test_build_utm_url():
    url = build_utm_url(
        "https://dealix.ai/dealix-diagnostic",
        utm_source="dealix",
        utm_medium="social",
        utm_campaign="w1",
    )
    assert "utm_campaign=w1" in url
    assert "utm_source=dealix" in url


def test_weekly_pack_has_slots():
    pack = generate_weekly_pack()
    assert pack["slot_count"] >= 3
    assert pack["slots"][0]["utm_campaign"]


def test_marketing_calendar_api(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "dev")
    from fastapi.testclient import TestClient

    from api.main import app

    cli = TestClient(app)
    r = cli.get("/api/v1/ops-autopilot/marketing/calendar", headers={"X-Admin-API-Key": "dev"})
    assert r.status_code == 200, r.text
    assert "items" in r.json()


def test_health_includes_marketing_kpis():
    st = get_autopilot_store()
    ingest_postgres_lead_fields(
        pg_lead_id="utm_lead",
        source="meta_lead_ads",
        contact_email="m@example.com",
        message="test",
        utm_source="meta",
        store=st,
    )
    blob = compute_full_ops_health(store=st)
    keys = {k["key"] for k in blob["kpis"]}
    assert "marketing_calendar_ready_pct" in keys
    assert "inbound_lead_utm_tag_pct" in keys
