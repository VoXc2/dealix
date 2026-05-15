"""Tests for capital_os.capital_ledger JSONL store."""

from __future__ import annotations

import pytest

from auto_client_acquisition.capital_os.capital_ledger import add_asset, list_assets


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    yield


def test_list_assets_empty_when_no_store() -> None:
    assert list_assets(customer_id="acme") == []


def test_add_asset_then_list_by_customer() -> None:
    add_asset(
        customer_id="acme",
        engagement_id="eng_1",
        asset_type="scoring_rule",
        title="Sector scoring rule",
    )
    add_asset(
        customer_id="other",
        engagement_id="eng_2",
        asset_type="draft_template",
        title="Arabic draft template",
    )
    acme = list_assets(customer_id="acme")
    assert len(acme) == 1
    assert acme[0].engagement_id == "eng_1"
    assert acme[0].asset_type == "scoring_rule"


def test_list_assets_filter_by_engagement() -> None:
    add_asset(
        customer_id="acme",
        engagement_id="eng_1",
        asset_type="scoring_rule",
        title="A",
    )
    add_asset(
        customer_id="acme",
        engagement_id="eng_2",
        asset_type="proof_example",
        title="B",
    )
    only = list_assets(customer_id="acme", engagement_id="eng_2")
    assert len(only) == 1
    assert only[0].title == "B"


def test_add_asset_requires_customer_id() -> None:
    with pytest.raises(ValueError):
        add_asset(
            customer_id="",
            engagement_id="eng_1",
            asset_type="scoring_rule",
            title="A",
        )
