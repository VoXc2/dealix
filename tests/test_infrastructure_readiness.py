"""Tests for the operational infrastructure runtime."""

from __future__ import annotations

import pytest
from starlette.testclient import TestClient

from api.main import app
from dealix_infrastructure import EnterpriseReadinessHarness
from dealix_infrastructure.runtime import (
    IdentityPrincipal,
    OperationalMemory,
    PermissionEngine,
    TenantBoundary,
    TenantIsolationError,
)


def test_enterprise_readiness_harness_reports_all_checks_green() -> None:
    result = EnterpriseReadinessHarness().run().to_dict()
    assert result["verdict"] == "enterprise_infrastructure_ready"
    assert all(result["checklist"].values())
    assert result["scenario"]["tenants"] == 1
    assert result["scenario"]["users"] == 3
    assert result["scenario"]["roles"] == 2
    assert result["scenario"]["workflows"] == 1
    assert result["scenario"]["integrations"] == 1


def test_memory_retrieval_is_permission_and_tenant_scoped() -> None:
    tenants = TenantBoundary()
    permissions = PermissionEngine()
    tenants.register("tenant_alpha")
    tenants.register("tenant_bravo")
    permissions.register_principal(
        IdentityPrincipal(
            principal_id="ops_alpha",
            principal_type="user",
            tenant_id="tenant_alpha",
            role="operator",
        )
    )
    permissions.register_principal(
        IdentityPrincipal(
            principal_id="viewer_bravo",
            principal_type="user",
            tenant_id="tenant_bravo",
            role="viewer",
        )
    )
    memory = OperationalMemory(tenants, permissions)
    memory.write(
        tenant_id="tenant_alpha",
        principal_id="ops_alpha",
        namespace="workflow_execution",
        content="lead qualified with evidence",
        citations=("crm://lead",),
        lineage=("run_a", "step_1"),
    )

    with pytest.raises(TenantIsolationError):
        memory.retrieve(
            tenant_id="tenant_alpha",
            principal_id="viewer_bravo",
            query="lead",
            namespace="workflow_execution",
        )


def test_infrastructure_readiness_api_endpoint() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/infrastructure/readiness-test")
    assert response.status_code == 200
    payload = response.json()
    assert payload["verdict"] == "enterprise_infrastructure_ready"
    assert payload["workflow_run"]["status"] == "completed"
