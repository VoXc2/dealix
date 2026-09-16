"""
Offer Router — sector → offer config table.

Pure data module (no FastAPI / DB deps). Imported by api/routers/dominance.py
and testable in pure unit tests without spinning up the app.
"""

from __future__ import annotations

from typing import Any

OFFER_ROUTES: dict[str, dict[str, Any]] = {
    "real_estate_developer": {
        "primary_offer": "pilot_customer_specific_lead_qualification_plus_viewing_booking",
        "value_prop": "تأهيل lead العقار + حجز معاينة بدلاً منكم",
        "headline_pain": "كل lead عقاري متأخر دقيقة = احتمال خسارة العميل لمنافس",
        "kpi": "Arabic-replied leads × demos booked × pipeline added",
        "best_channel": "phone_task_then_email", "pricing_tier": "Customer-specific quote",
    },
    "real_estate": {
        "primary_offer": "pilot_customer_specific_lead_qualification_plus_viewing_booking",
        "value_prop": "نأهل العميل ونحجز موعد المعاينة قبل ما يبرد",
        "headline_pain": "العمولة الواحدة في العقار = ربح أسبوع. لا تخسرونها لتأخر الرد",
        "kpi": "qualified leads × viewings booked",
        "best_channel": "phone_task_then_email", "pricing_tier": "Customer-specific quote",
    },
    "construction": {
        "primary_offer": "pilot_customer_specific_quote_request_qualification",
        "value_prop": "نفرز RFQs ونجمع المواصفات قبل تسعير المشروع",
        "headline_pain": "RFQ تتوزع بين قنوات متعددة بدون فرز موحد",
        "kpi": "RFQs qualified × pricing-engineer time saved",
        "best_channel": "phone_task", "pricing_tier": "Customer-specific quote",
    },
    "hospitality": {
        "primary_offer": "pilot_customer_specific_booking_inquiry_assistant",
        "value_prop": "نرد فوراً على استفسارات MICE/قاعات/إفطار-سحور ونحجز معاينات",
        "headline_pain": "استفسارات بأي ساعة + موظف غير متاح = حجز ضائع",
        "kpi": "MICE inquiries × site visits booked",
        "best_channel": "phone_task_or_email", "pricing_tier": "Customer-specific quote",
    },
    "events": {
        "primary_offer": "pilot_customer_specific_event_inquiry_with_viewing_booking",
        "value_prop": "نرد على lead الفعالية فوراً ونجمع التاريخ + العدد + الباقة",
        "headline_pain": "كل lead = موسم — خسارته = 5K-100K ريال",
        "kpi": "inquiries × site visits booked",
        "best_channel": "phone_task", "pricing_tier": "Customer-specific quote",
    },
    "food_beverage": {
        "primary_offer": "pilot_customer_specific_catering_franchise_inquiry_routing",
        "value_prop": "نفرز التموين/الفرنشايز عن طلبات الطعام العادية",
        "headline_pain": "تموين شركة = إيراد شهر، يضيع بين رسائل واتساب",
        "kpi": "catering leads qualified × management calls scheduled",
        "best_channel": "phone_task", "pricing_tier": "Customer-specific quote",
    },
    "restaurant": {
        "primary_offer": "pilot_customer_specific_catering_franchise_inquiry_routing",
        "value_prop": "نفرز التموين/الفرنشايز عن طلبات الطعام العادية",
        "headline_pain": "تموين شركة = إيراد شهر، يضيع بين رسائل واتساب",
        "kpi": "catering leads qualified × management calls scheduled",
        "best_channel": "phone_task", "pricing_tier": "Customer-specific quote",
    },
    "logistics": {
        "primary_offer": "pilot_customer_specific_RFQ_response_under_60_seconds",
        "value_prop": "نرد على RFQ شحن خلال دقيقة بالعربي",
        "headline_pain": "10 دقائق فرق في الرد = خسارة عقد لمنافس",
        "kpi": "RFQs answered <60s × dispatch tickets opened",
        "best_channel": "phone_or_email", "pricing_tier": "Customer-specific quote",
    },
    "saas": {
        "primary_offer": "pilot_customer_specific_saudi_arabic_inbound_response_layer",
        "value_prop": "AI sales rep بالعربي الخليجي يكمل CRMكم",
        "headline_pain": "Saudi inbound leads باللغة العربية، الفريق يرد بالإنجليزية/ترجمة",
        "kpi": "Arabic-lead-to-demo conversion uplift",
        "best_channel": "linkedin_manual_then_email", "pricing_tier": "Customer-specific quote",
    },
    "marketing_agency": {
        "primary_offer": "agency_partner_customer_specific",
        "value_prop": "Dealix يمكن أن يعمل كشريك تنفيذ/توزيع؛ الاقتصاديات والحقوق تُحدد باتفاق خاص ومعتمد",
        "headline_pain": "العملاء يطلبون AI sales rep بالعربي والوكالة بدون حل جاهز",
        "kpi": "agency clients signed × MRR share",
        "best_channel": "linkedin_manual_then_call", "pricing_tier": "Partnership",
    },
    "training_center": {
        "primary_offer": "pilot_customer_specific_course_inquiry_enrollment_assistant",
        "value_prop": "نرد على استفسار البرامج + نجمع التفاصيل + نوجه للتسجيل",
        "headline_pain": "موسم تسجيل = استفسارات كثيرة، الرد البطيء = طالب راح لمنافس",
        "kpi": "inquiries qualified × enrollments started",
        "best_channel": "phone_task_then_email", "pricing_tier": "Customer-specific quote",
    },
    "dental_clinic": {
        "primary_offer": "pilot_customer_specific_appointment_qualification",
        "value_prop": "نأخذ تفاصيل المريض + نقيم الحالة قبل الحجز",
        "headline_pain": "مكالمات استقبال غير مدربة = جدول مزدحم بمواعيد منخفضة الجدية",
        "kpi": "high-intent appointments × no-show rate reduction",
        "best_channel": "phone_task", "pricing_tier": "Customer-specific quote",
    },
    "medical_clinic": {
        "primary_offer": "pilot_customer_specific_appointment_qualification",
        "value_prop": "نأخذ تفاصيل المريض + نقيم الحالة قبل الحجز",
        "headline_pain": "مكالمات استقبال غير مدربة = جدول مزدحم بمواعيد منخفضة الجدية",
        "kpi": "high-intent appointments × no-show rate reduction",
        "best_channel": "phone_task", "pricing_tier": "Customer-specific quote",
    },
}

