"""Lead-lifecycle stage graph — integrity + transition guard."""

from __future__ import annotations

from auto_client_acquisition.policy_config import load_policy
from auto_client_acquisition.policy_config.stage_guard import (
    allowed_transitions,
    stages,
    validate_transition,
)


def test_graph_loads_with_initial_stage() -> None:
    policy = load_policy("stage_transitions")
    assert policy["initial"] in policy["stages"]


def test_no_orphan_targets() -> None:
    defined = set(stages())
    for stage in defined:
        for target in allowed_transitions(stage):
            assert target in defined, f"{stage} -> undefined stage {target}"


def test_every_stage_reachable_from_initial() -> None:
    initial = load_policy("stage_transitions")["initial"]
    seen: set[str] = set()
    frontier = [initial]
    while frontier:
        current = frontier.pop()
        if current in seen:
            continue
        seen.add(current)
        frontier.extend(allowed_transitions(current))
    assert seen == set(stages())


def test_allowed_transition_passes() -> None:
    result = validate_transition("new_lead", "qualified_a")
    assert result.allowed is True


def test_disallowed_transition_rejected() -> None:
    result = validate_transition("new_lead", "invoice_paid")
    assert result.allowed is False
    assert result.reason.startswith("transition_not_allowed")


def test_transition_blocked_when_required_evidence_missing() -> None:
    result = validate_transition("scope_sent", "invoice_sent", evidence=["scope_requested"])
    assert result.allowed is False
    assert "missing_evidence:scope_approved" in result.reason


def test_transition_allowed_when_required_evidence_present() -> None:
    result = validate_transition(
        "scope_sent", "invoice_sent", evidence=["scope_requested", "scope_approved"]
    )
    assert result.allowed is True


def test_unknown_stage_rejected() -> None:
    assert validate_transition("bogus", "new_lead").reason == "unknown_stage:bogus"
