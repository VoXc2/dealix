"""B6 — Playbooks store tests."""
from __future__ import annotations

import pytest

from auto_client_acquisition.vertical_playbooks.playbook_postgres import (
    PostgresPlaybookStore,
)
from db.models import PlaybookRecord


@pytest.fixture()
def store() -> PostgresPlaybookStore:
    return PostgresPlaybookStore(database_url="sqlite:///:memory:")


def test_round_trip(store: PostgresPlaybookStore) -> None:
    row = store.add(
        name="Agency Growth Playbook",
        vertical="agency",
        steps=["open", "qualify", "propose"],
        owner="founder",
    )
    fetched = store.get(str(row["id"]))
    assert fetched is not None
    assert fetched["name"] == "Agency Growth Playbook"
    assert fetched["status"] == "draft"
    assert fetched["steps"] == ["open", "qualify", "propose"]


def test_mandatory_fields(store: PostgresPlaybookStore) -> None:
    with pytest.raises(ValueError):
        store.add(name="", vertical="agency")


def test_update_status(store: PostgresPlaybookStore) -> None:
    row = store.add(name="P", vertical="saas")
    updated = store.update_status(str(row["id"]), "published")
    assert updated is not None
    assert updated["status"] == "published"


def test_soft_delete_hides_row(store: PostgresPlaybookStore) -> None:
    row = store.add(name="P", vertical="saas")
    assert store.soft_delete(str(row["id"])) is True
    assert store.get(str(row["id"])) is None
    assert all(r["id"] != row["id"] for r in store.list())


def test_seed_from_catalog(store: PostgresPlaybookStore) -> None:
    rows = store.seed_from_catalog()
    assert len(rows) == 5
    verticals = {r["vertical"] for r in store.list()}
    assert verticals == {
        "agency",
        "b2b_services",
        "saas",
        "training_consulting",
        "local_services",
    }


def test_list_filters(store: PostgresPlaybookStore) -> None:
    store.add(name="A", vertical="agency", status="draft")
    store.add(name="B", vertical="saas", status="published")
    assert len(store.list(vertical="agency")) == 1
    assert len(store.list(status="published")) == 1


def test_playbook_record_has_soft_delete_column() -> None:
    assert "deleted_at" in PlaybookRecord.__table__.columns
