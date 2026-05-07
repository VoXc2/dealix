"""LeadOps Spine orchestrator.

Runs the full pipeline:
  intake → normalize → dedupe → compliance → enrich → score
        → brief → offer route → next action → draft → approval

All steps are existing modules; this file only sequences them and
persists the LeadOpsRecord envelope to a JSONL file (Article 11
in-memory + JSONL pattern, like lead_inbox.py).

NEVER calls external send. NEVER auto-approves drafts.
"""
from __future__ import annotations

import hashlib
import json
import os
import uuid
from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.full_ops_contracts.schemas import LeadOpsRecord
from auto_client_acquisition.leadops_spine.compliance_gate import check_compliance
from auto_client_acquisition.leadops_spine.draft_builder import build_draft
from auto_client_acquisition.leadops_spine.next_action import suggest_next_action
from auto_client_acquisition.leadops_spine.offer_router import route_offer

_JSONL_PATH = os.path.join("data", "leadops_records.jsonl")
_RECORDS_INDEX: dict[str, LeadOpsRecord] = {}  # in-memory cache


def _ensure_dir() -> None:
    os.makedirs(os.path.dirname(_JSONL_PATH), exist_ok=True)


def _persist(record: LeadOpsRecord) -> None:
    _ensure_dir()
    _RECORDS_INDEX[record.leadops_id] = record
    with open(_JSONL_PATH, "a", encoding="utf-8") as f:
        f.write(record.model_dump_json() + "\n")


def _normalize(payload: dict[str, Any]) -> dict[str, Any]:
    """Light normalization. Native logic — kept simple + sync so the
    spine doesn't depend on whether existing modules are async."""
    return {
        "company": str(payload.get("company") or "").strip(),
        "email": str(payload.get("email") or "").strip().lower(),
        "phone": str(payload.get("phone") or "").strip(),
        "name": str(payload.get("name") or "").strip(),
        "sector": (str(payload.get("sector") or "").strip().lower() or None),
        "region": str(payload.get("region") or "").strip(),
        "message": str(payload.get("message") or "").strip(),
    }


def _dedup_key(normalized: dict[str, Any]) -> str:
    """Stable key for dedupe — email+phone+company hash."""
    keystr = "|".join([
        normalized.get("email") or "",
        normalized.get("phone") or "",
        (normalized.get("company") or "").lower(),
    ])
    return hashlib.sha256(keystr.encode("utf-8")).hexdigest()[:16]


def _enrich(normalized: dict[str, Any]) -> dict[str, Any]:
    """Static enrichment placeholder — provider abstraction lives in
    api/routers/prospect.py for async lookups. Spine stays sync."""
    return {"provider": "static_fallback", "fields": {}}


def _score(normalized: dict[str, Any], enrichment: dict[str, Any]) -> dict[str, Any]:
    """Heuristic 0..1 fit score from presence of key fields.

    Deeper scoring (BANT/MEDDPICC) lives in agents/qualification.py and
    is invoked separately by /api/v1/sales-os/qualify when needed.
    """
    fit = 0.0
    if normalized.get("email"):
        fit += 0.2
    if normalized.get("sector"):
        fit += 0.2
    if normalized.get("region"):
        fit += 0.2
    if normalized.get("company"):
        fit += 0.2
    if normalized.get("phone"):
        fit += 0.2
    return {"fit": round(min(fit, 1.0), 2), "urgency": 0.5, "risk": 0.2}


def _brief(normalized: dict[str, Any], enrichment: dict[str, Any]) -> dict[str, Any]:
    """Generate a 1-paragraph account brief. Pure deterministic."""
    sector = normalized.get("sector") or "—"
    region = normalized.get("region") or "—"
    company = normalized.get("company") or "this account"
    return {
        "headline_ar": f"حساب {company} — قطاع {sector} في {region}",
        "headline_en": f"Account {company} — {sector} sector in {region}",
        "summary_ar": (
            f"عميل محتمل من {sector} في {region}. "
            f"البيانات المتوفرة: {bool(normalized.get('email'))} email, "
            f"{bool(normalized.get('phone'))} phone."
        ),
        "summary_en": (
            f"Prospect from {sector} in {region}. "
            f"Data on file: {bool(normalized.get('email'))} email, "
            f"{bool(normalized.get('phone'))} phone."
        ),
    }


def run_pipeline(
    *,
    raw_payload: dict[str, Any],
    source: str = "manual",
    customer_handle: str | None = None,
) -> LeadOpsRecord:
    """Full pipeline run for one lead. Returns the persisted envelope."""
    leadops_id = f"lops_{uuid.uuid4().hex[:10]}"

    normalized = _normalize(raw_payload)
    dedup_key = _dedup_key(normalized)
    compliance = check_compliance(normalized=normalized)
    enrichment = _enrich(normalized) if compliance["status"] != "blocked" else {}
    score = _score(normalized, enrichment) if compliance["status"] != "blocked" else {}
    brief = _brief(normalized, enrichment) if compliance["status"] != "blocked" else None

    offer_route_dict = (
        route_offer(sector=normalized.get("sector"), score=score)
        if compliance["status"] == "allowed"
        else None
    )
    next_action_dict = suggest_next_action(
        compliance_status=compliance["status"],
        score=score,
        offer_route=offer_route_dict,
    )

    draft_id = None
    approval_id = None
    if compliance["status"] == "allowed" and offer_route_dict:
        draft = build_draft(
            leadops_id=leadops_id,
            customer_handle=customer_handle,
            sector=normalized.get("sector"),
            offer_route=offer_route_dict,
            next_action=next_action_dict,
        )
        draft_id = draft["draft_id"]
        # Route to approval_center (best-effort, non-fatal)
        try:
            from auto_client_acquisition.approval_center import create_approval
            approval = create_approval(draft["approval_payload"])
            approval_id = approval.approval_id
        except Exception:
            approval_id = None

    record = LeadOpsRecord(
        leadops_id=leadops_id,
        customer_handle=customer_handle,
        source=source,  # type: ignore[arg-type]
        raw_payload=raw_payload,
        normalized=normalized,
        dedup_key=dedup_key,
        compliance_status=compliance["status"],  # type: ignore[arg-type]
        enrichment=enrichment,
        score=score,
        brief=brief,
        offer_route=offer_route_dict,
        next_action=next_action_dict,
        draft_id=draft_id,
        approval_id=approval_id,
    )
    _persist(record)
    return record


def list_records(*, limit: int = 50) -> list[LeadOpsRecord]:
    """Most-recent-first list of in-memory records."""
    return sorted(
        _RECORDS_INDEX.values(),
        key=lambda r: r.created_at,
        reverse=True,
    )[:limit]


def debug_lead(leadops_id: str) -> dict[str, Any]:
    """Full pipeline trace for one lead — what every step produced."""
    rec = _RECORDS_INDEX.get(leadops_id)
    if not rec:
        return {"error": "not_found", "leadops_id": leadops_id}
    return {
        "leadops_id": rec.leadops_id,
        "trace": {
            "1_raw_payload": rec.raw_payload,
            "2_normalized": rec.normalized,
            "3_dedup_key": rec.dedup_key,
            "4_compliance": rec.compliance_status,
            "5_enrichment": rec.enrichment,
            "6_score": rec.score,
            "7_brief": rec.brief,
            "8_offer_route": rec.offer_route,
            "9_next_action": rec.next_action,
            "10_draft_id": rec.draft_id,
            "11_approval_id": rec.approval_id,
        },
        "safety_summary": rec.safety_summary,
        "created_at": rec.created_at.isoformat(),
    }
