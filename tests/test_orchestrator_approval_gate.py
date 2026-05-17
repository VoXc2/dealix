"""Guard: no orchestrator automation can execute a high-risk action.

Every high-risk automation must land as ``awaiting_approval`` with an
ApprovalRequest raised — never ``executing`` or ``succeeded`` (PR6).
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.approval_center import get_default_approval_store
from auto_client_acquisition.dealix_orchestrator import (
    get_default_task_queue,
    requires_approval,
    reset_default_task_queue,
    run_automation,
)
from auto_client_acquisition.dealix_orchestrator.automations import _AUTOMATION_SPECS
from auto_client_acquisition.evidence_control_plane_os.event_store import (
    reset_default_evidence_ledger,
)

_EXECUTED_STATES = {"executing", "succeeded"}


@pytest.fixture
def orch_env(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_EVIDENCE_LEDGER_DIR", str(tmp_path / "ev"))
    reset_default_task_queue()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()
    yield
    reset_default_task_queue()
    reset_default_evidence_ledger()
    get_default_approval_store().clear()


def test_no_automation_executes_directly(orch_env):
    for name in _AUTOMATION_SPECS:
        result = run_automation(name, entity_id=f"ent_{name}")
        assert result["task_status"] not in _EXECUTED_STATES, (
            f"automation '{name}' produced an executed task without approval"
        )


def test_every_high_risk_automation_is_approval_gated(orch_env):
    for name, (_agent, action, _entity) in _AUTOMATION_SPECS.items():
        if not requires_approval(action):
            continue
        result = run_automation(name, entity_id=f"hr_{name}")
        assert result["task_status"] == "awaiting_approval"
        assert result["approval_id"] is not None

        # An ApprovalRequest must exist in the pending queue.
        pending = get_default_approval_store().list_pending()
        assert any(p.object_id == f"hr_{name}" for p in pending)


def test_queued_high_risk_tasks_carry_requires_approval_flag(orch_env):
    run_automation("on_qualified", entity_id="lead_x")
    queue = get_default_task_queue()
    high_risk_tasks = [t for t in queue.tasks.values() if t.action_type == "first_outreach"]
    assert high_risk_tasks
    for task in high_risk_tasks:
        assert task.requires_approval is True
        assert task.status == "awaiting_approval"
