"""Enterprise Control Plane — agent governance: routing + tenant scope.

Check #6 of the verify contract: agent actions are contract-gated.
Exercises ``agent_governance`` (capability routing, forbidden tools,
approval-required tools) and the tenant-scoped ``agent_os`` registry.

Note: the original brief called this layer "agent_mesh_os"; the real
module is ``agent_governance`` + ``agent_os``.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.agent_governance.policy import (
    APPROVAL_REQUIRED_TOOLS,
    FORBIDDEN_TOOLS,
    evaluate_action,
)
from auto_client_acquisition.agent_governance.schemas import (
    AgentSpec,
    AutonomyLevel,
    ToolCategory,
    ToolPermission,
)
from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    list_agents,
    register_agent,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_agent_registry_for_tests()
    yield
    clear_agent_registry_for_tests()


def test_agent_spec_carries_tenant_id():
    spec = AgentSpec(
        agent_id="a1", tenant_id="t1", purpose_ar="غرض", purpose_en="purpose",
    )
    assert spec.tenant_id == "t1"


def test_forbidden_tool_is_denied_regardless_of_autonomy():
    verdict = evaluate_action(
        agent_id="a1",
        tool=ToolCategory.SEND_WHATSAPP_LIVE,
        autonomy_level=AutonomyLevel.L4_INTERNAL_AUTOMATION_ONLY,
        allowed_tools=[ToolCategory.SEND_WHATSAPP_LIVE],
    )
    assert verdict.permitted is False
    assert verdict.permission == ToolPermission.FORBIDDEN
    assert ToolCategory.SEND_WHATSAPP_LIVE in FORBIDDEN_TOOLS


def test_external_visible_tool_requires_approval():
    verdict = evaluate_action(
        agent_id="a1",
        tool=ToolCategory.DRAFT_EMAIL,
        autonomy_level=AutonomyLevel.L3_APPROVED_EXECUTE,
        allowed_tools=[ToolCategory.DRAFT_EMAIL],
    )
    assert verdict.permission == ToolPermission.REQUIRES_APPROVAL
    assert ToolCategory.DRAFT_EMAIL in APPROVAL_REQUIRED_TOOLS


def test_read_only_tool_is_allowed():
    verdict = evaluate_action(
        agent_id="a1",
        tool=ToolCategory.READ_INTERNAL_DOCS,
        autonomy_level=AutonomyLevel.L1_DRAFT_ONLY,
        allowed_tools=[ToolCategory.READ_INTERNAL_DOCS],
    )
    assert verdict.permitted is True
    assert verdict.permission == ToolPermission.ALLOWED


def test_tool_not_in_allowed_list_is_denied():
    verdict = evaluate_action(
        agent_id="a1",
        tool=ToolCategory.GENERATE_PROOF_PACK,
        autonomy_level=AutonomyLevel.L2_APPROVAL_REQUIRED,
        allowed_tools=[ToolCategory.READ_INTERNAL_DOCS],
    )
    assert verdict.permitted is False


def test_agent_registry_routes_by_tenant():
    register_agent(AgentCard("sales-t1", "Sales", "founder", "sell", 1, "active", tenant_id="t1"))
    register_agent(AgentCard("sales-t2", "Sales", "founder", "sell", 1, "active", tenant_id="t2"))
    t1_agents = list_agents(tenant_id="t1")
    assert "sales-t1" in t1_agents
    assert "sales-t2" not in t1_agents
