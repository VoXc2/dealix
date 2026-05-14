"""In-memory engagement snapshots for Founder Command Summary (MVP).

Revenue Intelligence pipeline stages call ``merge_pipeline_stage`` after each
HTTP step so GET /founder-summary can aggregate without a dedicated DB table.
Thread-safe for concurrent FastAPI workers within one process.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Any

_lock = threading.Lock()
_STORE: dict[str, "EngagementSnapshot"] = {}


@dataclass
class EngagementSnapshot:
    """Minimal state machine for one commercial engagement (e.g. RI sprint)."""

    engagement_id: str
    client_label: str | None = None
    import_done: bool = False
    score_done: bool = False
    draft_done: bool = False
    finalize_done: bool = False
    proof_generated: bool = False
    retainer_evaluated: bool = False
    data_quality_score: float | None = None
    proof_score: float | None = None
    client_health: float | None = None
    retainer_decision: str | None = None  # Continue | Expand | Pause
    pii_flagged: bool = False
    governance_notes: tuple[str, ...] = field(default_factory=tuple)
    top_opportunity_summary: str | None = None
    pipeline_context: dict[str, Any] = field(default_factory=dict)
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_public_dict(self) -> dict[str, Any]:
        return {
            "engagement_id": self.engagement_id,
            "client_label": self.client_label,
            "stages": {
                "import": self.import_done,
                "score": self.score_done,
                "draft_pack": self.draft_done,
                "finalize": self.finalize_done,
                "proof_pack": self.proof_generated,
                "retainer_gate": self.retainer_evaluated,
            },
            "data_quality_score": self.data_quality_score,
            "proof_score": self.proof_score,
            "client_health": self.client_health,
            "retainer_decision": self.retainer_decision,
            "pii_flagged": self.pii_flagged,
            "governance_notes": list(self.governance_notes),
            "top_opportunity_summary": self.top_opportunity_summary,
            "pipeline_context": dict(self.pipeline_context),
            "updated_at": self.updated_at.isoformat(),
        }


def get_snapshot(engagement_id: str) -> EngagementSnapshot | None:
    with _lock:
        return _STORE.get(engagement_id)


def list_snapshots() -> dict[str, EngagementSnapshot]:
    with _lock:
        return dict(_STORE)


def clear_all_for_tests() -> None:
    with _lock:
        _STORE.clear()


def merge_pipeline_stage(
    engagement_id: str,
    *,
    client_label: str | None = None,
    import_done: bool | None = None,
    score_done: bool | None = None,
    draft_done: bool | None = None,
    finalize_done: bool | None = None,
    proof_generated: bool | None = None,
    retainer_evaluated: bool | None = None,
    data_quality_score: float | None = None,
    proof_score: float | None = None,
    client_health: float | None = None,
    retainer_decision: str | None = None,
    pii_flagged: bool | None = None,
    governance_notes: tuple[str, ...] | None = None,
    top_opportunity_summary: str | None = None,
    pipeline_context_update: dict[str, Any] | None = None,
) -> EngagementSnapshot:
    """Upsert engagement snapshot (partial merge)."""
    now = datetime.now(UTC)
    with _lock:
        existing = _STORE.get(engagement_id)
        if existing is None:
            base = EngagementSnapshot(engagement_id=engagement_id, client_label=client_label)
        else:
            base = existing
        kwargs: dict[str, Any] = {"updated_at": now}
        if client_label is not None:
            kwargs["client_label"] = client_label
        for k, v in (
            ("import_done", import_done),
            ("score_done", score_done),
            ("draft_done", draft_done),
            ("finalize_done", finalize_done),
            ("proof_generated", proof_generated),
            ("retainer_evaluated", retainer_evaluated),
            ("data_quality_score", data_quality_score),
            ("proof_score", proof_score),
            ("client_health", client_health),
            ("retainer_decision", retainer_decision),
            ("pii_flagged", pii_flagged),
            ("governance_notes", governance_notes),
            ("top_opportunity_summary", top_opportunity_summary),
        ):
            if v is not None:
                kwargs[k] = v
        if pipeline_context_update is not None:
            kwargs["pipeline_context"] = {**base.pipeline_context, **pipeline_context_update}
        merged = replace(base, **kwargs)
        _STORE[engagement_id] = merged
        return merged
