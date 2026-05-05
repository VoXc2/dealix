"""Naive defensive token estimator — char/4 with a multiplier."""
from __future__ import annotations


def estimate_tokens(text: str, multiplier: float = 1.3) -> int:
    """Return an integer token estimate for ``text``.

    Naive char/4 heuristic — bounded and defensive. Non-string input
    or negative multipliers degrade to ``0`` rather than raising.
    """
    try:
        if not isinstance(text, str) or not text:
            return 0
        m = float(multiplier) if multiplier and multiplier > 0 else 1.0
        chars = len(text)
        base = chars / 4.0
        return max(0, int(round(base * m)))
    except Exception:  # noqa: BLE001 - never raise from estimator
        return 0
