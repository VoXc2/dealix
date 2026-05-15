"""Tenant isolation tests for Systems 26–35 operational objects."""

from __future__ import annotations

from dataclasses import fields

import pytest

from auto_client_acquisition.agent_mesh_os.repositories import AgentDescriptor, TrustBoundary
from auto_client_acquisition.assurance_contract_os.repositories import AssuranceContract
from auto_client_acquisition.control_plane_os.repositories import ApprovalTicket, ControlEvent, WorkflowRun
from auto_client_acquisition.control_plane_os.tenant_context import resolve_tenant_id
from auto_client_acquisition.human_ai_os.repositories import Delegation, Escalation
from auto_client_acquisition.org_graph_os.repositories import GraphNode
from auto_client_acquisition.runtime_safety_os.repositories import CanaryRollout, SandboxRun
from auto_client_acquisition.self_evolving_os.repositories import ImprovementProposal
from auto_client_acquisition.simulation_os.repositories import SimulationScenario
from auto_client_acquisition.value_engine_os.repositories import WorkflowValueMetric


def test_default_tenant_allowed_in_non_production() -> None:
    assert resolve_tenant_id(None, app_env="development") == "default"
    assert resolve_tenant_id(None, app_env="test") == "default"


def test_production_requires_real_tenant_id() -> None:
    with pytest.raises(ValueError, match="tenant_id is required in production"):
        resolve_tenant_id(None, app_env="production")


def test_operational_objects_include_tenant_id() -> None:
    model_types = (
        ControlEvent,
        ApprovalTicket,
        WorkflowRun,
        AgentDescriptor,
        TrustBoundary,
        AssuranceContract,
        SandboxRun,
        CanaryRollout,
        GraphNode,
        SimulationScenario,
        Delegation,
        Escalation,
        WorkflowValueMetric,
        ImprovementProposal,
    )
    for model in model_types:
        model_fields = {f.name for f in fields(model)}
        assert "tenant_id" in model_fields, f"{model.__name__} is missing tenant_id"
