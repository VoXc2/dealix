"""Lead-lifecycle stage-transition guard (reads stage_transitions.yaml).

Deterministic, side-effect-free: callers decide what to do with the result.
"""

from __future__ import annotations

from dataclasses import dataclass

from auto_client_acquisition.policy_config.loader import load_policy


def _graph() -> dict[str, dict]:
    stages = load_policy("stage_transitions").get("stages")
    if not isinstance(stages, dict) or not stages:
        msg = "invalid_policy_yaml:stage_transitions"
        raise ValueError(msg)
    return stages


def stages() -> tuple[str, ...]:
    """All defined stage names."""
    return tuple(_graph().keys())


def allowed_transitions(stage: str) -> tuple[str, ...]:
    """Stages reachable in one step from ``stage`` (empty for terminal/unknown)."""
    entry = _graph().get(stage) or {}
    return tuple(entry.get("allowed_next") or ())


def required_evidence(stage: str) -> tuple[str, ...]:
    """Evidence-event types that must exist before ``stage`` may be left."""
    entry = _graph().get(stage) or {}
    return tuple(entry.get("required_evidence") or ())


@dataclass(frozen=True)
class TransitionResult:
    allowed: bool
    reason: str


def validate_transition(
    from_stage: str,
    to_stage: str,
    evidence: list[str] | set[str] | tuple[str, ...] | None = None,
) -> TransitionResult:
    """Check a stage move: target must be allowed and required evidence present."""
    graph = _graph()
    if from_stage not in graph:
        return TransitionResult(False, f"unknown_stage:{from_stage}")
    if to_stage not in graph:
        return TransitionResult(False, f"unknown_stage:{to_stage}")
    if to_stage not in allowed_transitions(from_stage):
        return TransitionResult(False, f"transition_not_allowed:{from_stage}->{to_stage}")
    have = set(evidence or ())
    missing = [e for e in required_evidence(from_stage) if e not in have]
    if missing:
        return TransitionResult(False, f"missing_evidence:{','.join(missing)}")
    return TransitionResult(True, "ok")


__all__ = [
    "TransitionResult",
    "allowed_transitions",
    "required_evidence",
    "stages",
    "validate_transition",
]
