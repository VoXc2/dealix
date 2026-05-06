"""Company Growth Beast — service wrapper (draft-only, no live outbound)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body

from auto_client_acquisition.company_growth_beast import (
    build_command_center,
    build_content_pack,
    build_growth_diagnostic,
    build_proof_loop,
    build_warm_route_pack,
    build_weekly_growth_report,
    match_offer,
    plan_growth_experiment,
    rank_target_segments,
    support_questions_to_insights,
    upsert_company_profile,
)
from auto_client_acquisition.company_growth_beast import session_store as cgb_store

router = APIRouter(prefix="/api/v1/company-growth-beast", tags=["company-growth-beast"])


def _sid(payload: dict[str, Any]) -> str:
    return str(payload.get("session_id") or "default")


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "module": "company_growth_beast",
        "guardrails": {
            "no_live_send": True,
            "no_live_charge": True,
            "no_cold_whatsapp": True,
            "no_linkedin_automation": True,
            "no_scraping": True,
            "no_fake_proof": True,
            "arabic_primary": True,
            "default_action_modes": ["draft_only", "approval_required", "suggest_only", "blocked"],
        },
        "routes": [
            "GET /api/v1/company-growth-beast/status",
            "POST /api/v1/company-growth-beast/profile",
            "POST /api/v1/company-growth-beast/diagnostic",
            "POST /api/v1/company-growth-beast/targets",
            "POST /api/v1/company-growth-beast/offer",
            "POST /api/v1/company-growth-beast/content-pack",
            "POST /api/v1/company-growth-beast/warm-route",
            "POST /api/v1/company-growth-beast/experiment",
            "POST /api/v1/company-growth-beast/support-to-growth",
            "POST /api/v1/company-growth-beast/proof-loop",
            "GET /api/v1/company-growth-beast/weekly-report",
            "GET /api/v1/company-growth-beast/command-center",
        ],
    }


@router.post("/profile")
async def post_profile(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    sid = _sid(payload)
    result = upsert_company_profile(payload)
    if result.get("safety", {}).get("safe", True):
        cgb_store.save_profile(sid, result["profile"])
    return {"session_id": sid, **result}


@router.post("/diagnostic")
async def post_diagnostic(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile", "hint": "POST /profile first or pass profile in body"}
    diag = build_growth_diagnostic(prof)
    cgb_store.save_diagnostic(sid, diag)
    return {"session_id": sid, "diagnostic": diag}


@router.post("/targets")
async def post_targets(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile", "hint": "POST /profile first"}
    targets = rank_target_segments(prof)
    cgb_store.save_targets(sid, targets)
    return {"session_id": sid, "targets": targets}


@router.post("/offer")
async def post_offer(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile"}
    diag = cgb_store.get_diagnostic(sid)
    offer = match_offer(prof, diag)
    cgb_store.save_offer(sid, offer)
    return {"session_id": sid, **offer}


@router.post("/content-pack")
async def post_content_pack(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile"}
    offer = cgb_store.get_offer(sid)
    pack = build_content_pack(prof, offer)
    cgb_store.save_content(sid, pack)
    return {"session_id": sid, **pack}


@router.post("/warm-route")
async def post_warm_route(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile"}
    targets = cgb_store.get_targets(sid) or []
    warm = build_warm_route_pack(prof, targets)
    cgb_store.save_warm_route(sid, warm)
    return {"session_id": sid, **warm}


@router.post("/experiment")
async def post_experiment(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile"}
    targets = cgb_store.get_targets(sid) or []
    offer = cgb_store.get_offer(sid)
    exp = plan_growth_experiment(prof, targets, offer)
    cgb_store.save_experiment(sid, exp)
    return {"session_id": sid, **exp}


@router.post("/support-to-growth")
async def post_support_to_growth(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    sid = _sid(payload)
    raw = str(payload.get("support_questions") or payload.get("message") or "")
    out = support_questions_to_insights(raw)
    cgb_store.save_support(sid, out)
    return {"session_id": sid, **out}


@router.post("/proof-loop")
async def post_proof_loop(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    sid = _sid(payload)
    prof = cgb_store.get_profile(sid) or (payload.get("profile") if isinstance(payload.get("profile"), dict) else None)
    if not prof:
        return {"session_id": sid, "error": "missing_profile"}
    diag = cgb_store.get_diagnostic(sid)
    sup = cgb_store.get_support(sid)
    loop = build_proof_loop(prof, diag, sup)
    cgb_store.save_proof(sid, loop)
    return {"session_id": sid, **loop}


@router.get("/weekly-report")
async def get_weekly_report(session_id: str = "default") -> dict[str, Any]:
    sid = session_id.strip() or "default"
    report = build_weekly_growth_report(
        cgb_store.get_profile(sid),
        cgb_store.get_targets(sid),
        cgb_store.get_offer(sid),
        cgb_store.get_experiment(sid),
        cgb_store.get_support(sid),
        cgb_store.get_proof(sid),
    )
    return {"session_id": sid, **report}


@router.get("/command-center")
async def get_command_center(session_id: str = "default") -> dict[str, Any]:
    sid = session_id.strip() or "default"
    cc = build_command_center(
        cgb_store.get_profile(sid),
        cgb_store.get_targets(sid),
        cgb_store.get_offer(sid),
        cgb_store.get_content(sid),
        cgb_store.get_warm_route(sid),
        cgb_store.get_experiment(sid),
        cgb_store.get_support(sid),
        cgb_store.get_proof(sid),
    )
    return {"session_id": sid, **cc}
