"""
Orchestrator Policies — autonomy modes, approval gates, budget limits.

Every customer chooses their autonomy mode. The orchestrator consults the
policy on every action: should I run? do I need human approval? am I
within budget?
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from auto_client_acquisition.orchestrator.operating_company_contract import (
    DEFAULT_OPERATING_COMPANY_CONTRACT,
)


# ── Autonomy modes — the safety slider ────────────────────────────
class AutonomyMode:
    """Five named autonomy modes, ordered by independence."""

    MANUAL = "manual"                 # Dealix only suggests; user does everything
    SUGGEST = "suggest_only"          # Dealix shows what it would do; user actions
    DRAFT_APPROVE = "draft_and_approve"  # Dealix drafts; user approves before send
    SAFE_AUTOPILOT = "safe_autopilot"  # Dealix sends within rails; high-risk needs approval
    FULL_AUTOPILOT = "full_autopilot"  # Dealix runs end-to-end; user reviews logs


ALL_MODES: tuple[str, ...] = (
    AutonomyMode.MANUAL,
    AutonomyMode.SUGGEST,
    AutonomyMode.DRAFT_APPROVE,
    AutonomyMode.SAFE_AUTOPILOT,
    AutonomyMode.FULL_AUTOPILOT,
)


# ── Budget limits — protect against runaway spend ─────────────────
@dataclass
class BudgetLimit:
    """Per-day caps. Once hit, agents stop until next reset."""

    max_messages_per_day: int = 200
    max_llm_tokens_per_day: int = 200_000
    max_external_api_calls_per_day: int = 1_000
    max_cost_sar_per_day: float = 100.0


# ── Policy — what each mode allows ────────────────────────────────
@dataclass
class Policy:
    """Consolidated policy for one customer."""

    customer_id: str
    autonomy_mode: str = AutonomyMode.DRAFT_APPROVE
    budget: BudgetLimit = field(default_factory=BudgetLimit)
    require_human_for_first_send: bool = True
    require_human_for_high_value_deals_above_sar: float = 100_000
    require_human_for_legal_topics: bool = True
    blocked_sectors: tuple[str, ...] = ()
    blocked_keywords: tuple[str, ...] = ()  # any draft containing these → human review
    max_consecutive_followups: int = 3
    quiet_hours_riyadh: tuple[int, int] = (21, 8)  # 9pm - 8am no messaging
    blocked_dates: tuple[str, ...] = ()  # ISO dates: religious holidays, etc.


def default_policy(customer_id: str) -> Policy:
    return Policy(customer_id=customer_id)


# ── Action types the orchestrator can request ────────────────────
ACTION_TYPES: tuple[str, ...] = (
    "discover_leads",
    "enrich_lead",
    "draft_message",
    "send_message",
    "send_scope",
    "send_invoice",
    "start_delivery",
    "final_diagnostic",
    "publish_case_study",
    "security_claim",
    "agent_tool_action",
    "classify_reply",
    "book_meeting",
    "generate_proposal",
    "score_deal",
    "compute_health",
    "generate_qbr",
    "publish_pulse",
)


def _approval_action_id(action_type: str, risks: dict[str, Any]) -> str | None:
    if action_type == "send_scope":
        return "send_scope"
    if action_type == "send_invoice":
        return "send_invoice"
    if action_type == "start_delivery":
        return "start_delivery"
    if action_type == "final_diagnostic":
        return "final_diagnostic"
    if action_type == "publish_case_study":
        return "publish_case_study"
    if action_type == "security_claim":
        return "security_claim"
    if action_type == "agent_tool_action":
        return "agent_tool_action"
    if action_type == "send_message":
        if risks.get("is_first_send_to_account"):
            return "send_first_outreach"
        if risks.get("send_sample_proof_pack"):
            return "send_sample_proof_pack"
        if risks.get("reply_received"):
            return "send_followup_after_reply"
    return None


# ── Decision: requires_approval? ──────────────────────────────────
def requires_approval(
    *,
    action_type: str,
    policy: Policy,
    risk_factors: dict[str, Any] | None = None,
) -> tuple[bool, str | None]:
    """
    Decide whether an action needs human approval before execution.

    Returns (needs_approval, reason). reason is the human-readable rationale.
    """
    risks = risk_factors or {}

    # Mode-based blanket rules
    if policy.autonomy_mode in (AutonomyMode.MANUAL, AutonomyMode.SUGGEST):
        return True, f"autonomy_mode={policy.autonomy_mode}"
    if policy.autonomy_mode == AutonomyMode.DRAFT_APPROVE and action_type in (
        "send_message",
        "book_meeting",
        "generate_proposal",
        "send_scope",
        "send_invoice",
        "final_diagnostic",
        "security_claim",
        "publish_case_study",
    ):
        return True, "mode=draft_and_approve_requires_human_for_outbound"

    # Operating-company matrix gates (applies even in autopilot).
    action_id = _approval_action_id(action_type=action_type, risks=risks)
    if action_id:
        needs_matrix_approval, matrix_reason = (
            DEFAULT_OPERATING_COMPANY_CONTRACT.requires_approval_for_action(
                action_id=action_id,
                context={
                    "payment_proof": risks.get("payment_proof"),
                    "risk_level": risks.get("risk_level"),
                    "auto_followup_allowed": risks.get("auto_followup_allowed"),
                },
            )
        )
        if needs_matrix_approval:
            return True, f"operating_contract:{matrix_reason}"

    # Risk-based escalation (applies even in autopilot)
    if action_type == "send_message":
        if policy.require_human_for_first_send and risks.get("is_first_send_to_account"):
            return True, "first_send_to_account"
        deal_value = float(risks.get("deal_value_sar", 0))
        if deal_value >= policy.require_human_for_high_value_deals_above_sar:
            return True, f"high_value_deal_sar={deal_value:.0f}"
        if risks.get("contains_legal_topic") and policy.require_human_for_legal_topics:
            return True, "contains_legal_topic"
        sector = risks.get("sector")
        if sector in policy.blocked_sectors:
            return True, f"blocked_sector={sector}"
        for kw in policy.blocked_keywords:
            if kw in str(risks.get("draft_text", "")):
                return True, f"blocked_keyword={kw}"
        if risks.get("consecutive_followup_index", 0) >= policy.max_consecutive_followups:
            return True, "max_consecutive_followups_reached"

    return False, None


def is_in_quiet_hours(*, hour_riyadh: int, policy: Policy) -> bool:
    """Whether the current Riyadh hour is within the quiet window."""
    start, end = policy.quiet_hours_riyadh
    if start < end:
        return start <= hour_riyadh < end
    # Wraps midnight
    return hour_riyadh >= start or hour_riyadh < end


# ── Budget enforcement ───────────────────────────────────────────
@dataclass
class BudgetUsage:
    messages_today: int = 0
    llm_tokens_today: int = 0
    api_calls_today: int = 0
    cost_sar_today: float = 0.0


def within_budget(*, usage: BudgetUsage, budget: BudgetLimit) -> tuple[bool, str | None]:
    if usage.messages_today >= budget.max_messages_per_day:
        return False, "messages_per_day_reached"
    if usage.llm_tokens_today >= budget.max_llm_tokens_per_day:
        return False, "llm_tokens_per_day_reached"
    if usage.api_calls_today >= budget.max_external_api_calls_per_day:
        return False, "api_calls_per_day_reached"
    if usage.cost_sar_today >= budget.max_cost_sar_per_day:
        return False, "cost_sar_per_day_reached"
    return True, None
