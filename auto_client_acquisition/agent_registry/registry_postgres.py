"""Postgres-backed Agent Registry store — doctrine #9.

Persists :class:`AgentSpec` rows to :class:`db.models.AgentRegistryRecord`
(table ``agent_registry``, unique ``agent_name``). Every register / disable
mutation fires the audit hook.

``register`` hard-fails when ``owner`` or ``scope`` is empty — no agent is
registered without an owner and a scope.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import Engine, create_engine, select
from sqlalchemy.orm import sessionmaker

from auto_client_acquisition.agent_registry.audit_hook import emit_audit
from auto_client_acquisition.agent_registry.schemas import AgentSpec
from db.models import AgentRegistryRecord


class AgentRegistryError(Exception):
    """Raised on a governance violation in the Agent Registry."""


def _row_to_spec(row: AgentRegistryRecord) -> AgentSpec:
    return AgentSpec(
        agent_name=row.agent_name,
        owner=row.owner,
        scope=row.scope,
        allowed_tools=list(row.allowed_tools or []),
        risk_class=row.risk_class,  # type: ignore[arg-type]
        audit_hook=row.audit_hook,
    )


class PostgresAgentRegistry:
    """SQLAlchemy-backed Agent Registry store."""

    def __init__(
        self,
        *,
        engine: Engine | None = None,
        database_url: str | None = None,
        create_tables: bool = True,
    ) -> None:
        if engine is None:
            url = database_url or "sqlite:///:memory:"
            engine = create_engine(url, future=True)
        self._engine: Engine = engine
        self._sessionmaker = sessionmaker(self._engine, expire_on_commit=False, future=True)
        self._lock = threading.Lock()
        if create_tables:
            AgentRegistryRecord.__table__.create(self._engine, checkfirst=True)

    def register(self, spec: AgentSpec) -> AgentSpec:
        """Register or replace one agent. Hard-fails without owner + scope."""
        if not spec.owner or not spec.owner.strip():
            raise AgentRegistryError("agent owner is mandatory (doctrine #9)")
        if not spec.scope or not spec.scope.strip():
            raise AgentRegistryError("agent scope is mandatory (doctrine #9)")
        now = datetime.now(UTC)
        with self._lock, self._sessionmaker() as session:
            existing = session.execute(
                select(AgentRegistryRecord).where(
                    AgentRegistryRecord.agent_name == spec.agent_name
                )
            ).scalar_one_or_none()
            if existing is None:
                row = AgentRegistryRecord(
                    id=f"agt_{uuid4().hex[:20]}",
                    agent_name=spec.agent_name,
                    owner=spec.owner,
                    scope=spec.scope,
                    allowed_tools=list(spec.allowed_tools),
                    risk_class=spec.risk_class,
                    audit_hook=spec.audit_hook,
                    enabled=True,
                    created_at=now,
                    updated_at=now,
                )
                session.add(row)
            else:
                existing.owner = spec.owner
                existing.scope = spec.scope
                existing.allowed_tools = list(spec.allowed_tools)
                existing.risk_class = spec.risk_class
                existing.audit_hook = spec.audit_hook
                existing.updated_at = now
            session.commit()
        emit_audit(
            engine=self._engine,
            action="agent_registry.register",
            agent_name=spec.agent_name,
            detail={"owner": spec.owner, "risk_class": spec.risk_class},
        )
        return spec

    def get(self, agent_name: str) -> AgentSpec | None:
        """Fetch one agent spec by name, or None."""
        with self._lock, self._sessionmaker() as session:
            row = session.execute(
                select(AgentRegistryRecord).where(
                    AgentRegistryRecord.agent_name == agent_name
                )
            ).scalar_one_or_none()
        return _row_to_spec(row) if row is not None else None

    def list(self, *, include_disabled: bool = True) -> list[AgentSpec]:
        """Return all registered agents."""
        stmt = select(AgentRegistryRecord).order_by(AgentRegistryRecord.agent_name)
        if not include_disabled:
            stmt = stmt.where(AgentRegistryRecord.enabled.is_(True))
        with self._lock, self._sessionmaker() as session:
            rows = session.execute(stmt).scalars().all()
        return [_row_to_spec(r) for r in rows]

    def verify(self, agent_name: str) -> bool:
        """True only when the agent exists, is enabled and carries owner + scope."""
        with self._lock, self._sessionmaker() as session:
            row = session.execute(
                select(AgentRegistryRecord).where(
                    AgentRegistryRecord.agent_name == agent_name
                )
            ).scalar_one_or_none()
        if row is None or not row.enabled:
            return False
        if not row.owner or not row.owner.strip():
            return False
        if not row.scope or not row.scope.strip():
            return False
        return True

    def disable(self, agent_name: str) -> bool:
        """Disable one agent (kept for audit; not deleted). Returns True if found."""
        with self._lock, self._sessionmaker() as session:
            row = session.execute(
                select(AgentRegistryRecord).where(
                    AgentRegistryRecord.agent_name == agent_name
                )
            ).scalar_one_or_none()
            if row is None:
                return False
            row.enabled = False
            row.updated_at = datetime.now(UTC)
            session.commit()
        emit_audit(
            engine=self._engine,
            action="agent_registry.disable",
            agent_name=agent_name,
        )
        return True

    def can_run(self, agent_name: str) -> bool:
        """True only when the agent verifies AND its risk_class is not ``blocked``."""
        spec = self.get(agent_name)
        if spec is None or spec.risk_class == "blocked":
            emit_audit(
                engine=self._engine,
                action="agent_registry.run_check",
                agent_name=agent_name,
                detail={"allowed": False},
            )
            return False
        allowed = self.verify(agent_name)
        emit_audit(
            engine=self._engine,
            action="agent_registry.run_check",
            agent_name=agent_name,
            detail={"allowed": allowed},
        )
        return allowed

    def tool_allowed(self, agent_name: str, tool: str) -> bool:
        """True when the agent is registered and ``tool`` is in its allowlist."""
        spec = self.get(agent_name)
        return spec is not None and tool in spec.allowed_tools

    @property
    def engine(self) -> Engine:
        return self._engine

    def clear_for_test(self) -> None:
        """Test-only: drop and recreate the registry table."""
        with self._lock:
            AgentRegistryRecord.__table__.drop(self._engine, checkfirst=True)
            AgentRegistryRecord.__table__.create(self._engine, checkfirst=True)


__all__ = ["AgentRegistryError", "PostgresAgentRegistry"]
