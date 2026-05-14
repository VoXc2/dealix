"""Service Readiness Score (0–100) — deterministic weights for commercial services."""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import yaml

# Weights sum to 100 (aligned with docs/company/CAPABILITY_VERIFICATION_AR.md).
WEIGHTS: dict[str, int] = {
    "has_offer_page": 10,
    "has_intake": 10,
    "has_scope_template": 10,
    "has_module_support": 15,
    "has_report_template": 10,
    "has_qa_checklist": 15,
    "has_demo": 10,
    "has_compliance_checks": 10,
    "has_upsell_path": 10,
}


def _yaml_path() -> str:
    base = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(base, "governance_os", "policies", "service_readiness_defaults.yaml")


@lru_cache(maxsize=1)
def _load_defaults_file() -> dict[str, Any]:
    path = _yaml_path()
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def default_evidence_for(service_id: str) -> dict[str, bool]:
    """Baseline evidence from packaged YAML (maintained with repo)."""
    blob = _load_defaults_file()
    raw = (blob.get("services") or {}).get(service_id, {})
    out: dict[str, bool] = {}
    for k in WEIGHTS:
        out[k] = bool(raw.get(k, False))
    return out


def merge_evidence(
    service_id: str,
    overrides: dict[str, bool] | None,
) -> dict[str, bool]:
    base = default_evidence_for(service_id)
    if overrides:
        for k, v in overrides.items():
            if k in WEIGHTS:
                base[k] = bool(v)
    return base


def compute_service_readiness_score(
    service_id: str,
    *,
    evidence_overrides: dict[str, bool] | None = None,
) -> dict[str, Any]:
    """Return total score 0–100, per-criterion breakdown, and sellability hint."""
    ev = merge_evidence(service_id, evidence_overrides)
    breakdown: dict[str, dict[str, Any]] = {}
    total = 0
    for key, weight in WEIGHTS.items():
        earned = weight if ev.get(key) else 0
        total += earned
        breakdown[key] = {"weight": weight, "met": bool(ev.get(key)), "earned": earned}

    return {
        "service_id": service_id,
        "score": total,
        "max_score": 100,
        "breakdown": breakdown,
        "sellable_officially": total >= 80,
        "sellable_beta_only": total < 80,
        "weights_version": "1",
    }
