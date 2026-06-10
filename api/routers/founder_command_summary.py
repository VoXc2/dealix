"""Founder Command Summary API — daily CEO brief, per-engagement blockers, weekly agenda.

Read-only aggregates over in-memory engagement snapshots. Revenue Intelligence
pipeline stages should call ``merge_pipeline_stage`` after each successful step.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.compliance_trust_os.approval_engine import (
    GovernanceDecision,
)
from auto_client_acquisition.founder_command_summary import (
    build_daily_founder_summary,
    build_weekly_operating_agenda,
    classify_engagement_blocker,
    get_snapshot,
    list_snapshots,
)

router = APIRouter(prefix="/api/v1", tags=["founder-summary"])


def _governance_envelope(
    *,
    decision: GovernanceDecision,
    matched_rules: tuple[str, ...] = (),
    risk_level: str = "low",
) -> dict[str, Any]:
    return {
        "governance_decision": decision.value,
        "matched_rules": list(matched_rules),
        "risk_level": risk_level,
    }


@router.get("/founder-summary/weekly/agenda")
async def weekly_operating_agenda() -> dict[str, Any]:
    snaps = list_snapshots()
    agenda = build_weekly_operating_agenda(snaps)
    return {
        **_governance_envelope(decision=GovernanceDecision.ALLOW),
        "agenda": agenda,
    }


@router.get("/founder-summary")
async def daily_founder_summary() -> dict[str, Any]:
    snaps = list_snapshots()
    brief = build_daily_founder_summary(snaps)
    return {
        **_governance_envelope(decision=GovernanceDecision.ALLOW),
        "brief": brief,
    }


@router.get("/founder-summary/{engagement_id}")
async def founder_summary_per_engagement(engagement_id: str) -> dict[str, Any]:
    snap = get_snapshot(engagement_id)
    if snap is None:
        raise HTTPException(
            status_code=404,
            detail={"ar": "المشروع غير معروف", "en": "Unknown engagement"},
        )
    cat, next_ar, next_en, detail = classify_engagement_blocker(snap)
    gd = GovernanceDecision.ALLOW if cat == "none" else GovernanceDecision.ALLOW_WITH_REVIEW
    rules = () if cat == "none" else (f"engagement_blocker:{cat}",)
    return {
        **_governance_envelope(
            decision=gd,
            matched_rules=rules,
            risk_level="medium" if cat != "none" else "low",
        ),
        "engagement_id": engagement_id,
        "blocker_category": cat,
        "next_action": {"ar": next_ar, "en": next_en},
        "detail": detail,
        "snapshot": snap.to_public_dict(),
    }
