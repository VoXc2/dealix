"""Dealix Agentic Revenue Factory policy engine.

This module codifies the founder-led governance doctrine in deterministic
structures and helpers:

Signal -> Source -> Approval -> Action -> Evidence -> Decision -> Value -> Asset

No autonomous external execution is allowed.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Mapping


class AutomationLevel(StrEnum):
    FULLY_AUTOMATED = "fully_automated"
    AGENT_ASSISTED = "agent_assisted"
    FOUNDER_APPROVAL_REQUIRED = "founder_approval_required"


class ApprovalRiskLevel(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ApprovalType(StrEnum):
    EXTERNAL_MESSAGE = "external_message"
    INVOICE_SEND = "invoice_send"
    SCOPE_SEND = "scope_send"
    DIAGNOSTIC_FINAL = "diagnostic_final"
    CASE_STUDY = "case_study"
    SECURITY_CLAIM = "security_claim"
    AGENT_TOOL_ACTION = "agent_tool_action"
    REFUND_OR_DISCOUNT = "refund_or_discount"
    PARTNER_TERMS = "partner_terms"


GOVERNED_CHAIN: tuple[str, ...] = (
    "signal",
    "source",
    "approval",
    "action",
    "evidence",
    "decision",
    "value",
    "asset",
)


FULLY_AUTOMATED_ACTIONS: frozenset[str] = frozenset(
    {
        "lead_capture",
        "crm_creation",
        "lead_scoring",
        "tagging",
        "enrichment_draft",
        "meeting_brief_draft",
        "follow_up_reminder",
        "scope_draft",
        "invoice_draft",
        "proof_pack_skeleton",
        "delivery_checklist",
        "weekly_report",
        "evidence_logging",
    }
)


AGENT_ASSISTED_ACTIONS: frozenset[str] = frozenset(
    {
        "best_icp",
        "best_message",
        "best_sales_angle",
        "best_price",
        "best_next_action",
        "best_upsell",
        "best_partner",
        "best_objection_response",
    }
)


FOUNDER_APPROVAL_ACTIONS: frozenset[str] = frozenset(
    {
        "first_external_send",
        "invoice_send",
        "scope_send",
        "diagnostic_finalization",
        "case_study_publish",
        "security_claim_publish",
        "client_impacting_action",
        "money_impacting_action",
        "reputation_impacting_action",
        "autonomous_external_action",
    }
)


EXTERNAL_ACTION_KEYWORDS: tuple[str, ...] = (
    "send",
    "publish",
    "message",
    "email",
    "linkedin",
    "whatsapp",
    "invoice",
)


APPROVAL_RISK_BY_TYPE: dict[ApprovalType, ApprovalRiskLevel] = {
    ApprovalType.EXTERNAL_MESSAGE: ApprovalRiskLevel.MEDIUM,
    ApprovalType.INVOICE_SEND: ApprovalRiskLevel.HIGH,
    ApprovalType.SCOPE_SEND: ApprovalRiskLevel.HIGH,
    ApprovalType.DIAGNOSTIC_FINAL: ApprovalRiskLevel.HIGH,
    ApprovalType.CASE_STUDY: ApprovalRiskLevel.HIGH,
    ApprovalType.SECURITY_CLAIM: ApprovalRiskLevel.CRITICAL,
    ApprovalType.AGENT_TOOL_ACTION: ApprovalRiskLevel.CRITICAL,
    ApprovalType.REFUND_OR_DISCOUNT: ApprovalRiskLevel.HIGH,
    ApprovalType.PARTNER_TERMS: ApprovalRiskLevel.HIGH,
}


EVENT_AGENT_ROUTING: dict[str, tuple[str, ...]] = {
    "new_lead": ("LeadCaptureAgent",),
    "high_score": ("ICPScoringAgent", "MeetingBriefAgent"),
    "reply_received": ("OutreachPersonalizationAgent",),
    "meeting_booked": ("MeetingBriefAgent",),
    "meeting_done": ("SalesCallCoachAgent", "ScopeBuilderAgent"),
    "invoice_paid": ("DeliveryDiagnosticAgent",),
    "proof_pack_sent": ("UpsellAgent", "ContentEngineAgent"),
    "public_action_requested": ("GovernanceRiskAgent",),
    "partner_signal": ("PartnerAgent",),
}


@dataclass(frozen=True, slots=True)
class AgentContract:
    name: str
    mission: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    allowed_actions: tuple[str, ...]
    forbidden_actions: tuple[str, ...]
    approval_required_for: tuple[str, ...]
    evidence_required: tuple[str, ...]
    quality_checks: tuple[str, ...]


DEFAULT_AGENT_CONTRACTS: tuple[AgentContract, ...] = (
    AgentContract(
        name="MarketIntelligenceAgent",
        mission="Collect market signals and propose high-fit accounts daily.",
        inputs=("market_signals", "crm_notes", "founder_posts", "partner_lists"),
        outputs=("target_accounts", "buying_signals", "angle_recommendations"),
        allowed_actions=("classify", "score", "draft", "recommend"),
        forbidden_actions=("external_send", "cold_whatsapp", "scraping", "claim_without_source"),
        approval_required_for=(),
        evidence_required=("signal", "source"),
        quality_checks=("consent_respected", "no_sensitive_personal_data"),
    ),
    AgentContract(
        name="ICPScoringAgent",
        mission="Score and stage leads based on governed ICP rules.",
        inputs=("lead_profile", "company_profile", "source"),
        outputs=("score", "stage", "reason", "risk_flags"),
        allowed_actions=("score", "classify", "recommend"),
        forbidden_actions=("external_send",),
        approval_required_for=(),
        evidence_required=("source",),
        quality_checks=("no_budget_inference_without_input",),
    ),
    AgentContract(
        name="PositioningAgent",
        mission="Generate positioning angle by sector, pain, and trust constraints.",
        inputs=("industry", "role", "pain", "budget", "crm_status"),
        outputs=("message_angle", "pain_hypothesis", "recommended_offer"),
        allowed_actions=("recommend", "draft"),
        forbidden_actions=("publish_claim", "external_send"),
        approval_required_for=("external_send",),
        evidence_required=("source",),
        quality_checks=("no_overclaim",),
    ),
    AgentContract(
        name="ContentEngineAgent",
        mission="Convert objections and proof learnings into content drafts.",
        inputs=("objections", "proof_insights", "meeting_notes"),
        outputs=("linkedin_draft", "email_snippet", "video_script"),
        allowed_actions=("draft", "summarize", "recommend"),
        forbidden_actions=("publish_content", "external_send"),
        approval_required_for=("publish_content", "external_send"),
        evidence_required=("evidence", "source"),
        quality_checks=("no_client_data_without_approval",),
    ),
    AgentContract(
        name="OutreachPersonalizationAgent",
        mission="Create personalized outreach drafts with proof-led angles.",
        inputs=("target_account", "buyer_role", "buying_signal", "angle"),
        outputs=("linkedin_dm_draft", "email_draft", "followup_draft"),
        allowed_actions=("generate_draft", "classify", "recommend"),
        forbidden_actions=("external_send", "autonomous_outbound"),
        approval_required_for=("external_send",),
        evidence_required=("signal", "source"),
        quality_checks=("no_cheap_labor_positioning", "no_overclaim"),
    ),
    AgentContract(
        name="LeadCaptureAgent",
        mission="Convert inbound interactions into structured CRM records.",
        inputs=("form_submission", "reply", "manual_entry", "partner_intro"),
        outputs=("contact_record", "company_record", "next_action", "evidence_event"),
        allowed_actions=("create_internal_record", "score", "stage", "notify"),
        forbidden_actions=("external_send",),
        approval_required_for=(),
        evidence_required=("signal", "source", "evidence"),
        quality_checks=("dedupe_check", "source_tag_required"),
    ),
    AgentContract(
        name="MeetingBriefAgent",
        mission="Generate pre-call briefing and recommended discovery path.",
        inputs=("lead_profile", "account_context", "pipeline_stage"),
        outputs=("brief", "questions", "objection_map", "demo_path"),
        allowed_actions=("draft", "summarize", "recommend"),
        forbidden_actions=("diagnostic_finalization", "external_send"),
        approval_required_for=(),
        evidence_required=("source",),
        quality_checks=("include_risk_score",),
    ),
    AgentContract(
        name="SalesCallCoachAgent",
        mission="Turn call outcomes into governed next decisions.",
        inputs=("meeting_notes", "call_checklist"),
        outputs=("outcome_classification", "next_action", "evidence_event"),
        allowed_actions=("classify", "recommend", "log"),
        forbidden_actions=(
            "mark_l5_without_used_in_meeting",
            "mark_revenue_without_payment",
            "external_send",
        ),
        approval_required_for=(),
        evidence_required=("meeting_done", "source"),
        quality_checks=("lifecycle_gate_compliance",),
    ),
    AgentContract(
        name="ScopeBuilderAgent",
        mission="Generate diagnostic scope and invoice recommendation drafts.",
        inputs=("approved_meeting_notes", "offer_tier", "timeline", "price"),
        outputs=("scope_draft", "deliverables", "invoice_recommendation"),
        allowed_actions=("generate_draft", "request_missing_info", "update_internal_status"),
        forbidden_actions=("scope_send", "invoice_send", "security_claim_publish", "external_send"),
        approval_required_for=("scope_send", "invoice_send", "external_send"),
        evidence_required=("meeting_done", "scope_requested", "source"),
        quality_checks=("exclusions_included", "price_within_approved_range"),
    ),
    AgentContract(
        name="BillingAgent",
        mission="Prepare invoice lifecycle states from approved scope only.",
        inputs=("scope_approved", "pricing_tier", "payment_terms"),
        outputs=("invoice_draft", "payment_followup_plan", "billing_events"),
        allowed_actions=("generate_draft", "schedule_reminder", "log"),
        forbidden_actions=("invoice_send", "revenue_recognition_without_payment", "external_send"),
        approval_required_for=("invoice_send", "external_send"),
        evidence_required=("scope_approved", "source"),
        quality_checks=("no_delivery_before_payment",),
    ),
    AgentContract(
        name="DeliveryDiagnosticAgent",
        mission="Produce governed diagnostic findings from approved inputs.",
        inputs=("onboarding_form", "crm_export", "workflow_docs", "call_notes"),
        outputs=("workflow_map", "risk_register", "top_decisions"),
        allowed_actions=("analyze", "summarize", "recommend", "log"),
        forbidden_actions=("claim_without_source", "invent_missing_data", "external_send"),
        approval_required_for=("diagnostic_finalization",),
        evidence_required=("source", "evidence"),
        quality_checks=("estimates_marked", "missing_data_explicit"),
    ),
    AgentContract(
        name="ProofPackAgent",
        mission="Generate client-ready proof packs with evidence confidence.",
        inputs=("diagnostic_findings", "evidence_events"),
        outputs=("proof_pack_draft", "learning_note", "upsell_recommendation"),
        allowed_actions=("generate_draft", "summarize", "recommend"),
        forbidden_actions=("publish_case_study_without_approval", "external_send"),
        approval_required_for=("proof_pack_send", "case_study_publish"),
        evidence_required=("source", "evidence", "decision", "value"),
        quality_checks=("finding_has_source", "confidence_attached"),
    ),
    AgentContract(
        name="UpsellAgent",
        mission="Recommend next commercial offer based on diagnostic evidence.",
        inputs=("proof_pack", "workflow_maturity", "budget_signal"),
        outputs=("recommended_offer", "reason", "next_action"),
        allowed_actions=("recommend", "classify", "draft"),
        forbidden_actions=("external_send",),
        approval_required_for=("external_send",),
        evidence_required=("proof_pack_sent", "source"),
        quality_checks=("offer_selection_matches_rules",),
    ),
    AgentContract(
        name="PartnerAgent",
        mission="Build referral channel with founder-approved partner motions.",
        inputs=("partner_candidates", "fit_signals", "sector_focus"),
        outputs=("partner_list", "pitch_draft", "followup_draft"),
        allowed_actions=("score", "classify", "generate_draft"),
        forbidden_actions=("partner_terms_sign", "external_send"),
        approval_required_for=("partner_terms_sign", "external_send"),
        evidence_required=("source",),
        quality_checks=("no_unverified_referral_claims",),
    ),
    AgentContract(
        name="GovernanceRiskAgent",
        mission="Enforce risk gates and block unsupported high-risk actions.",
        inputs=("proposed_action", "draft", "required_evidence", "approval_status"),
        outputs=("risk_classification", "block_or_pass", "required_followups"),
        allowed_actions=("classify", "block", "escalate", "log"),
        forbidden_actions=("execute_external_action", "external_send"),
        approval_required_for=(),
        evidence_required=("approval", "source"),
        quality_checks=("no_unsupported_claims", "no_action_without_approval"),
    ),
)


def _normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def classify_automation_level(action_name: str) -> AutomationLevel:
    action = _normalize(action_name)
    if action in FULLY_AUTOMATED_ACTIONS:
        return AutomationLevel.FULLY_AUTOMATED
    if action in AGENT_ASSISTED_ACTIONS:
        return AutomationLevel.AGENT_ASSISTED
    if action in FOUNDER_APPROVAL_ACTIONS:
        return AutomationLevel.FOUNDER_APPROVAL_REQUIRED
    if any(token in action for token in EXTERNAL_ACTION_KEYWORDS):
        return AutomationLevel.FOUNDER_APPROVAL_REQUIRED
    return AutomationLevel.AGENT_ASSISTED


def founder_approval_required(
    action_name: str,
    *,
    first_external_send: bool = False,
    impacts_money: bool = False,
    impacts_client: bool = False,
    impacts_reputation: bool = False,
) -> bool:
    if first_external_send or impacts_money or impacts_client or impacts_reputation:
        return True
    return classify_automation_level(action_name) == AutomationLevel.FOUNDER_APPROVAL_REQUIRED


def approval_risk_for_type(approval_type: ApprovalType | str) -> ApprovalRiskLevel:
    try:
        key = ApprovalType(_normalize(str(approval_type)))
    except ValueError:
        return ApprovalRiskLevel.CRITICAL
    return APPROVAL_RISK_BY_TYPE.get(key, ApprovalRiskLevel.CRITICAL)


def validate_governed_event_chain(event: Mapping[str, Any]) -> tuple[bool, tuple[str, ...]]:
    """Validate a single event against the governing chain contract."""

    violations: list[str] = []

    for key in GOVERNED_CHAIN:
        value = event.get(key)
        if value in (None, "", [], {}):
            violations.append(f"missing_{key}")

    action = str(event.get("action", "")).lower()
    approval = str(event.get("approval", "")).lower()
    if any(token in action for token in EXTERNAL_ACTION_KEYWORDS):
        if approval in ("", "none", "not_required", "false"):
            violations.append("external_action_without_approval")

    value = event.get("value")
    evidence = event.get("evidence")
    if value not in (None, "", [], {}) and evidence in (None, "", [], {}):
        violations.append("value_without_evidence")

    return (len(violations) == 0, tuple(violations))


def route_event_to_agents(event_type: str) -> tuple[str, ...]:
    return EVENT_AGENT_ROUTING.get(_normalize(event_type), ("GovernanceRiskAgent",))


def get_agent_contract(name: str) -> AgentContract:
    normalized = _normalize(name)
    for contract in DEFAULT_AGENT_CONTRACTS:
        if _normalize(contract.name) == normalized:
            return contract
    raise KeyError(f"unknown_contract: {name}")


def contract_safety_violations(contract: AgentContract) -> tuple[str, ...]:
    """Return contract-level safety violations for fast audits."""
    violations: list[str] = []
    forbidden = {_normalize(x) for x in contract.forbidden_actions}
    allowed = {_normalize(x) for x in contract.allowed_actions}
    approvals = {_normalize(x) for x in contract.approval_required_for}
    outputs = {_normalize(x) for x in contract.outputs}

    if any("external_send" in x for x in allowed):
        violations.append("external_send_in_allowed_actions")
    if "external_send" not in forbidden:
        violations.append("external_send_not_forbidden")
    external_touchpoint = any(
        token in field
        for field in outputs
        for token in ("email", "dm", "message", "scope", "invoice", "pitch", "followup")
    )
    if "external_send" not in approvals and contract.name != "GovernanceRiskAgent" and external_touchpoint:
        violations.append("external_send_not_gated_by_approval")
    if "source" not in {_normalize(x) for x in contract.evidence_required}:
        violations.append("source_not_required")

    return tuple(violations)
