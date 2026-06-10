"""Next action suggestion for one LeadOpsRecord.

Emits a single concrete next step the founder/CSM should take, with
owner and deadline. Reads from compliance_status + score + offer_route.

Never auto-executes — pure suggestion.
"""
from __future__ import annotations

from datetime import UTC, datetime, timedelta, timezone
from typing import Any


def suggest_next_action(
    *,
    compliance_status: str,
    score: dict[str, Any] | None,
    offer_route: dict[str, Any] | None,
) -> dict[str, Any]:
    """Return {'action', 'owner', 'deadline_iso', 'reason'}."""
    score = score or {}
    offer_route = offer_route or {}
    fit = float(score.get("fit", 0))

    now = datetime.now(UTC)

    if compliance_status == "blocked":
        return {
            "action": "do_nothing_archive",
            "owner": "system",
            "deadline_iso": now.isoformat(),
            "reason": "compliance_blocked",
        }

    if compliance_status == "needs_review":
        return {
            "action": "founder_review_compliance",
            "owner": "founder",
            "deadline_iso": (now + timedelta(hours=24)).isoformat(),
            "reason": "compliance_needs_review",
        }

    if fit >= 0.8:
        return {
            "action": f"send_warm_outreach_via_{offer_route.get('channel', 'dashboard')}",
            "owner": "founder",
            "deadline_iso": (now + timedelta(hours=4)).isoformat(),
            "reason": "high_fit_score",
        }

    if fit >= 0.5:
        return {
            "action": "draft_qualification_followup",
            "owner": "csm_or_founder",
            "deadline_iso": (now + timedelta(hours=24)).isoformat(),
            "reason": "medium_fit_score",
        }

    return {
        "action": "nurture_low_fit_quarterly",
        "owner": "system",
        "deadline_iso": (now + timedelta(days=90)).isoformat(),
        "reason": "low_fit_score",
    }
