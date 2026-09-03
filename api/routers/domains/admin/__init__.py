"""
Admin domain — health, config, founder ops, executive reporting, roles.
مجال الإدارة — الصحة، التهيئة، عمليات المؤسس، التقارير التنفيذية، الأدوار.
"""

from __future__ import annotations

from copy import copy
from typing import Any

from fastapi import APIRouter

from api.routers import (
    admin,
    approval_center,
    business,
    command_center,
    data,
    designops,
    diagnostic,
    diagnostic_workflow,
    drafts,
    ecosystem,
    executive_os,
    executive_reporting,
    finance_os,
    founder,
    founder_beast_command_center,
    full_ops,
    full_os,
    health,
    personal_operator,
    public,
    role_command,
    role_command_os,
    sectors,
    self_growth,
    self_improvement_os,
)
from api.routers import (
    executive_command_center as executive_command_center_router,
)
from api.routers import (
    founder_command_summary as founder_command_summary_router,
)


def _retired_auto_send_gate(_approval_mode: str) -> bool:
    """Auto-send is retired; external email requires explicit approved execution."""

    return False


async def _blocked_auto_send_adapter(**_kwargs: Any) -> None:
    """Defense in depth if legacy auto-send code is called directly."""

    raise RuntimeError(
        "auto_send_low_risk_retired: use /api/v1/email/send-approved after approval"
    )


def _filtered_router(source: APIRouter, blocked_paths: set[str]) -> APIRouter:
    """Return a launch-safe router view without mutating shared router state."""

    filtered = copy(source)
    filtered.routes = [
        route
        for route in source.routes
        if getattr(route, "path", None) not in blocked_paths
    ]
    return filtered


# The legacy revenue-machine module still contains an exploratory auto-send
# branch. Bind the current product doctrine while preserving draft generation.
drafts._auto_send_low_risk_enabled = _retired_auto_send_gate
drafts.gmail_send_email = _blocked_auto_send_adapter

_LEGACY_FINANCE_PRICE_AUTHORITY_PATHS = {
    "/api/v1/finance/pricing",
    "/api/v1/finance/pricing/{tier_id}",
    "/api/v1/finance/invoice/draft",
}

# Finance OS remains the economic-truth/readiness surface. Use a filtered view
# so /api/v1/finance/status remains available without mutating the source router.
_finance_os_router = _filtered_router(finance_os.router, _LEGACY_FINANCE_PRICE_AUTHORITY_PATHS)

_LEGACY_COMMAND_CENTER_AUTHORITY_PATHS = {
    "/api/v1/command-center/agents",
    "/api/v1/command-center/agents/{agent_id}",
    "/api/v1/command-center/leaks",
    "/api/v1/command-center/proof-pack",
}

# Preserve non-authoritative command-center utilities, but do not mount the
# historical 11-agent/economic/proof authority surfaces at launch.
_command_center_router = _filtered_router(
    command_center.router,
    _LEGACY_COMMAND_CENTER_AUTHORITY_PATHS,
)


_ROUTERS = [
    health.router,
    admin.router,
    public.router,
    sectors.router,
    data.router,
    business.router,
    _finance_os_router,
    founder.router,
    founder_command_summary_router.router,
    founder_beast_command_center.router,
    role_command.router,
    role_command_os.router,
    executive_reporting.router,
    executive_os.router,
    executive_command_center_router.router,
    approval_center.router,
    _command_center_router,
    full_ops.router,
    full_os.router,
    drafts.router,
    personal_operator.router,
    self_growth.router,
    self_improvement_os.router,
    ecosystem.router,
    diagnostic.router,
    diagnostic_workflow.router,
    designops.router,
]


def get_routers() -> list[APIRouter]:
    """Return all admin-domain routers."""
    return _ROUTERS
