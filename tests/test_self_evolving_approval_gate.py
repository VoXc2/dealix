"""Self-evolving proposal approval gate behavior."""

from __future__ import annotations

import pytest

from auto_client_acquisition.control_plane_os.repositories import InMemoryControlPlaneRepository
from auto_client_acquisition.self_evolving_os.repositories import InMemorySelfEvolvingRepository


def test_proposal_cannot_apply_without_approval(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    repo = InMemorySelfEvolvingRepository()
    proposal = repo.create_proposal(
        tenant_id="tenant_a",
        title="Improve lead qualification",
        summary="Update scoring weights",
        proposed_by="agent",
    )
    with pytest.raises(ValueError, match="proposal_requires_approval"):
        repo.apply_proposal(tenant_id="tenant_a", proposal_id=proposal.proposal_id)


def test_apply_after_approval(tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DEALIX_CONTROL_LEDGER_PATH", str(tmp_path / "control.jsonl"))
    control = InMemoryControlPlaneRepository()
    repo = InMemorySelfEvolvingRepository()
    proposal = repo.create_proposal(
        tenant_id="tenant_a",
        title="Improve lead qualification",
        summary="Update scoring weights",
        proposed_by="agent",
    )
    ticket_id = repo.request_apply(
        tenant_id="tenant_a",
        proposal_id=proposal.proposal_id,
        actor="agent",
        control_repo=control,
    )
    control.grant_approval(tenant_id="tenant_a", ticket_id=ticket_id, actor="founder")
    repo.approve_proposal(tenant_id="tenant_a", proposal_id=proposal.proposal_id, approved_by="founder")
    applied = repo.apply_proposal(tenant_id="tenant_a", proposal_id=proposal.proposal_id)
    assert applied.state == "applied"
