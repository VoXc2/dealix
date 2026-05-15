"""Commercial sovereignty — avoid single-stream revenue fragility."""

from __future__ import annotations

COMMERCIAL_STREAMS: tuple[str, ...] = (
    "diagnostics",
    "sprints",
    "pilots",
    "retainers",
    "platform",
    "academy",
    "partners",
    "ventures",
    "enterprise",
)


def commercial_resilience_score(active_streams: frozenset[str]) -> int:
    if not COMMERCIAL_STREAMS:
        return 0
    n = sum(1 for s in COMMERCIAL_STREAMS if s in active_streams)
    return (n * 100) // len(COMMERCIAL_STREAMS)
