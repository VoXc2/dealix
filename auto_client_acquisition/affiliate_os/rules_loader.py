"""Affiliate OS — config loader for affiliate_rules.yaml.

Mirrors governance_os/policy_registry.py: an lru_cache'd yaml.safe_load with
a defensive fallback when the file is missing or malformed.
"""

from __future__ import annotations

import os
from functools import lru_cache
from typing import Any

import yaml

_DEFAULT_RATE = 0.10


def _rules_path() -> str:
    return os.path.join(os.path.dirname(__file__), "config", "affiliate_rules.yaml")


@lru_cache(maxsize=1)
def load_affiliate_rules() -> dict[str, Any]:
    path = _rules_path()
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        data = None
    if not isinstance(data, dict):
        return {"version": 0, "commission_tiers": {}, "forbidden_claims": []}
    return data


def commission_tiers() -> dict[str, Any]:
    raw = load_affiliate_rules().get("commission_tiers", {})
    return raw if isinstance(raw, dict) else {}


def tier_for_score(score: int) -> str:
    """Highest tier whose min_fit_score the affiliate clears. Defaults to
    'standard' so an unknown/empty config never produces a tier-less affiliate."""
    best_tier = "standard"
    best_floor = -1
    for name, spec in commission_tiers().items():
        if not isinstance(spec, dict):
            continue
        floor = int(spec.get("min_fit_score", 0))
        if score >= floor and floor > best_floor:
            best_tier, best_floor = str(name), floor
    return best_tier


def commission_rate_for_tier(tier: str) -> float:
    spec = commission_tiers().get(tier)
    if isinstance(spec, dict) and "rate" in spec:
        return float(spec["rate"])
    return _DEFAULT_RATE


def forbidden_claims() -> list[str]:
    raw = load_affiliate_rules().get("forbidden_claims", [])
    return [str(x).lower() for x in raw] if isinstance(raw, list) else []


def disclosure_text(locale: str = "en") -> str:
    raw = load_affiliate_rules().get("disclosure_text", {})
    if isinstance(raw, dict):
        return str(raw.get(locale) or raw.get("en") or "").strip()
    return ""


def payout_rules() -> dict[str, Any]:
    raw = load_affiliate_rules().get("payout", {})
    return raw if isinstance(raw, dict) else {}


def min_payout_sar() -> int:
    return int(payout_rules().get("min_payout_sar", 0))


__all__ = [
    "commission_rate_for_tier",
    "commission_tiers",
    "disclosure_text",
    "forbidden_claims",
    "load_affiliate_rules",
    "min_payout_sar",
    "payout_rules",
    "tier_for_score",
]
