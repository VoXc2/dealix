"""Governed Revenue Intelligence HTTP surface (MVP — deterministic, no live sends).

Stages update ``merge_pipeline_stage`` for Founder Command Summary aggregation.
"""

from __future__ import annotations

import threading
from typing import Any

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.data_os.data_quality_score import (
    duplicate_ratio_by_field,
    mean_completeness,
)
from auto_client_acquisition.founder_command_summary.engagement_registry import merge_pipeline_stage
from auto_client_acquisition.revenue_os.dedupe import suggest_dedupe_fingerprint
from auto_client_acquisition.revenue_os.draft_pack import build_revenue_draft_pack
from auto_client_acquisition.revenue_os.scoring import score_account_row

router = APIRouter(prefix="/api/v1/revenue-intelligence", tags=["revenue-intelligence"])

_LOCK = threading.Lock()
_STATE: dict[str, dict[str, Any]] = {}


def clear_revenue_intelligence_state_for_tests() -> None:
    with _LOCK:
        _STATE.clear()


def _gov(decision: GovernanceDecision, *, rules: tuple[str, ...] = ()) -> dict[str, Any]:
    return {
        "governance_decision": decision.value,
        "matched_rules": list(rules),
        "risk_level": "low" if decision == GovernanceDecision.ALLOW else "medium",
    }


def _eng(eid: str) -> dict[str, Any]:
    with _LOCK:
        if eid not in _STATE:
            _STATE[eid] = {
                "accounts": [],
                "scored": [],
                "passport": {},
                "draft_pack": {},
                "proof_narrative": {},
            }
        return _STATE[eid]


def _passport_min5(p: dict[str, Any]) -> tuple[bool, tuple[str, ...]]:
    required = ("source_id", "owner", "allowed_use", "contains_pii", "relationship_status")
    missing = tuple(k for k in required if p.get(k) in (None, "", []))
    return not missing, missing


class ImportBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    client_label: str | None = Field(default=None, max_length=200)
    source_passport: dict[str, Any] = Field(default_factory=dict)
    accounts: list[dict[str, Any]] = Field(default_factory=list)


@router.post("/{engagement_id}/import")
def ri_import(engagement_id: str, body: ImportBody = Body(...)) -> dict[str, Any]:
    ok, missing = _passport_min5(body.source_passport)
    if not ok:
        raise HTTPException(status_code=422, detail={"ar": "جواز مصدر ناقص", "en": "Incomplete source passport", "missing": list(missing)})
    rows = body.accounts
    if not rows:
        raise HTTPException(status_code=422, detail={"ar": "لا توجد حسابات", "en": "accounts required"})
    req_keys = ("company_name", "sector", "city", "source")
    mc = mean_completeness(rows, req_keys)
    dup = duplicate_ratio_by_field(rows, "company_name")
    dq = round(100.0 * (0.6 * mc + 0.4 * (1.0 - dup)), 2)
    pii_any = bool(body.source_passport.get("contains_pii")) or any(
        str(r.get("phone") or "").strip() for r in rows
    )
    hints = [
        suggest_dedupe_fingerprint(
            company_name=str(r.get("company_name") or "unknown"),
            domain=r.get("domain"),
            phone=r.get("phone"),
            email=r.get("email"),
        ).fingerprint_key
        for r in rows[:200]
    ]
    tier = "blocked" if dq < 40 else ("weak" if dq < 65 else ("good" if dq < 85 else "strong"))
    snap = merge_pipeline_stage(
        engagement_id,
        client_label=body.client_label,
        import_done=True,
        data_quality_score=dq,
        pii_flagged=pii_any,
        pipeline_context_update={
            "import_row_count": len(rows),
            "readiness_tier": tier,
            "dedupe_fingerprints_sample": hints[:5],
        },
    )
    st = _eng(engagement_id)
    st["accounts"] = rows
    st["passport"] = dict(body.source_passport)
    return {
        **_gov(GovernanceDecision.ALLOW),
        "engagement_id": engagement_id,
        "data_quality_score": dq,
        "mean_completeness": mc,
        "duplicate_ratio_company_name": dup,
        "readiness_tier": tier,
        "pii_flagged": pii_any,
        "founder_snapshot": snap.to_public_dict(),
    }


