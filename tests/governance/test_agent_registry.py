"""B3 — Agent Registry doctrine #9 tests (owner + scope + audit)."""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker

from auto_client_acquisition.agent_registry import (
    SEED_AGENT_NAMES,
    AgentSpec,
    seed_default_agents,
)
from auto_client_acquisition.agent_registry.registry_postgres import (
    AgentRegistryError,
    PostgresAgentRegistry,
)
from db.models import AuditLogRecord


@pytest.fixture()
def registry() -> PostgresAgentRegistry:
    engine = create_engine("sqlite:///:memory:", future=True)
    AuditLogRecord.__table__.create(engine, checkfirst=True)
    return PostgresAgentRegistry(engine=engine)


def _spec(**overrides) -> AgentSpec:
    base = dict(
        agent_name="demo_agent",
        owner="founder",
        scope="draft demo messages",
        allowed_tools=["draft_message"],
        risk_class="draft_only",
    )
    base.update(overrides)
    return AgentSpec(**base)


def test_registration_rejected_without_owner() -> None:
    with pytest.raises(Exception):
        AgentSpec(agent_name="x", owner="", scope="s")


def test_registration_rejected_without_scope() -> None:
    with pytest.raises(Exception):
        AgentSpec(agent_name="x", owner="founder", scope="")


def test_register_hard_fails_on_blank_owner(registry: PostgresAgentRegistry) -> None:
    spec = _spec()
    object.__setattr__(spec, "owner", "  ")
    with pytest.raises(AgentRegistryError):
        registry.register(spec)


def test_register_and_verify(registry: PostgresAgentRegistry) -> None:
    registry.register(_spec())
    assert registry.verify("demo_agent") is True
    assert registry.get("demo_agent") is not None


def test_verify_false_for_unregistered(registry: PostgresAgentRegistry) -> None:
    assert registry.verify("ghost_agent") is False


def test_allowed_tools_enforcement(registry: PostgresAgentRegistry) -> None:
    registry.register(_spec(allowed_tools=["draft_message"]))
    assert registry.tool_allowed("demo_agent", "draft_message") is True
    assert registry.tool_allowed("demo_agent", "send_email_live") is False


def test_blocked_agent_cannot_run(registry: PostgresAgentRegistry) -> None:
    registry.register(_spec(agent_name="blocked_agent", risk_class="blocked"))
    assert registry.can_run("blocked_agent") is False


def test_enabled_agent_can_run(registry: PostgresAgentRegistry) -> None:
    registry.register(_spec(agent_name="run_agent", risk_class="safe_auto"))
    assert registry.can_run("run_agent") is True


def test_disabled_agent_cannot_run(registry: PostgresAgentRegistry) -> None:
    registry.register(_spec(agent_name="off_agent", risk_class="safe_auto"))
    registry.disable("off_agent")
    assert registry.can_run("off_agent") is False
    assert registry.verify("off_agent") is False


def test_audit_hook_fires_on_register(registry: PostgresAgentRegistry) -> None:
    registry.register(_spec())
    maker = sessionmaker(registry.engine, future=True)
    with maker() as session:
        rows = session.execute(
            select(AuditLogRecord).where(
                AuditLogRecord.action == "agent_registry.register"
            )
        ).scalars().all()
    assert len(rows) >= 1
    assert rows[0].entity_id == "demo_agent"


def test_seed_registers_twelve_agents(registry: PostgresAgentRegistry) -> None:
    seed_default_agents(registry=registry)
    names = {a.agent_name for a in registry.list()}
    assert names == set(SEED_AGENT_NAMES)
    assert len(SEED_AGENT_NAMES) == 12
    # every seeded agent carries owner + scope
    for spec in registry.list():
        assert spec.owner.strip()
        assert spec.scope.strip()
