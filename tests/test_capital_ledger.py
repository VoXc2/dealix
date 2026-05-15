"""Capital ledger JSONL store — record + list reusable assets."""
from __future__ import annotations

import pytest

from auto_client_acquisition.capital_os.capital_ledger import (
    CapitalAsset,
    clear_for_test,
    list_assets,
    record_asset,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl"))
    clear_for_test()
    yield
    clear_for_test()


def test_list_assets_empty_when_no_ledger():
    assert list_assets(customer_id="acme") == []


def test_record_asset_returns_capital_asset():
    asset = record_asset(
        customer_id="acme",
        engagement_id="eng_1",
        asset_type="company_brain",
        title="Company Brain v1",
        description="reusable brain",
        evidence_ref="proof_1",
    )
    assert isinstance(asset, CapitalAsset)
    assert asset.customer_id == "acme"
    assert asset.engagement_id == "eng_1"
    assert asset.asset_id.startswith("CAP-")


def test_list_assets_scoped_by_customer_and_engagement():
    record_asset(
        customer_id="acme", engagement_id="eng_1", asset_type="brain", title="A"
    )
    record_asset(
        customer_id="acme", engagement_id="eng_2", asset_type="board", title="B"
    )
    record_asset(
        customer_id="other", engagement_id="eng_3", asset_type="brain", title="C"
    )
    assert len(list_assets(customer_id="acme")) == 2
    assert len(list_assets(engagement_id="eng_1")) == 1
    assert len(list_assets()) == 3


def test_record_asset_requires_customer_id():
    with pytest.raises(ValueError):
        record_asset(
            customer_id="", engagement_id="eng_1", asset_type="brain", title="A"
        )
