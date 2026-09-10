"""``/api/v1/pricing/usage`` decides what a customer is billed.

It takes ``customer_handle`` from the request body and records a billable
metered event against it. It carried no route-level authentication, so it sat
behind the shared platform API key alone — a credential that is neither an
admin credential nor tenant-bound. Any holder could add billable
``laas_per_reply`` / ``laas_per_demo`` events to any customer's account, or
inflate their own.

``docs/ops/LAAS_INVOICING_SOP.md`` documented it as admin-only from the start.
The code did not enforce it; these tests make the code match the contract.
"""

from __future__ import annotations

import pytest

PATH = "/api/v1/pricing/usage"
SERVICE_KEY = "service-key-for-the-middleware"
ADMIN_KEY = "admin-key-under-test"


@pytest.fixture
def client():
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from api.routers import pricing

    # The launch app intentionally quarantines these legacy commercial routes.
    # Mount the router in isolation so its defense-in-depth contracts remain tested
    # without accidentally requiring public/runtime exposure.
    isolated = FastAPI()
    isolated.include_router(pricing.router)
    return TestClient(isolated)


@pytest.fixture(autouse=True)
def _clean_idempotency_store():
    from dealix.reliability import idempotency

    idempotency._LOCAL_STORE.clear()
    yield
    idempotency._LOCAL_STORE.clear()


def _usage(event_id: str = "evt_1", handle: str = "victim_tenant") -> dict:
    return {
        "plan": "laas_per_reply",
        "customer_handle": handle,
        "event_id": event_id,
    }


def _production(monkeypatch) -> None:
    """Production with the platform key set, so the middleware is satisfied.

    Without it, APIKeyMiddleware rejects an unconfigured production request
    before routing and every case here would pass for the wrong reason.
    """
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("API_KEYS", SERVICE_KEY)
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)


def test_service_key_alone_cannot_bill_a_customer(client, monkeypatch):
    """The defect: the shared platform key was sufficient to add billing."""
    _production(monkeypatch)

    resp = client.post(PATH, json=_usage(), headers={"X-API-Key": SERVICE_KEY})

    assert resp.status_code in (401, 403), (
        f"a plain service-key holder recorded a billable event: {resp.text}"
    )


def test_wrong_admin_key_cannot_bill_a_customer(client, monkeypatch):
    _production(monkeypatch)

    resp = client.post(
        PATH,
        json=_usage(),
        headers={"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": "not-the-admin-key"},
    )

    assert resp.status_code == 403, resp.text


def test_admin_key_records_the_event(client, monkeypatch):
    _production(monkeypatch)

    resp = client.post(
        PATH,
        json=_usage(),
        headers={"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": ADMIN_KEY},
    )

    assert resp.status_code == 200, resp.text
    assert resp.json()["status"] == "recorded"


def test_idempotency_still_holds_behind_the_gate(client, monkeypatch):
    """The gate must not disturb the 30-day double-billing guard."""
    _production(monkeypatch)
    headers = {"X-API-Key": SERVICE_KEY, "X-Admin-API-Key": ADMIN_KEY}

    first = client.post(PATH, json=_usage("evt_dup"), headers=headers)
    second = client.post(PATH, json=_usage("evt_dup"), headers=headers)

    assert first.json()["status"] == "recorded"
    assert second.json()["status"] == "duplicate", "the same event was billed twice"


def test_unconfigured_dev_environment_stays_open(client, monkeypatch):
    """Local runs leave the admin key unset — they must keep working."""
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    monkeypatch.delenv("DEALIX_ADMIN_API_KEY", raising=False)

    resp = client.post(PATH, json=_usage("evt_dev"))

    assert resp.status_code == 200, resp.text


def test_public_plan_listing_is_not_gated(client, monkeypatch):
    """Prospects must still see the plans without any credential.

    The gate belongs on the billing mutation, not on the whole router.
    """
    _production(monkeypatch)

    resp = client.get("/api/v1/pricing/plans")

    assert resp.status_code == 200, resp.text
    assert "plans" in resp.json()
