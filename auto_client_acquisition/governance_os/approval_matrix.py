"""Approval matrix — deterministic risk routing (policy-driven).

Routing rules live in ``policy_config/approval_policy.yaml``; this module is the
deterministic evaluator. YAML defaults are byte-equivalent to the prior hardcoded
if-chain, so behaviour is unchanged.
"""

from __future__ import annotations

from typing import Literal

from auto_client_acquisition.policy_config.loader import load_policy

Risk = Literal["low", "medium", "high"]


def _rule_matches(action: str, match: dict) -> bool:
    if not match:
        return False
    any_terms = match.get("any") or []
    all_terms = match.get("all") or []
    if not any_terms and not all_terms:
        return False
    if any_terms and not any(term in action for term in any_terms):
        return False
    return not (all_terms and not all(term in action for term in all_terms))


def approval_for_action(action: str) -> tuple[Risk, str]:
    a = action.lower().strip()
    policy = load_policy("approval_policy")
    for rule in policy.get("rules") or []:
        if _rule_matches(a, rule.get("match") or {}):
            return rule["risk"], rule["route"]
    default = policy.get("default") or {}
    return default.get("risk", "low"), default.get("route", "auto")
