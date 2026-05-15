"""Evidence Control Plane — evidence objects, chain, compliance index, gaps."""
from __future__ import annotations

from auto_client_acquisition.evidence_control_plane_os.compliance_index import (
    build_compliance_index,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_graph import (
    MINI_CHAIN_KEYS,
    mini_evidence_chain_complete,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
    EvidenceObject,
    EvidenceType,
    evidence_object_valid,
    is_critical_evidence_type,
)
from auto_client_acquisition.evidence_control_plane_os.gap_detector import find_gaps


def _evidence(**over) -> EvidenceObject:
    base = dict(
        evidence_id="ev_1",
        evidence_type=EvidenceType.AI_RUN.value,
        client_id="acme",
        project_id="proj_1",
        actor_type="agent",
        actor_id="agt_1",
        human_owner="founder",
        source_ids=("src_1",),
        linked_artifacts=("out_1",),
        summary="ran scoring on imported accounts",
        confidence="estimated",
        timestamp_iso="2026-05-15T10:00:00+00:00",
    )
    base.update(over)
    return EvidenceObject(**base)


def test_valid_evidence_object_passes():
    ok, errors = evidence_object_valid(_evidence())
    assert ok is True
    assert errors == ()


def test_evidence_object_missing_fields_reported():
    ok, errors = evidence_object_valid(_evidence(evidence_id="", summary=""))
    assert ok is False
    assert "evidence_id_required" in errors
    assert "summary_required" in errors


def test_critical_evidence_types():
    assert is_critical_evidence_type(EvidenceType.GOVERNANCE_DECISION) is True
    assert is_critical_evidence_type(EvidenceType.AI_RUN) is True
    assert is_critical_evidence_type(EvidenceType.RISK) is False


def test_mini_evidence_chain_complete_when_all_keys_present():
    chain = dict.fromkeys(MINI_CHAIN_KEYS, "present")
    ok, missing = mini_evidence_chain_complete(chain)
    assert ok is True
    assert missing == ()


def test_mini_evidence_chain_reports_missing_keys():
    ok, missing = mini_evidence_chain_complete({"source": "x"})
    assert ok is False
    assert "governed_by" in missing


def test_compliance_index_covers_pdpl_zatca_internal():
    idx = build_compliance_index(customer_id="acme")
    frameworks = {item.framework for item in idx.items}
    assert "PDPL" in frameworks
    assert "ZATCA" in frameworks
    assert "Internal" in frameworks


def test_find_gaps_returns_a_list():
    gaps = find_gaps(customer_id="acme")
    assert isinstance(gaps, list)
    for gap in gaps:
        assert gap.severity in {"low", "med", "high"}
