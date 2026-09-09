"""Checkout idempotency is a reliability contract, not pricing authority.

The production app intentionally removes legacy public checkout/pricing routes
from its launch-safe router view. These tests therefore mount the source pricing
router in an isolated FastAPI app and use synthetic in-test plans. This proves
retry/idempotency behavior without resurrecting a public checkout surface or
binding reliability coverage to retired customer pricing.
"""

from __future__ import annotations

import pytest

PATH = "/api/v1/checkout"
PLAN = "synthetic_checkout_a"
OTHER_PLAN = "synthetic_checkout_b"
BUYER = "buyer@example.com"


@pytest.fixture(autouse=True)
def _clean_stores():
    from dealix.reliability import idempotency

    idempotency._LOCAL_STORE.clear()
    idempotency._LOCAL_VALUES.clear()
    yield
    idempotency._LOCAL_STORE.clear()
    idempotency._LOCAL_VALUES.clear()


@pytest.fixture
def approved_plans(monkeypatch):
    """Install two synthetic approved plans for this reliability test only."""
    from api.routers import pricing

    synthetic = {
        PLAN: {
            "name": "Synthetic Checkout A",
            "name_ar": "اختبار دفع أ",
            "amount_halalas": 100,
            "monthly": False,
            "kind": "one_off",
            "commercial_status": "test_only",
        },
        OTHER_PLAN: {
            "name": "Synthetic Checkout B",
            "name_ar": "اختبار دفع ب",
            "amount_halalas": 200,
            "monthly": False,
            "kind": "one_off",
            "commercial_status": "test_only",
        },
    }
    monkeypatch.setattr(pricing, "PLANS", synthetic)
    monkeypatch.setattr(pricing, "_PLANS_SOURCE", "registry")
    monkeypatch.setattr(pricing, "ALLOWED_PLANS", frozenset(synthetic))
    monkeypatch.setattr(pricing, "TEST_ONLY_PLANS", frozenset())


@pytest.fixture
def client(monkeypatch, approved_plans):
    """Exercise the retired checkout implementation without mounting it publicly.

    ``api.main`` deliberately filters ``/api/v1/checkout`` from the launch app.
    Reliability coverage still matters, so mount the source router only inside
    this test process. This fixture is not production routing authority.
    """
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from api.routers import pricing

    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "1")
    monkeypatch.setenv("APP_URL", "https://api.dealix.me")
    app = FastAPI()
    app.include_router(pricing.router)
    return TestClient(app)


@pytest.fixture
def moyasar(monkeypatch):
    """Counts invoice creations so a duplicate is visible."""
    from api.routers import pricing

    calls: list[dict] = []

    class _Client:
        async def create_invoice(self, **kwargs):
            calls.append(kwargs)
            return {
                "id": f"inv_{len(calls)}",
                "status": "initiated",
                "url": f"https://moyasar.test/pay/{len(calls)}",
            }

    monkeypatch.setattr(pricing, "MoyasarClient", _Client)
    return calls


def _order(**overrides) -> dict:
    body = {"plan": PLAN, "email": BUYER}
    body.update(overrides)
    return body


def test_a_retry_returns_the_first_invoice(client, moyasar):
    first = client.post(PATH, json=_order())
    second = client.post(PATH, json=_order())

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    assert len(moyasar) == 1, f"a retry minted a second invoice: {len(moyasar)} created"
    assert second.json()["invoice_id"] == first.json()["invoice_id"]
    assert second.json()["payment_url"] == first.json()["payment_url"]


def test_the_replay_is_labelled(client, moyasar):
    client.post(PATH, json=_order())
    replay = client.post(PATH, json=_order())
    assert replay.json()["idempotent_replay"] is True


def test_the_first_response_is_not_labelled_a_replay(client, moyasar):
    first = client.post(PATH, json=_order())
    assert "idempotent_replay" not in first.json()


def test_a_retry_is_not_refused(client, moyasar):
    client.post(PATH, json=_order())
    retry = client.post(PATH, json=_order())
    assert retry.status_code == 200


