"""
Agent permission matrix + registry (L0..L6) for all Dealix agents.

This is the single source of truth that the governance docs render from and
that ``tests/test_agent_permissions_market.py`` enforces. Every agent is
read-only-to-branch by default; nothing here can autonomously send, price,
commit legally, bypass suppression, edit secrets, deploy, or widen workflow
permissions.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from .constants import FORBIDDEN_ACTIONS, PERMISSION_LEVELS, RISK_LEVELS

# Highest permission level any autonomous agent may hold. L6 == forbidden.
MAX_AUTONOMOUS_LEVEL = "L4"


def _agent(
    name: str,
    mission: str,
    *,
    inputs: List[str],
    outputs: List[str],
    allowed: List[str],
    permission_level: str,
    risk_level: str,
    handoff: List[str],
    required_approval: bool = True,
    required_verification: Optional[List[str]] = None,
    extra_forbidden: Optional[List[str]] = None,
) -> Dict:
    return {
        "name": name,
        "mission": mission,
        "input_files": inputs,
        "output_files": outputs,
        "allowed_actions": allowed,
        # Every agent inherits the global forbidden list, plus any extras.
        "forbidden_actions": list(dict.fromkeys(FORBIDDEN_ACTIONS + (extra_forbidden or []))),
        "risk_level": risk_level,
        "permission_level": permission_level,
        "required_approval": required_approval,
        "required_verification": required_verification or ["self_check", "founder_review"],
        "handoff_targets": handoff,
        "collision_rules": "preserve_newer_safety_gates; do_not_overwrite_manual_edits; prefer_smaller_pr; conflict_report_on_overlap",
    }


# ---------------------------------------------------------------------------
# The 40 agents. Ordered to match the governance catalog.
# ---------------------------------------------------------------------------
_AGENTS: List[Dict] = [
    _agent("Founder Command Agent", "Orchestrate daily priorities and surface the single critical decision.",
           inputs=["reports/founder/DAILY_SUPER_COMMAND.md"], outputs=["reports/founder/DAILY_SUPER_COMMAND.md"],
           allowed=["read", "summarize", "prioritize", "draft_report"], permission_level="L1", risk_level="low",
           handoff=["Metrics Agent", "Approval Queue Agent"]),
    _agent("Brand Guard Agent", "Enforce brand voice and block exaggerated/guaranteed claims.",
           inputs=["docs/localization/*"], outputs=["reports/localization/*"],
           allowed=["read", "review", "flag_claims"], permission_level="L1", risk_level="low",
           handoff=["Draft Factory Agent", "Content Agent"]),
    _agent("Offer Catalog Agent", "Maintain the offer catalog with evidence levels.",
           inputs=["data/productized_services/services.yaml"], outputs=["docs/productized_services/SERVICE_CATALOG_AR.md"],
           allowed=["read", "draft_catalog", "update_data"], permission_level="L2", risk_level="low",
           handoff=["Proposal Agent", "Finance Agent"]),
    _agent("Product Catalog Agent", "Maintain product/service definitions used by proposals.",
           inputs=["data/productized_services/services.yaml"], outputs=["schemas/productized_service.schema.json"],
           allowed=["read", "draft_catalog", "update_data"], permission_level="L2", risk_level="low",
           handoff=["Proposal Agent"]),
    _agent("Sector Intelligence Agent", "Analyze sector pains from public + internal data.",
           inputs=["company_os/revenue/prospects.csv"], outputs=["reports/agents/MARKET_AGENT_AUDIT.md"],
           allowed=["read", "analyze", "draft_report"], permission_level="L1", risk_level="low",
           handoff=["Signal Detection Agent", "Prospect Research Agent"]),
    _agent("Signal Detection Agent", "Detect buying signals from public sources only.",
           inputs=["data/*"], outputs=["reports/agents/*"],
           allowed=["read", "analyze", "draft_report"], permission_level="L1", risk_level="medium",
           handoff=["Prospect Research Agent"], extra_forbidden=["unsafe_scraping"]),
    _agent("Prospect Research Agent", "Research prospects from public data, respect privacy + minimization.",
           inputs=["company_os/revenue/prospects.csv"], outputs=["company_os/revenue/prospects.csv"],
           allowed=["read", "research_public", "score", "update_data"], permission_level="L2", risk_level="medium",
           handoff=["Draft Factory Agent"], extra_forbidden=["unsafe_scraping", "purchased_lists"]),
    _agent("Draft Factory Agent", "Produce personalized outbound drafts (never sends).",
           inputs=["company_os/revenue/prospects.csv"], outputs=["company_os/revenue/outreach_queue.json"],
           allowed=["read", "draft_message"], permission_level="L3", risk_level="high",
           handoff=["Personalization Guard Agent", "Compliance Gate Agent"]),
    _agent("Personalization Guard Agent", "Enforce >= P1 personalization before a draft proceeds.",
           inputs=["company_os/revenue/outreach_queue.json"], outputs=["reports/agents/*"],
           allowed=["read", "grade", "block_below_threshold"], permission_level="L1", risk_level="medium",
           handoff=["Compliance Gate Agent"]),
    _agent("Compliance Gate Agent", "Block prohibited claims, missing unsubscribe, fake subjects, PII leaks.",
           inputs=["company_os/revenue/outreach_queue.json"], outputs=["reports/security/*"],
           allowed=["read", "validate", "block"], permission_level="L1", risk_level="high",
           handoff=["Deliverability Agent", "Approval Queue Agent"]),
    _agent("Deliverability Agent", "Verify SPF/DKIM/DMARC, suppression, ramp before any send-readiness.",
           inputs=["schemas/suppression.schema.json"], outputs=["reports/outreach/DELIVERABILITY_REVIEW.md"],
           allowed=["read", "verify_domain_health", "set_verdict"], permission_level="L1", risk_level="high",
           handoff=["Sending Ramp Agent", "Approval Queue Agent"]),
    _agent("Approval Queue Agent", "Maintain the human approval queue; never approves on its own.",
           inputs=["company_os/governance/approval_queue.json"], outputs=["company_os/governance/approval_queue.json"],
           allowed=["read", "enqueue", "record_human_decision"], permission_level="L2", risk_level="high",
           handoff=["Founder Command Agent"], extra_forbidden=["self_approval"]),
    _agent("Sending Ramp Agent", "Plan volume ramp; emits plan only, never executes a send.",
           inputs=["docs/outreach/SENDING_RAMP_PLAN_AR.md"], outputs=["reports/outreach/SENDING_RAMP_READINESS.md"],
           allowed=["read", "plan_ramp"], permission_level="L1", risk_level="high",
           handoff=["Deliverability Agent"]),
    _agent("Reply Handling Agent", "Classify inbound replies and route to safe next steps.",
           inputs=["company_os/revenue/followups.json"], outputs=["reports/agents/*"],
           allowed=["read", "classify", "route", "propose_suppression"], permission_level="L2", risk_level="high",
           handoff=["WhatsApp Concierge Agent", "Privacy Guard Agent", "Legal/Compliance Agent"]),
    _agent("WhatsApp Concierge Agent", "Handle WhatsApp post-consent only; never cold, never secrets.",
           inputs=["docs/whatsapp/*"], outputs=["reports/agents/*"],
           allowed=["read", "draft_reply_post_consent"], permission_level="L3", risk_level="high",
           handoff=["Approval Queue Agent", "Client Assessment Agent"], extra_forbidden=["cold_whatsapp", "api_keys_in_message"]),
    _agent("Client Assessment Agent", "Assess client fit and qualification from intake.",
           inputs=["company_os/delivery/p1_intake_template.md"], outputs=["reports/agents/*"],
           allowed=["read", "assess", "score_qualification"], permission_level="L1", risk_level="medium",
           handoff=["Action Card Agent", "Proposal Agent"]),
    _agent("Action Card Agent", "Turn assessments into recommended action cards (advice only).",
           inputs=["reports/agents/*"], outputs=["reports/agents/*"],
           allowed=["read", "draft_action_card"], permission_level="L1", risk_level="low",
           handoff=["Founder Command Agent"]),
    _agent("Permission Guard Agent", "Audit that agents stay within their permission level.",
           inputs=["docs/agents/AGENT_PERMISSION_MATRIX_AR.md"], outputs=["reports/agents/AGENT_GOVERNANCE_REVIEW.md"],
           allowed=["read", "audit", "flag_violation"], permission_level="L1", risk_level="medium",
           handoff=["Security Red Team Agent"]),
    _agent("Proposal Agent", "Draft proposals mapped to catalog for qualified opportunities (range only).",
           inputs=["data/productized_services/services.yaml"], outputs=["company_os/revenue/proposals.json"],
           allowed=["read", "draft_proposal", "quote_range"], permission_level="L3", risk_level="high",
           handoff=["Proof Pack Agent", "Approval Queue Agent"], extra_forbidden=["final_pricing", "send_proposal"]),
    _agent("Proof Pack Agent", "Assemble proof packs from verified, redacted evidence.",
           inputs=["company_os/delivery/proof_pack_template.md"], outputs=["reports/agents/*"],
           allowed=["read", "assemble_redacted_proof"], permission_level="L1", risk_level="medium",
           handoff=["Proposal Agent"], extra_forbidden=["fabricate_evidence"]),
    _agent("Payment Handoff Agent", "Prepare payment handoff; proceeds only on human approval.",
           inputs=["company_os/revenue/pipeline.json"], outputs=["reports/agents/*"],
           allowed=["read", "prepare_handoff"], permission_level="L3", risk_level="critical",
           handoff=["Approval Queue Agent", "Finance Agent"], extra_forbidden=["process_payment", "send_payment_link"]),
    _agent("Delivery Handoff Agent", "Hand won deals to delivery with scope + acceptance criteria.",
           inputs=["company_os/delivery/p1_delivery_sop.md"], outputs=["reports/agents/*"],
           allowed=["read", "draft_handoff"], permission_level="L2", risk_level="high",
           handoff=["Customer Success Agent"]),
    _agent("Renewal Agent", "Identify renewals only where delivered value is evidenced.",
           inputs=["company_os/revenue/pipeline.json"], outputs=["reports/agents/*"],
           allowed=["read", "identify_renewal_with_evidence"], permission_level="L1", risk_level="medium",
           handoff=["Customer Success Agent", "Approval Queue Agent"]),
    _agent("Customer Success Agent", "Drive adoption + value realization post-delivery.",
           inputs=["company_os/delivery/client_success_plan.md"], outputs=["reports/agents/*"],
           allowed=["read", "draft_success_plan"], permission_level="L1", risk_level="medium",
           handoff=["Renewal Agent"]),
    _agent("Content Agent", "Draft brand-safe content; no guaranteed claims, no PII.",
           inputs=["company_os/marketing/*"], outputs=["company_os/marketing/*"],
           allowed=["read", "draft_content"], permission_level="L3", risk_level="medium",
           handoff=["Brand Guard Agent"]),
    _agent("Press Agent", "Draft press/PR copy; factual, evidence-bound, no fabrication.",
           inputs=["company_os/marketing/*"], outputs=["reports/agents/*"],
           allowed=["read", "draft_press"], permission_level="L1", risk_level="medium",
           handoff=["Brand Guard Agent"], extra_forbidden=["fabricate_traction"]),
    _agent("Partnership Agent", "Identify partnership opportunities; no commitments.",
           inputs=["data/*"], outputs=["reports/agents/*"],
           allowed=["read", "analyze", "draft_outreach"], permission_level="L1", risk_level="medium",
           handoff=["Approval Queue Agent"], extra_forbidden=["sign_partnership"]),
    _agent("Finance Agent", "Compute unit economics, CAC/payback, channel ROI (advice only).",
           inputs=["company_os/finance/*"], outputs=["reports/finance/*"],
           allowed=["read", "compute_metrics", "draft_finance_report"], permission_level="L1", risk_level="medium",
           handoff=["Founder Command Agent"], extra_forbidden=["final_pricing", "create_invoice", "process_payment"]),
    _agent("Privacy Guard Agent", "Enforce PDPL minimization, retention, suppression, deletion runbook.",
           inputs=["docs/privacy/*"], outputs=["reports/privacy/*"],
           allowed=["read", "audit_privacy", "flag_pii", "trigger_handoff"], permission_level="L1", risk_level="high",
           handoff=["Legal/Compliance Agent", "Security Red Team Agent"]),
    _agent("Security Red Team Agent", "Threat-model agentic workflows; find injection/secret/escalation risks.",
           inputs=["docs/security/*", ".github/workflows/*"], outputs=["reports/security/*"],
           allowed=["read", "threat_model", "draft_security_report"], permission_level="L1", risk_level="high",
           handoff=["QA/Eval Agent", "Repo Integration Agent"]),
    _agent("QA/Eval Agent", "Maintain tests + evals; never weakens a safety gate.",
           inputs=["tests/*", "data/evals/*"], outputs=["tests/*", "data/evals/*"],
           allowed=["read", "write_tests", "add_evals"], permission_level="L3", risk_level="medium",
           handoff=["Security Red Team Agent"], extra_forbidden=["weaken_tests", "delete_safety_gate"]),
    _agent("Metrics Agent", "Aggregate funnel + agent-health metrics into dashboards/reports.",
           inputs=["company_os/*"], outputs=["reports/founder/*"],
           allowed=["read", "aggregate", "draft_dashboard"], permission_level="L1", risk_level="low",
           handoff=["Founder Command Agent"]),
    _agent("Repo Integration Agent", "Integrate agent outputs safely; resolve collisions via report.",
           inputs=["reports/agents/AGENT_GOVERNANCE_REVIEW.md"], outputs=["reports/agents/*"],
           allowed=["read", "merge_in_branch", "open_conflict_report"], permission_level="L3", risk_level="high",
           handoff=["Founder Command Agent"], extra_forbidden=["force_push", "delete_others_work"]),
    _agent("Frontend UX Agent", "Improve Arabic-first UX within branch; staging only.",
           inputs=["src/*"], outputs=["src/*"],
           allowed=["read", "edit_ui_in_branch"], permission_level="L3", risk_level="medium",
           handoff=["Repo Integration Agent"]),
    _agent("Procurement Agent", "Answer vendor/procurement questionnaires from verified facts.",
           inputs=["data/procurement/vendors.jsonl"], outputs=["docs/procurement/*"],
           allowed=["read", "draft_responses_with_evidence"], permission_level="L1", risk_level="medium",
           handoff=["Legal/Compliance Agent", "Data Room Agent"], extra_forbidden=["fabricate_certifications"]),
    _agent("Data Room Agent", "Maintain data-room index; mark unknowns TBD, never fabricate.",
           inputs=["docs/data_room/*"], outputs=["docs/data_room/*", "reports/data_room/*"],
           allowed=["read", "draft_index", "mark_tbd"], permission_level="L1", risk_level="medium",
           handoff=["Procurement Agent"], extra_forbidden=["fabricate_traction", "invent_customers"]),
    _agent("Legal/Compliance Agent", "Route legal-sensitive items to human; never gives binding advice.",
           inputs=["docs/procurement/LEGAL_HANDOFF_TRIGGERS_AR.md"], outputs=["reports/procurement/*"],
           allowed=["read", "flag", "trigger_human_handoff"], permission_level="L1", risk_level="critical",
           handoff=["Founder Command Agent"], extra_forbidden=["legal_commitment", "give_binding_legal_advice"]),
    _agent("Saudi Localization Agent", "Ensure Arabic-first tone, SAR, Riyadh TZ, KSA B2B norms.",
           inputs=["docs/localization/*"], outputs=["reports/localization/*"],
           allowed=["read", "review_localization", "draft_glossary"], permission_level="L1", risk_level="low",
           handoff=["Brand Guard Agent"]),
    _agent("Productized Services Agent", "Define productized services with scope + acceptance criteria.",
           inputs=["data/productized_services/services.yaml"], outputs=["docs/productized_services/*"],
           allowed=["read", "draft_service_def", "update_data"], permission_level="L2", risk_level="medium",
           handoff=["Offer Catalog Agent", "Finance Agent"]),
    _agent("Infrastructure Reliability Agent", "Review infra/reliability; staging only, no prod deploy.",
           inputs=["docs/infra/*"], outputs=["reports/infra/*"],
           allowed=["read", "review_infra", "draft_runbook"], permission_level="L4", risk_level="high",
           handoff=["Security Red Team Agent"], extra_forbidden=["production_deploy", "modify_prod_secrets", "weaken_deploy_gate"]),
]

AGENT_REGISTRY: Dict[str, Dict] = {a["name"]: a for a in _AGENTS}


def get_agent(name: str) -> Optional[Dict]:
    return AGENT_REGISTRY.get(name)


def is_forbidden_action(action: str) -> bool:
    """True if ``action`` is globally forbidden for all agents."""
    return action in FORBIDDEN_ACTIONS


def can_perform(agent_name: str, action: str) -> bool:
    """Whether an agent may perform an action.

    Forbidden actions are denied for everyone. Otherwise the action must be in
    the agent's allowed_actions list.
    """
    if is_forbidden_action(action):
        return False
    agent = get_agent(agent_name)
    if not agent:
        return False
    if action in agent["forbidden_actions"]:
        return False
    return action in agent["allowed_actions"]


def agent_can_change_workflow_permissions(agent_name: str) -> bool:
    """No agent may change CI/workflow permissions without human review."""
    return False
