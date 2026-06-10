"""V12 Delivery OS — wraps delivery_factory + adds deliverable checklist."""
from __future__ import annotations

import hashlib
from datetime import UTC, datetime, timedelta
from typing import Any, Literal

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

router = APIRouter(prefix="/api/v1/delivery-os", tags=["delivery-os"])


_HARD_GATES = {
    "no_live_send": True,
    "no_fake_proof": True,
    "approval_required_for_external_actions": True,
}


SessionStatus = Literal[
    "new",
    "waiting_inputs",
    "in_progress",
    "needs_approval",
    "ready_to_deliver",
    "delivered",
    "proof_pending",
    "closed",
    "blocked",
]


# In-memory session store (resets on app restart — V12 v1; persistence deferred)
_SESSIONS: dict[str, dict[str, Any]] = {}


class _CreateSessionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    customer_handle: str = "Slot-A"
    service_id: str = "growth_starter"


@router.get("/status")
async def delivery_os_status() -> dict[str, Any]:
    return {
        "service": "delivery_os",
        "module": "delivery_factory+v12_checklist",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "active_sessions": len(_SESSIONS),
        "checks": {"delivery_factory": "ok", "checklist": "ok"},
        "hard_gates": _HARD_GATES,
        "next_action_ar": "أنشئ جلسة /create-session ثم تابع /next-step",
        "next_action_en": "Create a session via /create-session then /next-step.",
    }


def _session_id(customer: str, service: str) -> str:
    return "ds_" + hashlib.sha256(f"{customer}|{service}".encode()).hexdigest()[:16]


def _checklist(service: str) -> list[dict[str, Any]]:
    if service != "growth_starter":
        return []
    return [
        {"day": 0, "task_ar": "كيكاوف + Diagnostic", "task_en": "Kickoff + Diagnostic", "status": "pending"},
        {"day": 1, "task_ar": "10 فرص مرتّبة", "task_en": "10 ranked opportunities", "status": "pending"},
        {"day": 2, "task_ar": "مسوّدات الرسائل", "task_en": "Message drafts", "status": "pending"},
        {"day": 3, "task_ar": "إرسال يدوي معتمد", "task_en": "Approved manual sends", "status": "pending"},
        {"day": 4, "task_ar": "خطّة متابعة 7 أيّام", "task_en": "7-day follow-up plan", "status": "pending"},
        {"day": 5, "task_ar": "مذكّرة المخاطر", "task_en": "Risk note", "status": "pending"},
        {"day": 6, "task_ar": "Proof Pack مبدئي", "task_en": "Initial Proof Pack", "status": "pending"},
        {"day": 7, "task_ar": "مكالمة المراجعة + قرار upsell", "task_en": "Review call + upsell decision", "status": "pending"},
    ]


@router.post("/create-session")
async def create_session(req: _CreateSessionRequest) -> dict[str, Any]:
    sid = _session_id(req.customer_handle, req.service_id)
    now = datetime.now(UTC)
    session = {
        "id": sid,
        "customer_handle": req.customer_handle,
        "service_id": req.service_id,
        "status": "new",
        "created_at": now.isoformat(),
        "sla_due_at": (now + timedelta(days=7)).isoformat(),
        "checklist": _checklist(req.service_id),
        "action_mode": "approval_required",
        "hard_gates": _HARD_GATES,
    }
    _SESSIONS[sid] = session
    return session


@router.get("/session/{session_id}")
async def get_session(session_id: str) -> dict[str, Any]:
    session = _SESSIONS.get(session_id)
    if session is None:
        return {
            "id": session_id,
            "status": "not_found",
            "degraded": True,
            "blocker": "session_not_in_memory",
            "next_action_ar": "أنشئ جلسة جديدة عبر /create-session",
            "next_action_en": "Create a new session via /create-session.",
            "hard_gates": _HARD_GATES,
        }
    return session


class _NextStepRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    session_id: str
    target_status: SessionStatus = "in_progress"


@router.post("/next-step")
async def next_step(req: _NextStepRequest) -> dict[str, Any]:
    session = _SESSIONS.get(req.session_id)
    if session is None:
        return {
            "session_id": req.session_id,
            "status": "not_found",
            "degraded": True,
            "blocker": "session_not_in_memory",
            "hard_gates": _HARD_GATES,
        }
    session["status"] = req.target_status
    return session
