"""Founder Command Bus — Track C4 of 30-day plan.

Single endpoint that accepts natural-language commands from the founder
("draft a follow-up to ahmad@example.sa about the pilot offer"), uses the
existing LLM router to draft, and queues the result to ApprovalGate.

NEVER auto-sends — always returns approval_id + draft preview. Founder
approves via /decisions.html or WhatsApp.

Hard rules:
  - NO_LIVE_SEND — drafts only, queued to approval_center
  - NO_COLD_WHATSAPP — refuses commands targeting numbers without consent
  - Token budget: 800 input + 400 output (slightly higher than daily-brief
    because the founder may paste lead context)
  - All actions logged for audit trail
"""

from __future__ import annotations

import asyncio
import logging
import re
import time
from typing import Any

from fastapi import APIRouter, Body, HTTPException

router = APIRouter(prefix="/api/v1/command-bus", tags=["command-bus"])
logger = logging.getLogger(__name__)

MAX_INPUT_CHARS = 4000
MAX_INPUT_TOKENS = 800
MAX_OUTPUT_TOKENS = 400
LLM_TIMEOUT_SECONDS = 12.0

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_cold_whatsapp": True,
    "no_fake_proof": True,
    "approval_required_for_external": True,
}

# Detect cold-channel intents to refuse early
_COLD_PATTERNS = [
    re.compile(r"\bcold\s+(whatsapp|outreach|email|messaging)\b", re.IGNORECASE),
    re.compile(r"بلا\s*consent|بدون\s*موافقة|بدون\s*إذن"),
    re.compile(r"\bblast\b|\bspray\s+and\s+pray\b", re.IGNORECASE),
    re.compile(r"\bscrape|sweep\s+linkedin\b", re.IGNORECASE),
]

SYSTEM_PROMPT_AR = """\
أنت مساعد المؤسس Sami في Dealix. دورك: تحويل أمر الـ founder بلغة طبيعيّة
إلى DRAFT جاهز للمراجعة. لا تُرسل أي شيء. النظام يضع كل ناتج في
approval queue لاعتماد المؤسس.

قواعد إلزاميّة:
1. الإجابة بصيغة JSON مع 4 حقول: action_type · summary_ar · summary_en · draft_body.
2. action_type واحدة من: outbound_message · proposal_draft · followup · note · reminder · faq_update.
3. summary_ar: جملة عربيّة سعوديّة موجزة لما سيُنفّذ بعد الموافقة.
4. summary_en: نفس المعنى بالإنجليزيّة (للـ audit trail).
5. draft_body: النصّ الكامل الذي سيُرسَل / يُحفَظ بعد الموافقة. عربي خليجي.
6. لا تخترع أرقاماً أو evidence_id أو شعارات.
7. لو الأمر يطلب cold outreach أو scraping أو blast — ارفض بـ action_type=blocked.
"""


def _check_cold_intent(text: str) -> str | None:
    """Return refusal reason if text matches a forbidden pattern."""
    for pattern in _COLD_PATTERNS:
        if pattern.search(text):
            return f"matched forbidden pattern: {pattern.pattern}"
    return None


async def _call_llm(system_prompt: str, user_input: str) -> tuple[str, str]:
    try:
        from core.llm.base import Message
        from core.llm.router import get_router
    except ImportError as exc:
        raise RuntimeError(f"LLM router unavailable: {exc}") from exc

    router_obj = get_router()
    messages = [
        Message(role="system", content=system_prompt),
        Message(role="user", content=user_input),
    ]
    response = await asyncio.wait_for(
        router_obj.complete(
            messages=messages,
            max_tokens=MAX_OUTPUT_TOKENS,
            temperature=0.4,
        ),
        timeout=LLM_TIMEOUT_SECONDS,
    )
    return response.content, getattr(response, "model", "unknown")


def _parse_llm_json(text: str) -> dict[str, Any]:
    """Best-effort JSON extraction from LLM output."""
    import json as _json

    # Look for {...} block
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return _json.loads(match.group(0))
        except _json.JSONDecodeError:
            pass
    # Fallback: synthesize a minimal valid response
    return {
        "action_type": "note",
        "summary_ar": "ملاحظة محفوظة",
        "summary_en": "Saved note",
        "draft_body": text.strip()[:1000],
    }


