"""Margin protection rules (deterministic recommendations)."""

from __future__ import annotations

from enum import StrEnum


class MarginAction(StrEnum):
    NO_ACTION = "no_action"
    RAISE_PRICE = "raise_price"
    REDUCE_SCOPE = "reduce_scope"
    ADD_ON_PAID = "add_on_paid"
    REJECT = "reject"


def margin_protection_action(*, gross_margin: float, min_margin: float = 0.35) -> MarginAction:
    if gross_margin >= min_margin:
        return MarginAction.NO_ACTION
    if gross_margin < 0.1:
        return MarginAction.REJECT
    if gross_margin < 0.2:
        return MarginAction.RAISE_PRICE
    return MarginAction.ADD_ON_PAID


__all__ = ["MarginAction", "margin_protection_action"]