DEFAULT_OFFER: dict[str, Any] = {
    "primary_offer": "pilot_customer_specific_managed",
    "value_prop": "Dealix يساعد على تنظيم inbound leads بالعربي الخليجي وقياس زمن الاستجابة من baseline موثق",
    "headline_pain": "سرعة الرد على العميل = ميزة تنافسية مباشرة",
    "kpi": "qualified leads × demos booked",
    "best_channel": "phone_or_email", "pricing_tier": "Customer-specific quote",
}


def route_offer(sector: str | None) -> dict[str, Any]:
    """Sector → offer config. Falls back to DEFAULT_OFFER for unknown sectors."""
    if not sector:
        return DEFAULT_OFFER
    return OFFER_ROUTES.get(sector.lower().strip(), DEFAULT_OFFER)


def build_tomorrow_recommendation(
    sector_leaderboard: list[dict[str, Any]],
    gmail_today: int,
    replies_14d: int,
) -> dict[str, Any]:
    """Compose a 'tomorrow plan' bullet list based on today's data."""
    actions: list[str] = []
    if gmail_today < 30:
        actions.append("نقص في drafts اليوم — شغّل revenue-machine/run يدوياً")
    if replies_14d < 3:
        actions.append("معدل الردود منخفض — راجع subject lines + opener angles")
    if sector_leaderboard:
        best = sector_leaderboard[0]
        if best.get("reply_rate", 0) >= 0.05:
            actions.append(
                f"ضاعف الاستهداف في {best['sector']} — reply_rate {best['reply_rate']:.0%}"
            )
        worst = sector_leaderboard[-1]
        if worst.get("sent", 0) >= 10 and worst.get("reply_rate", 0) < 0.02:
            actions.append(
                f"أوقف {worst['sector']} مؤقتاً — reply_rate {worst.get('reply_rate', 0):.0%}"
            )
    if not actions:
        actions.append("استمر بنفس الإيقاع — daily 50 + 20 + 10")
    return {"actions": actions, "based_on": "last_14_days_email_data"}
