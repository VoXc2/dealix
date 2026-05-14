"""Wave 16 — silence known-safe DeprecationWarnings at app boot.

Production on Railway flagged 46 warnings on the first deploy. Static
analysis identified the dominant source as `passlib` (via its `crypt`
import path that Python 3.13 deprecated; we run 3.11 in prod but
upstream emits the warning anyway via `warnings.warn`).

Doctrine: NEVER silence UserWarning or RuntimeWarning. Only specific
DeprecationWarning from named third-party modules, each with a TODO
deadline so we re-evaluate when those upstream packages cut new
releases.
"""
from __future__ import annotations

import warnings


# ── DeprecationWarning silencers ─────────────────────────────────────
# Each entry MUST cite the upstream issue/tracker (or "third-party noise")
# and have a re-evaluate-by date or trigger condition.

_KNOWN_SAFE = (
    # passlib emits a DeprecationWarning when it imports `crypt` on its
    # own initialization, regardless of whether we use the crypt-backed
    # hashers. We use bcrypt only. Re-evaluate when passlib > 1.7.4 ships
    # (it's been stale since 2020).
    # TODO(2026-09-01): re-check passlib version + lift this filter.
    {
        "category": DeprecationWarning,
        "module": "passlib",
        "reason": "passlib transitive crypt import; we use bcrypt only",
    },
    # passlib.utils imports crypt internally.
    # TODO(2026-09-01): re-check.
    {
        "category": DeprecationWarning,
        "module": "passlib.utils",
        "reason": "same as passlib; crypt import path",
    },
    # The "crypt" module itself emits the deprecation when imported.
    # We never import crypt directly — only transitively via passlib.
    # TODO(2026-09-01): re-check.
    {
        "category": DeprecationWarning,
        "module": "crypt",
        "reason": "transitive via passlib only",
    },
)


def install() -> None:
    """Install the known-safe filters. Call once at app boot.

    Idempotent: re-calling is safe; warnings.filterwarnings is
    additive but Python deduplicates identical filters.
    """
    for entry in _KNOWN_SAFE:
        warnings.filterwarnings(
            "ignore",
            category=entry["category"],
            module=entry["module"],
        )


def silenced_summary() -> list[dict[str, str]]:
    """Returns the silencer list for the launch-status endpoint to
    surface in the JSON. Helps auditors verify what's been suppressed.
    """
    return [
        {
            "module": entry["module"],
            "category": entry["category"].__name__,
            "reason": entry["reason"],
        }
        for entry in _KNOWN_SAFE
    ]


__all__ = ["install", "silenced_summary"]
