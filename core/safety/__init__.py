"""
Dealix Safety Engine
====================

Executable safety boundaries for the Dealix Saudi B2B Revenue Operating System.

This package turns the written safety policy (docs/security, docs/privacy,
docs/agents) into code that can be unit-tested, so unsafe behaviour fails
*automatically* instead of relying on documentation alone.

Global, non-negotiable defaults for every external-action surface:

    DRY_RUN           = True
    APPROVAL_REQUIRED = True
    SEND_ENABLED      = False

Nothing in this package may send an external message, set a final price,
make a legal commitment, bypass suppression, edit secrets, deploy to
production, or escalate workflow permissions. These modules only *evaluate*
whether an action would be safe; the human founder remains the actuator.
"""

from .constants import (
    APPROVAL_REQUIRED_DEFAULT,
    DRY_RUN_DEFAULT,
    SEND_ENABLED_DEFAULT,
    EVIDENCE_LEVELS,
    RISK_LEVELS,
    SUPPRESSION_REASONS,
    PERMISSION_LEVELS,
    FORBIDDEN_ACTIONS,
)
from .claims import find_prohibited_claims, has_prohibited_claims
from .draft import personalization_grade, grade_at_least, evaluate_draft
from .outreach import (
    is_fake_reply_subject,
    has_unsubscribe,
    is_purchased_list,
    assess_outreach,
)
from .whatsapp import (
    contains_secret_or_api_key,
    requests_api_key,
    assess_whatsapp_message,
)
from .suppression import SuppressionList, is_suppressed
from .replies import classify_reply, route_reply
from .commercial import (
    payment_handoff,
    evaluate_proposal,
    renewal_allowed,
    won_deal_handoff,
)
from .untrusted import (
    is_trusted_source,
    can_trigger_external_send,
    requires_human_handoff,
    treat_as_data_only,
)
from .permissions import (
    AGENT_REGISTRY,
    get_agent,
    can_perform,
    is_forbidden_action,
    agent_can_change_workflow_permissions,
)

__all__ = [
    "APPROVAL_REQUIRED_DEFAULT",
    "DRY_RUN_DEFAULT",
    "SEND_ENABLED_DEFAULT",
    "EVIDENCE_LEVELS",
    "RISK_LEVELS",
    "SUPPRESSION_REASONS",
    "PERMISSION_LEVELS",
    "FORBIDDEN_ACTIONS",
    "find_prohibited_claims",
    "has_prohibited_claims",
    "personalization_grade",
    "grade_at_least",
    "evaluate_draft",
    "is_fake_reply_subject",
    "has_unsubscribe",
    "is_purchased_list",
    "assess_outreach",
    "contains_secret_or_api_key",
    "requests_api_key",
    "assess_whatsapp_message",
    "SuppressionList",
    "is_suppressed",
    "classify_reply",
    "route_reply",
    "payment_handoff",
    "evaluate_proposal",
    "renewal_allowed",
    "won_deal_handoff",
    "is_trusted_source",
    "can_trigger_external_send",
    "requires_human_handoff",
    "treat_as_data_only",
    "AGENT_REGISTRY",
    "get_agent",
    "can_perform",
    "is_forbidden_action",
    "agent_can_change_workflow_permissions",
]
