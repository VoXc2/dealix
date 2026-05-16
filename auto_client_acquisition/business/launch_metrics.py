"""North-star and supporting metrics definitions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

_MANIFEST_PATH = Path(__file__).resolve().parents[2] / "dealix" / "transformation" / "north_star_manifest.yaml"


def _load_manifest_bridge() -> dict[str, str]:
    if not _MANIFEST_PATH.exists():
        return {}
    data = yaml.safe_load(_MANIFEST_PATH.read_text(encoding="utf-8")) or {}
    bridge = data.get("launch_metrics_bridge") or {}
    return {k: str(v) for k, v in bridge.items() if v}


def north_star_metrics() -> dict[str, Any]:
    bridge = _load_manifest_bridge()
    if bridge:
        return {
            "primary": bridge.get("primary", "measured_customer_value_sar"),
            "secondary": bridge.get("secondary", "governance_integrity_rate"),
            "guardrail": bridge.get("guardrail", "blocked_high_risk_outreach_count"),
            "manifest": "dealix/transformation/north_star_manifest.yaml",
        }
    return {
        "primary": "weekly_qualified_opportunities_accepted_or_drafted",
        "secondary": "meetings_booked_post_approval",
        "guardrail": "blocked_high_risk_outreach_count",
    }


def activation_metrics() -> dict[str, Any]:
    return {
        "time_to_first_brief_view_minutes": "target < 15",
        "time_to_first_opportunity_review": "target < 1 day",
        "first_approved_draft_hours": "target < 72h from signup",
    }


def retention_metrics() -> dict[str, Any]:
    return {
        "weekly_active_brief": "WAU brief opens",
        "proof_pack_open_rate": "target > 60%",
        "expansion_trigger": "multi-seat or performance addon attach",
    }


def revenue_metrics() -> dict[str, Any]:
    return {
        "mrr": "subscriptions + recurring performance (contracted)",
        "nrr": "expansion minus churn",
        "pipeline_influenced_sar": "attributed opportunities tracked in revenue memory",
    }


def ai_quality_metrics() -> dict[str, Any]:
    return {
        "approval_rate": "drafts approved / drafts proposed",
        "blocked_action_rate": "guardrail stops / risky attempts",
        "arabic_tone_checks": "sampled human review weekly",
        "hallucination_checks": "grounding to project chunks + radar evidence",
    }
