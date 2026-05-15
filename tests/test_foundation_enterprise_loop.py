from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.foundation_core import (
    EnterpriseLoopRequest,
    LeadInput,
    run_smallest_governed_loop,
)


def _demo_request(*, approval_granted: bool) -> EnterpriseLoopRequest:
    return EnterpriseLoopRequest(
        tenant_id="tenant_alpha",
        user_id="user_1",
        user_role="sales_manager",
        approval_granted=approval_granted,
        lead=LeadInput(
            company="Acme Riyadh",
            name="Fahad",
            email="fahad@acme.sa",
            phone="+966500000001",
            sector="technology",
            region="Saudi Arabia",
            message="Need help improving pipeline",
            budget=20000,
        ),
    )


def test_enterprise_loop_completes_when_approved() -> None:
    result = run_smallest_governed_loop(_demo_request(approval_granted=True))
    assert result["status"] == "completed"
    assert result["outputs"]["crm_update"]["status"] == "updated"
    assert result["outputs"]["governance"]["allowed"] is True
    assert result["readiness"]["workflow_count"] == 1
    assert result["readiness"]["rollback_drill"] == "passed"
    assert result["observability"]["trace_id"].startswith("trace_")


def test_enterprise_loop_blocks_without_approval() -> None:
    result = run_smallest_governed_loop(_demo_request(approval_granted=False))
    assert result["status"] == "blocked"
    assert result["outputs"]["governance"]["allowed"] is False
    assert result["outputs"]["crm_update"] is None
    assert result["error"] == "manual_approval_required"


@pytest.mark.asyncio
async def test_foundation_router_executes_enterprise_loop() -> None:
    from api.main import app

    payload = {
        "tenant_id": "tenant_beta",
        "user_id": "user_2",
        "user_role": "sales_manager",
        "approval_granted": True,
        "lead": {
            "company": "Beta LLC",
            "name": "Nora",
            "email": "nora@beta.sa",
            "phone": "+966500000002",
            "sector": "software",
            "region": "Saudi Arabia",
            "message": "Need revenue OS workflow",
            "budget": 12000,
        },
    }
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        status_res = await client.get("/api/v1/foundation/status")
        run_res = await client.post("/api/v1/foundation/enterprise-loop/run", json=payload)

    assert status_res.status_code == 200
    assert status_res.json()["service"] == "foundation_core"
    assert run_res.status_code == 200
    body = run_res.json()
    assert body["status"] == "completed"
    assert body["outputs"]["executive_metrics"]["pipeline_priority"] in {"P1", "P2", "P3"}
