from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest

from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.postgres_store import PostgresApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalRequest, ApprovalStatus


class _AuditFailureRuleEngine:
    def match(self, req, *, confidence: float, content: str):
        assert req.action_mode == "approval_required"
        return SimpleNamespace(rule_id="rule_fail", name="audit_failure_rule")

    def record_match(self, rule, req, *, confidence: float) -> None:
        raise RuntimeError("forced founder-rule audit failure")


def _request(suffix: str) -> ApprovalRequest:
    return ApprovalRequest(
        approval_id=f"apr_{suffix}",
        object_type="lead",
        object_id=f"lead_{suffix}",
        action_type="draft_email",
        action_mode="approval_required",
        channel="email",
        summary_en=f"request {suffix}",
        proof_impact="leadops:test",
    )


@pytest.mark.parametrize("backend", ["memory", "postgres"])
def test_founder_rule_audit_failure_never_grants_execution_authority(
    backend: str,
    tmp_path: Path,
) -> None:
    if backend == "memory":
        store = ApprovalStore()
    else:
        store = PostgresApprovalStore(
            database_url=f"sqlite:///{tmp_path / 'audit-fail.sqlite3'}",
            create_tables=True,
        )

    req = store.create_with_founder_rules(
        _request(backend),
        confidence=0.99,
        content="eligible founder rule pattern",
        engine=_AuditFailureRuleEngine(),
    )

    assert ApprovalStatus(req.status) == ApprovalStatus.PENDING
    assert req.action_mode == "approval_required"
    assert not any(row.get("action") == "auto_approve" for row in req.edit_history)

    restored = store.get(req.approval_id)
    assert restored is not None
    assert ApprovalStatus(restored.status) == ApprovalStatus.PENDING
    assert restored.action_mode == "approval_required"


def test_founder_rule_audit_failure_survives_store_restart_as_pending(
    tmp_path: Path,
) -> None:
    database_url = f"sqlite:///{tmp_path / 'audit-restart.sqlite3'}"
    first = PostgresApprovalStore(database_url=database_url, create_tables=True)
    req = first.create_with_founder_rules(
        _request("restart"),
        confidence=0.99,
        content="eligible founder rule pattern",
        engine=_AuditFailureRuleEngine(),
    )

    assert ApprovalStatus(req.status) == ApprovalStatus.PENDING

    second = PostgresApprovalStore(database_url=database_url, create_tables=False)
    restored = second.get(req.approval_id)
    assert restored is not None
    assert ApprovalStatus(restored.status) == ApprovalStatus.PENDING
    assert restored.action_mode == "approval_required"
    assert not any(row.get("action") == "auto_approve" for row in restored.edit_history)
