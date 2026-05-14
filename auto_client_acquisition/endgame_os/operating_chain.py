"""Sacred core operating chain — no skipping stages."""

from __future__ import annotations

CORE_OPERATING_CHAIN: tuple[str, ...] = (
    "signal",
    "capability_diagnostic",
    "productized_sprint",
    "governed_delivery",
    "qa",
    "proof_pack",
    "retainer",
    "capital_asset",
    "product_module",
    "business_unit",
    "standard",
    "academy_or_partner",
    "venture",
    "holding_company",
)


def chain_index(step_id: str) -> int:
    try:
        return CORE_OPERATING_CHAIN.index(step_id)
    except ValueError as e:
        msg = f"unknown chain step: {step_id}"
        raise ValueError(msg) from e


def can_enter_step(completed: frozenset[str], step_id: str) -> bool:
    """Prior step in chain must be completed (first step excepted)."""
    idx = chain_index(step_id)
    if idx == 0:
        return True
    prev = CORE_OPERATING_CHAIN[idx - 1]
    return prev in completed


def chain_complete_through(completed: frozenset[str], step_id: str) -> bool:
    """All steps up to and including step_id are in completed."""
    idx = chain_index(step_id)
    return all(s in completed for s in CORE_OPERATING_CHAIN[: idx + 1])
