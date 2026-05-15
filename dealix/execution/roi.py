"""
ROI Ledger — enterprise does not buy AI, it buys operational improvement.

Every workflow declares a manual baseline: how long the task takes a human
and what that human-minute costs. Each successful run books the delta as
realised savings. This is what an executive dashboard reports — not tokens.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ROIBaseline:
    """The manual cost a workflow run displaces."""

    workflow_name: str
    manual_minutes: float  # how long the task takes a human
    cost_per_minute_sar: float = 2.5  # loaded cost of an ops rep minute
    # A run only counts toward ROI once it reaches a successful terminal state.
    counts_when: tuple[str, ...] = ("completed",)

    @property
    def manual_cost_sar(self) -> float:
        return round(self.manual_minutes * self.cost_per_minute_sar, 2)


@dataclass(slots=True)
class ROIEntry:
    run_id: str
    workflow_name: str
    tenant_id: str
    minutes_saved: float
    cost_saved_sar: float
    automated_minutes: float


class ROILedger:
    """Books realised savings per workflow run."""

    def __init__(self) -> None:
        self._baselines: dict[str, ROIBaseline] = {}
        self._entries: list[ROIEntry] = []

    def register_baseline(self, baseline: ROIBaseline) -> None:
        self._baselines[baseline.workflow_name] = baseline

    def book(
        self,
        *,
        run_id: str,
        workflow_name: str,
        tenant_id: str,
        status: str,
        automated_ms: float,
    ) -> ROIEntry | None:
        """Book a run's ROI if its workflow has a baseline and it qualifies."""
        baseline = self._baselines.get(workflow_name)
        if baseline is None or status not in baseline.counts_when:
            return None
        automated_minutes = round(automated_ms / 60_000.0, 3)
        minutes_saved = max(0.0, baseline.manual_minutes - automated_minutes)
        cost_saved = round(minutes_saved * baseline.cost_per_minute_sar, 2)
        entry = ROIEntry(
            run_id=run_id,
            workflow_name=workflow_name,
            tenant_id=tenant_id,
            minutes_saved=round(minutes_saved, 3),
            cost_saved_sar=cost_saved,
            automated_minutes=automated_minutes,
        )
        self._entries.append(entry)
        return entry

    def summary(self, *, tenant_id: str | None = None) -> dict[str, Any]:
        entries = self._entries
        if tenant_id is not None:
            entries = [e for e in entries if e.tenant_id == tenant_id]
        return {
            "runs_booked": len(entries),
            "total_minutes_saved": round(sum(e.minutes_saved for e in entries), 2),
            "total_cost_saved_sar": round(sum(e.cost_saved_sar for e in entries), 2),
            "total_hours_saved": round(sum(e.minutes_saved for e in entries) / 60.0, 2),
        }


_LEDGER = ROILedger()


def get_roi_ledger() -> ROILedger:
    return _LEDGER


__all__ = ["ROIBaseline", "ROIEntry", "ROILedger", "get_roi_ledger"]
