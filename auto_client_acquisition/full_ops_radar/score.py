"""Full-Ops Score — 10-weight aggregate over health_checks.

Weights (sum = 100):
  LeadOps                15
  Customer Brain         10
  Service Sessions       10
  Approval Center        10
  Payment Ops            10
  Support                10
  Proof Ledger           10
  Customer Portal        10
  Executive Dashboard    10
  Safety / Compliance     5

Readiness labels:
  90-100 = Full Ops Ready
  75-89  = Customer Ready with Manual Ops
  60-74  = Diagnostic Only
  <60    = Internal Only
"""
from __future__ import annotations

from typing import Any, Literal

from auto_client_acquisition.full_ops_radar.health_checks import (
    run_all_health_checks,
)

ReadinessLabel = Literal[
    "Full Ops Ready",
    "Customer Ready with Manual Ops",
    "Diagnostic Only",
    "Internal Only",
]

SCORE_WEIGHTS: dict[str, int] = {
    "leadops": 15,
    "customer_brain": 10,
    "service_sessions": 10,
    "approval_center": 10,
    "payment_ops": 10,
    "support": 10,
    "proof_ledger": 10,
    "customer_portal": 10,
    "executive_dashboard": 10,
    "safety_compliance": 5,
}


def readiness_label(score: int | float) -> ReadinessLabel:
    if score >= 90:
        return "Full Ops Ready"
    if score >= 75:
        return "Customer Ready with Manual Ops"
    if score >= 60:
        return "Diagnostic Only"
    return "Internal Only"


def compute_full_ops_score() -> dict[str, Any]:
    """Returns score + breakdown + readiness label.

    Score = sum of (weight if available else 0) for each layer.
    Always a dict; never raises.
    """
    checks = run_all_health_checks()
    breakdown: list[dict[str, Any]] = []
    total = 0
    max_total = 0
    for c in checks:
        layer = c["layer"]
        weight = SCORE_WEIGHTS.get(layer, 0)
        max_total += weight
        achieved = weight if c["available"] else 0
        total += achieved
        breakdown.append({
            "layer": layer,
            "available": c["available"],
            "max_weight": weight,
            "achieved": achieved,
        })

    label = readiness_label(total)
    return {
        "score": total,
        "max_score": max_total,
        "percentage": round((total / max_total * 100) if max_total else 0.0, 1),
        "readiness_label": label,
        "breakdown": breakdown,
        "weights_table": SCORE_WEIGHTS,
        "safety_summary": "no_fake_green_each_layer_verified_via_health_check",
    }
