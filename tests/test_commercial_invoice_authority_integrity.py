"""Fail-closed and exact-once coverage for quote-bound invoice drafts."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine

from auto_client_acquisition.approval_center import get_default_approval_store
from dealix.revenue_ops_autopilot.postgres_store import AutopilotPostgresStore
from dealix.revenue_ops_autopilot.schemas import (
    EvidenceEvent,
    FunnelLeadRecord,
    InvoiceDraftRecord,
)
from dealix.revenue_ops_autopilot.store import (
    get_autopilot_store,
    reset_autopilot_store_for_tests,
)

_ADMIN = {"X-Admin-API-Key": "dev"}


@pytest.fixture(autouse=True)
def _isolated_commercial_stores() -> None:
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as fh:
        path = Path(fh.name)
    path.unlink(missing_ok=True)
    store = reset_autopilot_store_for_tests(path=path)
    approvals = get_default_approval_store()
    approvals.clear()
    yield
    approvals.clear()
    store._path.unlink(missing_ok=True)


def _quote_facts(lead_id: str, *, amount_sar: float = 12345.67) -> dict[str, object]:
    return {
        "lead_id": lead_id,
        "approved_amount_sar": amount_sar,
        "qualified_discovery_ref": "discovery:test:invoice-integrity",
        "customer_specific_scope_ref": "scope:test:invoice-integrity",
    }


def _invoice_payload(
    lead_id: str,
    quote_authority_ref: str,
    *,
    idempotency_key: str = "invoice-retry-0001",
    amount_sar: float = 12345.67,
) -> dict[str, object]:
    return {
        **_quote_facts(lead_id, amount_sar=amount_sar),
        "quote_authority_ref": quote_authority_ref,
        "idempotency_key": idempotency_key,
    }


def _authorized_quote(cli: TestClient, lead_id: str) -> str:
    store = get_autopilot_store()
    store.upsert_lead(FunnelLeadRecord(id=lead_id, stage="scope_sent"))
    requested = cli.post(
        "/api/v1/quotes/authority/request",
        headers=_ADMIN,
        json=_quote_facts(lead_id),
    )
    assert requested.status_code == 200, requested.text
    approval_id = str(requested.json()["quote_authority_ref"])
    approved = cli.post(
        f"/api/v1/approvals/{approval_id}/approve",
        json={"who": "founder-test"},
    )
    assert approved.status_code == 200, approved.text
    assert approved.json()["approval"]["status"] == "approved"
    return approval_id


def test_invoice_payload_requires_explicit_idempotency_key() -> None:
    from api.main import create_app

    cli = TestClient(create_app())
    approval_id = _authorized_quote(cli, "lead_missing_idempotency")
    payload = _invoice_payload("lead_missing_idempotency", approval_id)
    payload.pop("idempotency_key")

    response = cli.post("/api/v1/invoices/draft", headers=_ADMIN, json=payload)

    assert response.status_code == 422, response.text
    assert get_autopilot_store().list_invoice_drafts() == []


def test_invoice_approval_failure_does_not_persist_invoice_or_evidence(monkeypatch) -> None:
    from api.main import create_app

    cli = TestClient(create_app())
    approval_id = _authorized_quote(cli, "lead_approval_failure")
    approvals = get_default_approval_store()
    original_create = approvals.create

    def _fail_invoice_approval(req):
        if req.object_type == "invoice_draft":
            raise RuntimeError("forced approval persistence failure")
        return original_create(req)

    monkeypatch.setattr(approvals, "create", _fail_invoice_approval)
    response = cli.post(
        "/api/v1/invoices/draft",
        headers=_ADMIN,
        json=_invoice_payload("lead_approval_failure", approval_id),
    )

    assert response.status_code == 503, response.text
    assert response.json()["detail"]["reason"] == "approval_center_unavailable"
    store = get_autopilot_store()
    assert store.list_invoice_drafts() == []
    assert not any(
        event.event_type == "invoice_draft_created_from_verified_quote_fingerprint"
        for event in store.list_evidence(limit=500)
    )


def test_invoice_retry_is_exactly_once_with_durable_provenance() -> None:
    from api.main import create_app

    cli = TestClient(create_app())
    approval_id = _authorized_quote(cli, "lead_idempotent_invoice")
    payload = _invoice_payload("lead_idempotent_invoice", approval_id)

    first = cli.post("/api/v1/invoices/draft", headers=_ADMIN, json=payload)
    second = cli.post("/api/v1/invoices/draft", headers=_ADMIN, json=payload)

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    first_data = first.json()
    second_data = second.json()
    assert first_data["item"]["id"] == second_data["item"]["id"]
    assert first_data["authority"]["idempotent_replay"] is False
    assert second_data["authority"]["idempotent_replay"] is True
    assert first_data["authority"]["approval_idempotent_replay"] is False
    assert second_data["authority"]["approval_idempotent_replay"] is True

    stored = get_autopilot_store().list_invoice_drafts(limit=100)
    assert len(stored) == 1
    invoice = stored[0]
    assert invoice.quote_authority_ref == approval_id
    assert len(invoice.quote_fingerprint) == 64
    assert invoice.idempotency_key == "invoice-retry-0001"
    assert invoice.approval_id == first_data["authority"]["invoice_approval_id"]
    assert invoice.quote_authority_state == "verified_approval_center_fingerprint"

    invoice_events = [
        event
        for event in get_autopilot_store().list_evidence(limit=500)
        if event.event_type == "invoice_draft_created_from_verified_quote_fingerprint"
    ]
    assert len(invoice_events) == 1
    invoice_approvals = [
        approval
        for approval in get_default_approval_store().list_history(limit=500)
        if approval.object_type == "invoice_draft"
    ]
    assert len(invoice_approvals) == 1


def test_different_idempotency_keys_produce_distinct_drafts() -> None:
    from api.main import create_app

    cli = TestClient(create_app())
    approval_id = _authorized_quote(cli, "lead_distinct_invoices")
    first = cli.post(
        "/api/v1/invoices/draft",
        headers=_ADMIN,
        json=_invoice_payload(
            "lead_distinct_invoices",
            approval_id,
            idempotency_key="invoice-retry-A001",
        ),
    )
    second = cli.post(
        "/api/v1/invoices/draft",
        headers=_ADMIN,
        json=_invoice_payload(
            "lead_distinct_invoices",
            approval_id,
            idempotency_key="invoice-retry-B001",
        ),
    )

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert first.json()["item"]["id"] != second.json()["item"]["id"]
    assert len(get_autopilot_store().list_invoice_drafts(limit=100)) == 2


def _invoice_record(*, amount_sar: float = 100.0) -> InvoiceDraftRecord:
    return InvoiceDraftRecord(
        id="inv_exact_once",
        lead_id="lead_store",
        amount_sar=amount_sar,
        qualified_discovery_ref="discovery:store",
        customer_specific_scope_ref="scope:store",
        quote_authority_ref="apr_quote_store",
        quote_fingerprint="a" * 64,
        idempotency_key="store-retry-0001",
        approval_id="apr_invoice_store",
        quote_authority_state="verified_approval_center_fingerprint",
    )


def _invoice_event(*, summary: str = "stable") -> EvidenceEvent:
    return EvidenceEvent(
        id="ev_invoice_exact_once",
        event_type="invoice_draft_created_from_verified_quote_fingerprint",
        entity_type="invoice_draft",
        entity_id="inv_exact_once",
        summary=summary,
        approval_id="apr_invoice_store",
    )


def test_postgres_snapshot_idempotency_and_conflict_rollback() -> None:
    engine = create_engine("sqlite:///:memory:", future=True)
    store = AutopilotPostgresStore(engine=engine, create_tables=True)

    first, created_first = store.create_invoice_draft_idempotent(
        _invoice_record(),
        evidence=_invoice_event(),
    )
    second, created_second = store.create_invoice_draft_idempotent(
        _invoice_record(),
        evidence=_invoice_event(),
    )

    assert first.id == second.id == "inv_exact_once"
    assert created_first is True
    assert created_second is False
    assert len(store.list_invoice_drafts()) == 1
    assert len(store.list_evidence()) == 1

    with pytest.raises(ValueError, match="invoice_idempotency_conflict"):
        store.create_invoice_draft_idempotent(
            _invoice_record(amount_sar=101.0),
            evidence=_invoice_event(summary="conflicting"),
        )

    remaining = store.list_invoice_drafts()
    assert len(remaining) == 1
    assert remaining[0].amount_sar == 100.0
    assert len(store.list_evidence()) == 1
