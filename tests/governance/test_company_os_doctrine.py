"""Doctrine guards for the Company OS layer.

Enforces: the deferred roadmap phases stay gated, every agent template
is bounded, and every company-os endpoint carries a governance signal.
"""

from __future__ import annotations

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from api.routers import company_os as company_os_router
from auto_client_acquisition.agent_factory import all_templates_valid, validate_all
from auto_client_acquisition.company_os import (
    RoadmapPhase,
    doctrine_coverage,
    get_phase_gate,
)


@pytest_asyncio.fixture
async def cos_client():
    app = FastAPI()
    app.include_router(company_os_router.router)
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


def test_agentic_and_enterprise_phases_are_deferred() -> None:
    """Constitution Article 13: no Scale phase before commercial proof."""
    assert get_phase_gate(RoadmapPhase.AGENTIC_PLATFORM).deferred_gated is True
    assert get_phase_gate(RoadmapPhase.ENTERPRISE_READINESS).deferred_gated is True


def test_deferred_phases_require_three_paid_pilots() -> None:
    for phase in (RoadmapPhase.AGENTIC_PLATFORM, RoadmapPhase.ENTERPRISE_READINESS):
        gate = get_phase_gate(phase)
        assert gate.activation_condition == "3_paid_pilots_signed"


def test_every_agent_template_is_bounded() -> None:
    """no_unbounded_agents: no template may ship with doctrine violations."""
    violations = validate_all()
    assert all_templates_valid() is True, violations


def test_all_eleven_non_negotiables_are_enforced() -> None:
    coverage = doctrine_coverage()
    assert coverage["non_negotiable_count"] == 11
    assert coverage["fully_covered"] is True


@pytest.mark.asyncio
async def test_company_os_endpoints_return_governance_decision(cos_client) -> None:
    paths = (
        "/api/v1/company-os/systems",
        "/api/v1/company-os/maturity",
        "/api/v1/company-os/roadmap",
        "/api/v1/company-os/doctrine",
        "/api/v1/company-os/agent-factory/templates",
        "/api/v1/company-os/eval/metrics",
        "/api/v1/company-os/transformation/stages",
    )
    for path in paths:
        resp = await cos_client.get(path)
        assert resp.status_code == 200, path
        assert "governance_decision" in resp.json(), path
