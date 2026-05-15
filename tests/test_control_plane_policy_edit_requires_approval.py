"""Non-negotiable: control-plane policy edits never apply without approval.

Guards `no_unaudited_changes` and approval-first.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.approval_gate import (
    ApprovalGateError,
    get_approval_gate,
    reset_approval_gate,
)
from auto_client_acquisition.control_plane_os.core import (
    get_control_plane,
    reset_control_plane,
)
from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.control_plane_os.schemas import PolicyEdit


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_approval_gate()
    reset_control_plane()


def test_policy_edit_returns_pending_ticket() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1")
    edit = PolicyEdit(run_id=run.run_id, policy_id="pol1", change={"x": 1}, editor="f")
    ticket = cp.edit_policy(edit, actor="f")
    assert ticket.state == "pending"
    # the policy is NOT attached yet — nothing applied without approval
    assert "pol1" not in cp.get_run(run.run_id).attached_policy_ids


def test_policy_edit_cannot_finalize_without_grant() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1")
    edit = PolicyEdit(run_id=run.run_id, policy_id="pol1", change={"x": 1}, editor="f")
    ticket = cp.edit_policy(edit, actor="f")
    with pytest.raises(ApprovalGateError):
        cp.finalize_policy_edit(edit, ticket.ticket_id)


def test_policy_edit_applies_after_grant_and_is_audited() -> None:
    cp = get_control_plane()
    run = cp.register_run(workflow_id="wf1", customer_id="c1")
    edit = PolicyEdit(run_id=run.run_id, policy_id="pol1", change={"x": 1}, editor="f")
    ticket = cp.edit_policy(edit, actor="f")
    get_approval_gate().grant(ticket.ticket_id, "founder")
    updated = cp.finalize_policy_edit(edit, ticket.ticket_id)
    assert "pol1" in updated.attached_policy_ids
    events = get_control_ledger().list_events(event_type="policy_edited")
    assert events and events[0].payload["after"] == ["pol1"]
