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

# Canonical current commercial path. Legacy events/states remain below only for
# compatibility; they do not supersede this authority.
CANONICAL_COMMERCIAL_CHAIN: tuple[str, ...] = (
    "real_interaction",
    "verified_relationship",
    "qualified_problem",
    "free_mini_diagnostic",
    "qualified_discovery",
    "customer_specific_quote",
    "pilot_decision",
    "pilot_payment_verified",
    "pilot_delivery",
    "proof_review",
    "expansion_or_stop",
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
    required_any_prior_events: tuple[str, ...] = ()
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
        if action_id in {"start_delivery", "start_pilot_delivery"}:
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
        if guard.required_any_prior_events and not seen.intersection(
            guard.required_any_prior_events
        ):
            required_any = ",".join(guard.required_any_prior_events)
            return False, f"{guard.rejection_reason}:missing_any_prior={required_any}"
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
            "canonical_commercial_chain": list(CANONICAL_COMMERCIAL_CHAIN),
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
            mission=(
                "Turn market signals into evidenced real interactions and qualified "
                "problems without promoting research into relationships."
            ),
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
            mission=(
                "Move evidenced relationships through Free Mini Diagnostic, qualified "
                "Discovery, customer-specific Quote and paid 30-day Pilot."
            ),
            primary_loops=("sales_conversion_loop",),
        ),
        FactoryDefinition(
            factory_id="delivery_factory",
            name="Delivery Factory",
            mission=(
                "Deliver only approved paid Pilot scope after verified payment, with "
                "explicit acceptance criteria and evidence discipline."
            ),
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
        LoopDefinition(
            "market_signal_loop",
            "Market Signal Loop",
            "target_added",
            "interaction_captured",
            "research_to_real_interaction",
        ),
        LoopDefinition(
            "founder_trust_loop",
            "Founder Trust Loop",
            "proof_pack_sent",
            "meeting_booked",
            "trust_compounding",
        ),
        LoopDefinition(
            "proof_funnel_loop",
            "Proof Funnel Loop",
            "risk_score_completed",
            "scope_requested",
            "proof_to_scope",
        ),
        LoopDefinition(
            "sales_conversion_loop",
            "Sales Conversion Loop",
            "relationship_verified",
            "pilot_payment_verified",
            "paid_conversion",
        ),
        LoopDefinition(
            "delivery_loop",
            "Delivery Loop",
            "pilot_delivery_started",
            "value_confirmed",
            "value_delivery",
        ),
        LoopDefinition(
            "upsell_loop",
            "Upsell Loop",
            "final_proof_pack_ready",
            "expansion_decision",
            "expansion",
        ),
        LoopDefinition(
            "partner_loop",
            "Partner Loop",
            "referral_requested",
            "relationship_verified",
            "partner_sourced_relationship",
        ),
        LoopDefinition(
            "governance_loop",
            "Governance Loop",
            "message_prepared",
            "message_approved",
            "controlled_actions",
        ),
        LoopDefinition(
            "productization_loop",
            "Productization Loop",
            "value_confirmed",
            "expansion_decision",
            "service_to_module",
        ),
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
            mission="Rank research hypotheses without promoting them to relationships.",
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
            mission="Prepare high-signal call briefs and discovery path.",
            inputs=("account_profile", "contact_profile", "prior_events"),
            outputs=("meeting_brief", "discovery_questions", "close_path"),
        ),
        AgentRole(
            agent_id="sales_call_coach",
            mission="Turn call notes into evidence-backed commercial state decisions.",
            inputs=("meeting_notes", "qualification_signals", "budget_data"),
            outputs=("state_update", "objection_map", "scope_readiness"),
        ),
        AgentRole(
            agent_id="scope_builder",
            mission="Generate customer-specific Pilot scope drafts only after Discovery.",
            inputs=("discovery_notes", "account_profile", "selected_offer"),
            outputs=("scope_draft", "commercial_options", "evidence_requirements", "exclusions"),
            forbidden_actions=("send_to_client", "final_invoice_generation"),
        ),
        AgentRole(
            agent_id="billing",
            mission="Convert an approved customer-specific Quote into invoice workflow.",
            inputs=("approved_quote", "payment_terms", "contact_info"),
            outputs=("invoice_draft", "followup_schedule", "payment_status"),
            forbidden_actions=("start_delivery_without_payment_proof",),
        ),
        AgentRole(
            agent_id="delivery_diagnostic",
            mission="Prepare source-grounded Free Mini Diagnostic evidence before Discovery.",
            inputs=("interaction_evidence", "workflow_notes", "allowed_customer_context"),
            outputs=("revenue_leak_map", "risk_register", "top_decisions"),
        ),
        AgentRole(
            agent_id="proof_pack",
            mission="Package verified delivery findings into commercial proof assets.",
            inputs=("delivery_findings", "evidence_assets", "founder_review"),
            outputs=("proof_pack", "anonymized_insights", "expansion_hint"),
            forbidden_actions=("send_without_founder_review",),
        ),
        AgentRole(
            agent_id="upsell",
            mission="Recommend expansion only from verified unresolved value or risk.",
            inputs=("proof_pack", "risk_priority", "delivery_outcome"),
            outputs=("next_offer", "expansion_candidate", "nurture_path"),
        ),
        AgentRole(
            agent_id="partner",
            mission="Build partner-led relationship loops.",
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
        # Canonical commercial truth events.
        "interaction_captured",
        "relationship_verified",
        "problem_qualified",
        "diagnostic_started",
        "diagnostic_completed",
        "discovery_completed",
        "customer_specific_quote_prepared",
        "customer_specific_quote_approved",
        "pilot_decision_approved",
        "pilot_payment_verified",
        "pilot_delivery_started",
        "weekly_proof_ready",
        "final_proof_pack_ready",
        "expansion_decision",
        # Compatibility events retained for existing runners/readers.
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
        # Canonical commercial states.
        "research_signal",
        "real_interaction",
        "verified_relationship",
        "qualified_problem",
        "free_diagnostic",
        "qualified_discovery",
        "customer_specific_quote",
        "pilot_decision",
        "pilot_payment_verified",
        "pilot_delivery",
        "proof_review",
        "expansion_candidate",
        # Compatibility states retained for existing runners/readers.
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
        # Canonical path. Research cannot jump into a commercial state.
        "research_signal": ("real_interaction",),
        "real_interaction": ("verified_relationship", "nurture", "closed_lost"),
        "verified_relationship": ("qualified_problem", "nurture", "closed_lost"),
        "qualified_problem": ("free_diagnostic", "nurture", "closed_lost"),
        "free_diagnostic": ("qualified_discovery", "nurture", "closed_lost"),
        "qualified_discovery": ("customer_specific_quote", "nurture", "closed_lost"),
        "customer_specific_quote": ("pilot_decision", "closed_lost"),
        "pilot_decision": ("pilot_payment_verified", "closed_lost"),
        "pilot_payment_verified": ("pilot_delivery",),
        "pilot_delivery": ("proof_review", "closed_lost"),
        "proof_review": ("expansion_candidate", "closed_won", "closed_lost"),
        "expansion_candidate": ("closed_won", "closed_lost"),
        # Legacy compatibility path. It cannot create Closed Won from a partner
        # marker and still preserves payment proof before delivery.
        "new_lead": ("qualified_A", "qualified_B", "nurture", "partner_candidate", "closed_lost"),
        "qualified_A": ("meeting_booked",),
        "qualified_B": ("meeting_booked", "nurture", "partner_candidate"),
        "nurture": ("meeting_booked", "closed_lost"),
        "partner_candidate": ("meeting_booked", "closed_lost"),
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
        "send_customer_specific_quote": ApprovalRule(
            "send_customer_specific_quote",
            approval_required=True,
            reason="named_customer_commercial_commitment",
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
        "interaction_captured": EventGuardRule(
            event_type="interaction_captured",
            required_payload_fields=("interaction_evidence_ref",),
            rejection_reason="interaction_requires_evidence",
        ),
        "relationship_verified": EventGuardRule(
            event_type="relationship_verified",
            required_prior_events=("interaction_captured",),
            required_payload_fields=("interaction_evidence_ref",),
            rejection_reason="relationship_requires_real_interaction_evidence",
        ),
        "problem_qualified": EventGuardRule(
            event_type="problem_qualified",
            required_prior_events=("relationship_verified",),
            required_payload_fields=("problem_evidence_ref",),
            rejection_reason="qualification_requires_verified_relationship_and_problem_evidence",
        ),
        "diagnostic_started": EventGuardRule(
            event_type="diagnostic_started",
            # Current canonical path starts the Free Mini Diagnostic after a
            # qualified problem. invoice_paid is retained as a legacy-compatible
            # prior event for historical paid-diagnostic records only.
            required_any_prior_events=("problem_qualified", "invoice_paid"),
            rejection_reason="diagnostic_requires_qualified_problem_or_legacy_paid_context",
        ),
        "diagnostic_completed": EventGuardRule(
            event_type="diagnostic_completed",
            required_prior_events=("diagnostic_started",),
            required_payload_fields=("diagnostic_output_ref",),
            rejection_reason="diagnostic_completion_requires_evidence",
        ),
        "discovery_completed": EventGuardRule(
            event_type="discovery_completed",
            required_prior_events=("diagnostic_completed",),
            required_payload_fields=("discovery_notes_ref",),
            rejection_reason="discovery_requires_completed_diagnostic_and_notes",
        ),
        "customer_specific_quote_prepared": EventGuardRule(
            event_type="customer_specific_quote_prepared",
            required_prior_events=("discovery_completed",),
            required_payload_fields=("scope_evidence_ref",),
            rejection_reason="quote_requires_qualified_discovery_and_customer_scope",
        ),
        "customer_specific_quote_approved": EventGuardRule(
            event_type="customer_specific_quote_approved",
            required_prior_events=("customer_specific_quote_prepared",),
            required_payload_fields=("quote_authority_ref",),
            rejection_reason="quote_requires_explicit_authority",
        ),
        "pilot_decision_approved": EventGuardRule(
            event_type="pilot_decision_approved",
            required_prior_events=("customer_specific_quote_approved",),
            required_payload_fields=("decision_evidence_ref",),
            rejection_reason="pilot_decision_requires_approved_quote_and_evidence",
        ),
        "pilot_payment_verified": EventGuardRule(
            event_type="pilot_payment_verified",
            required_prior_events=("pilot_decision_approved",),
            required_payload_fields=("payment_proof_ref",),
            rejection_reason="pilot_payment_requires_verified_external_payment_evidence",
        ),
        "pilot_delivery_started": EventGuardRule(
            event_type="pilot_delivery_started",
            required_prior_events=("pilot_payment_verified",),
            required_payload_fields=("payment_proof_ref",),
            rejection_reason="pilot_delivery_requires_verified_payment",
        ),
        "weekly_proof_ready": EventGuardRule(
            event_type="weekly_proof_ready",
            required_prior_events=("pilot_delivery_started",),
            required_payload_fields=("proof_evidence_ref",),
            rejection_reason="weekly_proof_requires_delivery_evidence",
        ),
        "final_proof_pack_ready": EventGuardRule(
            event_type="final_proof_pack_ready",
            required_prior_events=("pilot_delivery_started",),
            required_payload_fields=("proof_evidence_ref",),
            rejection_reason="final_proof_requires_delivery_evidence",
        ),
        "expansion_decision": EventGuardRule(
            event_type="expansion_decision",
            required_prior_events=("final_proof_pack_ready",),
            required_payload_fields=("decision_evidence_ref",),
            rejection_reason="expansion_requires_final_proof_and_decision_evidence",
        ),
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
        "closed_won": EventGuardRule(
            event_type="closed_won",
            required_any_prior_events=("pilot_payment_verified", "invoice_paid"),
            required_payload_fields=("payment_proof_ref",),
            rejection_reason="closed_won_requires_verified_payment_evidence",
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
