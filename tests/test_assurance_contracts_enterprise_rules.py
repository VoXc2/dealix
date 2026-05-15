"""Enterprise Control Plane — assurance rules: deny-by-default + evidence.

Check #6 of the verify contract: a non-trivial action with no
governing contract (here: a data action with no Source Passport) is
denied, and every governance decision lands in the tenant-scoped
evidence trace.

Note: the original brief called this layer "assurance_contract_os";
the real modules are ``governance_os`` (the deny-by-default ``decide``)
and ``evidence_control_plane_os`` (the evidence chain).
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.evidence_control_plane_os.evidence_object import (
    EvidenceObject,
    evidence_object_valid,
    is_critical_evidence_type,
)
from auto_client_acquisition.evidence_control_plane_os.evidence_store import (
    clear_evidence_store_for_tests,
    list_evidence,
    record,
    run_trace,
)
from auto_client_acquisition.governance_os.runtime_decision import decide


@pytest.fixture(autouse=True)
def _isolated():
    clear_evidence_store_for_tests()
    yield
    clear_evidence_store_for_tests()


def test_no_source_passport_is_denied():
    """No contract (passport) on a data action → deny."""
    result = decide(action="run_scoring", context={"source_passport": None})
    assert result.decision.value == "BLOCK"
    assert "source_passport_required" in result.reasons


def test_pii_external_use_escalates():
    """PII + external use → escalate to a human approval gate."""
    result = decide(
        action="run_scoring",
        context={"source_passport": object(), "contains_pii": True, "external_use": True},
    )
    assert result.is_escalation
    assert result.approval_required is True


def test_low_risk_action_is_allowed():
    result = decide(action="read_internal_docs")
    assert result.decision.value == "ALLOW"


def test_evidence_object_requires_tenant_id():
    bad = EvidenceObject(
        evidence_id="ev1",
        evidence_type="approval",
        client_id="c1",
        project_id="p1",
        actor_type="system",
        actor_id="cp",
        human_owner="",
        source_ids=(),
        linked_artifacts=(),
        summary="x",
        confidence="medium",
        timestamp_iso="2026-05-15T00:00:00Z",
        tenant_id="",
    )
    ok, errors = evidence_object_valid(bad)
    assert ok is False
    assert "tenant_id_required" in errors


def test_critical_evidence_types():
    assert is_critical_evidence_type("approval")
    assert is_critical_evidence_type("governance_decision")
    assert not is_critical_evidence_type("source")


def test_governance_decisions_land_in_run_trace():
    record(
        tenant_id="t1",
        evidence_type="governance_decision",
        client_id="t1",
        summary="run_scoring blocked: no passport",
        run_id="run_x",
    )
    record(
        tenant_id="t1",
        evidence_type="approval",
        client_id="t1",
        summary="rollback approved",
        run_id="run_x",
    )
    trace = run_trace(tenant_id="t1", run_id="run_x")
    assert len(trace) == 2
    # A different tenant sees nothing.
    assert list_evidence(tenant_id="t2", run_id="run_x") == []
