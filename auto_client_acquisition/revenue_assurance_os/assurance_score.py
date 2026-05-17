"""Revenue Assurance Score — 7-category readiness aggregate (0-100).

Distinct from ``full_ops_radar`` (which measures infra layers). This score
answers: is the revenue machine assured enough to scale?

Categories (weights sum = 100):
  Sales Readiness       20
  Marketing Readiness   15
  Support Readiness     15
  Partner Readiness     15
  Governance Readiness  20
  Delivery Readiness    10
  Reporting Readiness    5

Each category is scored from a live signal (0.0-1.0 ratio passed by the
caller) when available, otherwise from module presence. Missing data scores
0 with a ``no_fake_green`` note — never silently inflated.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Literal

from auto_client_acquisition.integration_upgrade import safe_import

CATEGORY_WEIGHTS: dict[str, int] = {
    "sales_readiness": 20,
    "marketing_readiness": 15,
    "support_readiness": 15,
    "partner_readiness": 15,
    "governance_readiness": 20,
    "delivery_readiness": 10,
    "reporting_readiness": 5,
}

# Module probed per category when no live signal is supplied.
_CATEGORY_MODULE: dict[str, str] = {
    "sales_readiness": "auto_client_acquisition.sales_os",
    "marketing_readiness": "auto_client_acquisition.gtm_os",
    "support_readiness": "auto_client_acquisition.support_inbox",
    "partner_readiness": "auto_client_acquisition.partner_os",
    "governance_readiness": "auto_client_acquisition.governance_os",
    "delivery_readiness": "auto_client_acquisition.proof_os",
    "reporting_readiness": "auto_client_acquisition.executive_pack_v2",
}

ReadinessLabel = Literal[
    "Assured",
    "Customer-Ready with Manual Ops",
    "Diagnostic Only",
    "Internal Only",
]


@dataclass(frozen=True, slots=True)
class CategoryScore:
    category: str
    max_weight: int
    achieved: int
    available: bool
    note: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def readiness_label(score: int | float) -> ReadinessLabel:
    if score >= 90:
        return "Assured"
    if score >= 75:
        return "Customer-Ready with Manual Ops"
    if score >= 60:
        return "Diagnostic Only"
    return "Internal Only"


def _score_category(category: str, signal: float | None) -> CategoryScore:
    weight = CATEGORY_WEIGHTS[category]
    if signal is not None:
        ratio = max(0.0, min(1.0, float(signal)))
        achieved = round(ratio * weight)
        return CategoryScore(category, weight, achieved, True, "live_signal")
    module = _CATEGORY_MODULE[category]
    present = safe_import(module) is not None
    if present:
        return CategoryScore(category, weight, weight, True, "module_present_no_live_signal")
    return CategoryScore(category, weight, 0, False, "no_fake_green:module_missing")


def compute_assurance_score(signals: dict[str, float] | None = None) -> dict[str, Any]:
    """Aggregate the 7-category Revenue Assurance Score.

    ``signals`` maps a category key to a 0.0-1.0 readiness ratio. Categories
    absent from ``signals`` fall back to module presence. Never raises.
    """
    signals = signals or {}
    breakdown: list[dict[str, Any]] = []
    total = 0
    max_total = 0
    for category in CATEGORY_WEIGHTS:
        cat = _score_category(category, signals.get(category))
        breakdown.append(cat.to_dict())
        total += cat.achieved
        max_total += cat.max_weight
    return {
        "score": total,
        "max_score": max_total,
        "percentage": round((total / max_total * 100) if max_total else 0.0, 1),
        "readiness_label": readiness_label(total),
        "breakdown": breakdown,
        "weights_table": dict(CATEGORY_WEIGHTS),
        "safety_summary": "no_fake_green:categories_scored_from_live_signal_or_module_presence",
    }


__all__ = [
    "CATEGORY_WEIGHTS",
    "CategoryScore",
    "ReadinessLabel",
    "compute_assurance_score",
    "readiness_label",
]
