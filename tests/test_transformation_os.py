"""Transformation OS — 5-stage machine and JSONL store."""

from __future__ import annotations

import pytest

from auto_client_acquisition.transformation_os import (
    STAGE_TO_OFFER,
    StageEvidence,
    TransformationRecord,
    TransformationStage,
    advance_stage,
    can_advance,
    clear_for_test,
    emit,
    list_records,
)


@pytest.fixture(autouse=True)
def _isolated(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "DEALIX_TRANSFORMATION_LOG_PATH", str(tmp_path / "transformation.jsonl")
    )
    clear_for_test()
    yield
    clear_for_test()


def _evidence(stage: str, verified: bool = True) -> StageEvidence:
    return StageEvidence(
        evidence_id=f"ev_{stage}",
        stage=stage,
        kind="proof_pack",
        ref="docs/proof.md",
        verified=verified,
    )


def test_five_stages_map_to_offers() -> None:
    assert len(STAGE_TO_OFFER) == 5
    assert set(STAGE_TO_OFFER) == set(TransformationStage)


def test_new_record_starts_at_assessment() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    assert rec.current_stage == TransformationStage.ASSESSMENT.value
    assert rec.offer_for_current_stage() == "free_mini_diagnostic"


def test_advance_through_one_stage() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    advanced = advance_stage(
        rec,
        TransformationStage.PILOT.value,
        [_evidence(TransformationStage.ASSESSMENT.value)],
    )
    assert advanced.current_stage == TransformationStage.PILOT.value
    assert TransformationStage.ASSESSMENT.value in advanced.completed_stages


def test_cannot_skip_a_stage() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    ok, reasons = can_advance(
        rec,
        TransformationStage.WORKFLOW_REDESIGN.value,
        [_evidence(TransformationStage.ASSESSMENT.value)],
    )
    assert ok is False
    assert any("not allowed" in r for r in reasons)
    with pytest.raises(ValueError):
        advance_stage(
            rec,
            TransformationStage.WORKFLOW_REDESIGN.value,
            [_evidence(TransformationStage.ASSESSMENT.value)],
        )


def test_advance_rejected_without_evidence() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    ok, reasons = can_advance(rec, TransformationStage.PILOT.value, [])
    assert ok is False
    assert any("no evidence" in r for r in reasons)


def test_advance_rejected_with_unverified_evidence() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    ok, reasons = can_advance(
        rec,
        TransformationStage.PILOT.value,
        [_evidence(TransformationStage.ASSESSMENT.value, verified=False)],
    )
    assert ok is False
    assert any("verified" in r for r in reasons)


def test_advance_rejected_when_evidence_targets_wrong_stage() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    ok, reasons = can_advance(
        rec,
        TransformationStage.PILOT.value,
        [_evidence(TransformationStage.PILOT.value)],
    )
    assert ok is False
    assert any("stage being closed" in r for r in reasons)


def test_store_round_trip() -> None:
    rec = TransformationRecord(engagement_id="e1", client_id="c1")
    emit(rec)
    advanced = advance_stage(
        rec,
        TransformationStage.PILOT.value,
        [_evidence(TransformationStage.ASSESSMENT.value)],
    )
    emit(advanced)
    records = list_records(client_id="c1")
    assert len(records) == 2
    assert records[-1].current_stage == TransformationStage.PILOT.value


def test_store_scopes_by_client() -> None:
    emit(TransformationRecord(engagement_id="e1", client_id="c1"))
    emit(TransformationRecord(engagement_id="e2", client_id="c2"))
    assert len(list_records(client_id="c1")) == 1
    assert len(list_records(client_id="c2")) == 1
