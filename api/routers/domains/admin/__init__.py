"""
Admin domain — health, config, founder ops, executive reporting, roles.
مجال الإدارة — الصحة، التهيئة، عمليات المؤسس، التقارير التنفيذية، الأدوار.
"""

from __future__ import annotations

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


# The legacy revenue-machine module still contains an exploratory auto-send
# branch. The production application registers it only through this domain, so
# bind the current product doctrine before exposing the router. This preserves
# draft generation while making the env flag incapable of granting send power.
drafts._auto_send_low_risk_enabled = _retired_auto_send_gate
drafts.gmail_send_email = _blocked_auto_send_adapter

_LEGACY_FINANCE_PRICE_AUTHORITY_PATHS = {
    "/api/v1/finance/pricing",
    "/api/v1/finance/pricing/{tier_id}",
    "/api/v1/finance/invoice/draft",
}

# Finance OS remains the economic-truth/readiness surface, but the launch motion
# is quote-only after qualified discovery. Retire its old tier catalogue and
# tier-based invoice DTO endpoints from HTTP registration while retaining
# /api/v1/finance/status. This prevents a second pricing/invoice authority from
# competing with the canonical customer-specific quote path.
finance_os.router.routes[:] = [
    route
    for route in finance_os.router.routes
    if getattr(route, "path", None) not in _LEGACY_FINANCE_PRICE_AUTHORITY_PATHS
]

_LEGACY_COMMAND_CENTER_AUTHORITY_PATHS = {
    "/api/v1/command-center/agents",
    "/api/v1/command-center/agents/{agent_id}",
    "/api/v1/command-center/leaks",
    "/api/v1/command-center/proof-pack",
}

# The historical command-center module exposes an 11-agent catalogue plus
# economic/proof generators with fixed default values. That conflicts with the
# five canonical company agents and evidence-bound economic truth. Preserve the
# remaining signal/benchmark/playbook utilities, but do not mount these four
# authority-bearing compatibility routes until they are explicitly reconciled.
command_center.router.routes[:] = [
    route
    for route in command_center.router.routes
    if getattr(route, "path", None) not in _LEGACY_COMMAND_CENTER_AUTHORITY_PATHS
]


_ROUTERS = [
    health.router,
    admin.router,
    public.router,
    sectors.router,
    data.router,
    business.router,
    finance_os.router,
    founder.router,
    founder_command_summary_router.router,
    founder_beast_command_center.router,
    role_command.router,
    role_command_os.router,
    executive_reporting.router,
    executive_os.router,
    executive_command_center_router.router,
    approval_center.router,
    command_center.router,
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
