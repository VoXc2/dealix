"""B5 — Diagnostics store tests."""
from __future__ import annotations

import pytest

from auto_client_acquisition.diagnostic_engine.diagnostic_postgres import (
    PostgresDiagnosticStore,
)
from db.models import DiagnosticRecord


@pytest.fixture()
def store() -> PostgresDiagnosticStore:
    return PostgresDiagnosticStore(database_url="sqlite:///:memory:")


def test_round_trip(store: PostgresDiagnosticStore) -> None:
    row = store.add(
        subject_type="customer",
        subject_id="acme",
        diagnostic_type="capability",
        findings={"gap": "weak follow-up"},
        score=62.0,
        severity="medium",
        recommendations=["adopt SLA", "weekly brief"],
        run_by="founder",
    )
    fetched = store.get(str(row["id"]))
    assert fetched is not None
    assert fetched["diagnostic_type"] == "capability"
    assert fetched["score"] == 62.0
    assert fetched["recommendations"] == ["adopt SLA", "weekly brief"]


def test_findings_are_pii_free(store: PostgresDiagnosticStore) -> None:
    row = store.add(
        subject_type="lead",
        subject_id="lead_1",
        diagnostic_type="intake",
        findings={"note": "reach the owner at owner@example.com"},
        recommendations=["call owner@example.com back"],
    )
    fetched = store.get(str(row["id"]))
    assert fetched is not None
    assert "owner@example.com" not in repr(fetched["findings"])
    assert "owner@example.com" not in repr(fetched["recommendations"])


def test_mandatory_fields(store: PostgresDiagnosticStore) -> None:
    with pytest.raises(ValueError):
        store.add(subject_type="", subject_id="x", diagnostic_type="y")


def test_list_filters(store: PostgresDiagnosticStore) -> None:
    store.add(subject_type="customer", subject_id="a", diagnostic_type="capability")
    store.add(subject_type="lead", subject_id="b", diagnostic_type="intake")
    assert len(store.list(subject_type="customer")) == 1
    assert len(store.list(diagnostic_type="intake")) == 1
    assert len(store.list()) == 2


def test_diagnostic_record_has_soft_delete_column() -> None:
    assert "deleted_at" in DiagnosticRecord.__table__.columns
