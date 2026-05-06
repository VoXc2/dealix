"""Warm route suggestion — human-approved paths only."""
from __future__ import annotations


def primary_warm_route(fit_score: int) -> dict[str, Any]:
    route = "warm_intro" if fit_score >= 70 else "partner_intro"
    return {
        "schema_version": 1,
        "primary_route": route,
        "allowed": ["inbound", "warm_intro", "partner_intro", "manual_email"],
        "forbidden": ["cold_whatsapp", "scraping", "linkedin_auto_dm"],
        "action_mode": "approval_required",
    }
