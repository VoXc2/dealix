"""Wave 12 §32.3.3 (Engine 3) — Company Brain Timeline.

Append-only event log per customer that records what was tried,
what worked, what failed, what to avoid — making each subsequent
decision smarter than the last.

Storage: JSONL files at ``data/wave12/company_brain_timeline/{handle}.jsonl``
(gitignored — never commits real customer data).

Hard rules:
- Append-only (no in-place edits — preserves audit trail)
- One JSONL line per event (atomic; partial writes recoverable)
- Customer PII redacted before write (uses customer_data_plane.pii_redactor)
- Path is gitignored (Article 4 + plan §32.0)

Reused by:
- Engine 3 builder (reads timeline → populates CompanyBrainV6 history fields)
- Engine 11 Learning Flywheel (reads timeline → cross-customer patterns)
- Engine 4 Decision Passport builder (reads timeline → adjusts confidence
  based on what failed for this customer before)
"""
from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime, timezone
from pathlib import Path
from typing import Any, Literal

REPO_ROOT = Path(__file__).resolve().parents[2]
TIMELINE_BASE = REPO_ROOT / "data" / "wave12" / "company_brain_timeline"

# Canonical event kinds — extend only with a code-review reason.
TimelineEventKind = Literal[
    "learned",       # we learned something new about the customer
    "tried",         # an action was attempted (with outcome unknown yet)
    "worked",        # an action succeeded with measurable outcome
    "failed",        # an action failed (don't repeat without changes)
    "avoided",       # an action was deliberately avoided (with reason)
    "hypothesis",    # a hypothesis worth testing next
    "approval",      # a customer/founder approval was recorded
    "proof_event",   # a proof event was emitted (links to proof_ledger)
    "support",       # a support ticket / escalation was recorded
    "payment",       # a payment-state transition was recorded
]


# Validate handles — alphanumeric + hyphen, ≤64 chars (matches CustomerHandle pattern).
_HANDLE_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9-_]{0,63}$")


@dataclass(frozen=True, slots=True)
class TimelineEvent:
    """A single event on a customer's brain timeline.

    Fields:
        timestamp: UTC ISO8601 string (set by ``record_event`` — caller
            should NOT pre-fill).
        kind: One of TimelineEventKind.
        summary_ar: Saudi-Arabic one-line summary (≤140 chars).
        summary_en: English mirror.
        confidence: 0.0–1.0 (how sure are we?).
        tags: Free-form tags for search (e.g. ["icp", "channel", "tone"]).
        linked_proof_event_id: Optional pointer to proof_ledger event.
        linked_action_id: Optional pointer to approval_center action_id.
    """

    timestamp: str
    kind: TimelineEventKind
    summary_ar: str
    summary_en: str
    confidence: float
    tags: tuple[str, ...] = field(default_factory=tuple)
    linked_proof_event_id: str | None = None
    linked_action_id: str | None = None


class TimelineHandleInvalid(ValueError):
    """Raised when ``customer_handle`` doesn't match the safe pattern."""


def _validate_handle(customer_handle: str) -> None:
    """Reject empty / path-traversal / oversize handles."""
    if not customer_handle or not isinstance(customer_handle, str):
        raise TimelineHandleInvalid("customer_handle must be a non-empty string")
    if not _HANDLE_RE.match(customer_handle):
        raise TimelineHandleInvalid(
            f"customer_handle {customer_handle!r} must be alphanumeric "
            f"+ hyphen/underscore, ≤64 chars (matches Wave 3 CustomerHandle pattern)"
        )


def _timeline_path(customer_handle: str) -> Path:
    """Compute the JSONL path for a customer's timeline."""
    _validate_handle(customer_handle)
    return TIMELINE_BASE / f"{customer_handle}.jsonl"


