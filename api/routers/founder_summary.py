"""Founder Command Summary — Constitution v2 §39 final piece.

A read-only CEO-grade brief that aggregates every active engagement
into a single decision surface: top revenue opportunity, top delivery
risk, top governance risk, proof to improve, and one thing to stop
today (the daily-CEO-check format from operating_rhythm doctrine).

  GET /api/v1/founder-summary
      → Daily CEO brief across all active engagements.

  GET /api/v1/founder-summary/{engagement_id}
      → Single-engagement brief: pipeline state + blockers + next action.

  GET /api/v1/founder-summary/weekly
      → Weekly operating-meeting agenda template populated with current
      engagement data.

Doctrine bindings:
  * ``operating_rhythm_os.execution_council`` — eight role lenses.
  * ``operating_rhythm_os.weekly_meeting`` — 10-section agenda.
  * ``command_control_os.command_center`` — decision shape.
  * ``operating_manual_os.non_negotiables`` — pre-flight.
"""

from __future__ import annotations

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException

from auto_client_acquisition.operating_manual_os.non_negotiables import (
    NonNegotiableCheck,
    check_action_against_non_negotiables,
)
from auto_client_acquisition.operating_rhythm_os.execution_council import (
    EXECUTION_COUNCIL_ROLES,
)
from auto_client_acquisition.operating_rhythm_os.weekly_meeting import (
    WEEKLY_MEETING_SECTIONS,
)

router = APIRouter(prefix="/api/v1/founder-summary", tags=["founder-summary"])

_RI_STORE_ROOT = Path(
    os.getenv("DEALIX_REVENUE_INTELLIGENCE_STORE_ROOT", "var/revenue_intelligence")
)
_DIAGNOSTIC_STORE_PATH = Path(
    os.getenv("DEALIX_DIAGNOSTIC_STORE", "var/diagnostics.jsonl")
)
_PROOF_PACK_STORE_PATH = Path(
    os.getenv("DEALIX_PROOF_PACK_STORE", "var/proof_packs.jsonl")
)


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def _engagement_state(engagement_id: str) -> dict[str, Any] | None:
    path = _RI_STORE_ROOT / f"{engagement_id}.jsonl"
    events = _read_jsonl(path)
    if not events:
        return None
    state = {
        "imported": False, "scored": False, "drafted": False, "finalized": False,
    }
    summary: dict[str, Any] = {}
    for event in events:
        kind = event.get("type")
        if kind == "import_preview":
            state["imported"] = True
            summary["data_quality"] = event.get("data_quality")
            summary["total_rows"] = event.get("total_rows")
            summary["deduped_rows"] = event.get("deduped_rows")
            summary["pii_flagged_count"] = event.get("pii_flagged_count")
        elif kind == "scored_accounts":
            state["scored"] = True
            top = event.get("top_10") or []
            summary["top_score"] = top[0]["score"] if top else 0
            summary["top_account"] = top[0]["company_name"] if top else None
            summary["scored_count"] = len(top)
        elif kind == "draft_pack":
            state["drafted"] = True
            summary["drafts_count"] = event.get("drafts_count")
            summary["channels"] = event.get("channels")
        elif kind == "finalize":
            state["finalized"] = True
            summary["client_name"] = event.get("client_name")
    return {
        "engagement_id": engagement_id,
        "state": state,
        "last_event_ts": events[-1].get("ts"),
        "summary": summary,
        "events_count": len(events),
    }


def _all_engagements() -> list[dict[str, Any]]:
    if not _RI_STORE_ROOT.exists():
        return []
    out: list[dict[str, Any]] = []
    for path in sorted(_RI_STORE_ROOT.glob("*.jsonl")):
        engagement_id = path.stem
        rec = _engagement_state(engagement_id)
        if rec:
            out.append(rec)
    return out


def _proof_pack_for(engagement_id: str) -> dict[str, Any] | None:
    """Return the latest persisted Proof Pack record for an engagement."""

    rows = _read_jsonl(_PROOF_PACK_STORE_PATH)
    latest: dict[str, Any] | None = None
    for row in rows:
        if row.get("engagement_id") == engagement_id:
            latest = row
    return latest


