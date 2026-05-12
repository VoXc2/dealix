"""
Authorization adapter — wraps Cerbos when configured, falls back to the
existing static RBAC otherwise.

Public surface:
    await allowed(action, principal, resource) -> bool

Why a thin wrapper: policies live in cerbos/policies/*.yaml so review +
versioning happens there. Code calls `allowed(...)`; switching from
static RBAC to Cerbos is a config flip, not a refactor.

Behaviour without CERBOS_PDP_URL:
    Fall through to api.security.rbac role-set evaluation. The contract
    is the same: `bool`. This keeps the existing test surface green.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx

from core.logging import get_logger

log = get_logger(__name__)


@dataclass
class Principal:
    id: str
    roles: list[str]
    attr: dict[str, Any]


@dataclass
class Resource:
    kind: str
    id: str
    attr: dict[str, Any]


def _cerbos_url() -> str:
    return os.getenv("CERBOS_PDP_URL", "").strip()


async def allowed(action: str, principal: Principal, resource: Resource) -> bool:
    """Return True if `principal` may perform `action` on `resource`."""
    url = _cerbos_url()
    if url:
        try:
            return await _ask_cerbos(url, action, principal, resource)
        except Exception:
            log.exception(
                "cerbos_unreachable_falling_back_to_rbac",
                principal_id=principal.id,
                action=action,
                resource_kind=resource.kind,
            )
            # Deliberately fall through to static RBAC rather than denying
            # outright. In production you may want this to be `return False`
            # (fail-closed). Configure via env.
            if os.getenv("CERBOS_FAIL_CLOSED", "").strip().lower() in {"1", "true"}:
                return False
    return _static_rbac(action, principal, resource)


async def _ask_cerbos(
    url: str, action: str, principal: Principal, resource: Resource
) -> bool:
    payload = {
        "requestId": "dealix",
        "actions": [action],
        "principal": {
            "id": principal.id,
            "roles": principal.roles,
            "attr": principal.attr,
        },
        "resource": {
            "kind": resource.kind,
            "id": resource.id,
            "attr": resource.attr,
        },
    }
    async with httpx.AsyncClient(timeout=2.5) as c:
        r = await c.post(f"{url.rstrip('/')}/api/check/resources", json=payload)
        r.raise_for_status()
        data = r.json()
    # Cerbos returns one decision per (resource, action).
    for res in data.get("results", []):
        actions = res.get("actions", {})
        if actions.get(action) == "EFFECT_ALLOW":
            return True
    return False


def _static_rbac(action: str, principal: Principal, resource: Resource) -> bool:
    """Mirror of cerbos/policies/dealix_resources.yaml when the PDP is absent."""
    if resource.attr.get("tenant_id") != principal.attr.get("tenant_id"):
        return False
    roles = set(principal.roles)
    rk = resource.kind
    if rk == "lead":
        if action in {"read", "list"}:
            return bool(roles & {"owner", "admin", "sales_rep", "viewer"})
        if action in {"create", "update"}:
            return bool(roles & {"owner", "admin", "sales_rep"})
        if action == "delete":
            return bool(roles & {"owner", "admin"})
    if rk == "deal":
        if action in {"read", "list"}:
            return bool(roles & {"owner", "admin", "sales_rep", "viewer"})
        if action in {"create", "update"}:
            return bool(roles & {"owner", "admin", "sales_rep"})
        if action in {"delete", "approve_discount"}:
            return bool(roles & {"owner", "admin"})
    if rk == "tenant_settings":
        if action == "read":
            return bool(roles & {"owner", "admin", "sales_rep", "viewer"})
        if action in {"update", "manage_billing", "invite_user", "revoke_user"}:
            return bool(roles & {"owner", "admin"})
    if rk == "audit_log":
        if action == "read":
            return bool(roles & {"owner", "admin", "auditor"})
        if action == "export":
            return bool(roles & {"owner", "admin"})
    if rk == "agent_run":
        if action == "queue":
            return bool(roles & {"owner", "admin", "sales_rep", "agent_operator"})
        if action in {"execute", "approve"}:
            return bool(roles & {"owner", "admin", "agent_operator"})
    return False
