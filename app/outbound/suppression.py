"""Suppression authority for recipients who must never receive outbound messages.

The current implementation is intentionally in-memory and is suitable only for
unit tests, synthetic drills, and draft-only execution. It cannot prove that an
opt-out survives a process restart, horizontal replica, restore, or re-import.

The outbound policy gate therefore treats this backend as *not persistent* and
will not permit controlled live sending while it is the active implementation.
A future durable adapter must preserve the public interface below and provide an
independently tested ``persistent_suppression_ready()`` implementation before
live send can become eligible.

Suppression covers:
  - opt-outs (unsubscribe)
  - hard bounces
  - complaints
  - manual do-not-contact
  - legal/regulatory blocks (for example a scoped erasure/suppression request)
"""

from __future__ import annotations

from threading import Lock
from typing import Any

_LOCK = Lock()
# _SUPPRESSED[identifier] = set(channels) | {"__all__"}
_SUPPRESSED: "dict[str, set[str]]" = {}

ALL_CHANNELS = "__all__"
BACKEND_KIND = "memory"


def suppression_backend_kind() -> str:
    """Return the active suppression backend identifier."""

    return BACKEND_KIND


def persistent_suppression_ready() -> bool:
    """Whether suppression durability is proven for controlled live sends.

    This implementation deliberately returns ``False``. The in-memory store is
    process-local and cannot satisfy the privacy evidence requirement that an
    opt-out remains enforced after restart, replay, re-import, or restore.
    """

    return False


def suppression_backend_status() -> dict[str, Any]:
    """Return a non-sensitive status record for diagnostics and proof packs."""

    return {
        "backend": suppression_backend_kind(),
        "persistent": persistent_suppression_ready(),
        "live_send_eligible": persistent_suppression_ready(),
        "reason": "in_memory_suppression_is_not_durable",
    }


def _norm(identifier: str) -> str:
    return (identifier or "").strip().lower()


def is_suppressed(identifier: str, channel: str = "email") -> bool:
    """True if ``identifier`` is suppressed for ``channel`` or globally."""

    ident = _norm(identifier)
    if not ident:
        return False
    with _LOCK:
        entry = _SUPPRESSED.get(ident)
        if not entry:
            return False
        return ALL_CHANNELS in entry or channel in entry


def add_suppression(
    identifier: str,
    channel: str = ALL_CHANNELS,
    reason: str = "",
) -> None:
    """Add ``identifier`` to the process-local suppression list."""

    ident = _norm(identifier)
    if not ident:
        return
    with _LOCK:
        entry = _SUPPRESSED.setdefault(ident, set())
        entry.add(channel or ALL_CHANNELS)


def remove_suppression(identifier: str, channel: str | None = None) -> None:
    """Remove an entry from this process-local test backend."""

    ident = _norm(identifier)
    with _LOCK:
        if channel is None:
            _SUPPRESSED.pop(ident, None)
            return
        entry = _SUPPRESSED.get(ident)
        if entry:
            entry.discard(channel)
            if not entry:
                _SUPPRESSED.pop(ident, None)


def suppressed_channels(identifier: str) -> set[str]:
    """Return channels suppressed for ``identifier`` (may include ``__all__``)."""

    ident = _norm(identifier)
    with _LOCK:
        return set(_SUPPRESSED.get(ident, set()))


def clear_suppressions() -> None:
    """Clear process-local suppression state; used by tests only."""

    with _LOCK:
        _SUPPRESSED.clear()


def load_suppressions(items: list[dict[str, Any]]) -> None:
    """Bulk-load process-local suppression entries from dictionaries."""

    for item in items:
        add_suppression(
            str(item.get("identifier", "")),
            channel=str(item.get("channel", ALL_CHANNELS)),
            reason=str(item.get("reason", "")),
        )
