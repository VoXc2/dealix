"""V12 Self-Improvement OS — weekly-learning + prompt-quality stub.

Wraps `self_growth_os.weekly_growth_scorecard`. Adds a prompt-quality
stub that suggests improvements only — never auto-applies. NO
self-modifying code. NO automatic PR.

Full Ops 2.0 — `/weekly-learning` now runs two real learning loops
(reply -> objection library, ticket -> KB-article candidates) wired to
the live classifier output and ticket store. Suggestions only; nothing
is auto-applied.
"""
from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from fastapi import APIRouter

from auto_client_acquisition.learning_loops.reply_objection_loop import (
    build_objection_library,
)
from auto_client_acquisition.learning_loops.ticket_kb_loop import (
    build_kb_candidates,
    load_ticket_categories,
)

router = APIRouter(prefix="/api/v1/self-improvement-os", tags=["self-improvement-os"])


_HARD_GATES = {
    "no_self_modifying_code": True,
    "no_automatic_pr": True,
    "no_fake_metrics": True,
    "approval_required_for_external_actions": True,
}


@router.get("/status")
async def self_improvement_os_status() -> dict[str, Any]:
    return {
        "service": "self_improvement_os",
        "module": "self_growth_os+v12_quality_stub",
        "status": "operational",
        "version": "v12",
        "degraded": False,
        "checks": {
            "weekly_scorecard": "ok",
            "prompt_quality": "stub",
            "learning_loops": "live",
        },
        "hard_gates": _HARD_GATES,
        "next_action_ar": "اقرأ /weekly-learning كلّ يوم اثنين",
        "next_action_en": "Read /weekly-learning every Monday.",
    }


def _run_reply_objection_loop() -> dict[str, Any]:
    """Learning loop (a) — classified replies -> deduplicated objection library."""
    from auto_client_acquisition.learning_loops.reply_objection_loop import (
        load_classified_replies,
    )

    replies = load_classified_replies()
    library = build_objection_library(replies)
    return {
        "loop": "reply_to_objection_library",
        "replies_analyzed": len(replies),
        "objection_library": [e.to_dict() for e in library],
        "data_status": "live" if replies else "no_replies_recorded_yet",
        "action_mode": "suggest_only",
    }


def _run_ticket_kb_loop() -> dict[str, Any]:
    """Learning loop (b) — recurring tickets -> KB-article candidates."""
    categories = load_ticket_categories()
    candidates = build_kb_candidates(categories)
    return {
        "loop": "ticket_to_kb_article_candidate",
        "tickets_analyzed": len(categories),
        "kb_article_candidates": [c.to_dict() for c in candidates],
        "data_status": "live" if categories else "no_tickets_recorded_yet",
        "action_mode": "suggest_only",
    }


@router.get("/weekly-learning")
async def weekly_learning() -> dict[str, Any]:
    """Run the real learning loops. SUGGEST ONLY — nothing auto-applied.

    Two loops read live operational data:
      (a) reply classifier output -> deduplicated objection library
      (b) support ticket store -> KB-gap article candidates
    """
    reply_loop = _run_reply_objection_loop()
    ticket_loop = _run_ticket_kb_loop()
    any_data = bool(reply_loop["replies_analyzed"] or ticket_loop["tickets_analyzed"])
    return {
        "schema_version": 2,
        "generated_at": datetime.now(UTC).isoformat(),
        "learning_loops": [reply_loop, ticket_loop],
        "data_status": "live" if any_data else "no_signals_recorded_yet",
        "summary_ar": "حلقات تعلّم حقيقية — اقتراحات للنقاش بدون تطبيق آلي",
        "summary_en": "Real learning loops — suggestions for discussion, no auto-apply.",
        "hard_gates": _HARD_GATES,
    }
