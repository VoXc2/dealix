"""
WhatsApp Brief Renderer — turn a role brief dict into Arabic WhatsApp text.

INTERNAL-ONLY by design: this is the text managers receive via WhatsApp.
Customer-facing WhatsApp is a separate channel and goes through the
existing approval-first WhatsApp send path (which is gated False).

Rules enforced:
  - Max 3 decisions in the rendered text (slice if more).
  - Max 3 buttons per decision.
  - Arabic-first.
  - No "guaranteed" claims.
  - Includes risk note + action mode.
  - Returns plain text (no HTML).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


_ROLE_HEADERS_AR = {
    "ceo":              "ملخص اليوم — المدير التنفيذي",
    "sales_manager":    "ملخص المبيعات اليوم",
    "growth_manager":   "خطة النمو اليوم",
    "revops":           "تقرير RevOps الأسبوعي",
    "customer_success": "حالة العملاء اليوم",
    "agency_partner":   "حالة الوكالة اليوم",
    "finance":          "تحديث مالي",
    "compliance":       "تقرير الامتثال اليومي",
}


def _trim(items: list, n: int) -> list:
    return list(items)[:n]


def render(brief: dict[str, Any]) -> str:
    """Return the Arabic WhatsApp text for a role brief."""
    role = (brief.get("role") or "").lower()
    header = _ROLE_HEADERS_AR.get(role, "Dealix — ملخص يومي")
    date = brief.get("date") or datetime.now(timezone.utc).date().isoformat()
    lines: list[str] = []
    lines.append(f"صباح الخير 👋")
    lines.append(f"{header} — {date}")

    summary = brief.get("summary") or {}
    if summary:
        lines.append("")
        lines.append("الملخص:")
        for k, v in summary.items():
            label = _summary_label_ar(k)
            lines.append(f"- {label}: {v}")

    decisions = _trim(brief.get("top_decisions") or [], 3)
    if decisions:
        lines.append("")
        lines.append("أهم القرارات:")
        for i, d in enumerate(decisions, start=1):
            title = d.get("title_ar", "—")
            why = d.get("why_now_ar") or ""
            action = d.get("recommended_action_ar") or ""
            risk = d.get("risk_level") or "low"
            risk_ar = {"low": "منخفض", "medium": "متوسط", "high": "عالٍ"}.get(risk, risk)
            mode = d.get("action_mode") or "approval_required"
            mode_ar = {
                "approval_required": "موافقة مطلوبة",
                "approved_execute":  "بعد الموافقة",
                "draft_only":        "مسودة فقط",
                "blocked":           "محظور",
            }.get(mode, mode)
            buttons = _trim(d.get("buttons_ar") or [], 3)
            lines.append("")
            lines.append(f"{i}) {title}")
            if why:
                lines.append(f"   لماذا الآن: {why}")
            if action:
                lines.append(f"   الإجراء: {action}")
            lines.append(f"   مخاطرة: {risk_ar} · {mode_ar}")
            if buttons:
                lines.append("   [" + "] [".join(buttons) + "]")

    blocked = brief.get("blocked_today_ar") or []
    if blocked:
        lines.append("")
        lines.append("ممنوع اليوم:")
        for b in blocked:
            lines.append(f"- {b}")

    lines.append("")
    lines.append("📌 approval-first في كل خطوة. لا cold WhatsApp. لا live charge.")
    return "\n".join(lines)


def _summary_label_ar(key: str) -> str:
    table = {
        "deals_total": "إجمالي الصفقات",
        "deals_at_risk": "صفقات في خطر",
        "followups_due": "متابعات مطلوبة",
        "objections_open": "اعتراضات مفتوحة",
        "meetings_to_book": "اجتماعات للحجز",
        "pilot_offers_ready": "عروض Pilot جاهزة",
        "invoice_requests": "فواتير تحتاج إرسال",
        "focus_segment": "الشريحة المركّز عليها",
        "channels_planned": "القنوات المخططة",
        "experiment_active": "تجربة نشطة",
        "yesterday_drafts": "drafts الأمس",
        "yesterday_approvals": "موافقات الأمس",
        "yesterday_blocked": "محظور أمس",
        "high_churn_risk": "Churn risk عالٍ",
        "onboarding_pending": "Onboarding ناقص",
        "proof_delayed": "Proof Pack متأخر",
        "p0_open": "تذاكر P0 مفتوحة",
        "p1_open": "تذاكر P1 مفتوحة",
        "upgrade_ready": "جاهزون للترقية",
        "active_clients": "عملاء نشطون",
        "diagnostics_ready": "Diagnostics جاهزة",
        "proof_packs_ready": "Proof Packs جاهزة",
        "needs_followup": "بحاجة متابعة",
        "expected_commission_sar": "عمولة متوقعة (ر.س)",
        "invoices_ready": "فواتير جاهزة",
        "paid_this_week": "مدفوعات هذا الأسبوع",
        "refunded": "مرتجعات",
        "expected_partner_commission_sar": "عمولة شريك متوقعة (ر.س)",
        "risks_blocked_total": "محاولات تم منعها",
        "high_risk_blocked": "عالية المخاطرة محظورة",
        "live_gates_on_count": "Gates مُفعَّلة",
        "weekly_proof_revenue_sar": "أثر Proof الأسبوعي (ر.س)",
        "growth_segment_today": "شريحة النمو اليوم",
        "hot_partners": "شركاء جاهزون",
        "customers_total": "إجمالي العملاء",
    }
    return table.get(key, key.replace("_", " "))


# ── Internal send guard (gated) ───────────────────────────────────


def can_send_internal_brief(settings) -> tuple[bool, str]:
    """Return (allowed, reason). Default: NOT allowed.

    The router that handles `/api/v1/whatsapp/brief/send-internal` MUST call
    this and refuse with 403 unless allowed.
    """
    if bool(getattr(settings, "whatsapp_allow_internal_send", False)) is False:
        return False, "WHATSAPP_ALLOW_INTERNAL_SEND=false"
    if bool(getattr(settings, "whatsapp_allow_live_send", False)) is False:
        return False, "WHATSAPP_ALLOW_LIVE_SEND=false (master live-send gate is closed)"
    return True, "ok"
