"""Auditability OS — audit event row contract + evidence-chain completeness."""
from __future__ import annotations

from auto_client_acquisition.auditability_os.audit_event import (
    AuditEvent,
    audit_event_valid,
)
from auto_client_acquisition.auditability_os.evidence_chain import (
    EVIDENCE_CHAIN_STAGES,
    evidence_chain_complete,
)


def _event(**over) -> AuditEvent:
    base = dict(
        event_id="evt_1",
        actor="founder",
        source="data_os.import_preview",
        policy_checked="source_passport_ai_gate",
        matched_rule="allow",
        decision="allow_with_review",
        approval_status="not_required",
        output_id="out_1",
        timestamp_iso="2026-05-15T10:00:00+00:00",
    )
    base.update(over)
    return AuditEvent(**base)


def test_complete_audit_event_is_valid():
    assert audit_event_valid(_event()) is True


def test_audit_event_missing_actor_is_invalid():
    assert audit_event_valid(_event(actor="")) is False


def test_audit_event_missing_decision_is_invalid():
    assert audit_event_valid(_event(decision="")) is False


def test_audit_event_missing_timestamp_is_invalid():
    assert audit_event_valid(_event(timestamp_iso="")) is False


def test_evidence_chain_stages_are_the_seven_keys():
    assert len(EVIDENCE_CHAIN_STAGES) == 7
    assert "source" in EVIDENCE_CHAIN_STAGES
    assert "created_value" in EVIDENCE_CHAIN_STAGES


def test_evidence_chain_complete_when_all_stages_present():
    ok, missing = evidence_chain_complete(frozenset(EVIDENCE_CHAIN_STAGES))
    assert ok is True
    assert missing == ()


def test_evidence_chain_reports_missing_stages():
    ok, missing = evidence_chain_complete(frozenset({"source", "produced"}))
    assert ok is False
    assert "governed_by" in missing
    assert "reviewed_by" in missing
