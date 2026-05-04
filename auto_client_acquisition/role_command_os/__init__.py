"""Role Command OS v5 — 7 role-specific briefs over the existing data.

Composes ``daily_growth_loop`` + ``service_activation_matrix`` +
``partner_distribution_radar`` + ``geo_aio_radar`` into a brief
tuned for each operating role:

  CEO · Sales Manager · Growth Manager · Partnership Manager
  · Customer Success · Finance · Compliance

Each brief is bilingual (Arabic primary, English secondary) and
returns: top 3 decisions, risks, approvals needed, evidence,
next action, blocked actions. No LLM call — pure composition over
existing measurements.
"""
from auto_client_acquisition.role_command_os.role_briefs import (
    RoleName,
    build_role_brief,
    list_roles,
)
from auto_client_acquisition.role_command_os.schemas import (
    RoleBrief,
    RoleDecision,
)

__all__ = [
    "RoleName",
    "RoleBrief",
    "RoleDecision",
    "build_role_brief",
    "list_roles",
]
