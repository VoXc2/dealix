"""Agent mesh tenant isolation + routing policy tests."""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_mesh_os import AgentDescriptor, AgentMeshRepository


def test_autonomy_ceiling_rejects_high_autonomy_registration() -> None:
    repo = AgentMeshRepository(autonomy_ceiling=3)
    with pytest.raises(ValueError):
        repo.register(
            AgentDescriptor(
                agent_id="agent-high",
                tenant_id="tenant-a",
                name="High",
                owner="owner",
                autonomy_level=4,
                capabilities=["outreach"],
            ),
        )


def test_isolated_agents_are_never_routed() -> None:
    repo = AgentMeshRepository()
    repo.register(
        AgentDescriptor(
            agent_id="agent-1",
            tenant_id="tenant-a",
            name="A",
            owner="owner",
            capabilities=["outreach"],
            composite_score=0.9,
        ),
    )
    repo.isolate(tenant_id="tenant-a", agent_id="agent-1")
    with pytest.raises(ValueError):
        repo.route(tenant_id="tenant-a", capability="outreach")


def test_routing_picks_highest_composite_score_same_tenant() -> None:
    repo = AgentMeshRepository()
    repo.register(
        AgentDescriptor(
            agent_id="agent-low",
            tenant_id="tenant-a",
            name="Low",
            owner="owner",
            capabilities=["sales"],
            composite_score=0.3,
        ),
    )
    repo.register(
        AgentDescriptor(
            agent_id="agent-high",
            tenant_id="tenant-a",
            name="High",
            owner="owner",
            capabilities=["sales"],
            composite_score=0.8,
        ),
    )
    routed = repo.route(tenant_id="tenant-a", capability="sales")
    assert routed.agent_id == "agent-high"


def test_tenant_isolation_prevents_cross_tenant_routing() -> None:
    repo = AgentMeshRepository()
    repo.register(
        AgentDescriptor(
            agent_id="agent-b",
            tenant_id="tenant-b",
            name="B",
            owner="owner",
            capabilities=["sales"],
            composite_score=1.0,
        ),
    )
    with pytest.raises(ValueError):
        repo.route(tenant_id="tenant-a", capability="sales")
