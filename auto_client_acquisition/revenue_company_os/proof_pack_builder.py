"""
Proof Pack Builder — turns ledger events into a customer-facing summary.

The Proof Pack is Dealix's most important deliverable. It answers:
  1. What was created?
  2. What was protected?
  3. What needs approval?
  4. Estimated revenue impact (SAR).
  5. Recommended next action.

Pure summarization (no I/O). The router pulls events from the ledger and
calls `build_pack(events)` to get the renderable dict.
"""

from __future__ import annotations

from collections import Counter
from typing import Any, Iterable

from auto_client_acquisition.revenue_company_os.revenue_work_units import label_for


# Categories used in the "What was X" sections of the Proof Pack.
_CATEGORY_CREATED = (
    "opportunity_created",
    "draft_created",
    "meeting_drafted",
    "followup_created",
    "partner_suggested",
    "payment_link_drafted",
    "target_ranked",
)
_CATEGORY_PROTECTED = ("risk_blocked",)
_CATEGORY_PROOF = ("proof_generated",)
_CATEGORY_APPROVAL = ("approval_collected",)


def _is_active(ev) -> bool:
    """An event 'counts' if either no approval is required OR it's been approved."""
    if ev.approval_required and not ev.approved:
        return False
    return True


def build_pack(events: Iterable, *, customer_label: str | None = None) -> dict[str, Any]:
    evs = list(events)

    counts: Counter[str] = Counter()
    revenue_total = 0.0
    pending_approval = 0
    risks_blocked: list[dict[str, Any]] = []
    high_risk_blocked = 0

    for e in evs:
        counts[e.unit_type] += 1
        if e.approval_required and not e.approved:
            pending_approval += 1
        if e.unit_type == "risk_blocked":
            risks_blocked.append({
                "label_ar": e.label_ar or label_for(e.unit_type),
                "risk_level": e.risk_level,
                "occurred_at": e.occurred_at.isoformat() if e.occurred_at else None,
            })
            if e.risk_level == "high":
                high_risk_blocked += 1
        if _is_active(e):
            revenue_total += float(e.revenue_impact_sar or 0.0)

    created_breakdown = [
        {
            "unit_type": t,
            "label_ar": label_for(t),
            "count": counts.get(t, 0),
        }
        for t in _CATEGORY_CREATED
        if counts.get(t, 0) > 0
    ]

    next_action = _recommend_next_action(counts)

    return {
        "customer_label": customer_label,
        "totals": {
            "created_units": sum(counts[k] for k in _CATEGORY_CREATED),
            "protected_units": sum(counts[k] for k in _CATEGORY_PROTECTED),
            "proof_events": sum(counts[k] for k in _CATEGORY_PROOF),
            "approvals_collected": sum(counts[k] for k in _CATEGORY_APPROVAL),
            "pending_approvals": pending_approval,
            "high_risk_blocked": high_risk_blocked,
            "estimated_revenue_impact_sar": round(revenue_total, 2),
        },
        "what_was_created": created_breakdown,
        "what_was_protected": risks_blocked,
        "next_recommended_action_ar": next_action,
        "policy_notes_ar": [
            "كل draft يمر بموافقتك قبل الإرسال.",
            "لا cold WhatsApp · لا scraping · لا live charge.",
            "الأرقام محسوبة من ledger لحظي — قابلة للتحقق per-event.",
        ],
        "anti_claims_ar": [
            "لا نضمن نتائج محددة",
            "نُثبت الإنجاز بأرقام، لا بوعود",
        ],
    }


def _recommend_next_action(counts: Counter[str]) -> str:
    """Heuristic — rule-based. No LLM call."""
    if counts.get("proof_generated", 0) > 0 and counts.get("opportunity_created", 0) >= 5:
        return "ركّز هذا الأسبوع على متابعة أعلى 3 فرص — جهّز meeting briefs ومرّرها للموافقة."
    if counts.get("draft_created", 0) > counts.get("approval_collected", 0):
        return "هناك drafts تنتظر موافقتك — افتح Approval queue قبل ما تتقادم."
    if counts.get("risk_blocked", 0) >= 3:
        return "تم منع عدة محاولات outbound غير آمنة — راجع ICP + قائمة opt-in قبل التوسع."
    if counts.get("opportunity_created", 0) == 0:
        return "لا توجد فرص جديدة بعد — راجع intake/ICP وأعد signal scan."
    return "ابدأ الأسبوع بمراجعة Proof Pack مع المجلس + اختر فرصة واحدة للترقية إلى meeting."