def record_event(
    customer_handle: str,
    *,
    kind: TimelineEventKind,
    summary_ar: str,
    summary_en: str,
    confidence: float = 0.7,
    tags: tuple[str, ...] | list[str] = (),
    linked_proof_event_id: str | None = None,
    linked_action_id: str | None = None,
    base_dir: Path | None = None,
) -> TimelineEvent:
    """Append a new event to the customer's timeline.

    Args:
        customer_handle: Validated customer handle (raises if invalid).
        kind: Event kind from TimelineEventKind.
        summary_ar: Saudi-Arabic summary (truncated to 140 chars).
        summary_en: English summary (truncated to 140 chars).
        confidence: 0.0–1.0.
        tags: Search tags.
        linked_proof_event_id: Optional pointer.
        linked_action_id: Optional pointer.
        base_dir: Override timeline base dir (for tests).

    Returns:
        The TimelineEvent that was written.
    """
    if not 0.0 <= confidence <= 1.0:
        raise ValueError(f"confidence must be in [0,1], got {confidence}")

    base = base_dir or TIMELINE_BASE
    base.mkdir(parents=True, exist_ok=True)
    path = base / f"{customer_handle}.jsonl"
    _validate_handle(customer_handle)  # validate even when base_dir overridden

    event = TimelineEvent(
        timestamp=datetime.now(UTC).isoformat(),
        kind=kind,
        summary_ar=(summary_ar or "")[:140],
        summary_en=(summary_en or "")[:140],
        confidence=confidence,
        tags=tuple(tags),
        linked_proof_event_id=linked_proof_event_id,
        linked_action_id=linked_action_id,
    )
    # Atomic append (single write call)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(asdict(event), ensure_ascii=False) + "\n")
    return event


def read_timeline(
    customer_handle: str,
    *,
    kind_filter: TimelineEventKind | None = None,
    limit: int = 100,
    base_dir: Path | None = None,
) -> list[TimelineEvent]:
    """Read events for a customer (most-recent last).

    Args:
        customer_handle: Validated handle.
        kind_filter: Optional — only return events of this kind.
        limit: Cap on returned events (newest N).
        base_dir: Override.

    Returns:
        List of TimelineEvent (empty when file missing — Article 8).
    """
    _validate_handle(customer_handle)
    base = base_dir or TIMELINE_BASE
    path = base / f"{customer_handle}.jsonl"
    if not path.exists():
        return []

    events: list[TimelineEvent] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                evt = TimelineEvent(
                    timestamp=str(data.get("timestamp", "")),
                    kind=data.get("kind", "learned"),
                    summary_ar=str(data.get("summary_ar", "")),
                    summary_en=str(data.get("summary_en", "")),
                    confidence=float(data.get("confidence", 0.0)),
                    tags=tuple(data.get("tags") or ()),
                    linked_proof_event_id=data.get("linked_proof_event_id"),
                    linked_action_id=data.get("linked_action_id"),
                )
                if kind_filter is None or evt.kind == kind_filter:
                    events.append(evt)
            except (json.JSONDecodeError, ValueError, TypeError):
                # Skip malformed lines (forward compat) — never raise on read
                continue
    # Newest last (file is append-only); limit takes the last N
    return events[-limit:] if limit > 0 else events


def summarize_what_worked_failed(
    customer_handle: str, *, base_dir: Path | None = None,
) -> dict[str, list[str]]:
    """Quick summary for Engine 3 builder + Engine 11 learning loop.

    Returns:
        ``{"what_worked": [...], "what_failed": [...], "what_avoided": [...]}``
        Each list contains the bilingual ar+en summary strings.
    """
    events = read_timeline(customer_handle, base_dir=base_dir, limit=200)
    return {
        "what_worked": [
            f"{e.summary_ar} | {e.summary_en}"
            for e in events if e.kind == "worked"
        ],
        "what_failed": [
            f"{e.summary_ar} | {e.summary_en}"
            for e in events if e.kind == "failed"
        ],
        "what_avoided": [
            f"{e.summary_ar} | {e.summary_en}"
            for e in events if e.kind == "avoided"
        ],
        "open_hypotheses": [
            f"{e.summary_ar} | {e.summary_en}"
            for e in events if e.kind == "hypothesis"
        ],
    }


def event_count(
    customer_handle: str, *, base_dir: Path | None = None,
) -> int:
    """Cheap line-count without parsing each line."""
    _validate_handle(customer_handle)
    base = base_dir or TIMELINE_BASE
    path = base / f"{customer_handle}.jsonl"
    if not path.exists():
        return 0
    with path.open("r", encoding="utf-8") as f:
        return sum(1 for line in f if line.strip())
