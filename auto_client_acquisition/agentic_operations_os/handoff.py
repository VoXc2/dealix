"""Agent-to-human handoff — no ambiguous next step."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class HandoffObject:
    handoff_id: str
    agent_id: str
    output_id: str
    handoff_to: str
    reason: str
    required_action: str
    deadline: str


def handoff_valid(obj: HandoffObject) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if not obj.handoff_to.strip():
        errors.append("handoff_to_required")
    if not obj.required_action.strip():
        errors.append("required_action_required")
    if not obj.reason.strip():
        errors.append("reason_required_ambiguous_handoff")
    return not errors, tuple(errors)


def pii_output_requires_handoff(*, contains_pii: bool, handoff_to: str, required_action: str) -> bool:
    if not contains_pii:
        return True
    return bool(handoff_to.strip() and required_action.strip())
