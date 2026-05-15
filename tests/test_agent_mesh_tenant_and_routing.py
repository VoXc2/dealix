"""Agent mesh tenant-aware routing behavior."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_mesh_os.repositories import InMemoryAgentMeshRepository
from auto_client_acquisition.agent_mesh_os.schemas import AgentDescriptor


def _agent(
    *,
    agent_id: str,
    tenant_id: str,
    score: float,
    autonomy_level: int,
    status: str = "active",
) -> AgentDescriptor:
    return AgentDescriptor(
        agent_id=agent_id,
        tenant_id=tenant_id,
        name=agent_id,
        owner="owner",
        capabilities=["sales"],
        trust_tier="gold",
        status=status,
        autonomy_level=autonomy_level,
        tool_permissions=["whatsapp.send_message"],
        composite_score=score,
    )


def test_route_picks_highest_score_in_tenant() -> None:
    repo = InMemoryAgentMeshRepository()
    repo.register_agent(_agent(agent_id="a1", tenant_id="t1", score=0.7, autonomy_level=2))
    repo.register_agent(_agent(agent_id="a2", tenant_id="t1", score=0.9, autonomy_level=2))
    repo.register_agent(_agent(agent_id="a3", tenant_id="t2", score=0.99, autonomy_level=2))
    picked = repo.route_agent(tenant_id="t1", capability="sales", max_autonomy=3)
    assert picked.agent_id == "a2"


def test_isolated_agent_is_never_routed() -> None:
    repo = InMemoryAgentMeshRepository()
    repo.register_agent(_agent(agent_id="a1", tenant_id="t1", score=0.8, autonomy_level=2))
    repo.isolate_agent(tenant_id="t1", agent_id="a1")
    with pytest.raises(ValueError, match="no_eligible_agent"):
        repo.route_agent(tenant_id="t1", capability="sales", max_autonomy=3)


def test_autonomy_ceiling_is_enforced() -> None:
    repo = InMemoryAgentMeshRepository()
    repo.register_agent(_agent(agent_id="low", tenant_id="t1", score=0.5, autonomy_level=1))
    repo.register_agent(_agent(agent_id="high", tenant_id="t1", score=0.9, autonomy_level=5))
    picked = repo.route_agent(tenant_id="t1", capability="sales", max_autonomy=3)
    assert picked.agent_id == "low"
