"""Self-evolving proposal approval gate tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.self_evolving_os.repositories import (
    ImprovementProposal,
    InMemorySelfEvolvingRepository,
    ProposalApprovalRequiredError,
)


def test_proposal_cannot_apply_without_approval() -> None:
    repo = InMemorySelfEvolvingRepository()
    repo.submit_proposal(
        ImprovementProposal(
            proposal_id="prop-1",
            tenant_id="tenant-a",
            title="Tighten escalation thresholds",
            change_summary="Raise high-risk sensitivity to 0.65.",
            proposed_by="system",
        )
    )

    with pytest.raises(ProposalApprovalRequiredError) as exc_info:
        repo.apply_proposal(tenant_id="tenant-a", proposal_id="prop-1", applied_by="system")
    assert exc_info.value.status_code == 409

    approved = repo.approve_proposal(
        tenant_id="tenant-a",
        proposal_id="prop-1",
        approved_by="sami",
    )
    assert approved.state == "approved"
    applied = repo.apply_proposal(tenant_id="tenant-a", proposal_id="prop-1", applied_by="system")
    assert applied.state == "applied"
