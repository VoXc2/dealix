"""Proof Pack → moat flywheel stages (deterministic checklist)."""

from __future__ import annotations

PROOF_TO_MOAT_STAGES: tuple[str, ...] = (
    "client_expansion",
    "anonymized_insight",
    "benchmark_update",
    "sales_asset",
    "product_signal",
    "market_content",
    "trust_increase",
)


def proof_to_moat_progress(completed_stages: frozenset[str]) -> tuple[int, tuple[str, ...]]:
    """Return count done and ordered missing stage ids."""
    done = sum(1 for s in PROOF_TO_MOAT_STAGES if s in completed_stages)
    missing = tuple(s for s in PROOF_TO_MOAT_STAGES if s not in completed_stages)
    return done, missing


def proof_moat_loop_complete(completed_stages: frozenset[str]) -> bool:
    return all(s in completed_stages for s in PROOF_TO_MOAT_STAGES)
