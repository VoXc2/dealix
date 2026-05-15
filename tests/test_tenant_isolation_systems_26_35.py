"""Enterprise Control Plane — tenant isolation across the control modules.

Check #4 of the verify contract: every operational control-plane object
carries a ``tenant_id``, and the in-memory stores never leak one
tenant's objects to another.

Note on naming: the original brief referred to "Systems 26-35"; the real
modules are governance_os / institutional_control_os / approval_center /
agent_os / agent_governance / evidence_control_plane_os / value_os. This
test exercises those.
"""

from __future__ import annotations

import dataclasses

import pytest

from auto_client_acquisition.agent_governance.schemas import AgentSpec
from auto_client_acquisition.agent_os.agent_card import AgentCard
from auto_client_acquisition.agent_os.agent_registry import (
    clear_agent_registry_for_tests,
    get_agent,
    list_agents,
    register_agent,
)
from auto_client_acquisition.approval_center.approval_store import ApprovalStore
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.evidence_control_plane_os.evidence_object import EvidenceObject
from auto_client_acquisition.evidence_control_plane_os.evidence_store import (
    clear_evidence_store_for_tests,
    list_evidence,
    record,
)
from auto_client_acquisition.institutional_control_os.run_registry import (
    clear_run_registry_for_tests,
    get_run,
    list_runs,
    register_run,
)
from auto_client_acquisition.value_os.value_ledger import (
    ValueEvent,
    add_event,
    clear_value_ledger_for_tests,
    list_events,
)


@pytest.fixture(autouse=True)
def _isolated():
    clear_agent_registry_for_tests()
    clear_run_registry_for_tests()
    clear_evidence_store_for_tests()
    clear_value_ledger_for_tests()
    yield
    clear_agent_registry_for_tests()
    clear_run_registry_for_tests()
    clear_evidence_store_for_tests()
    clear_value_ledger_for_tests()


def _dataclass_has_field(cls: type, name: str) -> bool:
    return any(f.name == name for f in dataclasses.fields(cls))


def test_every_operational_object_has_tenant_id():
    """No operational control-plane object without ``tenant_id``."""
    assert _dataclass_has_field(AgentCard, "tenant_id")
    assert _dataclass_has_field(EvidenceObject, "tenant_id")
    assert _dataclass_has_field(ValueEvent, "tenant_id")
    # WorkflowRun is a dataclass too.
    from auto_client_acquisition.institutional_control_os.run_registry import WorkflowRun

    assert _dataclass_has_field(WorkflowRun, "tenant_id")
    # Pydantic models.
    assert "tenant_id" in ApprovalRequest.model_fields
    assert "tenant_id" in AgentSpec.model_fields


def test_agent_registry_is_tenant_scoped():
    register_agent(
        AgentCard("a1", "A1", "owner", "p", 1, "active", tenant_id="t1"),
    )
    register_agent(
        AgentCard("a2", "A2", "owner", "p", 1, "active", tenant_id="t2"),
    )
    assert set(list_agents(tenant_id="t1")) == {"a1"}
    assert set(list_agents(tenant_id="t2")) == {"a2"}
    # Cross-tenant fetch is treated as not found.
    assert get_agent("a1", tenant_id="t2") is None
    assert get_agent("a1", tenant_id="t1") is not None


def test_run_registry_is_tenant_scoped():
    r1 = register_run(tenant_id="t1", workflow_id="wf")
    r2 = register_run(tenant_id="t2", workflow_id="wf")
    assert [r.run_id for r in list_runs(tenant_id="t1")] == [r1.run_id]
    assert [r.run_id for r in list_runs(tenant_id="t2")] == [r2.run_id]
    assert get_run(r1.run_id, tenant_id="t2") is None
    assert get_run(r1.run_id, tenant_id="t1") is not None


def test_approval_store_is_tenant_scoped():
    store = ApprovalStore()
    store.create(
        ApprovalRequest(
            tenant_id="t1", object_type="x", object_id="1", action_type="draft_email",
        ),
    )
    store.create(
        ApprovalRequest(
            tenant_id="t2", object_type="x", object_id="2", action_type="draft_email",
        ),
    )
    assert len(store.list_pending(tenant_id="t1")) == 1
    assert len(store.list_pending(tenant_id="t2")) == 1
    assert len(store.list_pending()) == 2


def test_evidence_store_is_tenant_scoped():
    record(tenant_id="t1", evidence_type="approval", client_id="t1", summary="s1")
    record(tenant_id="t2", evidence_type="approval", client_id="t2", summary="s2")
    assert len(list_evidence(tenant_id="t1")) == 1
    assert len(list_evidence(tenant_id="t2")) == 1


def test_value_ledger_is_tenant_scoped():
    add_event(customer_id="c1", kind="time_saved", tier="estimated", tenant_id="t1")
    add_event(customer_id="c2", kind="time_saved", tier="estimated", tenant_id="t2")
    assert len(list_events(tenant_id="t1")) == 1
    assert len(list_events(tenant_id="t2")) == 1
