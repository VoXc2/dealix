"""
Call & Meeting Intelligence OS — System #6 of the Saudi Revenue Command OS.

Pure planner; takes loaded MeetingRecord rows + ProofEventRecord rows and
returns the daily brief + ranked decisions for the meeting_intelligence role.

No I/O. The router fetches rows.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Any


def _now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _to_naive(dt):
    if dt is None:
        return None
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


def meeting_snapshot(meetings, proof_events) -> dict[str, Any]:
    """Compute meeting/call snapshot from minimal inputs.

    Args:
      meetings: iterable of MeetingRecord-like (.outcome, .occurred_at,
                .follow_up_due_at, .customer_id, .next_action_ar)
      proof_events: iterable of ProofEventRecord-like used to detect meetings
                    held without a follow-up RWU recorded.
    """
    meetings = list(meetings or [])
    events = list(proof_events or [])
    now = _now()

    by_outcome: Counter[str] = Counter()
    overdue_followups: list[dict[str, Any]] = []
    no_followup_24h: list[dict[str, Any]] = []
    closed_count = 0

    customer_ids_with_followup_rwu: set[str] = {
        e.customer_id for e in events
        if getattr(e, "unit_type", None) == "followup_created" and getattr(e, "customer_id", None)
    }

    for m in meetings:
        outcome = (m.outcome or "held").lower()
        by_outcome[outcome] += 1
        if outcome == "closed_won":
            closed_count += 1

        deadline = _to_naive(getattr(m, "follow_up_due_at", None))
        occurred = _to_naive(getattr(m, "occurred_at", None))

        if deadline and deadline < now and outcome not in ("closed_won", "closed_lost"):
            overdue_followups.append({
                "meeting_id": getattr(m, "id", None),
                "customer_id": getattr(m, "customer_id", None),
                "outcome": outcome,
                "overdue_hours": round((now - deadline).total_seconds() / 3600.0, 1),
                "next_action_ar": getattr(m, "next_action_ar", None),
            })

        if (
            occurred
            and outcome == "held"
            and (now - occurred) > timedelta(hours=24)
            and getattr(m, "customer_id", None)
            and m.customer_id not in customer_ids_with_followup_rwu
        ):
            no_followup_24h.append({
                "meeting_id": getattr(m, "id", None),
                "customer_id": m.customer_id,
                "hours_since": round((now - occurred).total_seconds() / 3600.0, 1),
            })

    overdue_followups.sort(key=lambda x: x["overdue_hours"], reverse=True)
    no_followup_24h.sort(key=lambda x: x["hours_since"], reverse=True)

    return {
        "as_of": now.isoformat(),
        "summary": {
            "meetings_total": len(meetings),
            "meetings_held": by_outcome.get("held", 0) + by_outcome.get("closed_won", 0)
                              + by_outcome.get("closed_lost", 0) + by_outcome.get("follow_up_required", 0),
            "meetings_closed_won": closed_count,
            "meetings_no_show": by_outcome.get("no_show", 0),
            "overdue_followups": len(overdue_followups),
            "missing_followup_24h": len(no_followup_24h),
        },
        "by_outcome": dict(by_outcome),
        "overdue_followups": overdue_followups[:5],
        "missing_followup_24h": no_followup_24h[:5],
    }


def top_decisions(snapshot: dict[str, Any]) -> list[dict[str, Any]]:
    """Build the Top-3 decision cards for the meeting intelligence brief."""
    decisions: list[dict[str, Any]] = []
    overdue = snapshot.get("overdue_followups") or []
    missing = snapshot.get("missing_followup_24h") or []
    summary = snapshot.get("summary") or {}

    if overdue:
        d = overdue[0]
        decisions.append({
            "type": "overdue_followup",
            "title_ar": "متابعة اجتماع متأخرة",
            "why_now_ar": f"تجاوزت الموعد المتفق عليه بـ {d['overdue_hours']:.0f} ساعة (customer {str(d.get('customer_id') or '')[:10]}…).",
            "recommended_action_ar": "أرسل رسالة متابعة الآن أو حدّث المهمة بسبب التأخير.",
            "risk_level": "high" if d["overdue_hours"] >= 48 else "medium",
            "risk_badge": "P1" if d["overdue_hours"] >= 48 else "P2",
            "proof_impact": ["followup_created"],
            "action_mode": "approval_required",
            "buttons_ar": ["جهّز رسالة متابعة", "افتح الاجتماع", "أعد الجدولة"],
        })

    if missing:
        m = missing[0]
        decisions.append({
            "type": "missing_followup_after_meeting",
            "title_ar": "اجتماع تم بدون متابعة مُسجَّلة",
            "why_now_ar": f"مرّت {m['hours_since']:.0f} ساعة على الاجتماع بدون followup_created RWU.",
            "recommended_action_ar": "سجّل متابعة الآن: ملخص + خطوة تالية + موعد.",
            "risk_level": "medium",
            "risk_badge": "P2",
            "proof_impact": ["followup_created", "meeting_held"],
            "action_mode": "approval_required",
            "buttons_ar": ["سجّل متابعة", "افتح الاجتماع", "تخطى"],
        })

    if summary.get("meetings_no_show", 0) > 0:
        decisions.append({
            "type": "no_show_recovery",
            "title_ar": f"{summary['meetings_no_show']} no-show هذا الأسبوع",
            "why_now_ar": "فقدنا اجتماعاً واحداً على الأقل بسبب عدم الحضور — أعد الجدولة بقالب لطيف.",
            "recommended_action_ar": "أرسل قالب 'نعرف أن وقتك ضيق — هل يناسبك بعد ٢٤ ساعة؟'",
            "risk_level": "medium",
            "risk_badge": "P2",
            "proof_impact": ["meeting_drafted", "followup_created"],
            "action_mode": "approval_required",
            "buttons_ar": ["جهّز قالب الاعتذار", "اقترح موعد جديد", "أرشف"],
        })

    return decisions[:3]


def build_brief(meetings, proof_events) -> dict[str, Any]:
    snap = meeting_snapshot(meetings, proof_events)
    return {
        "role": "meeting_intelligence",
        "brief_type": "daily_meeting_brief",
        "date": _now().date().isoformat(),
        "summary": snap["summary"],
        "by_outcome": snap["by_outcome"],
        "top_decisions": top_decisions(snap),
        "blocked_today_ar": [
            "لا تسجيل مكالمة بدون موافقة العميل",
            "لا مشاركة ملاحظات اجتماع خارج الفريق",
            "لا اقتراح خصم في اجتماع بدون policy موافق عليها",
        ],
    }
