"""Founder v10 — composes all v6/v7/v10 layers into the daily brief.

Pure local composition. No LLM, no external HTTP, no PII, no live
action. Each compose-helper is wrapped defensively so the brief never
crashes a layer mid-deploy.
"""
from auto_client_acquisition.founder_v10.blockers import find_blockers
from auto_client_acquisition.founder_v10.cache import (
    cached_dashboard_payload,
    reset_cache,
)
from auto_client_acquisition.founder_v10.cost_summary import summarize_cost
from auto_client_acquisition.founder_v10.daily_brief import build_daily_brief
from auto_client_acquisition.founder_v10.dashboard_builder import (
    build_dashboard_payload,
)
from auto_client_acquisition.founder_v10.evidence_summary import summarize_evidence
from auto_client_acquisition.founder_v10.next_actions import compute_next_action
from auto_client_acquisition.founder_v10.schemas import (
    Blocker,
    DailyBrief,
    RiskEntry,
)

__all__ = [
    "Blocker",
    "DailyBrief",
    "RiskEntry",
    "build_daily_brief",
    "build_dashboard_payload",
    "cached_dashboard_payload",
    "compute_next_action",
    "find_blockers",
    "reset_cache",
    "summarize_cost",
    "summarize_evidence",
]
