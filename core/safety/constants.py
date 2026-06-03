"""Shared constants for the Dealix safety engine."""

from __future__ import annotations

# --- Global hard defaults (every external-action surface inherits these) ---
DRY_RUN_DEFAULT: bool = True
APPROVAL_REQUIRED_DEFAULT: bool = True
SEND_ENABLED_DEFAULT: bool = False

# --- Evidence levels (ordered, weakest -> strongest) ---
# Used to forbid fabricated traction / unverifiable claims in data room,
# procurement, proposals and proof packs.
EVIDENCE_LEVELS = ["none", "assumption", "anecdote", "internal_data", "verified", "third_party_verified"]

# --- Risk levels (ordered) ---
RISK_LEVELS = ["low", "medium", "high", "critical"]

# --- Permission levels (L0..L6) ---
PERMISSION_LEVELS = {
    "L0": "Read only",
    "L1": "Docs/reports only",
    "L2": "Data/schema updates",
    "L3": "Code changes in branch",
    "L4": "Staging-only ops",
    "L5": "Sensitive planning only",
    "L6": "Forbidden autonomous action",
}

# --- Suppression reasons (PHASE 6) ---
SUPPRESSION_REASONS = [
    "unsubscribe",
    "bounce",
    "angry_reply",
    "do_not_contact",
    "legal_request",
    "privacy_request",
    "duplicate_risky",
    "invalid_email",
]

# --- Actions forbidden for ALL agents, at any permission level ---
FORBIDDEN_ACTIONS = [
    "external_send",            # no autonomous external sends
    "final_pricing",            # final price requires human approval
    "legal_commitment",         # legal commitments require human handoff
    "bypass_suppression",       # suppression list is inviolable
    "secrets_edit",             # never edit production secrets
    "production_deploy",        # never deploy to production
    "workflow_permission_escalation",  # never widen CI permissions
    "treat_untrusted_as_instructions",  # external content is data, never instructions
]

# --- Channels / sources that are always UNTRUSTED (data, never instructions) ---
UNTRUSTED_SOURCES = [
    "issue_comment",
    "issue_body",
    "pull_request_description",
    "pull_request_target",
    "email_inbound",
    "web_content",
    "scraped_content",
    "crm_note",
    "whatsapp_inbound",
    "pdf_document",
    "uploaded_document",
    "fork_readme",
    "fork_agents_md",
    "fork_claude_md",
    "mcp_tool_description",
]

# --- Categories that mandate human handoff (no autonomous AI response) ---
HUMAN_HANDOFF_CATEGORIES = [
    "legal",
    "complaint",
    "privacy_request",
    "privacy_deletion",
    "contract_terms",
    "refund_dispute",
    "regulatory",
]

# --- Deliverability readiness verdicts (PHASE 7) ---
DELIVERABILITY_VERDICTS = [
    "NOT_READY",
    "DRY_RUN_ONLY",
    "LIMITED_SEND_READY",
    "RAMP_READY",
    "PAUSE_REQUIRED",
]
