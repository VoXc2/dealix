"""Tier degradation chain — strong → balanced → cheap → local."""
from __future__ import annotations

from auto_client_acquisition.llm_gateway_v10.schemas import ModelTier

_DEGRADE_ORDER: tuple[ModelTier, ...] = (
    ModelTier.strong_for_strategy,
    ModelTier.balanced_for_drafts,
    ModelTier.cheap_for_classification,
    ModelTier.local_no_model,
)


def fallback_chain(tier: ModelTier) -> list[ModelTier]:
    """Return the degrading chain starting at ``tier``.

    Includes ``tier`` first, then every cheaper tier. If ``tier`` is
    not recognised, returns the full chain so callers always have at
    least the local tier as a final stop.
    """
    try:
        if tier in _DEGRADE_ORDER:
            idx = _DEGRADE_ORDER.index(tier)
            return list(_DEGRADE_ORDER[idx:])
        return list(_DEGRADE_ORDER)
    except Exception:
        return list(_DEGRADE_ORDER)
