"""Self-evolving apply gate tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.self_evolving_os import (
    ImprovementProposal,
    SelfEvolvingRepository,
)


def test_self_evolving_proposal_cannot_apply_without_approval() -> None:
    repo = SelfEvolvingRepository()
    proposal = repo.propose(
        ImprovementProposal(
            tenant_id="tenant-a",
            run_id="run-1",
            title="Improve routing score weights",
        ),
    )
    with pytest.raises(ValueError):
        repo.apply(proposal_id=proposal.proposal_id)


def test_self_evolving_apply_after_granted_approval() -> None:
    repo = SelfEvolvingRepository()
    proposal = repo.propose(
        ImprovementProposal(
            tenant_id="tenant-a",
            run_id="run-1",
            title="Improve routing score weights",
        ),
    )
    repo.grant_approval(proposal_id=proposal.proposal_id, ticket_id="tkt-1")
    applied = repo.apply(proposal_id=proposal.proposal_id)
    assert applied.status == "applied"