def _classify_blocker(engagement: dict[str, Any]) -> str:
    """Return the single most pressing blocker keyword for a CEO brief."""

    state = engagement["state"]
    summary = engagement.get("summary", {})
    if not state["imported"]:
        return "needs_import"
    if not state["scored"]:
        return "needs_score"
    quality = (summary.get("data_quality") or {}).get("score", 0)
    if quality < 70:
        return "data_readiness_low"
    if not state["drafted"]:
        return "needs_draft_pack"
    if not state["finalized"]:
        return "needs_finalize"
    return "ready_for_retainer_gate"


def _retainer_signal(engagement_id: str) -> dict[str, Any] | None:
    pack = _proof_pack_for(engagement_id)
    if pack is None:
        return None
    proof_score = pack.get("proof_score", 0)
    tier = pack.get("tier", "unknown")
    return {
        "proof_score": proof_score,
        "tier": tier,
        "retainer_eligible": proof_score >= 80,
    }


@router.get("")
async def daily_brief() -> dict[str, Any]:
    """Daily CEO check — the five-question format from operating_rhythm."""

    # Doctrine pre-flight (no claims, no PII writes, no auto external action).
    check = check_action_against_non_negotiables(
        NonNegotiableCheck(action="render_founder_summary")
    )
    if not check.allowed:
        raise HTTPException(
            status_code=403,
            detail={"non_negotiables_violated": [v.value for v in check.violations]},
        )

    engagements = _all_engagements()
    if not engagements:
        return {
            "headline": "No active engagements yet — go run a Capability Diagnostic.",
            "next_actions": [
                "POST /api/v1/diagnostic/intent — open a paid Diagnostic.",
                "Or POST /api/v1/revenue-intelligence/{eid}/import for a synthetic test.",
            ],
            "engagements": [],
        }

    # Top revenue opportunity = engagement with highest top_score still un-finalized.
    revenue_candidates = [
        e for e in engagements
        if e["summary"].get("top_score", 0) > 0 and not e["state"]["finalized"]
    ]
    top_revenue = max(revenue_candidates, key=lambda e: e["summary"]["top_score"]) if revenue_candidates else None

    # Top delivery risk = engagement with lowest data quality.
    quality_with = [e for e in engagements if (e["summary"].get("data_quality") or {}).get("score")]
    top_risk = min(quality_with, key=lambda e: e["summary"]["data_quality"]["score"]) if quality_with else None

    # Top governance risk = engagement with PII flagged but not yet finalized.
    governance_candidates = [
        e for e in engagements
        if (e["summary"].get("pii_flagged_count") or 0) > 0 and not e["state"]["finalized"]
    ]
    governance_risk = max(
        governance_candidates,
        key=lambda e: e["summary"]["pii_flagged_count"],
    ) if governance_candidates else None

    # Proof to improve = finalized engagement whose Proof Pack score is < 80.
    proof_to_improve: dict[str, Any] | None = None
    for engagement in engagements:
        if engagement["state"]["finalized"]:
            signal = _retainer_signal(engagement["engagement_id"])
            if signal and not signal["retainer_eligible"]:
                proof_to_improve = {**engagement, "retainer_signal": signal}
                break

    # One thing to stop = first engagement requesting forbidden behavior is
    # blocked upstream by the non-negotiables gate, so we surface drift
    # via 'engagements with no finalize after import older than 14 days'.
    now = datetime.now(timezone.utc)
    stale: list[dict[str, Any]] = []
    for e in engagements:
        ts = e.get("last_event_ts")
        if not ts or e["state"]["finalized"]:
            continue
        try:
            age_days = (now - datetime.fromisoformat(ts)).days
        except ValueError:
            continue
        if age_days >= 14:
            stale.append({**e, "stale_days": age_days})
    one_thing_to_stop = max(stale, key=lambda e: e["stale_days"]) if stale else None

    return {
        "generated_at": now.isoformat(),
        "engagement_count": len(engagements),
        "ceo_brief": {
            "top_revenue_opportunity": (
                {
                    "engagement_id": top_revenue["engagement_id"],
                    "top_account": top_revenue["summary"].get("top_account"),
                    "top_score": top_revenue["summary"].get("top_score"),
                    "next_action": (
                        f"POST /api/v1/revenue-intelligence/{top_revenue['engagement_id']}/finalize"
                        if top_revenue["state"]["drafted"]
                        else f"POST /api/v1/revenue-intelligence/{top_revenue['engagement_id']}/draft-pack"
                    ),
                }
                if top_revenue else None
            ),
            "top_delivery_risk": (
                {
                    "engagement_id": top_risk["engagement_id"],
                    "data_quality_score": top_risk["summary"]["data_quality"]["score"],
                    "tier": top_risk["summary"]["data_quality"].get("tier"),
                    "next_action": "Run a Data Readiness Sprint before AI workflow.",
                }
                if top_risk else None
            ),
            "top_governance_risk": (
                {
                    "engagement_id": governance_risk["engagement_id"],
                    "pii_flagged_count": governance_risk["summary"]["pii_flagged_count"],
                    "next_action": "Verify Source Passport allowed_use covers PII handling.",
                }
                if governance_risk else None
            ),
            "proof_to_improve": (
                {
                    "engagement_id": proof_to_improve["engagement_id"],
                    "proof_score": proof_to_improve["retainer_signal"]["proof_score"],
                    "tier": proof_to_improve["retainer_signal"]["tier"],
                    "next_action": (
                        "Strengthen weakest Proof Score component before retainer push."
                    ),
                }
                if proof_to_improve else None
            ),
            "one_thing_to_stop": (
                {
                    "engagement_id": one_thing_to_stop["engagement_id"],
                    "stale_days": one_thing_to_stop["stale_days"],
                    "next_action": (
                        "Decide: finalize Proof Pack, pause, or close with reason."
                    ),
                }
                if one_thing_to_stop else None
            ),
        },
        "execution_council_lenses": [role.value for role in EXECUTION_COUNCIL_ROLES],
        "engagements": engagements,
    }


