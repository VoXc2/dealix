"""Tests for System 27 — agent_mesh_os."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from auto_client_acquisition.agent_mesh_os import (
    AUTONOMY_CEILING,
    AgentDescriptor,
    get_agent_mesh,
    reset_agent_mesh,
)
from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_agent_mesh()


def test_register_discover_route() -> None:
    mesh = get_agent_mesh()
    mesh.register_agent(
        AgentDescriptor(agent_id="a1", name="A", owner="o", capabilities=["draft"])
    )
    assert [a.agent_id for a in mesh.discover("draft")] == ["a1"]
    assert mesh.route(capability="draft").chosen_agent_id == "a1"


def test_isolated_agent_is_not_routable() -> None:
    mesh = get_agent_mesh()
    mesh.register_agent(
        AgentDescriptor(agent_id="a1", name="A", owner="o", capabilities=["draft"])
    )
    mesh.isolate_agent("a1", reason="misbehaving")
    assert mesh.discover("draft") == []
    assert mesh.route(capability="draft").chosen_agent_id is None


def test_route_picks_highest_score() -> None:
    mesh = get_agent_mesh()
    for aid in ("a1", "a2"):
        mesh.register_agent(
            AgentDescriptor(agent_id=aid, name=aid, owner="o", capabilities=["draft"])
        )
    mesh.score_agent("a1", reliability=0.5, safety=0.5, latency_ms=100)
    mesh.score_agent("a2", reliability=0.95, safety=0.99, latency_ms=50)
    assert mesh.route(capability="draft").chosen_agent_id == "a2"


def test_autonomy_is_bounded() -> None:
    # no_unbounded_agents — autonomy cannot exceed the MVP ceiling
    assert AUTONOMY_CEILING == 4
    with pytest.raises(ValidationError):
        AgentDescriptor(agent_id="bad", name="B", owner="o", autonomy_level=5)
