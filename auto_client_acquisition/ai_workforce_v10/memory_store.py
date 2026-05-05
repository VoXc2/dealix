"""Thread-safe in-memory short-term memory store.

Memory NEVER crosses customer boundaries. ``customer_handle`` is the
hard partition key. TTL defaults to 24h; expired entries are dropped
on read so the store stays bounded for short-running tests/processes.
"""
from __future__ import annotations

import threading
from datetime import UTC, datetime, timedelta

from auto_client_acquisition.ai_workforce_v10.schemas import WorkforceMemoryEntry


_LOCK = threading.RLock()
_MEMORY: dict[str, list[WorkforceMemoryEntry]] = {}


def record_memory(entry: WorkforceMemoryEntry) -> WorkforceMemoryEntry:
    """Persist ``entry`` keyed by its customer_handle."""
    with _LOCK:
        bucket = _MEMORY.setdefault(entry.customer_handle, [])
        bucket.append(entry)
    return entry


def _is_fresh(entry: WorkforceMemoryEntry, max_age_hours: int) -> bool:
    if max_age_hours <= 0:
        # Caller asked for "no age allowed" → only expire-time-zero entries
        # also count as expired.
        return False
    age = datetime.now(UTC) - entry.created_at
    cap = timedelta(hours=max(0, min(max_age_hours, entry.ttl_hours)))
    return age <= cap


def recall_memory(
    customer_handle: str,
    key: str | None = None,
    max_age_hours: int = 24,
) -> list[WorkforceMemoryEntry]:
    """Return matching, non-expired entries for one customer only."""
    with _LOCK:
        bucket = list(_MEMORY.get(customer_handle, []))
    fresh = [e for e in bucket if _is_fresh(e, max_age_hours)]
    if key is None:
        return fresh
    return [e for e in fresh if e.key == key]


def list_memory(customer_handle: str) -> list[WorkforceMemoryEntry]:
    """All entries for a customer (no TTL filter — for debugging routes)."""
    with _LOCK:
        return list(_MEMORY.get(customer_handle, []))


def reset_memory() -> None:
    """Test helper — drop all entries."""
    with _LOCK:
        _MEMORY.clear()
