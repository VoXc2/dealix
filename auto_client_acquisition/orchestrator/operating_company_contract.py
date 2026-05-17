"""
Dealix Operating Company Contract.

This module encodes the "governed acceleration" operating doctrine as
deterministic rules that can be reused by orchestrators, APIs, and tests.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

GOVERNED_ACCELERATION_CHAIN: tuple[str, ...] = (
    "signal",
    "source",
    "risk",
    "approval",
    "action",
    "evidence",
    "decision",
    "value",
    "asset",
)


@dataclass(frozen=True)
class FactoryDefinition:
    factory_id: str
    name: str
    mission: str
    primary_loops: tuple[str, ...]


@dataclass(frozen=True)
class LoopDefinition:
    loop_id: str
    name: str
    start_event: str
    end_event: str
    outcome: str


@dataclass(frozen=True)
class AgentRole:
    agent_id: str
    mission: str
    inputs: tuple[str, ...]
    outputs: tuple[str, ...]
    forbidden_actions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ApprovalRule:
    action_id: str
    approval_required: bool
    reason: str


@dataclass(frozen=True)
class EventGuardRule:
    event_type: str
    required_prior_events: tuple[str, ...] = ()
    required_payload_fields: tuple[str, ...] = ()
    required_truthy_payload_fields: tuple[str, ...] = ()
    rejection_reason: str = "guard_failed"


@dataclass(frozen=True)
class OperatingCompanyContract:
    factories: tuple[FactoryDefinition, ...]
    loops: tuple[LoopDefinition, ...]
    agent_roles: tuple[AgentRole, ...]
    event_taxonomy: tuple[str, ...]
    state_machine: tuple[str, ...]
    allowed_transitions: Mapping[str, tuple[str, ...]]
    approval_rules: Mapping[str, ApprovalRule]
    event_guard_rules: Mapping[str, EventGuardRule]

    def validate_chain(self, chain: tuple[str, ...]) -> tuple[bool, str | None]:
        if chain == GOVERNED_ACCELERATION_CHAIN:
            return True, None
        return False, "chain_must_match_governed_acceleration"

    def requires_approval_for_action(
        self,
        *,
        action_id: str,
        context: Mapping[str, Any] | None = None,
    ) -> tuple[bool, str | None]:
        ctx = context or {}
        if action_id == "start_delivery":
            if bool(ctx.get("payment_proof")):
                return False, None
            return True, "start_delivery_requires_payment_proof"
        if action_id == "agent_tool_action":
            risk_level = str(ctx.get("risk_level", "low")).lower()
            if risk_level in {"medium", "high", "critical"}:
                return True, f"risk_level={risk_level}"
            return False, None
        if action_id == "send_followup_after_reply":
            if bool(ctx.get("auto_followup_allowed")):
                return False, None
            return True, "followup_requires_contextual_approval"
        rule = self.approval_rules.get(action_id)
        if rule is None:
            return False, None
        return rule.approval_required, rule.reason if rule.approval_required else None

    def validate_event(
        self,
        *,
        event_type: str,
        history: tuple[str, ...],
        payload: Mapping[str, Any] | None = None,
    ) -> tuple[bool, str | None]:
        if event_type not in self.event_taxonomy:
            return False, f"unknown_event_type={event_type}"
        guard = self.event_guard_rules.get(event_type)
        if guard is None:
            return True, None
        seen = set(history)
        for required in guard.required_prior_events:
            if required not in seen:
                return False, f"{guard.rejection_reason}:missing_prior={required}"
        event_payload = payload or {}
        for field in guard.required_payload_fields:
            if field not in event_payload:
                return False, f"{guard.rejection_reason}:missing_field={field}"
        for field in guard.required_truthy_payload_fields:
            if not event_payload.get(field):
                return False, f"{guard.rejection_reason}:field_not_truthy={field}"
        return True, None

    def validate_state_transition(self, *, src: str, dst: str) -> tuple[bool, str | None]:
        if src not in self.state_machine:
            return False, f"unknown_state={src}"
        if dst not in self.state_machine:
            return False, f"unknown_state={dst}"
        allowed = set(self.allowed_transitions.get(src, ()))
        if dst in allowed:
            return True, None
        return False, f"transition_not_allowed:{src}->{dst}"

    def to_summary(self) -> dict[str, Any]:
        return {
            "governed_chain": list(GOVERNED_ACCELERATION_CHAIN),
            "factories_total": len(self.factories),
            "loops_total": len(self.loops),
            "agents_total": len(self.agent_roles),
            "event_types_total": len(self.event_taxonomy),
            "states_total": len(self.state_machine),
        }


def build_operating_company_contract() -> OperatingCompanyContract:
    factories = (
        FactoryDefinition(
            factory_id="demand_factory",
            name="Demand Factory",
            mission="Turn market signals into qualified opportunities.",
            primary_loops=("market_signal_loop", "partner_loop"),
        ),
        FactoryDefinition(
            factory_id="trust_factory",
            name="Trust Factory",
            mission="Convert delivery learning into founder-led trust assets.",
            primary_loops=("founder_trust_loop", "proof_funnel_loop"),
        ),
        FactoryDefinition(
            factory_id="sales_factory",
            name="Sales Factory",
            mission="Convert qualified intent to approved scope, invoice, and payment.",
            primary_loops=("sales_conversion_loop",),
        ),
        FactoryDefinition(
            factory_id="delivery_factory",
            name="Delivery Factory",
            mission="Deliver diagnostics with source, approval, and evidence discipline.",
            primary_loops=("delivery_loop",),
        ),
        FactoryDefinition(
            factory_id="proof_factory",
            name="Proof Factory",
            mission="Turn delivery output into proof packs and reusable assets.",
            primary_loops=("proof_funnel_loop", "upsell_loop"),
        ),
        FactoryDefinition(
            factory_id="product_learning_factory",
            name="Product Learning Factory",
            mission="Promote repeated work from manual to template to module.",
            primary_loops=("productization_loop",),
        ),
        FactoryDefinition(
            factory_id="governance_factory",
            name="Governance Factory",
            mission="Block unsafe actions and enforce approval/evidence gates.",
            primary_loops=("governance_loop",),
        ),
    )

    loops = (
        LoopDefinition("market_signal_loop", "Market Signal Loop", "target_added", "reply_received", "learning"),
        LoopDefinition("founder_trust_loop", "Founder Trust Loop", "proof_pack_sent", "meeting_booked", "trust_compounding"),
        LoopDefinition("proof_funnel_loop", "Proof Funnel Loop", "risk_score_completed", "scope_requested", "proof_to_scope"),
        LoopDefinition("sales_conversion_loop", "Sales Conversion Loop", "lead_captured", "invoice_paid", "paid_conversion"),
        LoopDefinition("delivery_loop", "Delivery Loop", "delivery_started", "value_confirmed", "value_delivery"),
        LoopDefinition("upsell_loop", "Upsell Loop", "proof_pack_sent", "retainer_proposed", "expansion"),
        LoopDefinition("partner_loop", "Partner Loop", "referral_requested", "qualified_A", "partner_sourced_pipeline"),
        LoopDefinition("governance_loop", "Governance Loop", "message_prepared", "message_approved", "controlled_actions"),
        LoopDefinition("productization_loop", "Productization Loop", "diagnostic_started", "closed_won", "service_to_module"),
    )

    agent_roles = (
        AgentRole(
            agent_id="market_intelligence",
            mission="Scan demand signals and shortlist high-fit accounts.",
            inputs=("market_signals", "company_profiles", "manual_notes"),
            outputs=("target_accounts", "buying_signals", "confidence_scores"),
            forbidden_actions=("external_send", "security_claims"),
        ),
        AgentRole(
            agent_id="icp_scoring",
            mission="Rank opportunities to protect founder focus.",
            inputs=("account_profile", "intent_signals", "pain_hypothesis"),
            outputs=("icp_grade", "fit_score", "routing_decision"),
        ),
        AgentRole(
            agent_id="positioning",
            mission="Generate sector-specific positioning angles.",
            inputs=("sector", "pain_points", "offer_catalog"),
            outputs=("angle", "demo_path", "proof_requirements"),
        ),
        AgentRole(
            agent_id="content_strategy",
            mission="Convert objections and evidence into trust content.",
            inputs=("objections", "delivery_findings", "market_signals"),
            outputs=("post_drafts", "proof_snippets", "faq_entries"),
            forbidden_actions=("publish_without_approval",),
        ),
        AgentRole(
            agent_id="outreach_drafting",
            mission="Draft personalized outreach without autonomous send.",
            inputs=("target_account", "contact_role", "signal"),
            outputs=("dm_draft", "email_draft", "followup_draft"),
            forbidden_actions=("auto_send_first_touch", "cold_whatsapp", "unsupported_claims"),
        ),
        AgentRole(
            agent_id="reply_classifier",
            mission="Classify replies and recommend safe next action.",
            inputs=("reply_text", "conversation_context", "risk_context"),
            outputs=("reply_class", "next_action", "risk_level"),
        ),
        AgentRole(
            agent_id="meeting_brief",
            mission="Prepare high-signal call briefs and demo path.",
            inputs=("account_profile", "contact_profile", "prior_events"),
            outputs=("meeting_brief", "discovery_questions", "close_path"),
        ),
        AgentRole(
            agent_id="sales_call_coach",
            mission="Turn call notes into state decision.",
            inputs=("meeting_notes", "qualification_signals", "budget_data"),
            outputs=("state_update", "objection_map", "scope_readiness"),
        ),
        AgentRole(
            agent_id="scope_builder",
            mission="Generate governed diagnostic scope drafts.",
            inputs=("meeting_notes", "account_profile", "selected_offer"),
            outputs=("scope_draft", "price_recommendation", "exclusions"),
            forbidden_actions=("send_to_client", "final_invoice_generation"),
        ),
        AgentRole(
            agent_id="billing",
            mission="Convert approved scope to invoice workflow.",
            inputs=("approved_scope", "payment_terms", "contact_info"),
            outputs=("invoice_draft", "followup_schedule", "payment_status"),
            forbidden_actions=("start_delivery_without_payment_proof",),
        ),
        AgentRole(
            agent_id="delivery_diagnostic",
            mission="Run source-grounded diagnostics.",
            inputs=("onboarding_form", "crm_export", "workflow_notes"),
            outputs=("workflow_map", "risk_register", "top_decisions"),
        ),
        AgentRole(
            agent_id="proof_pack",
            mission="Package findings into commercial proof assets.",
            inputs=("diagnostic_findings", "evidence_assets", "founder_review"),
            outputs=("proof_pack", "anonymized_insights", "upsell_hint"),
            forbidden_actions=("send_without_founder_review",),
        ),
        AgentRole(
            agent_id="upsell",
            mission="Recommend next paid step from unresolved risk.",
            inputs=("proof_pack", "risk_priority", "delivery_outcome"),
            outputs=("next_offer", "retainer_candidate", "nurture_path"),
        ),
        AgentRole(
            agent_id="partner",
            mission="Build partner-led pipeline loops.",
            inputs=("partner_profile", "segment_fit", "offer"),
            outputs=("partner_pitch_draft", "referral_path", "fit_score"),
            forbidden_actions=("auto_sign_agreement",),
        ),
        AgentRole(
            agent_id="governance",
            mission="Enforce policy and block unsupported actions.",
            inputs=("proposed_action", "risk_context", "evidence_context"),
            outputs=("gate_decision", "risk_flags", "audit_event"),
            forbidden_actions=("silent_override",),
        ),
    )

    event_taxonomy = (
        "target_added",
        "message_prepared",
        "message_approved",
        "message_sent",
        "reply_received",
        "proof_pack_requested",
        "risk_score_completed",
        "lead_captured",
        "qualified_A",
        "meeting_booked",
        "meeting_done",
        "scope_requested",
        "scope_sent",
        "scope_approved",
        "invoice_sent",
        "invoice_paid",
        "onboarding_submitted",
        "diagnostic_started",
        "proof_pack_drafted",
        "proof_pack_sent",
        "value_confirmed",
        "sprint_proposed",
        "retainer_proposed",
        "referral_requested",
        "case_study_approved",
        "closed_lost",
        "closed_won",
    )

    state_machine = (
        "new_lead",
        "qualified_A",
        "qualified_B",
        "nurture",
        "partner_candidate",
        "meeting_booked",
        "meeting_done",
        "scope_requested",
        "scope_sent",
        "invoice_sent",
        "invoice_paid",
        "delivery_started",
        "proof_pack_sent",
        "sprint_candidate",
        "retainer_candidate",
        "closed_won",
        "closed_lost",
    )

    transitions = {
        "new_lead": ("qualified_A", "qualified_B", "nurture", "partner_candidate", "closed_lost"),
        "qualified_A": ("meeting_booked",),
        "qualified_B": ("meeting_booked", "nurture", "partner_candidate"),
        "nurture": ("meeting_booked", "closed_lost"),
        "partner_candidate": ("meeting_booked", "closed_lost", "closed_won"),
        "meeting_booked": ("meeting_done", "closed_lost"),
        "meeting_done": ("scope_requested", "nurture", "partner_candidate", "closed_lost"),
        "scope_requested": ("scope_sent", "closed_lost"),
        "scope_sent": ("invoice_sent", "closed_lost"),
        "invoice_sent": ("invoice_paid", "closed_lost"),
        "invoice_paid": ("delivery_started",),
        "delivery_started": ("proof_pack_sent", "closed_lost"),
        "proof_pack_sent": ("sprint_candidate", "retainer_candidate", "closed_won", "closed_lost"),
        "sprint_candidate": ("closed_won", "closed_lost"),
        "retainer_candidate": ("closed_won", "closed_lost"),
        "closed_won": (),
        "closed_lost": (),
    }

    approval_rules = {
        "create_lead": ApprovalRule("create_lead", approval_required=False, reason="internal"),
        "score_lead": ApprovalRule("score_lead", approval_required=False, reason="internal"),
        "draft_message": ApprovalRule("draft_message", approval_required=False, reason="draft_only"),
        "send_first_outreach": ApprovalRule(
            "send_first_outreach",
            approval_required=True,
            reason="external_reputation_sensitive",
        ),
        "send_sample_proof_pack": ApprovalRule(
            "send_sample_proof_pack",
            approval_required=True,
            reason="requires_initial_human_review",
        ),
        "send_scope": ApprovalRule(
            "send_scope",
            approval_required=True,
            reason="commercial_commitment",
        ),
        "send_invoice": ApprovalRule(
            "send_invoice",
            approval_required=True,
            reason="financial_commitment",
        ),
        "final_diagnostic": ApprovalRule(
            "final_diagnostic",
            approval_required=True,
            reason="quality_and_liability_gate",
        ),
        "publish_case_study": ApprovalRule(
            "publish_case_study",
            approval_required=True,
            reason="client_legal_permission_required",
        ),
        "security_claim": ApprovalRule(
            "security_claim",
            approval_required=True,
            reason="high_risk_claim_requires_source",
        ),
    }

    event_guards = {
        "message_sent": EventGuardRule(
            event_type="message_sent",
            required_prior_events=("message_approved",),
            rejection_reason="message_send_requires_approval",
        ),
        "meeting_done": EventGuardRule(
            event_type="meeting_done",
            required_payload_fields=("meeting_notes_ref",),
            rejection_reason="meeting_notes_required",
        ),
        "scope_sent": EventGuardRule(
            event_type="scope_sent",
            required_prior_events=("scope_requested",),
            rejection_reason="scope_send_requires_request",
        ),
        "invoice_sent": EventGuardRule(
            event_type="invoice_sent",
            required_prior_events=("scope_approved",),
            rejection_reason="invoice_requires_approved_scope",
        ),
        "invoice_paid": EventGuardRule(
            event_type="invoice_paid",
            required_payload_fields=("payment_proof_ref",),
            rejection_reason="invoice_paid_requires_payment_proof",
        ),
        "diagnostic_started": EventGuardRule(
            event_type="diagnostic_started",
            required_prior_events=("invoice_paid",),
            rejection_reason="delivery_requires_paid_invoice",
        ),
        "proof_pack_sent": EventGuardRule(
            event_type="proof_pack_sent",
            required_truthy_payload_fields=("founder_reviewed",),
            rejection_reason="proof_pack_requires_founder_review",
        ),
        "case_study_approved": EventGuardRule(
            event_type="case_study_approved",
            required_truthy_payload_fields=("client_permission",),
            rejection_reason="case_study_requires_client_permission",
        ),
    }

    return OperatingCompanyContract(
        factories=factories,
        loops=loops,
        agent_roles=agent_roles,
        event_taxonomy=event_taxonomy,
        state_machine=state_machine,
        allowed_transitions=transitions,
        approval_rules=approval_rules,
        event_guard_rules=event_guards,
    )


DEFAULT_OPERATING_COMPANY_CONTRACT = build_operating_company_contract()
