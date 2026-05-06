"""Map outcomes to proof events and approval-gated content ideas."""

from __future__ import annotations

from typing import Any


def build_proof_loop(
    profile: dict[str, Any],
    diagnostic: dict[str, Any] | None,
    support_insights: dict[str, Any] | None,
) -> dict[str, Any]:
    events: list[dict[str, Any]] = [
        {
            "event_type": "diagnostic_draft_ready",
            "source": "company_growth_beast",
            "action_mode": "draft_only",
            "note_ar": "تسجيل يدوي بعد اعتماد المشغّل",
        },
        {
            "event_type": "content_pack_drafted",
            "source": "company_growth_beast",
            "action_mode": "approval_required",
            "note_ar": "أي استخدام علني يتطلب موافقة",
        },
    ]
    if diagnostic:
        events.append(
            {
                "event_type": "growth_diagnostic_generated",
                "source": "deterministic_engine",
                "action_mode": "draft_only",
            }
        )

    ideas: list[dict[str, Any]] = [
        {
            "idea_ar": "مقتطف دراسة حالة — مسودة فقط",
            "approval_required": True,
            "blocked_until": "written_customer_approval",
        }
    ]
    if support_insights and support_insights.get("themes"):
        ideas.append(
            {
                "idea_ar": f"مقالة تغطي المواضيع: {', '.join(support_insights['themes'][:3])}",
                "approval_required": True,
                "blocked_until": "kb_review",
            }
        )

    return {
        "schema_version": 1,
        "proof_events_suggested": events,
        "content_from_proof_ar": ideas,
        "no_fake_metrics": True,
        "language_primary": "ar",
    }
