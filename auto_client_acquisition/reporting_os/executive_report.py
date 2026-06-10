"""Executive report helpers — facade."""

from __future__ import annotations

from auto_client_acquisition.executive_reporting.schemas import WeeklyReport


def empty_weekly_report() -> WeeklyReport:
    return WeeklyReport(week_label="unscheduled")
