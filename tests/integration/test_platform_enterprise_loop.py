"""Integration tests — Enterprise Foundation Core loop (platform_core).

Verifies the eleven-step governed loop end to end, the doctrine guard on the
approval step, the rollback drill, and the live proof router.
"""

from __future__ import annotations

import platform as stdlib_platform

import pytest

from platform_core import enterprise_loop as loop
from platform_core import stores
from platform_core.agent_runtime import clear_agent_registry_for_tests, get_agent


@pytest.fixture(autouse=True)
def _clean_loop_state(monkeypatch):
    """Isolate every test from module-global state and run the router in dev mode.

    Clearing the key env vars puts ``require_admin_key`` into dev mode so the
    proof endpoints are reachable without a configured admin key. In a real
    deployment ADMIN_API_KEYS is set and the endpoints require the header.
    """
    monkeypatch.setenv("API_KEYS", "")
    monkeypatch.setenv("ADMIN_API_KEYS", "")
    clear_agent_registry_for_tests()
    loop.reset_runs_for_tests()
    stores.reset_stores_for_tests()
    yield
    clear_agent_registry_for_tests()
    loop.reset_runs_for_tests()
    stores.reset_stores_for_tests()


async def test_enterprise_loop_full_pass():
    """All eleven steps run, succeed, and produce a valid audit chain."""
    from platform_core.observability import audit_event_valid

    ctx = await loop.run_enterprise_loop(
        tenant_handle="acme_loop", tenant_name="Acme Loop Co",
    )

    assert len(ctx.steps) == 11
    assert all(s.ok for s in ctx.steps), [s.step for s in ctx.steps if not s.ok]
    assert all(audit_event_valid(s.audit) for s in ctx.steps)
    assert ctx.as_dict()["audit_chain_valid"] is True

    # The canonical proof checklist is satisfied.
    assert ctx.created["tenant"] is not None
    assert len(ctx.created["users"]) == 3
    assert len(ctx.created["roles"]) == 2
    assert ctx.created["agent"] is not None
    assert "workflow_draft" in ctx.artifacts
    assert "executive_report" in ctx.artifacts
    assert ctx.artifacts["eval_report"]["passed"] is True
    assert ctx.rolled_back is True


async def test_agent_requires_identity():
    """A blank owner fails the agent card — step 4 fails cleanly, no raise."""
    ctx = loop.new_run()
    await loop.step_provision_tenant(
        ctx, tenant_handle="id_loop", tenant_name="Identity Loop",
    )
    result = await loop.step_register_agent(ctx, owner="")

    assert result.ok is False
    assert result.detail["card_valid"] is False
    assert ctx.created["agent"] is None
    assert result.audit.decision == "agent_rejected"


async def test_doctrine_blocks_external_send():
    """Requesting an external send without approval raises and is audited."""
    ctx = loop.new_run()
    await loop.step_provision_tenant(
        ctx, tenant_handle="doc_loop", tenant_name="Doctrine Loop",
    )
    with pytest.raises(ValueError, match="doctrine_violations"):
        await loop.step_apply_approval(
            ctx, request_external_send_without_approval=True,
        )

    assert ctx.steps[-1].step == "apply_approval"
    assert ctx.steps[-1].ok is False
    assert ctx.steps[-1].audit.decision == "doctrine_violation"


async def test_approval_left_pending_human():
    """The approval flow is never auto-completed — human steps stay pending."""
    ctx = loop.new_run()
    await loop.step_provision_tenant(
        ctx, tenant_handle="apr_loop", tenant_name="Approval Loop",
    )
    result = await loop.step_apply_approval(ctx)

    assert result.ok is True
    assert result.detail["approval_flow_complete"] is False
    assert result.detail["approval_status"] == "pending_human"
    assert "client_approval" in result.detail["approval_flow_missing"]


