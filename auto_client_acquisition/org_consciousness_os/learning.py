"""System 42 — Organizational Learning Fabric.

Buckets friction events into rolling windows and detects friction kinds
that recur across windows — the patterns the organization should learn
from. Read-only.
"""

from __future__ import annotations

from datetime import datetime

from auto_client_acquisition.friction_log.schemas import FrictionEvent
from auto_client_acquisition.friction_log.store import list_events as friction_list_events
from auto_client_acquisition.org_consciousness_os._common import utcnow_naive
from auto_client_acquisition.org_consciousness_os.schemas import (
    LearningFabricReport,
    LearningPattern,
)


def _window_index(event: FrictionEvent, *, window_days: int, now_ts: float) -> int:
    """Return the rolling-window index of ``event`` (0 = most recent)."""
    try:
        ts = datetime.fromisoformat(event.occurred_at).timestamp()
    except ValueError:
        return -1
    age_days = (now_ts - ts) / 86400.0
    if age_days < 0:
        return 0
    return int(age_days // window_days)


def detect_learning_patterns(
    *,
    customer_id: str,
    lookback_windows: int = 4,
    window_days: int = 30,
) -> LearningFabricReport:
    """Detect recurring friction patterns for ``customer_id``."""
    span_days = max(1, lookback_windows) * max(1, window_days)
    events = friction_list_events(customer_id=customer_id, since_days=span_days, limit=10000)
    now_ts = utcnow_naive().timestamp()

    # kind -> {window_index: count}, and kind -> sample workflow ids
    by_kind: dict[str, dict[int, int]] = {}
    samples: dict[str, set[str]] = {}
    for ev in events:
        idx = _window_index(ev, window_days=window_days, now_ts=now_ts)
        if idx < 0 or idx >= lookback_windows:
            continue
        by_kind.setdefault(ev.kind, {})
        by_kind[ev.kind][idx] = by_kind[ev.kind].get(idx, 0) + 1
        if ev.workflow_id:
            samples.setdefault(ev.kind, set()).add(ev.workflow_id)

    half = max(1, lookback_windows // 2)
    patterns: list[LearningPattern] = []
    for kind, window_counts in by_kind.items():
        windows_seen = len(window_counts)
        if windows_seen < 2:
            continue  # not recurring
        occurrences = sum(window_counts.values())
        recent = sum(c for w, c in window_counts.items() if w < half)
        older = sum(c for w, c in window_counts.items() if w >= half)
        if recent > older:
            trend = "rising"
        elif recent < older:
            trend = "falling"
        else:
            trend = "stable"
        patterns.append(
            LearningPattern(
                pattern_key=kind,
                occurrences=occurrences,
                windows_seen=windows_seen,
                trend=trend,
                sample_workflows=tuple(sorted(samples.get(kind, set()))[:5]),
            )
        )

    patterns.sort(key=lambda p: p.occurrences, reverse=True)
    return LearningFabricReport(
        customer_id=customer_id,
        lookback_windows=lookback_windows,
        window_days=window_days,
        recurring_patterns=tuple(patterns),
    )


__all__ = ["detect_learning_patterns"]