@router.get("/{engagement_id}")
async def single_engagement_brief(engagement_id: str) -> dict[str, Any]:
    rec = _engagement_state(engagement_id)
    if rec is None:
        raise HTTPException(status_code=404, detail="engagement_not_found")
    rec["retainer_signal"] = _retainer_signal(engagement_id)
    rec["primary_blocker"] = _classify_blocker(rec)
    next_action_map = {
        "needs_import": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/import "
            "with rows + source_passport."
        ),
        "needs_score": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/score "
            "(no body required, uses default sector_priority)."
        ),
        "data_readiness_low": (
            "Run a Data Readiness Sprint or request cleaner client data."
        ),
        "needs_draft_pack": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/draft-pack "
            "with channels=['email','call_script','follow_up_plan']."
        ),
        "needs_finalize": (
            f"POST /api/v1/revenue-intelligence/{engagement_id}/finalize "
            "with client_name to generate Proof Pack v2 scaffold."
        ),
        "ready_for_retainer_gate": (
            f"POST /api/v1/proof-pack/{engagement_id}/retainer-gate "
            "with client_health, workflow_is_recurring, monthly_value_clear, "
            "stakeholder_engaged."
        ),
    }
    rec["next_action"] = next_action_map.get(rec["primary_blocker"], "review")
    return rec


@router.get("/weekly/agenda", response_model=None)
async def weekly_agenda() -> dict[str, Any]:
    """Pre-populated weekly operating-meeting agenda."""

    engagements = _all_engagements()
    finalized = [e for e in engagements if e["state"]["finalized"]]
    revenue_pipeline = [
        {
            "engagement_id": e["engagement_id"],
            "top_account": e["summary"].get("top_account"),
            "top_score": e["summary"].get("top_score"),
        }
        for e in engagements
        if e["state"]["scored"] and not e["state"]["finalized"]
    ]
    proof_packs = [
        {
            "engagement_id": e["engagement_id"],
            "client_name": e["summary"].get("client_name"),
            "retainer_signal": _retainer_signal(e["engagement_id"]),
        }
        for e in finalized
    ]
    governance_risks = [
        {
            "engagement_id": e["engagement_id"],
            "pii_flagged_count": e["summary"].get("pii_flagged_count", 0),
        }
        for e in engagements
        if (e["summary"].get("pii_flagged_count") or 0) > 0
    ]
    return {
        "agenda_sections": [s.value for s in WEEKLY_MEETING_SECTIONS],
        "filled": {
            "revenue_pipeline": revenue_pipeline,
            "active_delivery": [
                e["engagement_id"] for e in engagements if e["state"]["imported"]
            ],
            "proof_packs": proof_packs,
            "governance_risks": governance_risks,
        },
        "mandatory_outputs_reminder": {
            "decisions_count_min": 3,
            "commitments_count_min": 3,
            "one_thing_to_stop_required": True,
        },
        "note": (
            "Operating rhythm rule: a weekly meeting that does not end with "
            "'one thing to stop' is a sign of over-expansion."
        ),
    }
