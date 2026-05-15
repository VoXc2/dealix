"""Tests for evidence_control_plane_os."""

from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.accountability_map import (
    AccountabilityRecord,
    accountability_valid_for_execution,
    external_action_accountable,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_api import evidence_route_registered
from auto_client_acquisition.evidence_control_plane_os.evidence_dashboard import (
    evidence_coverage_band,
    evidence_coverage_percent,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_gap_detector import (
    EvidencePresence,
    GapSeverity,
    detect_evidence_gaps,
    gap_severity,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import mini_evidence_chain_complete
from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
    EvidenceObject,
    EvidenceType,
    evidence_object_valid,
    is_critical_evidence_type,
)
from auto_client_acquisition.evidence_control_plane_os.proof_linker import (
    PROOF_PACK_V3_SECTIONS,
    proof_pack_v3_sections_complete,
)


def test_evidence_object_valid() -> None:
    obj = EvidenceObject(
        evidence_id="EVD-1",
        evidence_type=EvidenceType.GOVERNANCE_DECISION,
        client_id="CL-1",
        project_id="PRJ-1",
        actor_type="agent",
        actor_id="AGT-1",
        human_owner="Rev Owner",
        source_ids=("SRC-1",),
        linked_artifacts=("AIR-1",),
        summary="Draft-only boundary.",
        confidence="high",
        timestamp_iso="2026-05-14T10:00:00Z",
    )
    ok, err = evidence_object_valid(obj)
    assert ok and err == ()


def test_mini_chain() -> None:
    ok, missing = mini_evidence_chain_complete({"source": "SRC-1"})
    assert not ok and "used_by" in missing


def test_detect_gaps() -> None:
    p = EvidencePresence(
        has_source_passport=False,
        has_governance_decision_on_output=True,
        has_approval_for_external=False,
        has_proof_for_claim=True,
        has_human_review=True,
        has_agent_auditability_card=True,
        has_value_event_for_retainer=False,
    )
    g = detect_evidence_gaps(p)
    assert "source_passport_missing" in g
    assert gap_severity("approval_missing_external") == GapSeverity.CRITICAL


def test_coverage_band() -> None:
    assert evidence_coverage_percent(satisfied=7, total=10) == 70.0
    assert evidence_coverage_band(69.0) == "fragile"
    assert evidence_coverage_band(90.0) == "client_ready"


def test_proof_pack_v3() -> None:
    ok, m = proof_pack_v3_sections_complete({})
    assert not ok
    assert set(m) == set(PROOF_PACK_V3_SECTIONS)


def test_accountability_external() -> None:
    rec = AccountabilityRecord(
        output_id="OUT-1",
        generated_by="AGT-1",
        reviewed_by="OP-1",
        approved_by="",
        governed_by="GOV-1",
        owned_by="Owner",
        client_sponsor="Sponsor",
        dealix_owner="Dealix",
    )
    ok, err = external_action_accountable(rec)
    assert not ok
    assert "no_approval_owner_no_external_action" in err


def test_evidence_api_route() -> None:
    assert evidence_route_registered("POST", "/evidence/source")
    assert not evidence_route_registered("DELETE", "/evidence/source")


def test_critical_type() -> None:
    assert is_critical_evidence_type(EvidenceType.AI_RUN)
