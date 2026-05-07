"""Executive Pack v2 — per-customer composer.

Wraps existing executive_reporting + role_command_os with the
4 missing sections (lead_kpis, support_sla_breaches, blockers,
next_3_actions) + market_context.

Per Article 11: extends in-place wrapping, no rebuild of existing
weekly_report_builder etc.
"""
from auto_client_acquisition.executive_pack_v2.composer import (
    build_daily_pack,
    build_weekly_pack,
)

__all__ = ["build_daily_pack", "build_weekly_pack"]
