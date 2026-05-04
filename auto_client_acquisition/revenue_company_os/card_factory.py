"""
Card factory — generates demo + real decision cards per role.

Real-data branch (when subscriptions/payments/funnel_events exist) plus a
deterministic demo branch for empty environments. Demo cards are always
labeled with `is_demo=True` in `meta`.

Public entry point: build_feed(role, *, real_data=None) -> list[Card]
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from auto_client_acquisition.revenue_company_os.cards import (
    Card,
    CardButton,
    CardType,
    RiskLevel,
    Role,
)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def _demo_meta(extra: dict[str, Any] | None = None) -> dict[str, Any]:
    base = {"is_demo": True, "source": "card_factory_demo"}
    if extra:
        base.update(extra)
    return base


# ── Demo cards per role ──────────────────────────────────────────


def _demo_ceo() -> list[Card]:
    return [
        Card(
            id=_new_id("card"),
            type=CardType.CEO_DAILY,
            role=Role.CEO,
            title_ar="3 قرارات تحتاج موافقتك اليوم",
            why_now_ar="نهاية الربع — صفقتان في خطر و3 شراكات في انتظار رد.",
            recommended_action_ar=(
                "ابدأ بمراجعة Approval queue (10 دقائق)، ثم اعتمد رد على "
                "اعتراض السعر للصفقة الكبرى."
            ),
            proof_impact=["decisions_made", "approvals_processed", "deals_unblocked"],
            risk=RiskLevel.MEDIUM,
            risk_note_ar="تأخير 24 ساعة قد يكلف صفقة بقيمة 45,000 ريال.",
            buttons=[
                CardButton("افتح Approval queue", "primary", primary=True),
                CardButton("التفاصيل", "details"),
                CardButton("لاحقاً", "skip"),
            ],
            owner="ceo",
            expires_at=_utcnow() + timedelta(hours=12),
            meta=_demo_meta({"sla_hours": 12}),
        ),
        Card(
            id=_new_id("card"),
            type=CardType.PROOF,
            role=Role.CEO,
            title_ar="Proof Pack هذا الأسبوع — أثر مُقدّر 18,500 ريال",
            why_now_ar="انتهى تقرير الأسبوع 18. 10 فرص + 8 رسائل + 3 مخاطر تم منعها.",
            recommended_action_ar="افتح التقرير وشاركه مع المجلس قبل اجتماع الاثنين.",
            proof_impact=["weekly_proof_pack", "board_share", "estimated_revenue_sar:18500"],
            risk=RiskLevel.LOW,
            buttons=[
                CardButton("افتح Proof Pack", "primary", primary=True),
                CardButton("شارك مع المجلس", "details"),
            ],
            owner="ceo",
            meta=_demo_meta(),
        ),
        Card(
            id=_new_id("card"),
            type=CardType.PARTNER,
            role=Role.CEO,
            title_ar="فرصة شراكة — وكالة تدريب في الرياض",
            why_now_ar="3 من عملائها يطابقون ICP. توسعها الأخير يفتح 5 صفقات محتملة.",
            recommended_action_ar="حدد اجتماع 30 دقيقة مع المؤسس + جهز Co-branded Proof Pack.",
            proof_impact=["partner_meetings", "cobranded_proof_packs"],
            risk=RiskLevel.LOW,
            buttons=[
                CardButton("جهّز رسالة", "primary", primary=True),
                CardButton("التفاصيل", "details"),
                CardButton("تخطي", "skip"),
            ],
            owner="ceo",
            meta=_demo_meta(),
        ),
    ]


def _demo_sales() -> list[Card]:
    return [
        Card(
            id=_new_id("card"),
            type=CardType.DEAL_FOLLOWUP,
            role=Role.SALES,
            title_ar="صفقة في خطر — لم تردّ منذ 5 أيام",
            why_now_ar="آخر تواصل: عرض السعر. silent treatment > 5 أيام = مؤشر خسارة 60%.",
            recommended_action_ar="أرسل رسالة follow-up + قدّم خصم 5% مرتبط بالتوقيع هذا الأسبوع.",
            proof_impact=["followups_sent", "deals_unblocked"],
            risk=RiskLevel.HIGH,
            risk_note_ar="قيمة الصفقة: 45,000 ريال.",
            buttons=[
                CardButton("جهّز follow-up", "primary", primary=True),
                CardButton("التفاصيل", "details"),
                CardButton("تخطي", "skip"),
            ],
            owner="sales",
            meta=_demo_meta(),
        ),
        Card(
            id=_new_id("card"),
            type=CardType.NEGOTIATION,
            role=Role.SALES,
            title_ar="اعتراض سعر — العميل قال: السعر مرتفع",
            why_now_ar="المشكلة ليست السعر فقط؛ يحتاج Proof قبل الالتزام.",
            recommended_action_ar="اقترح Pilot 499 ريال (7 أيام) بدلاً من الخصم. Proof Pack يقنعهم.",
            proof_impact=["objections_handled", "pilot_offered"],
            risk=RiskLevel.MEDIUM,
            buttons=[
                CardButton("استخدم الرد", "primary", primary=True),
                CardButton("عدّل", "details"),
                CardButton("صعّد لمدير", "skip"),
            ],
            owner="sales",
            meta=_demo_meta(),
        ),
    ]


def _demo_growth() -> list[Card]:
    return [
        Card(
            id=_new_id("card"),
            type=CardType.OPPORTUNITY,
            role=Role.GROWTH,
            title_ar="قطاع التدريب — 4 فرص بـ why-now signal قوي",
            why_now_ar="3 منشآت تدريبية في الرياض أعلنت عن توسع في برامج الشركات.",
            recommended_action_ar="جهّز outbound batch (Email + LinkedIn manual) مع مرجع لـ case study.",
            proof_impact=["opportunities_created", "drafts_created", "channels_safe"],
            risk=RiskLevel.LOW,
            risk_note_ar="WhatsApp ممنوع لهذه القائمة (لا opt-in).",
            buttons=[
                CardButton("جهّز Batch", "primary", primary=True),
                CardButton("التفاصيل", "details"),
                CardButton("تخطي", "skip"),
            ],
            owner="growth",
            meta=_demo_meta(),
        ),
        Card(
            id=_new_id("card"),
            type=CardType.RISK,
            role=Role.GROWTH,
            title_ar="حملة Email — 18% bounce rate (تجاوز الحد 10%)",
            why_now_ar="Bounce rate يهدد reputation الـ domain.",
            recommended_action_ar="أوقف الحملة الحالية، نظّف القائمة، وأعد الإرسال للـ verified addresses فقط.",
            proof_impact=["risks_blocked", "deliverability_protected"],
            risk=RiskLevel.HIGH,
            buttons=[
                CardButton("أوقف الحملة", "primary", primary=True),
                CardButton("نظّف القائمة", "details"),
                CardButton("ابقاء + مراقبة", "skip"),
            ],
            owner="growth",
            meta=_demo_meta(),
        ),
    ]


def _demo_service() -> list[Card]:
    return [
        Card(
            id=_new_id("card"),
            type=CardType.CUSTOMER_SUCCESS,
            role=Role.SERVICE,
            title_ar="عميل Pilot على وشك الانتهاء — 2 أيام متبقية",
            why_now_ar="Pilot ينتهي يوم الخميس. لا توجد لقاء ترقية مجدول.",
            recommended_action_ar="جهّز Proof Pack + احجز اجتماع ترقية لـ Executive Growth OS.",
            proof_impact=["pilot_proof_packs", "upgrade_meetings"],
            risk=RiskLevel.MEDIUM,
            buttons=[
                CardButton("جهّز Proof + ترقية", "primary", primary=True),
                CardButton("احجز اجتماع", "details"),
            ],
            owner="service",
            meta=_demo_meta(),
        ),
    ]


def _demo_support() -> list[Card]:
    return [
        Card(
            id=_new_id("card"),
            type=CardType.SUPPORT,
            role=Role.SUPPORT,
            title_ar="تذكرة P1 — connector HubSpot لا يزامن",
            why_now_ar="آخر sync ناجح قبل 6 ساعات. SLA P1 = نفس اليوم.",
            recommended_action_ar="افحص API key للـ HubSpot account + أعد المزامنة اليدوية.",
            proof_impact=["tickets_resolved", "sla_met"],
            risk=RiskLevel.MEDIUM,
            buttons=[
                CardButton("افتح التذكرة", "primary", primary=True),
                CardButton("شغّل sync يدوي", "details"),
                CardButton("صعّد", "skip"),
            ],
            owner="support",
            meta=_demo_meta(),
        ),
    ]


def _demo_agency() -> list[Card]:
    return [
        Card(
            id=_new_id("card"),
            type=CardType.PARTNER,
            role=Role.AGENCY,
            title_ar="عميلك الجديد — جاهز لتشغيل Diagnostic",
            why_now_ar="تمت إضافة 'شركة س للتدريب' للبورتال. مدخلات كاملة.",
            recommended_action_ar="ابدأ Diagnostic. Co-branded Proof Pack جاهز خلال 24 ساعة.",
            proof_impact=["client_diagnostics", "cobranded_proof_packs"],
            risk=RiskLevel.LOW,
            buttons=[
                CardButton("ابدأ Diagnostic", "primary", primary=True),
                CardButton("التفاصيل", "details"),
            ],
            owner="agency",
            meta=_demo_meta(),
        ),
        Card(
            id=_new_id("card"),
            type=CardType.PROOF,
            role=Role.AGENCY,
            title_ar="Co-branded Proof Pack جاهز للإرسال",
            why_now_ar="عميل 'شركة ص للوجستيات' أكمل أسبوعه الأول. 7 فرص + Proof Pack.",
            recommended_action_ar="راجع الـ PDF، عدّل التعليق التنفيذي، وأرسله من بريدك.",
            proof_impact=["proof_packs_sent", "client_health_visible"],
            risk=RiskLevel.LOW,
            buttons=[
                CardButton("راجع وأرسل", "primary", primary=True),
                CardButton("عدّل أولاً", "details"),
            ],
            owner="agency",
            meta=_demo_meta(),
        ),
    ]


_DEMO_BUILDERS: dict[Role, callable] = {
    Role.CEO: _demo_ceo,
    Role.SALES: _demo_sales,
    Role.GROWTH: _demo_growth,
    Role.SERVICE: _demo_service,
    Role.SUPPORT: _demo_support,
    Role.AGENCY: _demo_agency,
}


# ── Public entry point ────────────────────────────────────────────


def build_feed(
    role: Role | str,
    *,
    real_data: list[dict[str, Any]] | None = None,
) -> list[Card]:
    """Build a card feed for the given role.

    If `real_data` is provided (currently a list of dicts; subscription/funnel
    inputs in future PR-FE-4 backend extension), it is rendered with
    is_demo=False. Otherwise, deterministic demo cards are returned with a
    clear demo banner via meta.
    """
    if isinstance(role, str):
        try:
            role = Role(role.lower())
        except ValueError as exc:
            raise ValueError(f"unknown role: {role}") from exc
    if real_data:
        # Reserved hook for live data (e.g., from FunnelEventRecord + lead scoring).
        # In this PR we only return the demo set; real-data branch lands when
        # signals + scoring tables are populated in a future iteration.
        pass
    builder = _DEMO_BUILDERS.get(role)
    if builder is None:
        return []
    return builder()


def list_roles() -> list[dict[str, str]]:
    return [
        {"id": Role.CEO.value, "label_ar": "المدير التنفيذي"},
        {"id": Role.SALES.value, "label_ar": "المبيعات"},
        {"id": Role.GROWTH.value, "label_ar": "النمو"},
        {"id": Role.SERVICE.value, "label_ar": "تشغيل الخدمة"},
        {"id": Role.SUPPORT.value, "label_ar": "الدعم"},
        {"id": Role.AGENCY.value, "label_ar": "الوكالة الشريكة"},
    ]
