"""SaaS transition readiness score."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

SaasReadinessBand = Literal["hold", "pilot", "accelerate"]


@dataclass(frozen=True, slots=True)
class SaasTransitionSignals:
    workflow_stable_repeat: bool = False
    client_asks_access: bool = False
    high_manual_delivery_time: bool = False
    internal_module_in_production_use: bool = False
    retainers_need_dashboard: bool = False


_SAAS_WEIGHTS: dict[str, int] = {
    "workflow_stable_repeat": 25,
    "client_asks_access": 20,
    "high_manual_delivery_time": 15,
    "internal_module_in_production_use": 25,
    "retainers_need_dashboard": 15,
}


def compute_saas_transition_score(s: SaasTransitionSignals) -> int:
    d = {
        "workflow_stable_repeat": s.workflow_stable_repeat,
        "client_asks_access": s.client_asks_access,
        "high_manual_delivery_time": s.high_manual_delivery_time,
        "internal_module_in_production_use": s.internal_module_in_production_use,
        "retainers_need_dashboard": s.retainers_need_dashboard,
    }
    if set(d) != set(_SAAS_WEIGHTS):
        raise RuntimeError("SaaS signal keys out of sync with weights")
    return sum(_SAAS_WEIGHTS[k] for k, v in d.items() if v)


def saas_readiness_band(score: int) -> SaasReadinessBand:
    if score < 0 or score > 100:
        raise ValueError(f"score must be 0..100, got {score}")
    if score < 40:
        return "hold"
    if score < 70:
        return "pilot"
    return "accelerate"
