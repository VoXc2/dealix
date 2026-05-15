"""Agent-to-agent handoff protocol — task 7 of the Agent Operating System.

A handoff carries state + context + an evidence reference. Doctrine: no
source-less answers — a handoff without evidence is rejected.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from typing import Any
from uuid import uuid4

_PII_KEY_HINTS: tuple[str, ...] = (
    "email", "phone", "mobile", "national", "iqama", "passport", "iban",
)


def _key_looks_like_pii(name: str) -> bool:
    n = name.lower()
    return any(hint in n for hint in _PII_KEY_HINTS)


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(frozen=True, slots=True)
class HandoffEnvelope:
    handoff_id: str
    from_agent: str
    to_agent: str
    state: str
    evidence_ref: str
    context: dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    accepted_by: str = ""
    accepted_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class HandoffValidation:
    ok: bool
    issues: tuple[str, ...]


def new_handoff(
    *,
    from_agent: str,
    to_agent: str,
    state: str,
    evidence_ref: str,
    context: dict[str, Any] | None = None,
) -> HandoffEnvelope:
    """Build a validated handoff envelope.

    Raises ValueError when identity, state, or evidence is missing.
    """
    if not from_agent.strip():
        raise ValueError("from_agent is required")
    if not to_agent.strip():
        raise ValueError("to_agent is required")
    if from_agent.strip() == to_agent.strip():
        raise ValueError("from_agent and to_agent must differ")
    if not state.strip():
        raise ValueError("state is required")
    if not evidence_ref.strip():
        raise ValueError("evidence_ref is required (no source-less handoff)")
    return HandoffEnvelope(
        handoff_id=f"hof_{uuid4().hex[:12]}",
        from_agent=from_agent.strip(),
        to_agent=to_agent.strip(),
        state=state.strip(),
        evidence_ref=evidence_ref.strip(),
        context=dict(context or {}),
        created_at=_now_iso(),
    )


def validate_handoff(env: HandoffEnvelope) -> HandoffValidation:
    """Non-raising validation — also flags PII-looking context keys."""
    issues: list[str] = []
    if not env.evidence_ref.strip():
        issues.append("missing_evidence_ref")
    if not env.state.strip():
        issues.append("missing_state")
    if env.from_agent.strip() == env.to_agent.strip():
        issues.append("same_from_to_agent")
    for key in env.context:
        if _key_looks_like_pii(str(key)):
            issues.append(f"pii_in_context:{key}")
    return HandoffValidation(ok=not issues, issues=tuple(issues))


def accept_handoff(env: HandoffEnvelope, *, receiving_agent_id: str) -> HandoffEnvelope:
    """Mark a handoff accepted. Raises when the receiver is not the target."""
    if receiving_agent_id.strip() != env.to_agent:
        raise ValueError(
            f"handoff target is {env.to_agent!r}, not {receiving_agent_id!r}",
        )
    from dataclasses import replace

    return replace(env, accepted_by=receiving_agent_id.strip(), accepted_at=_now_iso())


__all__ = [
    "HandoffEnvelope",
    "HandoffValidation",
    "accept_handoff",
    "new_handoff",
    "validate_handoff",
]
