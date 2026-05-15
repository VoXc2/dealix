"""Non-negotiable: the self-evolving fabric never auto-applies a change.

Guards `no_unaudited_changes` and approval-first — propose-don't-execute.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.approval_gate import (
    get_approval_gate,
    reset_approval_gate,
)
from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)
from auto_client_acquisition.self_evolving_os import (
    ImprovementTarget,
    ProposalNotApprovedError,
    get_self_evolving_fabric,
    reset_self_evolving_fabric,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_approval_gate()
    reset_self_evolving_fabric()


def test_proposal_is_always_created_as_proposed() -> None:
    proposal = get_self_evolving_fabric().propose_improvement(
        target=ImprovementTarget.WORKFLOW, target_id="wf1", rationale="too slow"
    )
    assert proposal.status == "proposed"
    assert proposal.approval_ticket_id is not None


def test_apply_without_approval_raises() -> None:
    fabric = get_self_evolving_fabric()
    proposal = fabric.propose_improvement(
        target=ImprovementTarget.GOVERNANCE, target_id="pol1"
    )
    with pytest.raises(ProposalNotApprovedError):
        fabric.apply_proposal(proposal.proposal_id)


def test_apply_after_grant_succeeds_and_is_audited() -> None:
    fabric = get_self_evolving_fabric()
    proposal = fabric.propose_improvement(
        target=ImprovementTarget.ORCHESTRATION, target_id="orch1"
    )
    get_approval_gate().grant(proposal.approval_ticket_id, "founder")
    applied = fabric.apply_proposal(proposal.proposal_id, actor="founder")
    assert applied.status == "applied"
    events = get_control_ledger().list_events(event_type="improvement_applied")
    assert events and events[0].subject_id == proposal.proposal_id
