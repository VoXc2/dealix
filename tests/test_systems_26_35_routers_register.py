"""Smoke test: the ten Systems 26-35 routers register and respond.

A standalone FastAPI app is built from just the new routers so this test does
not depend on the rest of `api.main` importing.
"""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import (
    agent_mesh_os,
    assurance_contract_os,
    control_plane_os,
    human_ai_os,
    org_graph_os,
    org_simulation_os,
    runtime_safety_os,
    sandbox_os,
    self_evolving_os,
    value_engine_os,
)
from auto_client_acquisition.control_plane_os.approval_gate import reset_approval_gate
from auto_client_acquisition.control_plane_os.core import reset_control_plane
from auto_client_acquisition.control_plane_os.ledger import (
    get_control_ledger,
    reset_control_ledger,
)

_ROUTER_MODULES = [
    control_plane_os,
    agent_mesh_os,
    assurance_contract_os,
    sandbox_os,
    org_graph_os,
    runtime_safety_os,
    org_simulation_os,
    human_ai_os,
    value_engine_os,
    self_evolving_os,
]


@pytest.fixture
def client() -> TestClient:
    reset_control_ledger()
    get_control_ledger().clear_dir()
    reset_approval_gate()
    reset_control_plane()
    app = FastAPI()
    for module in _ROUTER_MODULES:
        app.include_router(module.router)
    return TestClient(app)


def test_all_ten_routers_register() -> None:
    app = FastAPI()
    for module in _ROUTER_MODULES:
        app.include_router(module.router)
    prefixes = {
        "/api/v1/control-plane",
        "/api/v1/agent-mesh",
        "/api/v1/assurance-contracts",
        "/api/v1/sandbox",
        "/api/v1/org-graph",
        "/api/v1/runtime-safety",
        "/api/v1/org-simulation",
        "/api/v1/human-ai",
        "/api/v1/value-engine",
        "/api/v1/self-evolving",
    }
    paths = {r.path for r in app.routes if hasattr(r, "path")}
    for prefix in prefixes:
        assert any(p.startswith(prefix) for p in paths), prefix


def test_control_plane_run_roundtrip(client: TestClient) -> None:
    resp = client.post(
        "/api/v1/control-plane/runs",
        json={"workflow_id": "wf1", "customer_id": "c1", "correlation_id": "x1"},
    )
    assert resp.status_code == 201
    run_id = resp.json()["run_id"]
    assert client.get(f"/api/v1/control-plane/runs/{run_id}").status_code == 200


def test_endpoints_resolve_non_404(client: TestClient) -> None:
    # GET list-style endpoints on each router should resolve (not 404)
    for path in (
        "/api/v1/control-plane/runs",
        "/api/v1/agent-mesh/agents",
        "/api/v1/assurance-contracts/contracts",
        "/api/v1/runtime-safety/circuit-breakers",
        "/api/v1/org-simulation/scenarios",
        "/api/v1/human-ai/oversight-queue",
        "/api/v1/value-engine/optimization-candidates",
        "/api/v1/self-evolving/proposals",
    ):
        assert client.get(path).status_code == 200, path


def test_self_evolving_apply_blocked_without_approval(client: TestClient) -> None:
    created = client.post(
        "/api/v1/self-evolving/proposals",
        json={"target": "workflow", "target_id": "wf1", "rationale": "slow"},
    )
    assert created.status_code == 201
    proposal_id = created.json()["proposal_id"]
    blocked = client.post(
        f"/api/v1/self-evolving/proposals/{proposal_id}/apply", json={"actor": "f"}
    )
    assert blocked.status_code == 409
