"""Revenue Ops Machine — the per-lead funnel context.

The context is the small JSON blob persisted under
``LeadRecord.meta_json["revenue_ops"]``. No DB migration is needed: the
``metadata`` JSON column already exists. ``load_context`` defends against
schema drift by defaulting every field, so an older or partial blob never
crashes the machine.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.revenue_ops_machine.funnel_state import (
    FunnelState,
    advance,
    legacy_stage,
)

META_KEY = "revenue_ops"
_SCHEMA_VERSION = 1


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass
class FunnelContext:
    """Mutable funnel state for a single lead."""

    lead_id: str
    funnel_state: FunnelState = FunnelState.visitor
    abcd_grade: str = ""
    abcd_score: int = 0
    abcd_signals: dict[str, bool] = field(default_factory=dict)
    recommended_offer_id: str = ""
    case_study_approved: bool = False
    version: int = 1
    history: list[dict[str, str]] = field(default_factory=list)
    queued_draft_ids: list[str] = field(default_factory=list)

    def has_reached(self, state: FunnelState) -> bool:
        """True if the funnel is currently at, or has previously visited, ``state``."""
        if self.funnel_state == state:
            return True
        return any(entry.get("state") == str(state) for entry in self.history)

    def transition_to(self, target: FunnelState) -> FunnelState:
        """Validate via :func:`advance`, then mutate this context.

        Raises :class:`IllegalTransition` (from ``funnel_state``) on a bad move,
        leaving the context untouched.
        """
        new_state = advance(self.funnel_state, target, self)
        self.history.append({"state": str(self.funnel_state), "at": _now_iso()})
        self.funnel_state = new_state
        self.version += 1
        return new_state

    @property
    def legacy_stage(self) -> str:
        """The legacy 12-stage deal stage this funnel state maps onto."""
        return legacy_stage(self.funnel_state)

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": _SCHEMA_VERSION,
            "funnel_state": str(self.funnel_state),
            "abcd_grade": self.abcd_grade,
            "abcd_score": self.abcd_score,
            "abcd_signals": dict(self.abcd_signals),
            "recommended_offer_id": self.recommended_offer_id,
            "case_study_approved": self.case_study_approved,
            "version": self.version,
            "history": list(self.history),
            "queued_draft_ids": list(self.queued_draft_ids),
        }


def new_context(lead_id: str) -> FunnelContext:
    """A fresh context for a brand-new lead (starts at ``visitor``)."""
    return FunnelContext(lead_id=lead_id)


def load_context(lead_id: str, meta_json: dict[str, Any] | None) -> FunnelContext:
    """Build a :class:`FunnelContext` from a lead's ``meta_json``.

    Every field is defaulted; unknown keys are ignored. A missing or malformed
    ``revenue_ops`` blob yields a fresh ``visitor`` context rather than an error.
    """
    blob: dict[str, Any] = {}
    if isinstance(meta_json, dict):
        candidate = meta_json.get(META_KEY)
        if isinstance(candidate, dict):
            blob = candidate

    try:
        state = FunnelState(blob.get("funnel_state", FunnelState.visitor))
    except ValueError:
        state = FunnelState.visitor

    history = blob.get("history")
    if not isinstance(history, list):
        history = []
    queued = blob.get("queued_draft_ids")
    if not isinstance(queued, list):
        queued = []
    signals = blob.get("abcd_signals")
    if not isinstance(signals, dict):
        signals = {}

    return FunnelContext(
        lead_id=lead_id,
        funnel_state=state,
        abcd_grade=str(blob.get("abcd_grade", "") or ""),
        abcd_score=int(blob.get("abcd_score", 0) or 0),
        abcd_signals=signals,
        recommended_offer_id=str(blob.get("recommended_offer_id", "") or ""),
        case_study_approved=bool(blob.get("case_study_approved", False)),
        version=int(blob.get("version", 1) or 1),
        history=[h for h in history if isinstance(h, dict)],
        queued_draft_ids=[str(q) for q in queued],
    )


def save_context(meta_json: dict[str, Any] | None, ctx: FunnelContext) -> dict[str, Any]:
    """Return a NEW ``meta_json`` dict with the funnel context written in.

    A new dict is returned (not mutated in place) so the caller can reassign
    the SQLAlchemy JSON column and reliably flag it dirty.
    """
    merged = dict(meta_json) if isinstance(meta_json, dict) else {}
    merged[META_KEY] = ctx.to_dict()
    return merged


__all__ = [
    "META_KEY",
    "FunnelContext",
    "new_context",
    "load_context",
    "save_context",
]