async def test_rollback_drill():
    """Rollback soft-deletes the run's entities and deregisters its agent."""
    ctx = await loop.run_enterprise_loop(
        tenant_handle="rb_loop", tenant_name="Rollback Loop",
    )
    agent_id = ctx.created["agent"]
    tenant_id = ctx.created["tenant"]

    assert get_agent(agent_id) is None  # deregistered by the drill
    assert stores._TENANTS[tenant_id].deleted is True
    assert all(stores._USERS[u].deleted for u in ctx.created["users"])
    assert all(stores._ROLES[r].deleted for r in ctx.created["roles"])


async def test_crm_step_is_draft_only():
    """The CRM step never performs a live send."""
    ctx = await loop.run_enterprise_loop(
        tenant_handle="crm_loop", tenant_name="CRM Loop",
    )
    crm = ctx.artifacts["crm_draft"]
    assert crm["mode"] == "draft_only"
    assert crm["synced"] is False


async def test_invalid_tenant_handle_rejected():
    """An invalid tenant handle is rejected before anything is created."""
    ctx = loop.new_run()
    with pytest.raises(ValueError, match="invalid_tenant_handle"):
        await loop.step_provision_tenant(
            ctx, tenant_handle="X", tenant_name="Bad Handle",
        )


async def test_stdlib_platform_not_shadowed():
    """The platform_core package must not shadow the stdlib `platform` module."""
    import platform_core  # noqa: F401

    assert stdlib_platform.python_version()
    assert hasattr(stdlib_platform, "system")


@pytest.fixture
def admin_client(async_client):
    """async_client with a dev admin key — endpoints are admin-key gated."""
    async_client.headers["X-Admin-API-Key"] = "dev"
    return async_client


async def test_router_loop_run(admin_client):
    """The live proof endpoint runs the full loop and returns a valid chain."""
    resp = await admin_client.post(
        "/api/v1/platform/loop/run",
        json={"tenant_handle": "router_loop", "tenant_name": "Router Loop Co"},
    )
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert len(body["steps"]) == 11
    assert body["audit_chain_valid"] is True
    assert all(s["ok"] for s in body["steps"])


async def test_router_health(admin_client):
    """The facade health endpoint reports a clean foundation."""
    resp = await admin_client.get("/api/v1/platform/health")
    assert resp.status_code == 200, resp.text
    body = resp.json()
    assert body["status"] == "ok"
    assert body["stdlib_platform_ok"] is True
    assert len(body["facades"]) == 7


async def test_router_step_by_step(admin_client):
    """Walking the loop step by step produces a complete audited run."""
    rid = "stepwise_demo"
    await admin_client.post(
        f"/api/v1/platform/loop/{rid}/step/tenant",
        json={"tenant_handle": "stepwise_loop", "tenant_name": "Stepwise Co"},
    )
    for step in ("users", "roles", "agent", "workflow", "approval",
                 "crm", "executive-report", "eval-report", "rollback"):
        resp = await admin_client.post(f"/api/v1/platform/loop/{rid}/step/{step}", json={})
        assert resp.status_code == 200, (step, resp.text)
        assert resp.json()["step"]["ok"] is True

    audit = await admin_client.get(f"/api/v1/platform/loop/{rid}/audit")
    assert audit.status_code == 200
    assert audit.json()["all_valid"] is True
    assert audit.json()["event_count"] == 11


async def test_router_doctrine_returns_403(admin_client):
    """An external-send-without-approval request returns HTTP 403."""
    rid = "doctrine_demo"
    await admin_client.post(
        f"/api/v1/platform/loop/{rid}/step/tenant",
        json={"tenant_handle": "doctrine_loop", "tenant_name": "Doctrine Co"},
    )
    resp = await admin_client.post(
        f"/api/v1/platform/loop/{rid}/step/approval",
        json={"request_external_send_without_approval": True},
    )
    assert resp.status_code == 403, resp.text
    assert "doctrine_violations" in resp.text
