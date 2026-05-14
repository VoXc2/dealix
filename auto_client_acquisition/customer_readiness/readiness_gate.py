"""Per-customer readiness gate — pure computation, no I/O.

Distinct from `scores.py` (which computes Comfort + Expansion).
This module produces the **PROCEED / HOLD_FOR_SCOPE / HOLD_FOR_GOVERNANCE**
gate that fronts a sales conversation: "is it safe AND useful for us to
sell this buyer the next rung today?"

The public projection (`public_projection`) deliberately omits numeric
counts and internal rationale codes — see
`api/routers/customer_readiness.py` for the safety contract.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class CustomerReadinessGate:
    """Full breakdown — admin-gated only."""

    handle: str
    source_passport_status: str   # "present" | "missing" | "unknown"
    governance_decisions_7d: int
    proof_pack_count: int
    capital_asset_count: int
    has_signed_scope: bool
    recommendation: str           # "PROCEED" | "HOLD_FOR_SCOPE" | "HOLD_FOR_GOVERNANCE"
    rationale: tuple[str, ...]


THRESHOLD_DECISIONS_OK = 5
THRESHOLD_PROOF_OK = 1


def compute_readiness_gate(
    *,
    handle: str,
    source_passport_status: str,
    governance_decisions_7d: int,
    proof_pack_count: int,
    capital_asset_count: int,
    has_signed_scope: bool,
) -> CustomerReadinessGate:
    """Pure computation. Inputs come from the calling layer; no I/O here."""
    rationale: list[str] = []

    if source_passport_status not in ("present", "missing", "unknown"):
        source_passport_status = "unknown"

    if source_passport_status != "present":
        rationale.append("source_passport_not_present")
    if governance_decisions_7d < THRESHOLD_DECISIONS_OK:
        rationale.append(f"governance_decisions_7d_lt_{THRESHOLD_DECISIONS_OK}")
    if proof_pack_count < THRESHOLD_PROOF_OK:
        rationale.append("no_proof_pack_yet")
    if not has_signed_scope:
        rationale.append("scope_not_signed")

    # Hierarchy of recommendations: governance > scope > proceed.
    if (
        source_passport_status != "present"
        or governance_decisions_7d < THRESHOLD_DECISIONS_OK
    ):
        recommendation = "HOLD_FOR_GOVERNANCE"
    elif not has_signed_scope:
        recommendation = "HOLD_FOR_SCOPE"
    else:
        recommendation = "PROCEED"

    return CustomerReadinessGate(
        handle=handle,
        source_passport_status=source_passport_status,
        governance_decisions_7d=governance_decisions_7d,
        proof_pack_count=proof_pack_count,
        capital_asset_count=capital_asset_count,
        has_signed_scope=has_signed_scope,
        recommendation=recommendation,
        rationale=tuple(rationale),
    )


# Public projection — MUST NOT include numeric counts, internal flags,
# or rationale codes. Only the recommendation + as_of + a doctrine
# statement pointing at the public verifier.
def public_projection(r: CustomerReadinessGate, as_of: str) -> dict[str, Any]:
    return {
        "handle": r.handle,
        "recommendation": r.recommendation,
        "as_of": as_of,
        "doctrine": (
            "PROCEED is awarded only when Source Passport is present, "
            "Governance Runtime is exercising the account, and a signed "
            "scope exists. See /api/v1/dealix-promise."
        ),
    }


__all__ = [
    "CustomerReadinessGate",
    "compute_readiness_gate",
    "public_projection",
    "THRESHOLD_DECISIONS_OK",
    "THRESHOLD_PROOF_OK",
]
