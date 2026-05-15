"""
Role-Based Access Control (RBAC) definitions.
تعريفات التحكم في الوصول القائم على الأدوار.

Roles (in ascending privilege order):
  viewer         — read-only access to own tenant data
  sales_rep      — read/write leads and deals
  sales_manager  — manages reps + full CRM access
  tenant_admin   — full tenant management
  super_admin    — system-wide (cross-tenant) admin (system_role flag)
"""

from __future__ import annotations

from enum import StrEnum


class Role(StrEnum):
    """Tenant-scoped roles stored in RoleRecord.name."""

    VIEWER = "viewer"
    SALES_REP = "sales_rep"
    SALES_MANAGER = "sales_manager"
    TENANT_ADMIN = "tenant_admin"


class SystemRole(StrEnum):
    """System-level roles stored in UserRecord.system_role."""

    SUPER_ADMIN = "super_admin"


# Role hierarchy — higher index = more privilege
_ROLE_ORDER = [
    Role.VIEWER,
    Role.SALES_REP,
    Role.SALES_MANAGER,
    Role.TENANT_ADMIN,
]

# Permission sets per role (use glob-style wildcards internally)
ROLE_PERMISSIONS: dict[str, set[str]] = {
    Role.VIEWER: {
        "leads:read",
        "deals:read",
        "reports:read",
        "profile:read",
        "profile:write",
    },
    Role.SALES_REP: {
        "leads:read",
        "leads:write",
        "leads:create",
        "deals:read",
        "deals:write",
        "deals:create",
        "agents:run",
        "profile:read",
        "profile:write",
    },
    Role.SALES_MANAGER: {
        "leads:*",
        "deals:*",
        "users:read",
        "agents:*",
        "reports:read",
        "reports:export",
        "profile:read",
        "profile:write",
    },
    Role.TENANT_ADMIN: {
        "tenant:read",
        "tenant:write",
        "users:*",
        "roles:*",
        "leads:*",
        "deals:*",
        "agents:*",
        "reports:*",
        "settings:*",
        "profile:read",
        "profile:write",
        "invites:*",
    },
    SystemRole.SUPER_ADMIN: {"*"},  # all permissions
}


def _role_has_permission(role_perms: set[str], permission: str) -> bool:
    """Check if permission is granted by a set of permission strings.
    Supports `*` wildcard at end: 'leads:*' grants 'leads:read', 'leads:write', etc.
    """
    if "*" in role_perms:
        return True
    if permission in role_perms:
        return True
    # Check namespace wildcards  e.g. "leads:*" matches "leads:read"
    ns = permission.rsplit(":", 1)[0] if ":" in permission else ""
    return f"{ns}:*" in role_perms


def has_permission(role_name: str | None, permission: str) -> bool:
    """Return True if the given role grants the requested permission."""
    if not role_name:
        return False
    perms = ROLE_PERMISSIONS.get(role_name, set())
    return _role_has_permission(perms, permission)


def is_at_least(role_name: str | None, minimum: Role) -> bool:
    """Check if role_name has privilege >= minimum in the role hierarchy."""
    if not role_name:
        return False
    try:
        role = Role(role_name)
    except ValueError:
        return False
    return _ROLE_ORDER.index(role) >= _ROLE_ORDER.index(minimum)


# System role guard
def is_super_admin(system_role: str | None) -> bool:
    return system_role == SystemRole.SUPER_ADMIN


# Default system roles bootstrapped for every new tenant
DEFAULT_TENANT_ROLES: list[dict] = [
    {
        "name": Role.VIEWER,
        "description": "Read-only access",
        "permissions": sorted(ROLE_PERMISSIONS[Role.VIEWER]),
        "is_system": True,
    },
    {
        "name": Role.SALES_REP,
        "description": "Manages leads and deals",
        "permissions": sorted(ROLE_PERMISSIONS[Role.SALES_REP]),
        "is_system": True,
    },
    {
        "name": Role.SALES_MANAGER,
        "description": "Sales team manager",
        "permissions": sorted(ROLE_PERMISSIONS[Role.SALES_MANAGER]),
        "is_system": True,
    },
    {
        "name": Role.TENANT_ADMIN,
        "description": "Full tenant administrator",
        "permissions": sorted(ROLE_PERMISSIONS[Role.TENANT_ADMIN]),
        "is_system": True,
    },
]
