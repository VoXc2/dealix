"""Phase D — assert SafeAgentRuntime blocks restricted actions.

The runtime in ``auto_client_acquisition/v3/agents.py:66`` has a
``restricted_actions`` set covering cold WhatsApp, LinkedIn DM
automation, data deletion, and PII export. Every restricted action
must produce ``status=BLOCKED`` and ``risk_level="blocked"``;
``approve()`` must NOT unblock a BLOCKED task; ``execute()`` must
refuse to run a BLOCKED task.

This is the runtime side of the closure cell ``LIVE_GATES_SAFE``.
"""
from __future__ import annotations

import pytest

from auto_client_acquisition.v3.agents import (
    AgentName,
    AgentTask,
    SafeAgentRuntime,
    TaskStatus,
)


@pytest.fixture
def runtime() -> SafeAgentRuntime:
    return SafeAgentRuntime()


def _make_task(action: str, agent: AgentName = AgentName.OUTREACH) -> AgentTask:
    return AgentTask(
        agent=agent,
        objective=f"safety-test::{action}",
        customer_id="test-customer",
        context={"action": action},
    )


@pytest.mark.parametrize(
    "restricted_action",
    ["send_cold_whatsapp", "auto_linkedin_dm", "delete_data", "export_pii"],
)
def test_restricted_action_creates_blocked_task(
    runtime: SafeAgentRuntime, restricted_action: str
) -> None:
    task = runtime.create_task(_make_task(restricted_action))
    assert task.status == TaskStatus.BLOCKED, (
        f"{restricted_action!r} must produce BLOCKED, got {task.status.value}"
    )
    assert task.risk_level == "blocked"


@pytest.mark.parametrize(
    "restricted_action",
    ["send_cold_whatsapp", "auto_linkedin_dm", "delete_data", "export_pii"],
)
def test_approve_cannot_unblock_restricted_task(
    runtime: SafeAgentRuntime, restricted_action: str
) -> None:
    """A BLOCKED task stays BLOCKED even if approve() is called."""
    task = runtime.create_task(_make_task(restricted_action))
    after = runtime.approve(task.task_id)
    assert after.status == TaskStatus.BLOCKED, (
        "approve() MUST NOT promote a BLOCKED task to APPROVED."
    )


@pytest.mark.parametrize(
    "restricted_action",
    ["send_cold_whatsapp", "auto_linkedin_dm", "delete_data", "export_pii"],
)
def test_execute_refuses_blocked_task(
    runtime: SafeAgentRuntime, restricted_action: str
) -> None:
    task = runtime.create_task(_make_task(restricted_action))
    result = runtime.execute(task.task_id)
    assert result["ok"] is False
    assert result["reason"] == "approval_required_or_blocked"


def test_safe_action_routes_to_approval_or_approved(
    runtime: SafeAgentRuntime,
) -> None:
    """A non-restricted action follows the normal approval path."""
    task = runtime.create_task(_make_task("draft_outreach_message"))
    assert task.status in {TaskStatus.NEEDS_APPROVAL, TaskStatus.APPROVED}
    assert task.risk_level != "blocked"


def test_restricted_actions_set_is_complete():
    """Defensive: catch silent removal of any of the four core blocks."""
    expected = {"send_cold_whatsapp", "auto_linkedin_dm", "delete_data", "export_pii"}
    assert expected.issubset(SafeAgentRuntime.restricted_actions), (
        f"restricted_actions lost protection for: "
        f"{expected - SafeAgentRuntime.restricted_actions}"
    )
