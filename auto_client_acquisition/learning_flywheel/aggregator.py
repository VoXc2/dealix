"""Wave 12 §32.3.11 — Learning Flywheel Aggregator.

Append-only learning event log + weekly synthesis.

Storage: ``data/wave12/learning_events.jsonl`` (gitignored).

Hard rule (Article 8): aggregate functions return ``None`` / empty
when source data is missing — never fabricate numbers.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[2]
LEARNING_EVENTS_PATH = REPO_ROOT / "data" / "wave12" / "learning_events.jsonl"

# Canonical learning event types (from plan §32.3.11).
LearningEventKind = Literal[
    "signal_created",
    "lead_created",
    "lead_scored",
    "decision_passport_created",
    "action_created",
    "action_approved",
    "action_rejected",
    "manual_message_sent",
    "reply_received",
    "demo_booked",
    "diagnostic_delivered",
    "pilot_requested",
    "payment_confirmed",
    "delivery_started",
    "proof_created",
    "upsell_offered",
    "upsell_accepted",
    "monthly_started",
    "churn_risk_detected",
    "feature_request_received",
]


@dataclass(frozen=True, slots=True)
class LearningEvent:
    """A single learning event (matches Engine 11 spec)."""

    timestamp: str
    kind: LearningEventKind
    customer_handle: str
    sector: str = ""
    channel: str = ""
    offer: str = ""
    icp_tier: str = ""
    succeeded: bool | None = None
    revenue_sar: float = 0.0
    notes_ar: str = ""
    notes_en: str = ""
    tags: tuple[str, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class WeeklyLearningReport:
    """Weekly synthesis — replaces the skeleton in revenue_os/learning_weekly.py."""

    period_start: str  # ISO date
    period_end: str
    events_total: int
    what_worked: list[str]
    what_failed: list[str]
    best_icp: str | None
    best_channel: str | None
    best_offer: str | None
    most_frequent_objection: str | None
    revenue_confirmed_sar: float
    paid_pilots_count: int
    feature_requests_repeated: list[str]
    next_recommendation_ar: str
    next_recommendation_en: str


def record_learning_event(
    *,
    kind: LearningEventKind,
    customer_handle: str,
    sector: str = "",
    channel: str = "",
    offer: str = "",
    icp_tier: str = "",
    succeeded: bool | None = None,
    revenue_sar: float = 0.0,
    notes_ar: str = "",
    notes_en: str = "",
    tags: tuple[str, ...] | list[str] = (),
    storage_path: Path | None = None,
) -> LearningEvent:
    """Append a learning event to the global learning log.

    Args:
        kind: Event kind from LearningEventKind.
        customer_handle: Tenant scope.
        sector / channel / offer / icp_tier: Optional dimensions for
            cross-cutting analysis (best ICP / channel / offer).
        succeeded: True / False / None (unknown — recommended default).
        revenue_sar: Confirmed revenue (Article 8 — only set when
            payment_confirmed). Default 0.
        notes_ar / notes_en: Bilingual short summary (≤200 chars).
        tags: Free-form search tags.
        storage_path: Override (for tests).

    Returns:
        The LearningEvent that was written.
    """
    path = storage_path or LEARNING_EVENTS_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    event = LearningEvent(
        timestamp=datetime.now(UTC).isoformat(),
        kind=kind,
        customer_handle=customer_handle,
        sector=sector, channel=channel, offer=offer, icp_tier=icp_tier,
        succeeded=succeeded, revenue_sar=float(revenue_sar),
        notes_ar=(notes_ar or "")[:200],
        notes_en=(notes_en or "")[:200],
        tags=tuple(tags),
    )
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
    return event


def _read_events(
    storage_path: Path | None = None,
) -> list[LearningEvent]:
    """Read all learning events. Empty list when file missing."""
    path = storage_path or LEARNING_EVENTS_PATH
    if not path.exists():
        return []
    events: list[LearningEvent] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                events.append(LearningEvent(
                    timestamp=str(data.get("timestamp", "")),
                    kind=data.get("kind", "signal_created"),
                    customer_handle=str(data.get("customer_handle", "")),
                    sector=str(data.get("sector", "")),
                    channel=str(data.get("channel", "")),
                    offer=str(data.get("offer", "")),
                    icp_tier=str(data.get("icp_tier", "")),
                    succeeded=data.get("succeeded"),
                    revenue_sar=float(data.get("revenue_sar", 0.0)),
                    notes_ar=str(data.get("notes_ar", "")),
                    notes_en=str(data.get("notes_en", "")),
                    tags=tuple(data.get("tags") or ()),
                ))
            except (json.JSONDecodeError, ValueError, TypeError):
                continue
    return events


def _mode(items: list[str]) -> str | None:
    """Most-frequent string in a list (None when empty or all-empty)."""
    cleaned = [x for x in items if x]
    if not cleaned:
        return None
    counts: dict[str, int] = {}
    for x in cleaned:
        counts[x] = counts.get(x, 0) + 1
    return max(counts.items(), key=lambda kv: kv[1])[0]


def aggregate_weekly_report(
    *,
    period_end: datetime | None = None,
    period_days: int = 7,
    storage_path: Path | None = None,
) -> WeeklyLearningReport:
    """Compute the weekly learning report from recorded events.

    Args:
        period_end: End of the window (default: now UTC).
        period_days: Window size in days (default 7).
        storage_path: Override.

    Returns:
        WeeklyLearningReport. Empty / None fields when no source data
        in window — Article 8 (no fabrication).
    """
    end = period_end or datetime.now(UTC)
    start = end - timedelta(days=period_days)
    all_events = _read_events(storage_path=storage_path)

    # Filter to window
    in_window: list[LearningEvent] = []
    for evt in all_events:
        try:
            ts = datetime.fromisoformat(evt.timestamp.replace("Z", "+00:00"))
            if start <= ts <= end:
                in_window.append(evt)
        except (ValueError, AttributeError):
            continue

    # what_worked / what_failed = bilingual summaries
    what_worked = [
        f"{e.notes_ar or e.notes_en} ({e.channel})"
        for e in in_window
        if e.succeeded is True and (e.notes_ar or e.notes_en)
    ]
    what_failed = [
        f"{e.notes_ar or e.notes_en} ({e.channel})"
        for e in in_window
        if e.succeeded is False and (e.notes_ar or e.notes_en)
    ]

    # Best-of tracking — mode of dimensions among succeeded events
    succeeded_events = [e for e in in_window if e.succeeded is True]
    best_icp = _mode([e.icp_tier for e in succeeded_events])
    best_channel = _mode([e.channel for e in succeeded_events])
    best_offer = _mode([e.offer for e in succeeded_events])

    # Most-frequent objection (extract from failed events' notes)
    failed_notes = [e.notes_en for e in in_window if e.succeeded is False]
    most_frequent_objection = _mode(failed_notes) if failed_notes else None

    # Revenue truth — only payment_confirmed events count
    revenue_confirmed_sar = sum(
        e.revenue_sar for e in in_window
        if e.kind == "payment_confirmed"
    )
    paid_pilots_count = sum(
        1 for e in in_window
        if e.kind == "payment_confirmed" and e.revenue_sar > 0
    )

    # Feature requests repeated by ≥3 different customers
    feat_by_note: dict[str, set[str]] = {}
    for e in in_window:
        if e.kind == "feature_request_received":
            note = e.notes_en or e.notes_ar
            if note:
                feat_by_note.setdefault(note, set()).add(e.customer_handle)
    feature_requests_repeated = sorted(
        note for note, handles in feat_by_note.items() if len(handles) >= 3
    )

    # Recommendation
    if paid_pilots_count >= 3:
        rec_ar = "أرسل أول case study لتعزيز التحويل"
        rec_en = "Publish the first case study to lift conversion"
    elif paid_pilots_count >= 1:
        rec_ar = f"تم {paid_pilots_count} pilot — اتبع warm intros جدد للوصول إلى 3"
        rec_en = f"{paid_pilots_count} pilot(s) — send more warm intros to reach 3"
    else:
        rec_ar = "ابدأ بأول 5 رسائل warm intro لإطلاق المسار"
        rec_en = "Start with the first 5 warm-intro messages to ignite the funnel"

    return WeeklyLearningReport(
        period_start=start.date().isoformat(),
        period_end=end.date().isoformat(),
        events_total=len(in_window),
        what_worked=what_worked,
        what_failed=what_failed,
        best_icp=best_icp,
        best_channel=best_channel,
        best_offer=best_offer,
        most_frequent_objection=most_frequent_objection,
        revenue_confirmed_sar=revenue_confirmed_sar,
        paid_pilots_count=paid_pilots_count,
        feature_requests_repeated=feature_requests_repeated,
        next_recommendation_ar=rec_ar,
        next_recommendation_en=rec_en,
    )
