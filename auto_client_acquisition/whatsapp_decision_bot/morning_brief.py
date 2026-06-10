"""Wave 13 Phase 7 — Standardized morning-brief + approval-card formatters.

Per plan §32.4A.5 — the founder reads this on phone every 8AM KSA.
NEVER auto-sends; always returns text for founder to copy/paste.

Hard rules:
  Article 4 NO_LIVE_SEND — these are pure formatters
  Article 8 — commitment language only; no fake numbers
"""

from __future__ import annotations

from typing import Any

# Action mode taxonomy (per §32.4A.5)
ACTION_MODES = ("suggest_only", "draft_only", "approval_required",
                "approved_manual", "blocked")


def build_morning_brief(
    *,
    customer_handle: str,
    p0_leads_count: int = 0,
    pending_approvals_count: int = 0,
    proof_packs_due_count: int = 0,
    support_alerts_count: int = 0,
    top_decision_summary: str | None = None,
) -> dict[str, Any]:
    """Build the structured morning-brief payload.

    Returns dict with: text_ar (the WhatsApp-formatted string), counts,
    suggested_replies. Caller renders via format_morning_brief() or
    embeds in API response.
    """
    summary = top_decision_summary or "راجع الفرص الجديدة في البوابة"
    return {
        "customer_handle": customer_handle,
        "counts": {
            "p0_leads": int(p0_leads_count),
            "pending_approvals": int(pending_approvals_count),
            "proof_packs_due": int(proof_packs_due_count),
            "support_alerts": int(support_alerts_count),
        },
        "top_decision_summary_ar": summary,
        "suggested_replies": ["1", "2", "3", "4"],
        "action_mode": "suggest_only",  # Article 4: always suggest
        "is_estimate": True,
    }


def format_morning_brief(brief: dict[str, Any]) -> str:
    """Format morning brief in the exact §32.4A.5 founder template.

    صباح الخير 👋
    ملخص Dealix اليوم:
    1. عندك N فرص عالية الأولوية.
    2. عندك N رسائل/قرارات تحتاج موافقة.
    3. عندك Proof Pack قيد التجهيز.
    4. عندك تذكرة دعم عالية الأهمية.
    5. القرار الأهم: <summary>
    اكتب:
    1 لعرض الفرص
    2 للموافقات
    3 للدعم
    4 للتقرير
    """
    counts = brief.get("counts", {})
    summary = brief.get("top_decision_summary_ar", "—")

    lines = [
        "صباح الخير 👋",
        "ملخص Dealix اليوم:",
        f"1. عندك {counts.get('p0_leads', 0)} فرص عالية الأولوية.",
        f"2. عندك {counts.get('pending_approvals', 0)} رسائل/قرارات تحتاج موافقة.",
    ]
    if counts.get("proof_packs_due", 0) > 0:
        lines.append(f"3. عندك {counts.get('proof_packs_due', 0)} Proof Pack قيد التجهيز.")
    else:
        lines.append("3. لا Proof Packs مستحقّة اليوم.")
    if counts.get("support_alerts", 0) > 0:
        lines.append(f"4. عندك {counts.get('support_alerts', 0)} تذكرة دعم تحتاج تصعيد.")
    else:
        lines.append("4. لا تنبيهات دعم.")
    lines.append(f"5. القرار الأهم: {summary}")
    lines.append("")
    lines.append("اكتب:")
    lines.append("1 لعرض الفرص")
    lines.append("2 للموافقات")
    lines.append("3 للدعم")
    lines.append("4 للتقرير")
    return "\n".join(lines)


def render_approval_card(
    *,
    approval_id: str,
    text_ar: str,
    risk_ar: str = "لا ترسل عبر واتساب بدون consent.",
    action_index: int = 1,
) -> str:
    """Format one approval card per §32.4A.5 template.

    الرسالة 2:
    [النص الكامل ≤ 150 حرف]
    المخاطر:
    لا ترسل عبر واتساب بدون consent.
    القرار:
    1 اعتماد للاستخدام اليدوي  (action_mode=approved_manual)
    2 تعديل  (action_mode=draft_only — يفتح للتعديل)
    3 رفض  (action_mode=blocked — يسجل سبب الرفض)
    """
    text_clipped = text_ar.strip()
    if len(text_clipped) > 150:
        text_clipped = text_clipped[:147] + "…"

    lines = [
        f"الرسالة {action_index}:",
        text_clipped,
        "",
        "المخاطر:",
        risk_ar,
        "",
        "القرار:",
        "1 اعتماد للاستخدام اليدوي  (action_mode=approved_manual)",
        "2 تعديل  (action_mode=draft_only — يفتح للتعديل)",
        "3 رفض  (action_mode=blocked — يسجل سبب الرفض)",
        "",
        f"approval_id: {approval_id}",
    ]
    return "\n".join(lines)


def parse_approval_response(*, response: str) -> dict[str, Any]:
    """Parse founder's '1' / '2' / '3' reply into a structured action_mode result.

    Article 4: NEVER returns 'live_send' or 'auto_send'. Highest action_mode
    is 'approved_manual' (founder copies + sends manually).
    """
    response = response.strip()
    if response in ("1", "اعتمد", "اعتماد", "approve"):
        return {
            "action_mode": "approved_manual",
            "audit_note": "founder_approved_via_whatsapp",
        }
    if response in ("2", "عدّل", "تعديل", "edit"):
        return {
            "action_mode": "draft_only",
            "audit_note": "founder_requested_edit",
        }
    if response in ("3", "ارفض", "رفض", "reject"):
        return {
            "action_mode": "blocked",
            "audit_note": "founder_rejected",
        }
    return {
        "action_mode": "suggest_only",
        "audit_note": "unrecognized_response",
    }
