"""
Admin domain — health, config, founder ops, executive reporting, roles.
مجال الإدارة — الصحة، التهيئة، عمليات المؤسس، التقارير التنفيذية، الأدوار.
"""

from __future__ import annotations

from fastapi import APIRouter

from api.routers import (
    admin,
    approval_center,
    business,
    capital_assets,
    command_center,
    data,
    dealix_promise,
    designops,
    diagnostic,
    diagnostic_workflow,
    doctrine,
    drafts,
    ecosystem,
    executive_command_center as executive_command_center_router,
    executive_os,
    executive_reporting,
    finance_os,
    founder,
    founder_beast_command_center,
    founder_command_summary as founder_command_summary_router,
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
    trust_status,
)

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
    # Wave 20 — public verification spine (no auth, public read-only).
    dealix_promise.router,
    doctrine.router,
    capital_assets.router,
    # Wave 21 — public trust surface.
    trust_status.router,
]


def get_routers() -> list[APIRouter]:
    """Return all admin-domain routers."""
    return _ROUTERS
