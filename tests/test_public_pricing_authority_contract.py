from __future__ import annotations

import json
from pathlib import Path

import pytest

from api.routers import pricing

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "commercial" / "public_pricing_authority_v1.json"


def test_contract_is_quote_only_and_env_flags_are_non_authority() -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert data["public_fixed_pricing"] is False
    assert data["public_checkout_authority"] is False
    assert data["environment_flags_may_create_public_price_authority"] is False
    assert data["customer_specific_quote_required"] is True
    assert data["payment_execution_requires_separate_authority"] is True


def test_current_public_pricing_is_empty_even_when_legacy_env_flags_are_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("DEALIX_PUBLIC_PRICING_ENABLED", "true")
    monkeypatch.setenv("DEALIX_PUBLIC_PLAN_IDS", "starter,growth,scale,pilot_1sar")
    assert pricing.ALLOWED_PLANS == frozenset()
    assert pricing._public_plan_ids() == frozenset()


def test_test_plan_can_never_be_public_or_normal_checkout() -> None:
    assert "pilot_1sar" in pricing.TEST_ONLY_PLANS
    assert "pilot_1sar" not in pricing.ALLOWED_PLANS


def test_quote_and_payment_truth_are_separate() -> None:
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    firewall = set(data["truth_firewall"])
    assert "catalog_price != customer_quote" in firewall
    assert "invoice != payment" in firewall
    assert "provider_acceptance != payment_evidence" in firewall
