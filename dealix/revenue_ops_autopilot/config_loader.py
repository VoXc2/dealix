"""Load dealix/config YAML policies with in-code fallbacks."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parents[2]
_CONFIG = _REPO / "dealix" / "config"


@lru_cache(maxsize=16)
def _load_yaml(name: str) -> dict[str, Any]:
    path = _CONFIG / name
    if not path.is_file():
        return {}
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
        return raw if isinstance(raw, dict) else {}
    except (OSError, yaml.YAMLError):
        return {}


def lead_scoring_config() -> dict[str, Any]:
    return _load_yaml("lead_scoring.yaml")


def stage_transitions_config() -> dict[str, Any]:
    return _load_yaml("stage_transitions.yaml")


def icp_agency_wedge_config() -> dict[str, Any]:
    return _load_yaml("icp_agency_wedge.yaml")


def approval_policy_config() -> dict[str, Any]:
    return _load_yaml("approval_policy.yaml")


def routing_thresholds() -> dict[str, int]:
    cfg = lead_scoring_config().get("routing_thresholds") or {}
    return {
        "qualified_a_min": int(cfg.get("qualified_a_min", 15)),
        "qualified_b_min": int(cfg.get("qualified_b_min", 10)),
        "nurture_min": int(cfg.get("nurture_min", 6)),
    }


def allowed_stage_edges() -> dict[str, list[str]]:
    cfg = stage_transitions_config().get("allowed_transitions") or {}
    return {str(k): list(v) if isinstance(v, list) else [] for k, v in cfg.items()}


def wedge_message_for_segment(segment: str) -> str:
    cfg = icp_agency_wedge_config()
    wedges = cfg.get("wedges") or cfg.get("segments") or {}
    if isinstance(wedges, dict):
        hit = wedges.get(segment) or wedges.get("agency_wedge")
        if isinstance(hit, dict):
            return str(hit.get("message_ar") or hit.get("angle_ar") or "")
        if isinstance(hit, str):
            return hit
    angles = cfg.get("message_angles_ar") or []
    if isinstance(angles, list) and angles:
        return str(angles[0])
    return ""
