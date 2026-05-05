"""Language preference picker for a workforce run.

Trivial deterministic mapping; tests just need a stable default.
"""
from __future__ import annotations

from typing import Literal

from auto_client_acquisition.ai_workforce.schemas import WorkforceGoal


def pick_language(goal: WorkforceGoal) -> Literal["ar", "en", "bilingual"]:
    """Return the rendering language for a goal.

    Defaults to ``ar`` (Arabic-primary) — the founder's product is
    Saudi-first. Caller can still pass ``en`` or ``bilingual``.
    """
    pref = goal.language_preference if goal.language_preference else "ar"
    if pref not in ("ar", "en", "bilingual"):
        return "ar"
    return pref  # type: ignore[return-value]
