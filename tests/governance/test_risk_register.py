"""B4 — Risk Register store tests."""
from __future__ import annotations

import pytest

from auto_client_acquisition.risk_resilience_os.risk_postgres import (
    PostgresRiskRegister,
    RiskValidationError,
)
from auto_client_acquisition.risk_resilience_os.risk_register import (
    RISK_TAXONOMY_CATEGORIES,
)
from db.models import RiskRecord


@pytest.fixture()
def register() -> PostgresRiskRegister:
    return PostgresRiskRegister(database_url="sqlite:///:memory:")


def test_round_trip(register: PostgresRiskRegister) -> None:
    row = register.add(category="data_risk", title="Stale lead data", owner="founder")
    fetched = register.get(str(row["id"]))
    assert fetched is not None
    assert fetched["title"] == "Stale lead data"
    assert fetched["status"] == "open"


def test_category_validated_against_taxonomy(register: PostgresRiskRegister) -> None:
    with pytest.raises(RiskValidationError):
        register.add(category="made_up_risk", title="x")


def test_every_taxonomy_category_accepted(register: PostgresRiskRegister) -> None:
    for category in RISK_TAXONOMY_CATEGORIES:
        row = register.add(category=category, title=f"risk-{category}")
        assert row["category"] == category


def test_title_is_mandatory(register: PostgresRiskRegister) -> None:
    with pytest.raises(RiskValidationError):
        register.add(category="data_risk", title="   ")


def test_update_status(register: PostgresRiskRegister) -> None:
    row = register.add(category="market_risk", title="Pricing pressure")
    updated = register.update_status(str(row["id"]), "mitigated")
    assert updated is not None
    assert updated["status"] == "mitigated"


def test_soft_delete_hides_row(register: PostgresRiskRegister) -> None:
    row = register.add(category="client_risk", title="Churn risk")
    assert register.soft_delete(str(row["id"])) is True
    assert register.get(str(row["id"])) is None
    assert all(r["id"] != row["id"] for r in register.list())


def test_list_filters(register: PostgresRiskRegister) -> None:
    register.add(category="data_risk", title="a", status="open")
    register.add(category="market_risk", title="b", status="closed")
    assert len(register.list(category="data_risk")) == 1
    assert len(register.list(status="closed")) == 1


def test_risk_record_has_soft_delete_column() -> None:
    assert "deleted_at" in RiskRecord.__table__.columns
