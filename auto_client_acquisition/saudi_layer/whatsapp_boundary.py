"""WhatsApp boundaries — PDPL-compliant, cold-outreach safe communication.

Saudi regulations: PDPL consent + CITC WhatsApp bulk messaging rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

WHATSAPP_POSTURE_AR = (
    "واتساب: مسودة فقط مع علاقة/موافقة صريحة؛ لا إرسال بارد ولا أتمتة."
)

WHATSAPP_POSTURE_EN = (
    "WhatsApp: Draft only with prior relationship/explicit consent; "
    "no cold outreach and no automation."
)


class WhatsAppRelationshipType(str, Enum):
    """Type of relationship with the WhatsApp contact."""

    NONE = "none"               # No prior relationship — cold outreach NOT allowed
    INQUIRY = "inquiry"         # Contact made an inquiry via website/form
    MEETING = "meeting"         # Had a meeting (online or in-person)
    CLIENT = "client"           # Current or past client
    REFERRAL = "referral"       # Referred by an existing client/partner
    EXISTING_CHAT = "existing"  # Existing WhatsApp conversation
    OPT_IN = "opt_in"           # Explicitly opted in via form/checkbox


WHATSAPP_ALLOWED_ACTIONS: dict[WhatsAppRelationshipType, list[str]] = {
    WhatsAppRelationshipType.NONE: [],
    WhatsAppRelationshipType.INQUIRY: ["respond_to_inquiry", "send_proposal"],
    WhatsAppRelationshipType.MEETING: ["follow_up", "send_proposal", "schedule_next"],
    WhatsAppRelationshipType.CLIENT: [
        "follow_up", "send_proposal", "schedule_next", "send_update",
        "request_feedback", "send_invoice", "support",
    ],
    WhatsAppRelationshipType.REFERRAL: [
        "introduce", "send_intro_pack", "schedule_meeting",
    ],
    WhatsAppRelationshipType.EXISTING_CHAT: [
        "continue_conversation", "send_proposal", "send_update",
    ],
    WhatsAppRelationshipType.OPT_IN: [
        "send_newsletter", "send_offer", "send_update", "send_proposal",
        "request_feedback",
    ],
}


@dataclass
class WhatsAppRule:
    """A WhatsApp communication boundary rule."""

    rule_id: str
    title_ar: str
    title_en: str
    description_ar: str
    description_en: str
    category: str  # consent, timing, content, frequency


WHATSAPP_RULES: list[WhatsAppRule] = [
    WhatsAppRule(
        rule_id="w1",
        title_ar="لا إرسال بارد",
        title_en="No Cold Outreach",
        description_ar="لا يجوز إرسال رسالة واتساب تجارية لشخص ليس لديك علاقة سابقة معه أو موافقته الصريحة.",
        description_en="Cannot send a commercial WhatsApp message to someone without prior relationship or explicit consent.",
        category="consent",
    ),
    WhatsAppRule(
        rule_id="w2",
        title_ar="موافقة صريحة",
        title_en="Explicit Consent",
        description_ar="يجب الحصول على موافقة صريحة (اختيارية) قبل إضافة العميل إلى قوائم البث.",
        description_en="Explicit opt-in consent required before adding to broadcast lists.",
        category="consent",
    ),
    WhatsAppRule(
        rule_id="w3",
        title_ar="خيار إلغاء الاشتراك",
        title_en="Opt-Out Option",
        description_ar="يجب توفير خيار إلغاء الاشتراك في كل رسالة تسويقية.",
        description_en="Must provide opt-out option in every marketing message.",
        category="consent",
    ),
    WhatsAppRule(
        rule_id="w4",
        title_ar="لا أتمتة كاملة",
        title_en="No Full Automation",
        description_ar="يجب أن يكون للإنسان إشراف على كل رسالة تسويقية. لا يُسمح بإرسال تلقائي بالكامل.",
        description_en="Human oversight required for every marketing message. Fully automated sending is not allowed.",
        category="content",
    ),
    WhatsAppRule(
        rule_id="w5",
        title_ar="توقيت مناسب",
        title_en="Appropriate Timing",
        description_ar="لا ترسل قبل ٨ صباحاً ولا بعد ٩ مساءً. رمضان: يفضل بعد الإفطار.",
        description_en="Do not send before 8am or after 9pm. Ramadan: prefer after Iftar.",
        category="timing",
    ),
    WhatsAppRule(
        rule_id="w6",
        title_ar="أوقات الصلاة",
        title_en="Prayer Times",
        description_ar="تجنب الإرسال في أوقات الصلاة (قبل وبعد ١٥ دقيقة).",
        description_en="Avoid sending during prayer times (±15 minutes).",
        category="timing",
    ),
    WhatsAppRule(
        rule_id="w7",
        title_ar="الجمعة",
        title_en="Friday",
        description_ar="الجمعة يوم إجازة في السعودية. تجنب الإرسال من ١١:٣٠ صباحاً إلى ٢:٠٠ مساءً (وقت صلاة الجمعة).",
        description_en="Friday is a holiday in Saudi. Avoid 11:30am-2:00pm (Friday prayer).",
        category="timing",
    ),
    WhatsAppRule(
        rule_id="w8",
        title_ar="رمضان",
        title_en="Ramadan Adjustment",
        description_ar="في رمضان: وقت الإرسال المناسب بعد الإفطار حتى ١٠ مساءً. تقليل عدد الرسائل.",
        description_en="Ramadan: appropriate time is after Iftar until 10pm. Reduce message frequency.",
        category="timing",
    ),
    WhatsAppRule(
        rule_id="w9",
        title_ar="لا صور عشوائية",
        title_en="No Unsolicited Images",
        description_ar="لا ترسل صوراً أو ملفات بدون طلب العميل أو موافقته المسبقة.",
        description_en="Do not send images or files without client request or prior consent.",
        category="content",
    ),
    WhatsAppRule(
        rule_id="w10",
        title_ar="إفصاح PDPL",
        title_en="PDPL Disclosure",
        description_ar="أول رسالة بعد جمع البيانات يجب أن تحتوي على إفصاح الخصوصية.",
        description_en="First message after data collection must include privacy disclosure.",
        category="content",
    ),
    WhatsAppRule(
        rule_id="w11",
        title_ar="لا إرسال متكرر",
        title_en="No Spamming",
        description_ar="الحد الأقصى: ٣-٤ رسائل في الأسبوع، مع استجابة العميل يحدد الإيقاع.",
        description_en="Maximum: 3-4 messages per week, client response determines cadence.",
        category="frequency",
    ),
    WhatsAppRule(
        rule_id="w12",
        title_ar="لا إعادة إرسال بعد الرفض",
        title_en="No Resend After Rejection",
        description_ar="إذا رفض العميل أو قال 'لا شكراً'، لا تعاود الإرسال إلا بعد ٣ أشهر على الأقل.",
        description_en="If client rejects or says 'no thanks', do not resend for at least 3 months.",
        category="consent",
    ),
    WhatsAppRule(
        rule_id="w13",
        title_ar="قوائم البث",
        title_en="Broadcast Lists",
        description_ar="استخدم قوائم البث وليس المجموعات. أضف فقط من لديهم موافقة صريحة.",
        description_en="Use broadcast lists, not groups. Only add those with explicit consent.",
        category="content",
    ),
    WhatsAppRule(
        rule_id="w14",
        title_ar="رسالة تعريفية أولاً",
        title_en="Intro Message First",
        description_ar="أول رسالة يجب أن تكون تعريفية وتعرض القيمة وتطلب الإذن بالمتابعة.",
        description_en="First message should be introductory, show value, and ask permission to continue.",
        category="content",
    ),
    WhatsAppRule(
        rule_id="w15",
        title_ar="لغة مهذبة",
        title_en="Polite Language",
        description_ar="لغة مهذبة ورسمية في البداية. يمكن أن تصبح أقل رسمية بعد بناء العلاقة.",
        description_en="Polite and formal initially. Can become less formal as relationship builds.",
        category="content",
    ),
]


@dataclass
class WhatsAppBoundaryCheck:
    """Result of checking WhatsApp communication boundaries."""

    allowed: bool
    blocked_reasons: list[str]
    warnings: list[str]
    applicable_rules: list[str]


def check_whatsapp_boundary(
    relationship: WhatsAppRelationshipType,
    intended_action: str,
    current_hour: int | None = None,
    is_friday: bool = False,
    is_ramadan: bool = False,
    is_prayer_time: bool = False,
    previous_rejection: bool = False,
) -> WhatsAppBoundaryCheck:
    """Check if a WhatsApp action is allowed given boundaries.

    Args:
        relationship: Relationship type with the contact.
        intended_action: The intended action.
        current_hour: Current hour in 24h format (KSA time).
        is_friday: Whether today is Friday.
        is_ramadan: Whether currently in Ramadan.
        is_prayer_time: Whether currently in a prayer time window.
        previous_rejection: Whether the contact previously rejected outreach.

    Returns:
        WhatsAppBoundaryCheck with allow/block decision.
    """
    blocked_reasons: list[str] = []
    warnings: list[str] = []
    applicable_rules: list[str] = [w.rule_id for w in WHATSAPP_RULES]

    # Relationship check
    if relationship == WhatsAppRelationshipType.NONE:
        blocked_reasons.append("لا توجد علاقة سابقة — ممنوع الإرسال البارد")

    # Action check
    allowed_actions = WHATSAPP_ALLOWED_ACTIONS.get(relationship, [])
    if intended_action not in allowed_actions:
        blocked_reasons.append(f"هذا الإجراء ({intended_action}) غير مسموح به لهذا النوع من العلاقة")

    # Timing checks
    if current_hour is not None:
        if current_hour < 8:
            blocked_reasons.append("قبل ٨ صباحاً — خارج وقت التواصل المسموح")
        if current_hour >= 21:
            blocked_reasons.append("بعد ٩ مساءً — خارج وقت التواصل المسموح")

    if is_friday:
        warnings.append("الجمعة — يفضل تجنب الإرسال خاصة وقت صلاة الجمعة")

    if is_ramadan:
        warnings.append("رمضان — قلل عدد الرسائل وراعِ أوقات الإفطار")

    if is_prayer_time:
        warnings.append("وقت صلاة — يفضل الانتظار حتى انتهاء وقت الصلاة")

    if previous_rejection:
        blocked_reasons.append("رفض سابق — لا تعاود الإرسال حالياً")

    allowed = len(blocked_reasons) == 0

    return WhatsAppBoundaryCheck(
        allowed=allowed,
        blocked_reasons=blocked_reasons,
        warnings=warnings,
        applicable_rules=applicable_rules,
    )


def get_whatsapp_intro_template(relationship: WhatsAppRelationshipType) -> str | None:
    """Get appropriate WhatsApp intro template for the relationship type.

    Args:
        relationship: The relationship type.

    Returns:
        Arabic intro template or None if not allowed.
    """
    templates: dict[WhatsAppRelationshipType, str] = {
        WhatsAppRelationshipType.INQUIRY: (
            "وعليكم السلام ورحمة الله وبركاتة {name}،\n"
            "نشكر لتواصلك مع {company}. هذا {sender} من فريق المبيعات.\n"
            "يسعدنا الرد على استفسارك بخصوص {topic}.\n"
            "هل تفضل المتابعة هنا أو عبر البريد الإلكتروني؟"
        ),
        WhatsAppRelationshipType.MEETING: (
            "السلام عليكم {name}،\n"
            "تشرفنا بلقائكم. نرفق لكم ملخص ما تم الاتفاق عليه.\n"
            "نتطلع للتعاون معكم."
        ),
        WhatsAppRelationshipType.CLIENT: (
            "السلام عليكم {name}،\n"
            "نأمل أن كل الأمور على ما يرام.\n"
            "بخصوص {topic}، يسرنا إطلاعكم على آخر المستجدات."
        ),
        WhatsAppRelationshipType.REFERRAL: (
            "السلام عليكم {name}،\n"
            "تواصل معنا {referrer} وأشاد بخبرتكم في {field}.\n"
            "يسعدنا تقديم عرض تعريفي لخدماتنا."
        ),
    }
    return templates.get(relationship)


__all__ = [
    "WHATSAPP_ALLOWED_ACTIONS",
    "WHATSAPP_POSTURE_AR",
    "WHATSAPP_POSTURE_EN",
    "WHATSAPP_RULES",
    "WhatsAppBoundaryCheck",
    "WhatsAppRelationshipType",
    "WhatsAppRule",
    "check_whatsapp_boundary",
    "get_whatsapp_intro_template",
]
