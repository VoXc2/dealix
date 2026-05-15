"""Campaign lifecycle FSM — blocks transitions that skip approval gate."""
from __future__ import annotations

from auto_client_acquisition.growth_v10.schemas import Campaign

# Valid transitions: state → set of allowed next states.
_VALID_TRANSITIONS: dict[str, set[str]] = {
    "draft": {"approved", "blocked"},
    "approved": {"running", "blocked", "draft"},
    "running": {"paused", "done", "blocked"},
    "paused": {"running", "done", "blocked"},
    "done": set(),
    "blocked": set(),
}


def transition_campaign(
    c: Campaign,
    target: str,
    *,
    consent_evidence: str | None = None,
) -> Campaign:
    """Transition a campaign — block if the target skips an approval gate.

    Rules:
      * The target state must be reachable from the current state.
      * If consent_required is True and we'd transition to ``running``
        without ``consent_evidence``, force the campaign to ``blocked``.
    """
    current = c.status
    allowed = _VALID_TRANSITIONS.get(current, set())

    if target not in allowed:
        # Block illegal transitions instead of mutating to nonsense.
        return c.model_copy(update={"status": "blocked"})

    if target == "running" and c.consent_required and not consent_evidence:
        return c.model_copy(update={"status": "blocked"})

    return c.model_copy(update={"status": target})
