"""Tests for System 33 — human_ai_os.

Also guards `no_unbounded_agents` — every delegation must be time-bounded.
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
from auto_client_acquisition.human_ai_os import (
    HumanAIError,
    get_human_ai_model,
    reset_human_ai_model,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_approval_gate()
    reset_human_ai_model()


def test_delegation_requires_positive_ttl() -> None:
    with pytest.raises(HumanAIError):
        get_human_ai_model().delegate(
            from_human="f", to_agent="a", scope=["x"], ttl_hours=0
        )


def test_bounded_delegation_is_active() -> None:
    model = get_human_ai_model()
    delegation = model.delegate(
        from_human="f", to_agent="a", scope=["draft"], ttl_hours=24
    )
    assert delegation.expires_at > delegation.created_at
    assert model.is_delegation_active(delegation.delegation_id) is True


def test_revoked_delegation_is_inactive() -> None:
    model = get_human_ai_model()
    delegation = model.delegate(
        from_human="f", to_agent="a", scope=["draft"], ttl_hours=24
    )
    model.revoke_delegation(delegation.delegation_id)
    assert model.is_delegation_active(delegation.delegation_id) is False


def test_escalation_creates_oversight_item() -> None:
    model = get_human_ai_model()
    escalation = model.escalate(run_id="run1", reason="needs human review")
    queue = model.oversight_queue()
    assert escalation.ticket_id in {item.ticket_id for item in queue}