def test_a_different_buyer_gets_their_own_invoice(client, moyasar):
    client.post(PATH, json=_order())
    other = client.post(PATH, json=_order(email="someone.else@example.com"))
    assert len(moyasar) == 2
    assert other.json()["invoice_id"] == "inv_2"


def test_a_different_plan_gets_its_own_invoice(client, moyasar):
    client.post(PATH, json=_order())
    other = client.post(PATH, json=_order(plan=OTHER_PLAN))
    assert len(moyasar) == 2
    assert other.json()["invoice_id"] == "inv_2"


def test_an_explicit_idempotency_key_scopes_the_window(client, moyasar):
    first = client.post(PATH, json=_order(idempotency_key="order-1"))
    second = client.post(PATH, json=_order(idempotency_key="order-2"))
    repeat = client.post(PATH, json=_order(idempotency_key="order-1"))

    assert len(moyasar) == 2
    assert repeat.json()["invoice_id"] == first.json()["invoice_id"]
    assert second.json()["invoice_id"] != first.json()["invoice_id"]


def test_the_email_is_matched_case_insensitively(client, moyasar):
    client.post(PATH, json=_order())
    again = client.post(PATH, json=_order(email=BUYER.upper()))
    assert len(moyasar) == 1
    assert again.json()["idempotent_replay"] is True


@pytest.mark.parametrize(
    "changed",
    [
        {"email": "someone.else@example.com"},
        {"plan": OTHER_PLAN},
    ],
)
def test_client_key_cannot_replay_another_order(client, moyasar, changed):
    first = client.post(PATH, json=_order(idempotency_key="shared-client-key"))
    other = client.post(PATH, json=_order(idempotency_key="shared-client-key", **changed))

    assert first.status_code == 200, first.text
    assert other.status_code == 200, other.text
    assert len(moyasar) == 2
    assert other.json()["invoice_id"] != first.json()["invoice_id"]
    assert other.json()["payment_url"] != first.json()["payment_url"]


def test_nothing_is_remembered_when_checkout_is_not_approved(client, monkeypatch, moyasar):
    monkeypatch.delenv("DEALIX_CHECKOUT_ENABLED", raising=False)
    resp = client.post(PATH, json=_order())
    assert resp.status_code == 503
    assert resp.json()["detail"] == "checkout_not_founder_approved"
    assert not moyasar


def test_an_invalid_email_is_still_rejected(client, moyasar):
    resp = client.post(PATH, json=_order(email="not-an-email"))
    assert resp.status_code == 400
    assert not moyasar


def test_a_provider_failure_is_not_remembered_as_success(client, monkeypatch):
    from api.routers import pricing

    calls: list[int] = []

    class _Flaky:
        async def create_invoice(self, **kwargs):
            calls.append(1)
            if len(calls) == 1:
                raise RuntimeError("moyasar down")
            return {
                "id": "inv_after_recovery",
                "status": "initiated",
                "url": "https://moyasar.test/pay/ok",
            }

    monkeypatch.setattr(pricing, "MoyasarClient", _Flaky)
    failed = client.post(PATH, json=_order())
    recovered = client.post(PATH, json=_order())

    assert failed.status_code == 502
    assert recovered.status_code == 200
    assert recovered.json()["invoice_id"] == "inv_after_recovery"


def test_remember_and_recall_round_trip():
    from dealix.reliability.idempotency import IdempotencyStore

    store = IdempotencyStore(prefix="test:checkout:")
    assert store.recall("k") is None
    store.remember("k", {"invoice_id": "inv_1"}, ttl_seconds=60)
    assert store.recall("k") == {"invoice_id": "inv_1"}


def test_recall_of_an_unknown_key_is_none_not_an_error():
    from dealix.reliability.idempotency import IdempotencyStore

    assert IdempotencyStore(prefix="test:checkout:").recall("never-written") is None


def test_value_memory_is_separate_from_the_claim_flag():
    from dealix.reliability.idempotency import IdempotencyStore

    store = IdempotencyStore(prefix="test:checkout:")
    store.remember("shared", {"v": 1}, ttl_seconds=60)
    assert store.claim("shared", ttl_seconds=60) is True
    assert store.recall("shared") == {"v": 1}
