"""Meta-governance optimization primitives (System 62)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PolicyRule:
    rule_id: str
    domain: str
    priority: int
    condition_key: str
    outcome: str


def detect_policy_conflicts(rules: tuple[PolicyRule, ...]) -> tuple[str, ...]:
    """Detect conflicting outcomes for the same domain/condition pair."""
    seen: dict[tuple[str, str], str] = {}
    conflicts: list[str] = []
    for rule in rules:
        key = (rule.domain, rule.condition_key)
        prior = seen.get(key)
        if prior is None:
            seen[key] = rule.outcome
            continue
        if prior != rule.outcome:
            conflicts.append(f"conflict:{rule.domain}:{rule.condition_key}")
    return tuple(sorted(set(conflicts)))


def approval_overload(
    *,
    total_requests: int,
    approved_with_changes: int,
    median_wait_minutes: float,
) -> tuple[bool, tuple[str, ...]]:
    """Detect approval bottlenecks that weaken governance throughput."""
    blockers: list[str] = []
    if total_requests >= 100 and median_wait_minutes > 120:
        blockers.append("approval_queue_overloaded")
    if total_requests > 0 and (approved_with_changes / total_requests) > 0.4:
        blockers.append("upstream_draft_quality_low")
    return len(blockers) > 0, tuple(blockers)


def governance_optimization_actions(
    conflicts: tuple[str, ...],
    overload_blockers: tuple[str, ...],
) -> tuple[str, ...]:
    """Return deterministic optimization actions for governance runtime."""
    actions: list[str] = []
    if conflicts:
        actions.append("run_policy_conflict_resolution")
    if "approval_queue_overloaded" in overload_blockers:
        actions.append("introduce_risk_based_fastlane")
    if "upstream_draft_quality_low" in overload_blockers:
        actions.append("tighten_draft_contract_and_templates")
    if not actions:
        actions.append("no_change_required")
    return tuple(actions)
