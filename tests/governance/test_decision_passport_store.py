"""B2 — Decision Passport append-only store doctrine tests."""
from __future__ import annotations

from datetime import UTC, datetime

import pytest

from auto_client_acquisition.decision_passport import (
    DecisionPassport,
    PassportApproval,
    PassportPersistenceError,
)
from auto_client_acquisition.decision_passport.passport_postgres import (
    PostgresPassportStore,
)
from auto_client_acquisition.decision_passport.schema import ScoreBoard
from db.models import DecisionPassportRecord


def _scores() -> ScoreBoard:
    return ScoreBoard(
        fit_score=0.7,
        intent_score=0.6,
        urgency_score=0.5,
        revenue_potential_score=0.6,
        engagement_score=0.5,
        data_quality_score=0.6,
        warm_route_score=0.7,
        compliance_risk_score=0.2,
        deliverability_risk_score=0.3,
    )


def _passport(**overrides) -> DecisionPassport:
    base = dict(
        lead_id="lead_1",
        company="Acme Co",
        source="website_inbound",
        why_now_ar="x",
        why_now_en="x",
        icp_tier="A",
        priority_bucket="P1_THIS_WEEK",
        scores=_scores(),
        best_channel="email_draft_approval_first",
        recommended_action="prepare_mini_diagnostic",
        recommended_action_ar="x",
        proof_target="demo_booked",
        proof_target_ar="x",
        next_step_ar="x",
        next_step_en="x",
        owner="founder",
        approval=PassportApproval(approver="founder", approved_at=datetime.now(UTC)),
        measurable_impact="book one discovery call",
    )
    base.update(overrides)
    return DecisionPassport(**base)


@pytest.fixture()
def store() -> PostgresPassportStore:
    return PostgresPassportStore(database_url="sqlite:///:memory:")


def test_round_trip_store_and_get(store: PostgresPassportStore) -> None:
    pid = store.add(_passport())
    fetched = store.get(pid)
    assert fetched is not None
    assert fetched.lead_id == "lead_1"
    assert fetched.measurable_impact == "book one discovery call"
    assert fetched.approval is not None
    assert fetched.approval.approver == "founder"


def test_validation_rejects_empty_proof_target(store: PostgresPassportStore) -> None:
    with pytest.raises(PassportPersistenceError):
        store.add(_passport(proof_target=""))


def test_validation_rejects_empty_owner(store: PostgresPassportStore) -> None:
    p = _passport()
    object.__setattr__(p, "owner", "")
    with pytest.raises(PassportPersistenceError):
        store.add(p)


def test_source_is_mandatory_for_persistence(store: PostgresPassportStore) -> None:
    p = _passport()
    object.__setattr__(p, "source", "")
    with pytest.raises(PassportPersistenceError):
        store.add(p)


def test_approval_is_mandatory_for_persistence(store: PostgresPassportStore) -> None:
    with pytest.raises(PassportPersistenceError):
        store.add(_passport(approval=None))


def test_not_null_governance_columns() -> None:
    """source / approved_by / approved_at are NOT NULL columns."""
    cols = DecisionPassportRecord.__table__.columns
    assert cols["source"].nullable is False
    assert cols["approved_by"].nullable is False
    assert cols["approved_at"].nullable is False


def test_store_is_append_only_no_mutation_method() -> None:
    for forbidden in ("update", "delete", "remove", "edit", "patch"):
        assert not hasattr(PostgresPassportStore, forbidden), (
            f"PostgresPassportStore must not expose {forbidden!r}"
        )


def test_list_newest_first(store: PostgresPassportStore) -> None:
    store.add(_passport(lead_id="lead_a"))
    store.add(_passport(lead_id="lead_b"))
    rows = store.list()
    assert len(rows) == 2
    only_a = store.list(lead_id="lead_a")
    assert len(only_a) == 1
    assert only_a[0].lead_id == "lead_a"
