"""Gap-fill stores for the enterprise loop.

The existing modules provide governance, identity, workflow and audit
primitives but no standalone callables for provisioning a tenant / users /
roles, and no rollback mechanism. This module fills exactly those gaps and
nothing more.

Design:
  * An in-memory mirror is the source of truth for a loop run, so the loop
    is fully runnable in any environment (no DB required).
  * Every DB write is best-effort: when the DB layer is unavailable the loop
    logs and continues against the in-memory mirror.
  * No PII is written to audit fields — IDs and structural data only.
"""

from __future__ import annotations

import logging
import re
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone

from auto_client_acquisition.agent_os import agent_registry
from auto_client_acquisition.auditability_os.audit_event import AuditEvent

log = logging.getLogger(__name__)

_SLUG_RE = re.compile(r"^[a-z][a-z0-9_]{1,62}[a-z0-9]$")


# ── In-memory mirrors (source of truth for a loop run) ──────────────

@dataclass
class TenantEntity:
    id: str
    handle: str
    name: str
    deleted: bool = False


@dataclass
class UserEntity:
    id: str
    tenant_id: str
    email: str
    name: str
    role_name: str
    deleted: bool = False


@dataclass
class RoleEntity:
    id: str
    tenant_id: str
    name: str
    permissions: list[str] = field(default_factory=list)
    deleted: bool = False


_TENANTS: dict[str, TenantEntity] = {}
_USERS: dict[str, UserEntity] = {}
_ROLES: dict[str, RoleEntity] = {}


def reset_stores_for_tests() -> None:
    """Clear all in-memory mirrors (test isolation)."""
    _TENANTS.clear()
    _USERS.clear()
    _ROLES.clear()


def _now() -> datetime:
    return datetime.now(timezone.utc)


# ── Tenant / user / role provisioning ───────────────────────────────

async def create_tenant(handle: str, name: str) -> TenantEntity:
    """Provision a tenant. Raises ValueError on an invalid handle."""
    handle = handle.strip().lower()
    if not _SLUG_RE.match(handle):
        msg = f"invalid_tenant_handle: must match {_SLUG_RE.pattern}"
        raise ValueError(msg)
    tenant = TenantEntity(id=f"tn_{uuid.uuid4().hex[:16]}", handle=handle, name=name.strip())
    _TENANTS[tenant.id] = tenant
    await _db_insert_tenant(tenant)
    return tenant


async def create_user(tenant_id: str, email: str, name: str, role_name: str) -> UserEntity:
    """Provision a non-login user fixture for the loop."""
    user = UserEntity(
        id=f"usr_{uuid.uuid4().hex[:16]}",
        tenant_id=tenant_id,
        email=email.strip(),
        name=name.strip(),
        role_name=role_name.strip(),
    )
    _USERS[user.id] = user
    await _db_insert_user(user)
    return user


async def create_role(tenant_id: str, name: str, permissions: list[str]) -> RoleEntity:
    """Provision an RBAC role for the loop."""
    role = RoleEntity(
        id=f"rol_{uuid.uuid4().hex[:16]}",
        tenant_id=tenant_id,
        name=name.strip(),
        permissions=list(permissions),
    )
    _ROLES[role.id] = role
    await _db_insert_role(role)
    return role


# ── Rollback drill ──────────────────────────────────────────────────

async def rollback_run(
    *,
    tenant_id: str | None,
    user_ids: list[str],
    role_ids: list[str],
    agent_id: str | None,
) -> dict[str, list[str]]:
    """Soft-delete the entities a loop run created and drop its agent.

    Returns a map of what was rolled back. Idempotent.
    """
    rolled: dict[str, list[str]] = {"tenant": [], "users": [], "roles": [], "agent": []}

    for uid in user_ids:
        u = _USERS.get(uid)
        if u is not None and not u.deleted:
            u.deleted = True
            rolled["users"].append(uid)
    for rid in role_ids:
        r = _ROLES.get(rid)
        if r is not None and not r.deleted:
            r.deleted = True
            rolled["roles"].append(rid)
    if tenant_id is not None:
        t = _TENANTS.get(tenant_id)
        if t is not None and not t.deleted:
            t.deleted = True
            rolled["tenant"].append(tenant_id)

    if agent_id is not None and agent_registry.get_agent(agent_id) is not None:
        # The registry exposes no public single-delete (only a test-wide
        # clear), so the rollback drill pops this run's agent directly.
        agent_registry._REGISTRY.pop(agent_id, None)  # noqa: SLF001
        rolled["agent"].append(agent_id)

    await _db_rollback(tenant_id, user_ids, role_ids)
    return rolled


