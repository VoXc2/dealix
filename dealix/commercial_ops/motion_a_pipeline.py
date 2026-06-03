"""Motion A (agency wedge) — daily P0 pipeline plan toward first paid Diagnostic."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic
from dealix.commercial_ops.outreach_drafts import attach_outreach_drafts
from dealix.commercial_ops.targeting_csv import build_war_room_today, load_targets
from dealix.commercial_ops.targeting_rotation import select_daily_p0_targets

STATUS_NEXT_AR: dict[str, str] = {
    "not_contacted": "مسودة لمسة أولى — وافق ثم أرسل يدوياً (لا بارد)",
    "message_drafted": "راجع المسودة في /ar/ops/founder ثم أرسل يدوياً",
    "approved_to_send": "أرسل اللمسة يدوياً وسجّل message_sent_manual",
    "sent_manual": "متابعة خلال 48س — سجّل reply_received أو demo_booked",
    "replied": "احجز Discovery 10 دقائق — سجّل demo_booked",
    "meeting_booked": "أكمل Discovery السبعة — سجّل scope_requested",
    "scope_requested": "أرسل فاتورة Diagnostic — سجّل invoice_sent ثم payment_received",
}


def _stage_for_status(status: str, paid_tracker: dict[str, Any]) -> str:
    st = (status or "not_contacted").strip().lower()
    if paid_tracker.get("first_close_ready"):
        return "repeat_motion_a"
    if paid_tracker.get("payment_received_real"):
        return "deliver_proof_pack"
    if paid_tracker.get("invoice_sent_real") or st == "scope_requested":
        return "close_payment"
    if st in {"meeting_booked", "replied"}:
        return "discovery_to_scope"
    if st in {"sent_manual", "approved_to_send", "message_drafted"}:
        return "warm_follow_up"
    return "outreach_p0"


def build_motion_a_pipeline_plan(*, top_n: int = 10) -> dict[str, Any]:
    from dealix.commercial_ops.motion_pipelines import build_motion_pipeline_plan

    plan = build_motion_pipeline_plan(motion="A", top_n=top_n)
    paid = plan["first_paid"]
    focus_ar = list(plan.get("focus_ar") or [])
    if paid["verdict"] == "PIPELINE_OPEN":
        focus_ar.append("الأولوية: 3 لمسات P0 + 1 Discovery + سطر evidence اليوم")
    plan["focus_ar"] = focus_ar
    plan["war_room_path"] = "data/war_room_today.json"
    plan["dod_doc"] = paid["dod_doc"]
    plan["refs"] = {
        "dod": "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
        "manual_payment": "docs/ops/MANUAL_PAYMENT_SOP.md",
        "proof_template": "docs/delivery/PROOF_PACK_TEMPLATE.md",
        "motion_a": "docs/commercial/operations/motion_a_agency/",
    }
    return plan


def render_motion_a_markdown(plan: dict[str, Any]) -> str:
    lines = [
        "# Motion A — خط أنابيب اليوم",
        "",
        f"**توليد:** {plan.get('generated_at', '')}",
        "",
        "## تركيز",
    ]
    for item in plan.get("focus_ar") or []:
        lines.append(f"- {item}")
    lines.extend(["", "## أعلى P0", ""])
    for i, t in enumerate(plan.get("targets") or [], start=1):
        lines.append(
            f"{i}. **{t.get('company') or '—'}** · `{t.get('status')}` · "
            f"مرحلة `{t.get('stage')}` — {t.get('next_action_ar')}"
        )
    fp = plan.get("first_paid") or {}
    lines.extend(
        [
            "",
            "## بوابة أول Diagnostic",
            f"- verdict: `{fp.get('verdict')}`",
            f"- payment_received (real): {fp.get('payment_received_real', 0)}",
            f"- proof_pack_delivered (real): {fp.get('proof_pack_delivered_real', 0)}",
            "",
        ]
    )
    return "\n".join(lines)
