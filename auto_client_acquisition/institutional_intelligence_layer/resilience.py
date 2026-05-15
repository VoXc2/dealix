"""Resilience and chaos readiness checks (System 61)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FailureEvent:
    workflow_id: str
    failure_type: str
    has_checkpoint: bool
    replay_available: bool
    rollback_available: bool
    blast_radius: str


def resilience_recovery_status(event: FailureEvent) -> dict[str, object]:
    """Assess if a failure can be recovered without institutional outage."""
    missing: list[str] = []
    if not event.workflow_id.strip():
        missing.append("workflow_id_missing")
    if not event.has_checkpoint:
        missing.append("checkpoint_missing")
    if not (event.replay_available or event.rollback_available):
        missing.append("no_recovery_path")
    if event.blast_radius == "unbounded":
        missing.append("blast_radius_unbounded")
    return {
        "can_recover": len(missing) == 0,
        "required_actions": tuple(missing),
    }


def chaos_readiness(
    *,
    canary_enabled: bool,
    replay_tested: bool,
    rollback_tested: bool,
) -> tuple[bool, tuple[str, ...]]:
    """Institutional chaos readiness requires tested replay and rollback."""
    blockers: list[str] = []
    if not canary_enabled:
        blockers.append("canary_not_enabled")
    if not replay_tested:
        blockers.append("replay_not_tested")
    if not rollback_tested:
        blockers.append("rollback_not_tested")
    return len(blockers) == 0, tuple(blockers)
