"""No Weak Scale Rule — refuse to scale anything weak.

See ``docs/strategic_control/NO_WEAK_SCALE_RULE.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class WeakScaleTarget(str, Enum):
    SERVICE = "service"
    PARTNER = "partner"
    PRODUCT = "product"
    MARKET = "market"


WEAK_SCALE_TARGETS: tuple[WeakScaleTarget, ...] = tuple(WeakScaleTarget)


@dataclass(frozen=True)
class WeakScaleSignals:
    target: WeakScaleTarget

    # Service signals
    weak_proof: bool = False
    unstable_qa: bool = False
    no_retainer_path: bool = False
    no_governance_enforcement: bool = False
    thin_margin: bool = False
    not_repeatable: bool = False

    # Partner signals
    does_not_understand_method: bool = False
    does_not_accept_qa: bool = False
    sells_guaranteed_outcomes: bool = False
    bypasses_governance: bool = False

    # Product signals
    not_used_internally: bool = False
    does_not_save_time: bool = False
    not_tied_to_revenue: bool = False
    does_not_reduce_risk: bool = False

    # Market signals
    buyer_unclear: bool = False
    weak_budget: bool = False
    data_risk_high: bool = False
    sales_cycle_exceeds_engagement: bool = False


@dataclass(frozen=True)
class WeakScaleResult:
    allow_scale: bool
    blocking_signals: tuple[str, ...]


def _service_blocks(s: WeakScaleSignals) -> list[str]:
    blocks: list[str] = []
    if s.weak_proof:
        blocks.append("weak_proof")
    if s.unstable_qa:
        blocks.append("unstable_qa")
    if s.no_retainer_path:
        blocks.append("no_retainer_path")
    if s.no_governance_enforcement:
        blocks.append("no_governance_enforcement")
    if s.thin_margin:
        blocks.append("thin_margin")
    if s.not_repeatable:
        blocks.append("not_repeatable")
    return blocks


def _partner_blocks(s: WeakScaleSignals) -> list[str]:
    blocks: list[str] = []
    if s.does_not_understand_method:
        blocks.append("does_not_understand_method")
    if s.does_not_accept_qa:
        blocks.append("does_not_accept_qa")
    if s.sells_guaranteed_outcomes:
        blocks.append("sells_guaranteed_outcomes")
    if s.bypasses_governance:
        blocks.append("bypasses_governance")
    return blocks


def _product_blocks(s: WeakScaleSignals) -> list[str]:
    blocks: list[str] = []
    if s.not_used_internally:
        blocks.append("not_used_internally")
    if s.does_not_save_time:
        blocks.append("does_not_save_time")
    if s.not_tied_to_revenue:
        blocks.append("not_tied_to_revenue")
    if s.does_not_reduce_risk:
        blocks.append("does_not_reduce_risk")
    return blocks


def _market_blocks(s: WeakScaleSignals) -> list[str]:
    blocks: list[str] = []
    if s.buyer_unclear:
        blocks.append("buyer_unclear")
    if s.weak_budget:
        blocks.append("weak_budget")
    if s.data_risk_high:
        blocks.append("data_risk_high")
    if s.sales_cycle_exceeds_engagement:
        blocks.append("sales_cycle_exceeds_engagement")
    return blocks


_BLOCK_FNS = {
    WeakScaleTarget.SERVICE: _service_blocks,
    WeakScaleTarget.PARTNER: _partner_blocks,
    WeakScaleTarget.PRODUCT: _product_blocks,
    WeakScaleTarget.MARKET: _market_blocks,
}


def evaluate_weak_scale(signals: WeakScaleSignals) -> WeakScaleResult:
    blocks = _BLOCK_FNS[signals.target](signals)
    return WeakScaleResult(
        allow_scale=not blocks,
        blocking_signals=tuple(blocks),
    )
