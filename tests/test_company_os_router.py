"""Company OS router — read-only spine endpoints.

Mounts only the company-os router on a fresh app so the suite stays
isolated from unrelated routers.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers import company_os as company_os_router


@pytest_asyncio.fixture
async def cos_client():
    app = FastAPI()
    app.include_router(company_os_router.router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_get_systems(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/systems")
    assert resp.status_code == 200
    body = resp.json()
    assert body["system_count"] == 7
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_one_system(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/systems/governance_system")
    assert resp.status_code == 200
    body = resp.json()
    assert body["system"]["system_id"] == "governance_system"
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_unknown_system_404(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/systems/nope")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_get_maturity(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/maturity")
    assert resp.status_code == 200
    body = resp.json()
    assert body["system_count"] == 7
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_roadmap_defers_phase_three(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/roadmap")
    assert resp.status_code == 200
    body = resp.json()
    phase3 = next(
        p for p in body["phases"] if p["phase"] == "phase_3_agentic_platform"
    )
    assert phase3["deferred_gated"] is True
    assert phase3["active"] is False
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_roadmap_unlocks_at_three_pilots(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/roadmap?paid_pilots=3")
    assert resp.status_code == 200
    phase3 = next(
        p for p in resp.json()["phases"] if p["phase"] == "phase_3_agentic_platform"
    )
    assert phase3["active"] is True


@pytest.mark.asyncio
async def test_get_doctrine(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/doctrine")
    assert resp.status_code == 200
    body = resp.json()
    assert body["non_negotiable_count"] == 11
    assert body["fully_covered"] is True
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_agent_factory_templates(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/agent-factory/templates")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["templates"]) == 6
    assert body["all_valid"] is True
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_eval_metrics(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/eval/metrics")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["categories"]) == 4
    assert body["metric_count"] >= 8
    assert body["governance_decision"] == "ALLOW"


@pytest.mark.asyncio
async def test_get_transformation_stages(cos_client) -> None:
    resp = await cos_client.get("/api/v1/company-os/transformation/stages")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["stages"]) == 5
    assert body["governance_decision"] == "ALLOW"
