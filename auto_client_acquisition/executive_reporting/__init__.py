"""Executive Reporting v6 — weekly report composer.

Pure read-only composition over existing layers. NEVER calls an LLM,
NEVER opens a network connection, NEVER persists. Output is bilingual
markdown the founder can copy-paste into LinkedIn / Notion / email.

Hard guarantees:
  - no LLM call
  - no external HTTP
  - no marketing claims (forbidden tokens scrubbed before render)
  - no PII (proof events go through ``export_redacted`` first)
"""
from auto_client_acquisition.executive_reporting.decision_summary import (
    decision_summary,
)
from auto_client_acquisition.executive_reporting.next_week_plan import (
    next_week_plan,
)
from auto_client_acquisition.executive_reporting.proof_summary import (
    proof_summary,
)
from auto_client_acquisition.executive_reporting.risk_summary import (
    risk_summary,
)
from auto_client_acquisition.executive_reporting.schemas import WeeklyReport
from auto_client_acquisition.executive_reporting.weekly_report_builder import (
    build_weekly_report,
)

__all__ = [
    "WeeklyReport",
    "build_weekly_report",
    "decision_summary",
    "next_week_plan",
    "proof_summary",
    "risk_summary",
]
