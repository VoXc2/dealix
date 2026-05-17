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


@router.get("/founder-summary/command-center")
async def founder_command_center() -> dict[str, Any]:
    """Founder Command Center — today's focus, qualified leads, pending
    approvals, and the doctrine no-build warning.

    Real aggregates only: counts come from durable stores (the lead inbox
    and the approval gate). Nothing is fabricated — an empty system returns
    zeros, not invented numbers.
    """
    from auto_client_acquisition import lead_inbox

    all_records = lead_inbox.list_leads(limit=2000)
    # Status changes are appended as separate audit lines — fold the latest
    # status back onto each lead so "converted" leads are detectable.
    latest_status: dict[str, str] = {}
    for rec in reversed(all_records):  # list_leads is newest-first
        if rec.get("event") == "status_change":
            lid = str(rec.get("lead_id") or "")
            if lid:
                latest_status[lid] = str(rec.get("status") or "")

    leads = [r for r in all_records if r.get("event") != "status_change"]

    def _status(rec: dict[str, Any]) -> str:
        return latest_status.get(str(rec.get("id") or ""), rec.get("status", "new"))

    qualified = [r for r in leads if r.get("risk_bucket") in ("high", "medium")]
    high = [r for r in leads if r.get("risk_bucket") == "high"]
    blocked = [r for r in leads if r.get("risk_bucket") == "blocked"]
    new_leads = [r for r in leads if _status(r) == "new"]
    converted = [r for r in leads if _status(r) == "converted"]

    pending_approvals = 0
    try:
        from api.deps import get_approval_gate

        gate = await get_approval_gate()
        pending_approvals = len(await gate.list_pending(limit=200))
    except Exception:  # noqa: BLE001 — degrade to a real zero, never fabricate
        pending_approvals = 0

    # Top 3 actions — deterministic, derived strictly from real state.
    top_actions: list[dict[str, str]] = []
    if pending_approvals:
        top_actions.append({
            "ar": f"راجِع {pending_approvals} طلب موافقة معلّق.",
            "en": f"Review {pending_approvals} pending approval(s).",
        })
    if high:
        lead = high[0]
        label = str(lead.get("company") or lead.get("name") or "—")
        top_actions.append({
            "ar": f"تابِع أعلى عميل محتمل: {label}.",
            "en": f"Follow up with top qualified lead: {label}.",
        })
    if blocked:
        top_actions.append({
            "ar": f"راجِع {len(blocked)} طلبًا محظورًا (مخالفة دكترين).",
            "en": f"Review {len(blocked)} blocked request(s) (doctrine violation).",
        })
    if not leads:
        top_actions.append({
            "ar": "لا عملاء محتملون بعد — وجّه الزيارات إلى صفحة التشخيص /dealix-diagnostic.",
            "en": "No leads yet — drive traffic to the /dealix-diagnostic page.",
        })
    if not top_actions:
        top_actions.append({
            "ar": "راجِع العملاء المحتملين الجدد وحرّك المسار.",
            "en": "Review new leads and advance the pipeline.",
        })
    top_actions = top_actions[:3]

    # No-build warning maps to doctrine L6 (Focus Law) / L7 (Kill Law):
    # do not build new features before there is paid proof of demand.
    no_build_active = len(converted) == 0
    no_build_warning = {
        "active": no_build_active,
        "reason_ar": (
            "لا فاتورة مدفوعة بعد — لا تبنِ ميزات جديدة قبل إثبات الطلب "
            "المدفوع (دكترين L6/L7)."
            if no_build_active
            else "يوجد عميل مدفوع — البناء مسموح ضمن نطاق محكوم."
        ),
        "reason_en": (
            "No paid invoice yet — do not build new features before paid "
            "proof of demand (Doctrine L6/L7)."
            if no_build_active
            else "A paid customer exists — scoped building is permitted."
        ),
    }

    return {
        **_governance_envelope(decision=GovernanceDecision.ALLOW),
        "command_center": {
            "top_actions": top_actions,
            "new_qualified_leads": {
                "count": len(qualified),
                "items": [
                    {
                        "id": r.get("id"),
                        "company": r.get("company"),
                        "name": r.get("name"),
                        "bucket": r.get("risk_bucket"),
                        "fit_score": r.get("fit_score"),
                        "sector": r.get("sector"),
                        "received_at": r.get("received_at"),
                    }
                    for r in qualified[:8]
                ],
            },
            "new_leads_count": len(new_leads),
            "pending_approvals": {"count": pending_approvals},
            "payments_pending": {"count": 0, "note": "wire_to_payment_ops"},
            "proof_packs_in_progress": {"count": 0, "note": "wire_to_proof_os"},
            "blocked_actions": {
                "count": len(blocked),
                "items": [
                    {
                        "id": r.get("id"),
                        "company": r.get("company"),
                        "reasons": r.get("doctrine_violations", []),
                    }
                    for r in blocked[:8]
                ],
            },
            "no_build_warning": no_build_warning,
        },
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
