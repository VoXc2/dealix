"""Agent mesh tenant isolation and routing tests."""

from __future__ import annotations

from auto_client_acquisition.agent_mesh_os.repositories import (
    AgentDescriptor,
    InMemoryAgentMeshRepository,
    TrustBoundary,
)


def test_agent_mesh_routes_within_tenant_boundary() -> None:
    repo = InMemoryAgentMeshRepository()
    repo.set_trust_boundary(
        TrustBoundary(
            boundary_id="b1",
            tenant_id="tenant-a",
            scope="sales",
            max_autonomy_level=2,
        )
    )
    repo.register_agent(
        AgentDescriptor(
            agent_id="sales-agent-a",
            tenant_id="tenant-a",
            name="Sales Agent A",
            owner="ops",
            capabilities=("outbound_sales",),
            trust_tier="trusted",
            status="active",
            autonomy_level=2,
            composite_score=0.91,
        )
    )
    repo.register_agent(
        AgentDescriptor(
            agent_id="sales-agent-b",
            tenant_id="tenant-b",
            name="Sales Agent B",
            owner="ops",
            capabilities=("outbound_sales",),
            trust_tier="trusted",
            status="active",
            autonomy_level=2,
            composite_score=0.99,
        )
    )

    routed = repo.route_agent(tenant_id="tenant-a", capability="outbound_sales")
    assert routed is not None
    assert routed.agent_id == "sales-agent-a"
    assert routed.tenant_id == "tenant-a"

    repo.isolate_agent(tenant_id="tenant-a", agent_id="sales-agent-a")
    assert repo.route_agent(tenant_id="tenant-a", capability="outbound_sales") is None