@router.post("/{engagement_id}/score")
def ri_score(engagement_id: str) -> dict[str, Any]:
    st = _eng(engagement_id)
    rows = st.get("accounts") or []
    if not rows:
        raise HTTPException(status_code=400, detail={"ar": "شغّل import أولًا", "en": "Run import first"})
    icp_sectors = frozenset({"technology", "services", "consulting", "training", "real_estate_services"})
    icp_cities = frozenset({"riyadh", "jeddah", "dammam", "khobar", "dhahran"})
    scored: list[dict[str, Any]] = []
    for r in rows:
        out = score_account_row(dict(r), icp_sectors=icp_sectors, icp_cities=icp_cities)
        scored.append({"row": r, **out})
    scored.sort(key=lambda x: x["score"], reverse=True)
    top = scored[:10]
    summary = ", ".join(str(x["row"].get("company_name") or "?") for x in top[:3])
    snap = merge_pipeline_stage(
        engagement_id,
        score_done=True,
        top_opportunity_summary=summary or None,
        pipeline_context_update={"top_10": [{"company": t["row"].get("company_name"), "score": t["score"]} for t in top]},
    )
    st["scored"] = scored
    return {
        **_gov(GovernanceDecision.ALLOW),
        "engagement_id": engagement_id,
        "ranked_accounts": top,
        "founder_snapshot": snap.to_public_dict(),
    }


class DraftPackBody(BaseModel):
    model_config = ConfigDict(extra="forbid")

    request_cold_whatsapp: bool = False
    request_linkedin_automation: bool = False
    request_scraping: bool = False
    request_bulk_outreach: bool = False
    include_whatsapp_draft: bool = False
    relationship_status: str = ""


@router.post("/{engagement_id}/draft-pack")
def ri_draft_pack(engagement_id: str, body: DraftPackBody = Body(default_factory=DraftPackBody)) -> dict[str, Any]:
    st = _eng(engagement_id)
    scored = st.get("scored") or []
    if not scored:
        raise HTTPException(status_code=400, detail={"ar": "شغّل score أولًا", "en": "Run score first"})
    top = scored[0]["row"]
    try:
        pack = build_revenue_draft_pack(
            dict(top),
            request_cold_whatsapp=body.request_cold_whatsapp,
            request_linkedin_automation=body.request_linkedin_automation,
            request_scraping=body.request_scraping,
            request_bulk_outreach=body.request_bulk_outreach,
            include_whatsapp_draft=body.include_whatsapp_draft,
            relationship_status=body.relationship_status,
        )
    except ValueError as e:
        raise HTTPException(status_code=403, detail={"ar": "رُفض — سياسة الحوكمة", "en": "Blocked — governance doctrine", "detail": str(e)}) from e
    snap = merge_pipeline_stage(
        engagement_id,
        draft_done=True,
        governance_notes=("draft_only_external_channels",),
        pipeline_context_update={"draft_pack_channels": list(pack.keys())},
    )
    st["draft_pack"] = pack
    return {
        **_gov(GovernanceDecision.DRAFT_ONLY, rules=("external_channels_draft_only",)),
        "engagement_id": engagement_id,
        "draft_pack": pack,
        "founder_snapshot": snap.to_public_dict(),
    }


@router.post("/{engagement_id}/finalize")
def ri_finalize(engagement_id: str) -> dict[str, Any]:
    st = _eng(engagement_id)
    if not st.get("draft_pack"):
        raise HTTPException(status_code=400, detail={"ar": "شغّل draft-pack أولًا", "en": "Run draft-pack first"})
    sections = {
        "executive_summary": "Governed Revenue Intelligence — narrative draft.",
        "problem": "Fragmented account data and weak follow-up discipline.",
        "inputs": "Client-uploaded accounts + Source Passport.",
        "source_passports": st.get("passport", {}),
        "work_completed": "Import, dedupe hints, scoring, draft-only outreach pack.",
        "outputs": st.get("draft_pack", {}),
        "quality_scores": {"data_quality": st.get("accounts") and "see import", "icp_fit": "see score response"},
        "governance_decisions": ["DRAFT_ONLY on external channels"],
        "blocked_risks": ["no_cold_whatsapp", "no_linkedin_automation"],
        "value_metrics": {"accounts_ranked": len(st.get("scored") or [])},
        "limitations": "MVP narrative — human review required.",
        "recommended_next_step": "Generate Proof Pack + retainer gate.",
        "capital_assets_created": ["ranked_account_list", "draft_pack", "governance_log"],
        "appendices": {"passport": st.get("passport", {}), "score_sample": (st.get("scored") or [])[:5]},
    }
    snap = merge_pipeline_stage(
        engagement_id,
        finalize_done=True,
        pipeline_context_update={"proof_sections_ready": len(sections)},
    )
    st["proof_narrative"] = sections
    return {
        **_gov(GovernanceDecision.ALLOW_WITH_REVIEW, rules=("proof_narrative_human_review",)),
        "engagement_id": engagement_id,
        "proof_pack_v2_narrative_sections": sections,
        "founder_snapshot": snap.to_public_dict(),
    }
