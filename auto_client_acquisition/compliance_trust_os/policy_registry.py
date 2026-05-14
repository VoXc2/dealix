"""Policy registry — known runtime rule identifiers for governance matching."""

from __future__ import annotations

KNOWN_RUNTIME_POLICY_RULES: tuple[str, ...] = (
    "external_action_requires_approval",
    "pii_requires_review",
    "no_source_no_ai",
    "unsupported_claim_block",
    "channel_draft_only_default",
)


def policy_rule_known(rule_id: str) -> bool:
    return rule_id in KNOWN_RUNTIME_POLICY_RULES