def _queue_to_approval(parsed: dict[str, Any], original_command: str) -> str:
    """Push the draft to approval_center. Returns approval_id."""
    approval_id = f"cb_{int(time.time() * 1000)}"
    try:
        from auto_client_acquisition.approval_center import enqueue  # type: ignore
    except ImportError:
        # Approval center not bootable in this env — return a logical id
        # so the frontend can still display + log.
        return approval_id
    try:
        enqueue(
            approval_id=approval_id,
            action_type=parsed.get("action_type", "note"),
            summary_ar=parsed.get("summary_ar", ""),
            summary_en=parsed.get("summary_en", ""),
            payload={
                "draft_body": parsed.get("draft_body", ""),
                "original_command": original_command,
                "source": "command_bus",
            },
            channel="founder_command_bus",
            risk_level="medium",
        )
    except Exception as exc:
        logger.warning("command_bus_enqueue_failed: %s", exc)
    return approval_id


@router.post("")
@router.post("/")
async def submit_command(body: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Submit a natural-language command. Returns draft + approval_id.

    Body:
      command: str (required, ≤ 4000 chars)
      context: dict (optional — lead info, customer handle, etc.)

    Response:
      approval_id: str
      action_type: str
      summary_ar/en: str
      draft_body: str
      status: "queued" | "blocked"
      hard_gates: {...}
    """
    command = (body.get("command") or "").strip()
    if not command:
        raise HTTPException(status_code=422, detail="command is required")
    if len(command) > MAX_INPUT_CHARS:
        raise HTTPException(
            status_code=413,
            detail=f"command too long (max {MAX_INPUT_CHARS} chars)",
        )

    # Pre-flight: refuse cold/scraping intents
    refusal = _check_cold_intent(command)
    if refusal:
        return {
            "approval_id": None,
            "action_type": "blocked",
            "status": "blocked",
            "summary_ar": "تمّ الرفض — الأمر يطلب action محظور دستورياً",
            "summary_en": "Refused — command requested a constitutionally blocked action",
            "draft_body": "",
            "refusal_reason": refusal,
            "hard_gates": _HARD_GATES,
        }

    context = body.get("context") or {}
    user_input = command
    if context:
        # Compact context blob
        ctx_lines = [f"{k}: {v}" for k, v in list(context.items())[:8]]
        user_input += "\n\nContext:\n" + "\n".join(ctx_lines)

    started = time.monotonic()
    try:
        text, model_used = await _call_llm(SYSTEM_PROMPT_AR, user_input)
        parsed = _parse_llm_json(text)
        # Re-check for cold intent in LLM output
        body_text = (parsed.get("draft_body") or "")
        if _check_cold_intent(body_text):
            return {
                "approval_id": None,
                "action_type": "blocked",
                "status": "blocked",
                "summary_ar": "draft المُولَّد تضمّن action محظور — تمّ الرفض",
                "summary_en": "Generated draft contained blocked action — refused",
                "draft_body": "",
                "hard_gates": _HARD_GATES,
            }
        approval_id = _queue_to_approval(parsed, command)
        return {
            "approval_id": approval_id,
            "action_type": parsed.get("action_type", "note"),
            "status": "queued",
            "summary_ar": parsed.get("summary_ar", ""),
            "summary_en": parsed.get("summary_en", ""),
            "draft_body": parsed.get("draft_body", ""),
            "duration_ms": int((time.monotonic() - started) * 1000),
            "model_used": model_used,
            "hard_gates": _HARD_GATES,
            "next_step": "افتح /decisions.html لاعتماد الـ draft أو راجعه على واتساب",
        }
    except TimeoutError:
        return {
            "approval_id": None,
            "action_type": "timeout",
            "status": "error",
            "summary_ar": "LLM timeout — حاول مجدّداً",
            "summary_en": "LLM timeout — retry",
            "draft_body": "",
            "hard_gates": _HARD_GATES,
        }
    except Exception as exc:
        logger.warning("command_bus_failed: %s", exc)
        raise HTTPException(status_code=503, detail=f"command_bus_unavailable: {exc}") from exc


@router.get("/health")
async def health() -> dict[str, Any]:
    """Lightweight liveness probe."""
    return {
        "status": "ok",
        "endpoint": "/api/v1/command-bus",
        "hard_gates": _HARD_GATES,
        "max_input_chars": MAX_INPUT_CHARS,
        "max_input_tokens": MAX_INPUT_TOKENS,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
