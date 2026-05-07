"""Executive Command Center — read-model with 15 sections.

Composes data from existing modules + Wave 4 layers (full_ops_radar,
unified_operating_graph, whatsapp_decision_bot) into a single
admin-facing daily/weekly executive view.

100% read-only. Never raises (uses safe_call). Customer-safe labels
in any consumer-facing output.
"""
from auto_client_acquisition.executive_command_center.builder import (
    build_command_center,
    build_daily,
    build_weekly,
)

__all__ = ["build_command_center", "build_daily", "build_weekly"]
