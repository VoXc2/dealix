"""RBAC facade — autonomy ladder, tool boundary, and role definitions.

``AutonomyLevel`` is the 0..4 numeric ladder for agents. ``OWNER_ROLES`` is
the canonical set of human owner roles from the Decision Passport schema.
``RoleRecord`` is the per-tenant RBAC role model.
"""

from __future__ import annotations

from auto_client_acquisition.agent_os.autonomy_levels import AutonomyLevel
from auto_client_acquisition.agent_os.tool_permissions import (
    ALLOWED_TOOLS_MVP,
    FORBIDDEN_TOOLS_MVP,
    tool_allowed_mvp,
)
from db.models import RoleRecord

# Canonical human owner roles (mirrors decision_passport/schema.py Owner literal).
OWNER_ROLES: tuple[str, ...] = ("founder", "csm", "sales_rep", "customer", "system_auto")

__all__ = [
    "ALLOWED_TOOLS_MVP",
    "FORBIDDEN_TOOLS_MVP",
    "OWNER_ROLES",
    "AutonomyLevel",
    "RoleRecord",
    "tool_allowed_mvp",
]
