"""The /api/v1/evidence/events endpoint must reject illegal CEL transitions."""

from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.revenue_memory.event_store import reset_default_store

client = TestClient(app)


def _setup() -> None:
    reset_default_store()


def test_legal_transition_is_recorded() -> None:
    _setup()
    resp = client.post(
        "/api/v1/evidence/events",
        json={
            "customer_id": "cust_ev1",
            "subject_type": "account",
            "subject_id": "acc_ev1",
            "next_state": "prepared_not_sent",
        },
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["commercial_state"] == "prepared_not_sent"
    assert body["cel"] == "CEL2"
    assert body["event_type"] == "commercial.prepared"


def test_illegal_transition_returns_422() -> None:
    _setup()
    # Jumping straight to `sent` with no `prepared_not_sent` first is illegal.
    resp = client.post(
        "/api/v1/evidence/events",
        json={
            "customer_id": "cust_ev2",
            "subject_type": "account",
            "subject_id": "acc_ev2",
            "next_state": "sent",
            "founder_confirmed": True,
        },
    )
    assert resp.status_code == 422, resp.text
    assert "illegal_transition" in str(resp.json()["detail"])


def test_sent_without_founder_confirmed_returns_422() -> None:
    _setup()
    prep = client.post(
        "/api/v1/evidence/events",
        json={
            "customer_id": "cust_ev3",
            "subject_type": "account",
            "subject_id": "acc_ev3",
            "next_state": "prepared_not_sent",
        },
    )
    assert prep.status_code == 200, prep.text
    # `sent` without founder_confirmed violates hard rule 1.
    resp = client.post(
        "/api/v1/evidence/events",
        json={
            "customer_id": "cust_ev3",
            "subject_type": "account",
            "subject_id": "acc_ev3",
            "next_state": "sent",
            "founder_confirmed": False,
        },
    )
    assert resp.status_code == 422, resp.text
    assert "founder_confirmed" in str(resp.json()["detail"])


def test_unknown_field_is_rejected() -> None:
    _setup()
    resp = client.post(
        "/api/v1/evidence/events",
        json={
            "customer_id": "cust_ev4",
            "subject_id": "acc_ev4",
            "next_state": "prepared_not_sent",
            "rogue_field": "x",
        },
    )
    assert resp.status_code == 422, resp.text