# ── Best-effort DB persistence (never raises into the loop) ─────────

async def _db_insert_tenant(tenant: TenantEntity) -> None:
    try:
        from db.models import TenantRecord
        from db.session import async_session_factory
    except Exception:  # noqa: BLE001 — DB layer optional for the loop
        return
    try:
        async with async_session_factory()() as session:
            session.add(
                TenantRecord(
                    id=tenant.id,
                    name=tenant.name,
                    slug=tenant.handle,
                    plan="pilot",
                    status="active",
                    features={},
                    meta_json={"created_via": "enterprise_loop"},
                    created_at=_now(),
                    updated_at=_now(),
                ),
            )
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("enterprise_loop tenant DB persist skipped: %s", exc)


async def _db_insert_role(role: RoleEntity) -> None:
    try:
        from db.models import RoleRecord
        from db.session import async_session_factory
    except Exception:  # noqa: BLE001
        return
    try:
        async with async_session_factory()() as session:
            session.add(
                RoleRecord(
                    id=role.id,
                    tenant_id=role.tenant_id,
                    name=role.name,
                    permissions=list(role.permissions),
                    description="enterprise_loop fixture role",
                    is_system=False,
                    created_at=_now(),
                ),
            )
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("enterprise_loop role DB persist skipped: %s", exc)


async def _db_insert_user(user: UserEntity) -> None:
    try:
        from db.models import UserRecord
        from db.session import async_session_factory
    except Exception:  # noqa: BLE001
        return
    try:
        async with async_session_factory()() as session:
            session.add(
                UserRecord(
                    id=user.id,
                    tenant_id=user.tenant_id,
                    role_id=None,
                    email=user.email,
                    name=user.name,
                    hashed_password="",  # non-login loop fixture
                    is_active=True,
                    is_verified=False,
                    created_at=_now(),
                    updated_at=_now(),
                ),
            )
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("enterprise_loop user DB persist skipped: %s", exc)


async def _db_rollback(
    tenant_id: str | None,
    user_ids: list[str],
    role_ids: list[str],
) -> None:
    try:
        from sqlalchemy import update

        from db.models import RoleRecord, TenantRecord, UserRecord
        from db.session import async_session_factory
    except Exception:  # noqa: BLE001
        return
    try:
        async with async_session_factory()() as session:
            now = _now()
            if user_ids:
                await session.execute(
                    update(UserRecord)
                    .where(UserRecord.id.in_(user_ids))
                    .values(deleted_at=now),
                )
            if tenant_id is not None:
                await session.execute(
                    update(TenantRecord)
                    .where(TenantRecord.id == tenant_id)
                    .values(deleted_at=now, status="suspended"),
                )
            # RoleRecord has no soft-delete column; hard-delete the fixtures.
            for rid in role_ids:
                role = await session.get(RoleRecord, rid)
                if role is not None:
                    await session.delete(role)
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("enterprise_loop rollback DB step skipped: %s", exc)


async def persist_audit(tenant_id: str, event: AuditEvent) -> None:
    """Best-effort durable copy of an audit event (PDPL Article 18 trail)."""
    try:
        from db.models import AuditLogRecord
        from db.session import async_session_factory
    except Exception:  # noqa: BLE001
        return
    try:
        async with async_session_factory()() as session:
            session.add(
                AuditLogRecord(
                    id=event.event_id,
                    tenant_id=tenant_id or "unknown",
                    user_id=None,
                    action=event.decision,
                    entity_type="enterprise_loop",
                    entity_id=event.output_id or event.source,
                    diff={
                        "actor": event.actor,
                        "source": event.source,
                        "policy_checked": event.policy_checked,
                        "matched_rule": event.matched_rule,
                        "approval_status": event.approval_status,
                    },
                    status="ok",
                    created_at=_now(),
                ),
            )
            await session.commit()
    except Exception as exc:  # noqa: BLE001
        log.warning("enterprise_loop audit DB persist skipped: %s", exc)


__all__ = [
    "RoleEntity",
    "TenantEntity",
    "UserEntity",
    "create_role",
    "create_tenant",
    "create_user",
    "persist_audit",
    "reset_stores_for_tests",
    "rollback_run",
]
