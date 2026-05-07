"""8-field card schema for ECC sections (Phase 2 finalization).

Every customer-facing decision card has the same 8 fields:
  signal              — what the system noticed
  why_now             — why this matters at this moment
  recommended_action  — concrete next step
  risk                — what could go wrong if ignored
  impact              — what happens if addressed
  owner               — who should act
  action_mode         — draft_only / approval_required / approved_manual / blocked
  proof_link          — pointer to evidence (or null if internal-only)
"""
from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

ActionMode = Literal[
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
    "blocked",
]


class DecisionCard(BaseModel):
    """The canonical 8-field card. Every ECC card SHOULD use this shape."""

    model_config = ConfigDict(extra="forbid")

    signal: str
    why_now: str
    recommended_action: str
    risk: str
    impact: str
    owner: str
    action_mode: ActionMode
    proof_link: str | None = None


def to_card_dict(
    *,
    signal: str,
    why_now: str = "",
    recommended_action: str = "",
    risk: str = "",
    impact: str = "",
    owner: str = "founder",
    action_mode: ActionMode = "approval_required",
    proof_link: str | None = None,
) -> dict[str, Any]:
    """Build an 8-field card dict (no validation — for renderer use)."""
    return DecisionCard(
        signal=signal,
        why_now=why_now or "—",
        recommended_action=recommended_action or "—",
        risk=risk or "—",
        impact=impact or "—",
        owner=owner,
        action_mode=action_mode,
        proof_link=proof_link,
    ).model_dump(mode="json")


def card_keys() -> list[str]:
    return [
        "signal", "why_now", "recommended_action", "risk", "impact",
        "owner", "action_mode", "proof_link",
    ]
