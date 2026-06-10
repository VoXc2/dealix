"""Dominance scorecard — weakest-link style recommendations."""

from __future__ import annotations

from dataclasses import dataclass, fields


@dataclass(frozen=True, slots=True)
class DominanceScorecard:
    """Each dimension is 0-100; higher is stronger (including governance health)."""

    category: int = 0
    offer: int = 0
    proof: int = 0
    retainer: int = 0
    product: int = 0
    governance: int = 0
    market: int = 0
    standard: int = 0
    venture: int = 0
    holding: int = 0


_PRIORITY_ORDER: tuple[str, ...] = (
    "governance",
    "category",
    "offer",
    "proof",
    "retainer",
    "product",
    "market",
    "standard",
    "venture",
    "holding",
)

_MESSAGES: dict[str, str] = {
    "governance": "governance_weak_stop_expansion",
    "category": "increase_education",
    "offer": "focus_wedge",
    "proof": "fix_delivery",
    "retainer": "fix_value_cadence",
    "product": "productize_repetition",
    "market": "build_distribution",
    "standard": "standards_and_academy",
    "venture": "venture_readiness",
    "holding": "holding_readiness",
}


def recommend_dominance_focus(card: DominanceScorecard) -> str:
    """Return a canonical focus code from the lowest priority-ordered dimension."""
    for name in _PRIORITY_ORDER:
        v = getattr(card, name)
        if not 0 <= v <= 100:
            raise ValueError(f"{name} must be 0..100, got {v}")
    weakest = min(_PRIORITY_ORDER, key=lambda n: getattr(card, n))
    return _MESSAGES[weakest]
