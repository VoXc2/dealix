"""Dealix Intelligence — Task → Model Tier registry.

Maps Dealix-specific tasks (decision_passport, executive_summary, etc.)
to the appropriate ModelTier from llm_gateway_v10.

Hard rule (Article 11): this module is a thin classifier on top of
``llm_gateway_v10``'s ModelTier enum — it doesn't define new tiers,
it just declares which Dealix task should use which tier.

Privacy rule: tasks tagged ``customer_internal`` MUST stay local
(or be sent to a privacy-tier provider with no training opt-in).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from auto_client_acquisition.llm_gateway_v10.schemas import ModelTier

# Canonical Dealix intelligence tasks (matches plan §32.4 + intelligence
# stack master prompt). Add new tasks here only when they map to a real
# Engine sub-phase.
DealixTask = Literal[
    # Engine 2 — Lead Intelligence
    "lead_classification",       # local cheap — boolean fit yes/no
    "lead_extract_entities",     # local — extract company/contact from raw text
    # Engine 3 — Company Brain
    "company_brain_build",        # mid — synthesizes intake into CompanyBrainV6
    "company_brain_summarize",    # mid — produces customer-safe summary
    # Engine 4 — Decision Passport
    "decision_passport",          # mid — composes Decision Passport from scores
    # Engine 5 — WhatsApp Decision
    "intent_classify",            # local cheap — Saudi-Arabic intent detection
    # Engine 7 — Delivery
    "draft_message_arabic",       # strong — Saudi-dialect outreach drafts
    "draft_message_english",      # strong — English outreach drafts
    "call_script",                # strong — bilingual call talk-track
    # Engine 8 — Support
    "support_classify",           # local cheap — Sentiment + category
    "support_reply_draft",        # mid — bilingual draft reply
    # Engine 9 — Payment
    "payment_evidence_summary",   # local cheap — extract amount/date from screenshot text
    # Engine 10 — Proof
    "proof_event_summarize",      # mid — proof_event → customer-safe sentence
    "proof_pack_assemble",        # strong — multi-event narrative
    "executive_summary",          # strong — Executive Pack Arabic+English
    # Engine 11 — Learning
    "learning_weekly_synthesis",  # strong — what worked / what failed
    "feature_request_triage",     # local cheap — pattern-match repeated requests
    # Engine 12 — Trust/Compliance
    "pii_redaction",              # local fast — detect+redact PII
    "safety_check",               # local fast — forbidden-token + risk score
    # Generic
    "json_extract_structured",    # local — text → structured JSON
    "deterministic_lookup",       # NO MODEL — pure rules/lookup
]


# Privacy levels — controls whether cloud is allowed
PrivacyLevel = Literal[
    "public_or_aggregated",   # safe to send to any cloud (no PII)
    "customer_internal",      # MUST stay local OR privacy-tier cloud only
    "founder_only",           # MUST stay local; never sent to cloud
]


@dataclass(frozen=True, slots=True)
class TaskRequirements:
    """What a Dealix task requires from the model layer.

    Used by ``dealix_model_router.py`` to choose the right ModelTier
    + decide whether local-only or cloud-fallback is allowed.
    """

    task: DealixTask
    tier: ModelTier
    requires_arabic_quality: bool
    requires_tool_calling: bool
    requires_structured_output: bool
    privacy_level: PrivacyLevel
    max_cost_usd_per_call: float
    fallback_to_human: bool
    """When the model is unavailable AND privacy/safety blocks cloud,
    should the task degrade to a draft awaiting human (True) or fail
    silently (False)?
    """


# The canonical mapping. Every DealixTask MUST appear here.
# Order: cheapest local → mid → strong cloud-friendly.
_REGISTRY: dict[DealixTask, TaskRequirements] = {
    # Local fast classifiers (low cost, high volume, no PII outside tenant)
    "lead_classification": TaskRequirements(
        task="lead_classification", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=False, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.001, fallback_to_human=False,
    ),
    "lead_extract_entities": TaskRequirements(
        task="lead_extract_entities", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.001, fallback_to_human=False,
    ),
    "intent_classify": TaskRequirements(
        task="intent_classify", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.0005, fallback_to_human=False,
    ),
    "support_classify": TaskRequirements(
        task="support_classify", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.001, fallback_to_human=False,
    ),
    "payment_evidence_summary": TaskRequirements(
        task="payment_evidence_summary", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="founder_only",
        max_cost_usd_per_call=0.0, fallback_to_human=True,
    ),
    "feature_request_triage": TaskRequirements(
        task="feature_request_triage", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.0005, fallback_to_human=False,
    ),
    "pii_redaction": TaskRequirements(
        task="pii_redaction", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="founder_only",
        max_cost_usd_per_call=0.0, fallback_to_human=False,
    ),
    "safety_check": TaskRequirements(
        task="safety_check", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="founder_only",
        max_cost_usd_per_call=0.0, fallback_to_human=False,
    ),
    "json_extract_structured": TaskRequirements(
        task="json_extract_structured", tier=ModelTier.cheap_for_classification,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.0005, fallback_to_human=False,
    ),
    # Mid-tier — composition / structured generation
    "company_brain_build": TaskRequirements(
        task="company_brain_build", tier=ModelTier.balanced_for_drafts,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.01, fallback_to_human=True,
    ),
    "company_brain_summarize": TaskRequirements(
        task="company_brain_summarize", tier=ModelTier.balanced_for_drafts,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.005, fallback_to_human=False,
    ),
    "decision_passport": TaskRequirements(
        task="decision_passport", tier=ModelTier.balanced_for_drafts,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.01, fallback_to_human=True,
    ),
    "support_reply_draft": TaskRequirements(
        task="support_reply_draft", tier=ModelTier.balanced_for_drafts,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.005, fallback_to_human=True,
    ),
    "proof_event_summarize": TaskRequirements(
        task="proof_event_summarize", tier=ModelTier.balanced_for_drafts,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.005, fallback_to_human=False,
    ),
    # Strong — strategy / final composition (cloud-friendly when allowed)
    "draft_message_arabic": TaskRequirements(
        task="draft_message_arabic", tier=ModelTier.strong_for_strategy,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.05, fallback_to_human=True,
    ),
    "draft_message_english": TaskRequirements(
        task="draft_message_english", tier=ModelTier.strong_for_strategy,
        requires_arabic_quality=False, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.03, fallback_to_human=True,
    ),
    "call_script": TaskRequirements(
        task="call_script", tier=ModelTier.strong_for_strategy,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.03, fallback_to_human=True,
    ),
    "proof_pack_assemble": TaskRequirements(
        task="proof_pack_assemble", tier=ModelTier.strong_for_strategy,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.10, fallback_to_human=True,
    ),
    "executive_summary": TaskRequirements(
        task="executive_summary", tier=ModelTier.strong_for_strategy,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=False, privacy_level="customer_internal",
        max_cost_usd_per_call=0.10, fallback_to_human=True,
    ),
    "learning_weekly_synthesis": TaskRequirements(
        task="learning_weekly_synthesis", tier=ModelTier.strong_for_strategy,
        requires_arabic_quality=True, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="customer_internal",
        max_cost_usd_per_call=0.10, fallback_to_human=True,
    ),
    # Pure rules — no model
    "deterministic_lookup": TaskRequirements(
        task="deterministic_lookup", tier=ModelTier.local_no_model,
        requires_arabic_quality=False, requires_tool_calling=False,
        requires_structured_output=True, privacy_level="public_or_aggregated",
        max_cost_usd_per_call=0.0, fallback_to_human=False,
    ),
}


def get_task_requirements(task: DealixTask) -> TaskRequirements:
    """Return the canonical TaskRequirements for a Dealix task.

    Raises ``KeyError`` for unknown tasks (Article 11 — no silent
    defaults that mask new task drift).
    """
    if task not in _REGISTRY:
        raise KeyError(
            f"Unknown DealixTask {task!r}. Add it to dealix_task_registry._REGISTRY "
            f"with explicit tier + privacy level + cost cap before use."
        )
    return _REGISTRY[task]


def all_tasks() -> tuple[DealixTask, ...]:
    """Return all registered DealixTask values (for tests + verifier)."""
    return tuple(_REGISTRY.keys())


def tasks_by_tier(tier: ModelTier) -> tuple[DealixTask, ...]:
    """All tasks routed to a specific ModelTier."""
    return tuple(t for t, req in _REGISTRY.items() if req.tier == tier)


def tasks_requiring_local_only() -> tuple[DealixTask, ...]:
    """Tasks tagged ``founder_only`` privacy — MUST stay local."""
    return tuple(t for t, req in _REGISTRY.items() if req.privacy_level == "founder_only")
