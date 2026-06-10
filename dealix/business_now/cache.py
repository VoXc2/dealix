"""Persisted verdict cache for fast Business NOW API reads."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

_REPO = Path(__file__).resolve().parents[2]
CACHE_PATH = _REPO / "dealix" / "transformation" / "business_now_cache.yaml"


def load_cache() -> dict[str, Any] | None:
    if not CACHE_PATH.exists():
        return None
    try:
        data = yaml.safe_load(CACHE_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def write_cache(
    *,
    transformation_verdict: str,
    enterprise_control_plane_verdict: str,
    governed_domains: int,
    generated_at: str | None = None,
) -> None:
    payload = {
        "generated_at": generated_at or datetime.now(UTC).isoformat(),
        "transformation_verdict": transformation_verdict,
        "enterprise_control_plane_verdict": enterprise_control_plane_verdict,
        "governed_domains": governed_domains,
        "verdict_source": "generator",
    }
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )


def apply_cache_to_platform(platform: dict[str, Any]) -> dict[str, Any]:
    """Overlay cached verdicts when live verify was skipped."""
    cached = load_cache()
    if not cached:
        platform["verdict_source"] = "none"
        platform["notes_ar"] = (
            "شغّل bash scripts/run_business_now.sh لتحديث أحكام التحقق من المستودع."
        )
        return platform

    platform["transformation_verdict"] = cached.get(
        "transformation_verdict", platform.get("transformation_verdict")
    )
    platform["enterprise_control_plane_verdict"] = cached.get(
        "enterprise_control_plane_verdict", "UNKNOWN"
    )
    if cached.get("governed_domains") is not None:
        platform["governed_domains"] = cached["governed_domains"]
    platform["verdict_source"] = cached.get("verdict_source", "cache")
    platform["cache_generated_at"] = cached.get("generated_at")
    return platform
