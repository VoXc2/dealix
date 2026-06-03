"""Outcome / usage pricing simulation (Wave 3 economics)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

_SKU_BANDS: dict[str, dict[str, Any]] = {
    "governed_diagnostic": {
        "phase": 1,
        "fixed_sar_min": 4999,
        "fixed_sar_max": 15000,
        "proof_packs_required": 0,
    },
    "revenue_sprint": {
        "phase": 1,
        "fixed_sar": 499,
        "proof_packs_required": 0,
    },
    "data_pack": {
        "phase": 1,
        "fixed_sar": 1500,
        "proof_packs_required": 0,
    },
    "growth_ops": {
        "phase": 1,
        "fixed_sar_monthly": 2999,
        "proof_packs_required": 1,
        "retainer_eligible": True,
    },
    "executive_command_center": {
        "phase": 3,
        "fixed_sar_monthly": 7500,
        "proof_packs_required": 3,
        "enterprise_gate": True,
    },
}


@dataclass(frozen=True)
class PricingOutcomeInput:
    sku: str
    proof_packs_delivered: int = 0
    agent_actions_monthly: int = 0
    measured_roi_sar: float = 0.0


def simulate_pricing_outcome(inp: PricingOutcomeInput) -> dict[str, Any]:
    band = _SKU_BANDS.get(inp.sku)
    if not band:
        return {"ok": False, "error": f"unknown sku: {inp.sku}"}

    phase = int(band.get("phase", 1))
    required_proofs = int(band.get("proof_packs_required", 0))
    proofs_ok = inp.proof_packs_delivered >= required_proofs

    recommendation = "fixed"
    if phase >= 2 and inp.agent_actions_monthly > 500:
        recommendation = "usage_credits"
    if phase >= 3 and inp.measured_roi_sar > 0 and proofs_ok:
        recommendation = "outcome_linked"

    base_sar = float(
        band.get("fixed_sar")
        or band.get("fixed_sar_min")
        or band.get("fixed_sar_monthly")
        or 0
    )
    uplift = min(0.15, 0.03 * inp.proof_packs_delivered)
    total_estimated_sar = base_sar * (1.0 + uplift) if base_sar else 0.0

    return {
        "ok": True,
        "sku": inp.sku,
        "phase": phase,
        "proofs_ok": proofs_ok,
        "recommendation": recommendation,
        "band": band,
        "base_sar": base_sar,
        "total_estimated_sar": total_estimated_sar,
        "inputs": {
            "proof_packs_delivered": inp.proof_packs_delivered,
            "agent_actions_monthly": inp.agent_actions_monthly,
            "measured_roi_sar": inp.measured_roi_sar,
        },
    }
