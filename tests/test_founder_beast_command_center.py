"""Founder Beast Command Center — composition + resilience."""
from __future__ import annotations

import pytest
from httpx import ASGITransport, AsyncClient

from api.main import app
from auto_client_acquisition.founder_v10.cache import reset_cache


@pytest.fixture(autouse=True)
def _clear_founder_cache() -> None:
    reset_cache()
    yield
    reset_cache()


@pytest.mark.asyncio
async def test_beast_command_center_returns_200() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/founder/beast-command-center")
        assert r.status_code == 200


@pytest.mark.asyncio
async def test_hard_gates_eight_no_star_fields() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/founder/beast-command-center")
        body = r.json()
        hg = body["hard_gates"]
        assert len(hg) == 8
        for k in (
            "no_live_send",
            "no_live_charge",
            "no_cold_whatsapp",
            "no_linkedin_automation",
            "no_scraping",
            "no_fake_proof",
            "no_fake_revenue",
            "no_unapproved_testimonial",
        ):
            assert hg[k] is True


@pytest.mark.asyncio
async def test_nine_roles_in_role_command_status() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/founder/beast-command-center")
        roles = r.json()["role_command_status"]["roles_supported"]
        assert len(roles) == 9
        assert "ceo" in roles and "finance" in roles


@pytest.mark.asyncio
async def test_revenue_truth_section_present() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/founder/beast-command-center")
        rt = r.json()["revenue_truth"]
        assert not rt.get("_error"), rt
        assert "revenue_live" in rt
        assert "blockers" in rt


@pytest.mark.asyncio
async def test_next_best_action_bilingual() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/founder/beast-command-center")
        b = r.json()
        assert b["next_best_action_ar"]
        assert b["next_best_action_en"]


@pytest.mark.asyncio
async def test_degraded_sections_is_list() -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/founder/beast-command-center")
        assert isinstance(r.json()["degraded_sections"], list)
