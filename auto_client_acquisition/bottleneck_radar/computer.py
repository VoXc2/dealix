"""Bottleneck Radar computer — composes existing layer state.

Pure-fn (deterministic). Inputs come from the caller (router pulls
real counts from approval_center / payment_ops / service_sessions /
support_os) — keeps this module Article 11 thin and testable.
"""

from __future__ import annotations

from auto_client_acquisition.bottleneck_radar.schemas import (
    BottleneckSeverity,
    FounderBottleneck,
)


def _severity_for(total: int) -> BottleneckSeverity:
    if total == 0:
        return "clear"
    if total <= 2:
        return "watch"
    if total <= 5:
        return "blocking"
    return "critical"


def _summary(total: int, *, customer_handle: str | None) -> tuple[str, str]:
    """Bilingual single-sentence summary."""
    label_ar = customer_handle if customer_handle else "البورتفوليو"
    label_en = customer_handle if customer_handle else "the portfolio"
    if total == 0:
        return (
            f"لا اختناقات حاليًا في {label_ar}.",
            f"No current bottlenecks in {label_en}.",
        )
    return (
        f"عندك {total} عنصر معطّل في {label_ar} يحتاج إجراء.",
        f"{total} blocked item(s) in {label_en} need action.",
    )


def _single_action(
    *,
    blocking_approvals_count: int,
    pending_payment_confirmations: int,
    pending_proof_packs_to_send: int,
    overdue_followups: int,
    sla_at_risk_tickets: int,
) -> tuple[str, str]:
    """Choose the highest-leverage single action (priority order)."""
    if pending_payment_confirmations > 0:
        return (
            "أكّد الدفعات المعلّقة الآن — أعلى أولوية للإيراد.",
            "Confirm pending payments now — highest revenue priority.",
        )
    if blocking_approvals_count > 0:
        return (
            f"اعتمد {blocking_approvals_count} موافقة معلّقة (>٢٤ ساعة).",
            f"Approve {blocking_approvals_count} pending request(s) (>24h).",
        )
    if sla_at_risk_tickets > 0:
        return (
            f"رد على {sla_at_risk_tickets} تذكرة دعم قبل breach SLA.",
            f"Respond to {sla_at_risk_tickets} support ticket(s) before SLA breach.",
        )
    if pending_proof_packs_to_send > 0:
        return (
            f"راجع {pending_proof_packs_to_send} Proof Pack وأرسلها للعميل.",
            f"Review {pending_proof_packs_to_send} Proof Pack(s) and send to customer.",
        )
    if overdue_followups > 0:
        return (
            f"تابع {overdue_followups} مكالمة/رسالة متأخرة.",
            f"Follow up on {overdue_followups} overdue call(s)/message(s).",
        )
    return (
        "لا إجراء عاجل اليوم. واصل الإيقاع الأسبوعي.",
        "No urgent action today. Continue normal weekly cadence.",
    )


def compute_bottleneck(
    *,
    customer_handle: str | None = None,
    blocking_approvals_count: int = 0,
    pending_payment_confirmations: int = 0,
    pending_proof_packs_to_send: int = 0,
    overdue_followups: int = 0,
    sla_at_risk_tickets: int = 0,
) -> FounderBottleneck:
    """Pure compute fn — caller passes counts, we return assessment.

    Returns FounderBottleneck. Caller (router or CLI) responsible
    for sourcing the counts from the right layer modules.
    """
    total = (
        blocking_approvals_count
        + pending_payment_confirmations
        + pending_proof_packs_to_send
        + overdue_followups
        + sla_at_risk_tickets
    )
    severity = _severity_for(total)
    summ_ar, summ_en = _summary(total, customer_handle=customer_handle)
    act_ar, act_en = _single_action(
        blocking_approvals_count=blocking_approvals_count,
        pending_payment_confirmations=pending_payment_confirmations,
        pending_proof_packs_to_send=pending_proof_packs_to_send,
        overdue_followups=overdue_followups,
        sla_at_risk_tickets=sla_at_risk_tickets,
    )
    return FounderBottleneck(
        customer_handle=customer_handle,
        severity=severity,
        blocking_approvals_count=blocking_approvals_count,
        pending_payment_confirmations=pending_payment_confirmations,
        pending_proof_packs_to_send=pending_proof_packs_to_send,
        overdue_followups=overdue_followups,
        sla_at_risk_tickets=sla_at_risk_tickets,
        bottleneck_summary_ar=summ_ar,
        bottleneck_summary_en=summ_en,
        today_single_action_ar=act_ar,
        today_single_action_en=act_en,
        is_estimate=True,
    )


def compute_founder_view(
    *,
    blocking_approvals_count: int = 0,
    pending_payment_confirmations: int = 0,
    pending_proof_packs_to_send: int = 0,
    overdue_followups: int = 0,
    sla_at_risk_tickets: int = 0,
) -> FounderBottleneck:
    """Convenience wrapper for the founder portfolio view (no customer_handle)."""
    return compute_bottleneck(
        customer_handle=None,
        blocking_approvals_count=blocking_approvals_count,
        pending_payment_confirmations=pending_payment_confirmations,
        pending_proof_packs_to_send=pending_proof_packs_to_send,
        overdue_followups=overdue_followups,
        sla_at_risk_tickets=sla_at_risk_tickets,
    )
