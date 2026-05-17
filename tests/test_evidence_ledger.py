"""Tests for the append-only Evidence Ledger (PR1)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.evidence_control_plane_os.event_store import (
    EvidenceEvent,
    EvidenceLedger,
    get_default_evidence_ledger,
    list_evidence_events,
    record_evidence_event,
    reset_default_evidence_ledger,
)


@pytest.fixture
def ledger(tmp_path) -> EvidenceLedger:
    return EvidenceLedger(base_dir=tmp_path)


@pytest.fixture
def default_ledger(tmp_path, monkeypatch):
    """Point the process-wide ledger singleton at an isolated tmp dir."""
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path))
    reset_default_evidence_ledger()
    yield get_default_evidence_ledger()
    reset_default_evidence_ledger()


def _evt(**kw) -> EvidenceEvent:
    base = dict(event_type="lead_captured", entity_type="lead", entity_id="lead_1")
    base.update(kw)
    return EvidenceEvent(**base)


def test_record_persists_and_lists(ledger: EvidenceLedger):
    ledger.record(_evt())
    rows = ledger.list_events()
    assert len(rows) == 1
    assert rows[0].entity_id == "lead_1"
    assert rows[0].event_id.startswith("ev_")


def test_list_filters_by_entity(ledger: EvidenceLedger):
    ledger.record(_evt(entity_type="lead", entity_id="lead_1"))
    ledger.record(_evt(entity_type="ticket", entity_id="tkt_1", event_type="ticket_created"))
    assert len(ledger.list_events(entity_type="lead")) == 1
    assert len(ledger.list_events(entity_id="tkt_1")) == 1
    assert len(ledger.list_events(event_type="ticket_created")) == 1
    assert len(ledger.list_events()) == 2


def test_is_estimate_round_trips(ledger: EvidenceLedger):
    ledger.record(_evt(is_estimate=True, source="public_diagnostic_estimate",
                        payload={"risk_score": 42}))
    row = ledger.list_events()[0]
    assert row.is_estimate is True
    assert row.source == "public_diagnostic_estimate"
    assert row.payload["risk_score"] == 42


def test_get_by_id_and_missing(ledger: EvidenceLedger):
    stored = ledger.record(_evt())
    assert ledger.get(stored.event_id) is not None
    assert ledger.get("ev_does_not_exist") is None


def test_pii_redacted_before_persistence(ledger: EvidenceLedger):
    ledger.record(_evt(summary_en="contact ahmed@example.com about the deal"))
    row = ledger.list_events()[0]
    assert "ahmed@example.com" not in row.summary_en


def test_ledger_has_no_mutation_methods():
    """Append-only contract: no update/delete/edit path exists."""
    for forbidden in ("update", "delete", "remove", "edit", "patch"):
        assert not hasattr(EvidenceLedger, forbidden)


def test_record_evidence_event_helper(default_ledger):
    ev = record_evidence_event(
        event_type="message_prepared",
        entity_type="lead",
        entity_id="lead_99",
        action="draft_outreach",
    )
    assert ev.event_type == "message_prepared"
    assert any(e.entity_id == "lead_99" for e in list_evidence_events())


async def test_evidence_router_lists_events(async_client, default_ledger):
    record_evidence_event(event_type="lead_captured", entity_type="lead",
                          entity_id="lead_api_1")
    resp = await async_client.get("/api/v1/evidence")
    assert resp.status_code == 200
    body = resp.json()
    assert body["count"] >= 1
    assert any(e["entity_id"] == "lead_api_1" for e in body["events"])


async def test_evidence_router_status(async_client):
    resp = await async_client.get("/api/v1/evidence/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["append_only"] is True
    assert body["guardrails"]["no_update_path"] is True


async def test_evidence_router_get_missing(async_client, default_ledger):
    resp = await async_client.get("/api/v1/evidence/ev_missing")
    assert resp.status_code == 404
