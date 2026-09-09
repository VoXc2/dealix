"""Pricing/Moyasar safety under the current quote-only launch authority."""

from __future__ import annotations

import inspect

import pytest

from api.routers import pricing


def test_internal_pricing_registry_contains_no_nonpositive_payable_plan():
    """Future/internal payable entries must still be structurally valid."""
    for key, info in pricing.PLANS.items():
        assert int(info["amount_halalas"]) > 0, key


@pytest.mark.asyncio
async def test_legacy_public_pricing_endpoint_is_quarantined_from_launch(async_client):
    """The launch app owns quote-only commercial truth, not the legacy plan list."""
    r = await async_client.get("/api/v1/pricing/plans")
    assert r.status_code == 404


def test_no_literal_github_pat_in_pricing_module_source():
    src = inspect.getsource(pricing)
    assert "ghp_" not in src
    assert "github_pat_" not in src


def test_checkout_is_disabled_by_default_even_inside_legacy_module(monkeypatch):
    monkeypatch.delenv("DEALIX_CHECKOUT_ENABLED", raising=False)
    assert pricing._checkout_enabled() is False


def test_no_public_plan_is_implicitly_authorized() -> None:
    assert pricing.ALLOWED_PLANS == frozenset()
