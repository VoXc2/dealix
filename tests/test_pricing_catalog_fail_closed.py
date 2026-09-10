"""A price catalogue that failed to load must not sell anything.

``PLANS`` is built once at import from
``auto_client_acquisition.service_catalog.registry`` — the module comment calls
it the single source of truth for what a customer is charged. The import was
wrapped in a bare ``except Exception`` that returned a **hardcoded copy of the
ladder**, with no log line. Any failure in that import chain silently swapped
the catalogue and checkout carried on selling from stale numbers.

The copy had already drifted, which is the proof that hand-syncing does not
hold:

* its Data-to-Revenue key was ``data_to_revenue_1500``, against the registry's
  ``data_to_revenue_pack_1500`` — so a canonical checkout link 400s in fallback
  mode and a legacy one 400s in normal mode;
* the 7,500 SAR Executive Command Center and every transformation offering were
  absent, making the whole top of the ladder unsellable;
* the ``starter`` / ``growth`` / ``scale`` aliases were absent, so
  ``PLANS["starter"]`` — which ``tests/test_billing_amounts.py`` reads —
  raised ``KeyError``.

The fallback is gone. An unloadable catalogue is now empty and visible:
reads report ``catalog_status: "unavailable"`` and checkout returns 503 rather
than charging a price nobody approved. Quoting the wrong number is worse than
quoting none.
"""

from __future__ import annotations

import pytest


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


@pytest.fixture
def broken_catalog(monkeypatch):
    """Simulate the registry having failed to load, without reimporting."""
    from api.routers import pricing

    monkeypatch.setattr(pricing, "_PLANS_SOURCE", "unavailable")
    monkeypatch.setattr(pricing, "PLANS", {})
    return pricing


# ── The catalogue is intact in the normal case ────────────────────────────


def test_catalog_loads_from_the_registry():
    from api.routers import pricing

    assert pricing._PLANS_SOURCE == "registry"
    assert pricing.catalog_available() is True
    assert pricing.PLANS


def test_every_plan_price_matches_the_registry():
    """The reason the fallback existed at all: keeping two copies in step."""
    from api.routers.pricing import PLANS
    from auto_client_acquisition.service_catalog.registry import OFFERINGS

    drift = [
        (o.id, int(o.price_sar * 100), PLANS[o.id]["amount_halalas"])
        for o in OFFERINGS
        if o.id in PLANS and int(o.price_sar * 100) != PLANS[o.id]["amount_halalas"]
    ]

    assert not drift, f"catalogue prices diverged from the registry: {drift}"


def test_backwards_compat_aliases_charge_the_canonical_amount():
    """An alias that drifts from its target silently charges the wrong price."""
    from api.routers.pricing import PLANS

    for alias, canonical in (
        ("growth", "growth_ops_monthly_2999"),
        ("scale", "executive_command_center_7500"),
        ("starter", "growth_ops_monthly_2999"),
    ):
        assert alias in PLANS, f"{alias} disappeared — existing checkout links 400"
        assert PLANS[alias]["amount_halalas"] == PLANS[canonical]["amount_halalas"], (
            f"{alias} charges a different amount from {canonical}"
        )
    assert "pilot_managed" not in PLANS
    assert "revenue_proof_sprint_499" not in PLANS


def test_no_payable_plan_is_free_or_negative():
    from api.routers.pricing import PLANS

    bad = {k: v["amount_halalas"] for k, v in PLANS.items() if v["amount_halalas"] <= 0}
    assert not bad, f"unchargeable amounts on payable plans: {bad}"


def test_every_allowed_plan_is_resolvable():
    """``create_checkout`` indexes ``PLANS[plan]`` after the allowlist check."""
    from api.routers.pricing import ALLOWED_PLANS, PLANS

    missing = sorted(set(ALLOWED_PLANS) - set(PLANS))
    assert not missing, f"allowlisted plans that would KeyError at checkout: {missing}"


# ── The catalogue failing must stop the sale ──────────────────────────────


def test_checkout_refuses_when_the_catalog_is_unavailable(
    client, broken_catalog, monkeypatch
):
    """The regression: this used to sell from the stale hardcoded copy."""
    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "1")

    resp = client.post(
        "/api/v1/checkout",
        json={"plan": "revenue_proof_sprint_499", "email": "buyer@example.com"},
    )

    assert resp.status_code == 503, resp.text
    assert resp.json()["detail"] == "pricing_catalog_unavailable", (
        "an unloadable catalogue must not be reported as an unknown plan"
    )


def test_plan_listing_reports_the_outage(client, broken_catalog):
    resp = client.get("/api/v1/pricing/plans")

    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["catalog_status"] == "unavailable"
    assert body["plans"] == {}


def test_menu_is_not_sales_ready_when_the_catalog_is_down(
    client, broken_catalog, monkeypatch
):
    """Founder approval does not make a broken catalogue sellable."""
    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "1")

    resp = client.get("/api/v1/pricing/menu")

    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["sales_ready"] is False
    assert body["catalog_status"] == "unavailable"
    assert body["checkout_status"] == "unavailable"


def test_healthy_quote_only_catalog_stays_not_sales_ready(client, monkeypatch):
    monkeypatch.setenv("DEALIX_CHECKOUT_ENABLED", "1")

    resp = client.get("/api/v1/pricing/menu")

    body = resp.json()
    assert body["catalog_status"] == "registry"
    assert body["sales_ready"] is False
    assert body["checkout_status"] == "founder_approval_required"


def test_checkout_stays_founder_gated_with_a_healthy_catalog(client, monkeypatch):
    """The pre-existing approval gate must survive the new one."""
    monkeypatch.delenv("DEALIX_CHECKOUT_ENABLED", raising=False)

    resp = client.post(
        "/api/v1/checkout",
        json={"plan": "revenue_proof_sprint_499", "email": "buyer@example.com"},
    )

    assert resp.status_code == 503
    assert resp.json()["detail"] == "checkout_not_founder_approved"
