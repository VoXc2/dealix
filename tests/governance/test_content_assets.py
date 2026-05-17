"""B7 — Content Assets store tests (approval gate + checksum integrity)."""
from __future__ import annotations

import pytest

from auto_client_acquisition.designops.asset_postgres import (
    PostgresContentAssetStore,
)
from db.models import ContentAssetRecord


@pytest.fixture()
def store() -> PostgresContentAssetStore:
    return PostgresContentAssetStore(database_url="sqlite:///:memory:")


def test_new_asset_starts_draft(store: PostgresContentAssetStore) -> None:
    """The approval gate — a freshly created asset has no approver and is draft."""
    row = store.add(asset_type="proof_pack", title="Acme Proof Pack")
    assert row["status"] == "draft"
    assert row["approved_by"] is None
    assert row["approved_at"] is None


def test_approve_requires_approver(store: PostgresContentAssetStore) -> None:
    row = store.add(asset_type="proof_pack", title="Acme Proof Pack")
    with pytest.raises(ValueError):
        store.approve(str(row["id"]), approver="")
    # asset still draft after the rejected approval
    fetched = store.get(str(row["id"]))
    assert fetched is not None
    assert fetched["status"] == "draft"


def test_approve_moves_to_approved(store: PostgresContentAssetStore) -> None:
    row = store.add(asset_type="proposal_page", title="Acme Proposal")
    approved = store.approve(str(row["id"]), approver="founder")
    assert approved is not None
    assert approved["status"] == "approved"
    assert approved["approved_by"] == "founder"
    assert approved["approved_at"] is not None


def test_checksum_integrity(store: PostgresContentAssetStore) -> None:
    row = store.add(
        asset_type="pricing_page", title="Pricing", uri="/pricing.html"
    )
    assert row["checksum"]
    assert store.verify_checksum(str(row["id"])) is True


def test_mandatory_fields(store: PostgresContentAssetStore) -> None:
    with pytest.raises(ValueError):
        store.add(asset_type="", title="x")


def test_soft_delete_hides_row(store: PostgresContentAssetStore) -> None:
    row = store.add(asset_type="proof_pack", title="P")
    assert store.soft_delete(str(row["id"])) is True
    assert store.get(str(row["id"])) is None
    assert all(r["id"] != row["id"] for r in store.list())


def test_list_filters(store: PostgresContentAssetStore) -> None:
    a = store.add(asset_type="proof_pack", title="A")
    store.add(asset_type="proposal_page", title="B")
    store.approve(str(a["id"]), approver="founder")
    assert len(store.list(asset_type="proof_pack")) == 1
    assert len(store.list(status="approved")) == 1
    assert len(store.list(status="draft")) == 1


def test_content_asset_record_has_soft_delete_column() -> None:
    assert "deleted_at" in ContentAssetRecord.__table__.columns
