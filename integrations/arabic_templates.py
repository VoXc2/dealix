"""
Arabic email and WhatsApp templates for the Saudi market.
قوالب البريد الإلكتروني والواتساب العربية للسوق السعودي.

Includes:
  - Standard outreach templates (Arabic + English)
  - Ramadan-specific templates with adjusted tone
  - Follow-up sequences (Day 2, Day 5, Day 10)
  - Service delivery notifications
  - Invoice delivery templates
  - PDPL consent templates (covered in pdpl.py)

Style guide:
  - Formal Saudi Khaleeji Arabic (not Egyptian or Levantine)
  - Honorifics: حضرة / الأستاذ / المدير
  - Avoid English loanwords where Arabic equivalent exists
  - Ramadan: warmer, community-focused tone
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


# ── Template Types ─────────────────────────────────────────────────────────

@dataclass
class EmailTemplate:
    """Email template with Arabic and English variants."""

    template_id: str
    subject_ar: str
    subject_en: str
    body_ar: str
    body_en: str
    category: str   # outreach / follow_up / invoice / notification / ramadan
    channel: str = "email"


@dataclass
class WhatsAppTemplate:
    """WhatsApp template with Arabic and English variants."""

    template_id: str
    message_ar: str
    message_en: str
    category: str
    channel: str = "whatsapp"


# ── Outreach Templates ─────────────────────────────────────────────────────

OUTREACH_INITIAL_AR = """السلام عليكم ورحمة الله وبركاته

حضرة {contact_name} المحترم،

أتواصل معكم من فريق {company_name} المتخصص في {service_description}.

لفت انتباهي {trigger_reason}، وأعتقد أن خدماتنا تتوافق تماماً مع احتياجات {buyer_company}.

نحن نساعد شركات مثل شركتكم على {value_proposition}.

هل تودّون تخصيص 15 دقيقة لاستعراض كيف يمكننا دعم مسيرة نمو {buyer_company}؟

مع خالص التقدير والاحترام،
{sender_name}
{company_name}
{phone_number}"""

OUTREACH_INITIAL_EN = """Dear {contact_name},

I'm reaching out from {company_name}, specializing in {service_description}.

I noticed {trigger_reason} and believe our solutions align perfectly with {buyer_company}'s goals.

We help companies like yours {value_proposition}.

Would you be open to a brief 15-minute call to explore how we can support {buyer_company}'s growth?

Best regards,
{sender_name}
{company_name}
{phone_number}"""


# ── Follow-up Templates ────────────────────────────────────────────────────

FOLLOWUP_DAY2_AR = """السلام عليكم {contact_name}،

أتمنى أن تكونوا بخير وعافية.

أردت المتابعة بخصوص رسالتي السابقة حول كيف يمكن لـ {company_name} دعم {buyer_company}.

هل لديكم أي أسئلة أو استفسارات؟ يسعدني الرد في أي وقت.

مع التحية،
{sender_name}"""

FOLLOWUP_DAY5_AR = """مرحباً {contact_name}،

لا أريد الإلحاح عليكم، لكنني أعتقد حقاً أن ما نقدمه في {company_name} يستحق دقيقتين من وقتكم.

لدينا {specific_case_study} حقق نتائج ملموسة لشركة مشابهة لـ {buyer_company}.

هل يمكننا تحديد موعد سريع هذا الأسبوع؟

{booking_link}

شكراً لوقتكم الكريم،
{sender_name}"""

FOLLOWUP_DAY10_AR = """السلام عليكم {contact_name}،

هذه رسالتي الأخيرة حتى لا أُثقل عليكم.

إذا كان التوقيت غير مناسب حالياً، فأهلاً بكم في المستقبل متى شئتم.

لمن أحببتم التواصل مجدداً:
📧 {sender_email}
📱 {phone_number}

أطيب التمنيات لـ {buyer_company} بالتوفيق والنجاح،
{sender_name}"""


# ── Ramadan Templates ──────────────────────────────────────────────────────

RAMADAN_OUTREACH_AR = """رمضان كريم 🌙

حضرة {contact_name} المحترم،

في هذا الشهر الفضيل، يسعدنا أن نتواصل معكم من فريق {company_name}.

نحن نعلم أن رمضان موسم مميز للتأمل والتخطيط للمستقبل. وفي هذا السياق، أود مشاركتكم كيف يمكن لـ {company_name} دعم أهداف {buyer_company} للعام القادم.

{value_proposition}

كل عام وأنتم بألف خير، وتقبّل الله منكم الصيام والقيام.

{sender_name}
{company_name}"""

RAMADAN_FOLLOWUP_AR = """رمضان كريم {contact_name} 🌙

أتمنى أن يكون شهركم مباركاً ومليئاً بالخير.

تواصلت معكم سابقاً حول {topic}، وأودّ أن أعلمكم بأننا خصصنا لعملاء رمضان عرضاً خاصاً يسري حتى نهاية الشهر المبارك.

هل يُتيح لكم وقتكم لحديث سريع بعد الإفطار؟

تقبّل الله صيامكم وقيامكم،
{sender_name}"""

RAMADAN_OUTREACH_EN = """Ramadan Kareem 🌙

Dear {contact_name},

During this blessed month, the team at {company_name} would like to reach out.

Ramadan is a time for reflection and planning ahead. In that spirit, we'd love to share how {company_name} can support {buyer_company}'s goals for the coming year.

{value_proposition}

Wishing you and your team a blessed Ramadan.

{sender_name}
{company_name}"""


# ── Invoice Delivery Templates ─────────────────────────────────────────────

INVOICE_DELIVERY_AR = """السلام عليكم {contact_name}،

يسعدنا إرفاق الفاتورة الإلكترونية الصادرة وفق متطلبات هيئة الزكاة والضريبة والجمارك (ZATCA).

تفاصيل الفاتورة:
• رقم الفاتورة: {invoice_number}
• التاريخ: {issue_date}
• المبلغ الإجمالي: {total_sar} ريال سعودي
• ضريبة القيمة المضافة: {vat_amount} ريال سعودي

لأي استفسار، يرجى التواصل معنا.
شكراً لثقتكم بنا.

{company_name}"""

INVOICE_DELIVERY_EN = """Dear {contact_name},

Please find attached your ZATCA Phase 2 compliant e-invoice.

Invoice Details:
• Invoice Number: {invoice_number}
• Date: {issue_date}
• Total Amount: SAR {total_sar}
• VAT Amount: SAR {vat_amount}

For any queries, please don't hesitate to contact us.
Thank you for your business.

{company_name}"""


# ── WhatsApp Templates ─────────────────────────────────────────────────────

WA_INITIAL_AR = """السلام عليكم {contact_name} 👋

أنا {sender_name} من فريق {company_name}.

لاحظنا {trigger_reason} وأردنا التواصل معكم بخصوص {topic}.

هل يمكننا التحدث لدقائق معدودة؟ 🙏"""

WA_FOLLOWUP_AR = """مرحباً {contact_name} 😊

متابعة لرسالتي السابقة — هل لديكم وقت للحديث عن {topic}؟

يمكنكم حجز موعد سريع هنا:
{booking_link}"""

WA_RAMADAN_AR = """رمضان كريم {contact_name} 🌙

{sender_name} من {company_name}.
{ramadan_message}

تقبّل الله منكم الصيام والقيام 🤲"""

WA_INVOICE_DELIVERY_AR = """السلام عليكم {contact_name} 👋

تم إصدار فاتورتكم الإلكترونية بنجاح ✅

• رقم الفاتورة: {invoice_number}
• المبلغ: {total_sar} ريال
• رمز QR للتحقق مرفق

للاستفسار: {support_phone}
شكراً لثقتكم بنا — {company_name}"""

WA_PRAYER_REMINDER = """تذكير 🕌

أوقات الصلاة اليوم في الرياض:
• الفجر: {fajr}
• الظهر: {dhuhr}
• العصر: {asr}
• المغرب: {maghrib}
• العشاء: {isha}

لن نرسل رسائل تجارية خلال أوقات الصلاة."""


# ── Template Registry ──────────────────────────────────────────────────────

EMAIL_TEMPLATES: dict[str, EmailTemplate] = {
    "outreach_initial": EmailTemplate(
        template_id="outreach_initial",
        subject_ar="تواصل من {company_name} — فرصة تعاون مميزة",
        subject_en="Partnership Opportunity from {company_name}",
        body_ar=OUTREACH_INITIAL_AR,
        body_en=OUTREACH_INITIAL_EN,
        category="outreach",
    ),
    "followup_day2": EmailTemplate(
        template_id="followup_day2",
        subject_ar="متابعة — {company_name}",
        subject_en="Following up — {company_name}",
        body_ar=FOLLOWUP_DAY2_AR,
        body_en=FOLLOWUP_DAY2_AR,  # reuse AR for brevity; override in EN context
        category="follow_up",
    ),
    "followup_day5": EmailTemplate(
        template_id="followup_day5",
        subject_ar="دراسة حالة — نتائج ملموسة لشركة مشابهة",
        subject_en="Case Study — Proven results for similar companies",
        body_ar=FOLLOWUP_DAY5_AR,
        body_en=FOLLOWUP_DAY5_AR,
        category="follow_up",
    ),
    "followup_day10": EmailTemplate(
        template_id="followup_day10",
        subject_ar="رسالة أخيرة من {company_name}",
        subject_en="Last note from {company_name}",
        body_ar=FOLLOWUP_DAY10_AR,
        body_en=FOLLOWUP_DAY10_AR,
        category="follow_up",
    ),
    "ramadan_outreach": EmailTemplate(
        template_id="ramadan_outreach",
        subject_ar="رمضان كريم من {company_name} 🌙",
        subject_en="Ramadan Kareem from {company_name} 🌙",
        body_ar=RAMADAN_OUTREACH_AR,
        body_en=RAMADAN_OUTREACH_EN,
        category="ramadan",
    ),
    "ramadan_followup": EmailTemplate(
        template_id="ramadan_followup",
        subject_ar="عرض رمضان الخاص — {company_name}",
        subject_en="Ramadan Special Offer — {company_name}",
        body_ar=RAMADAN_FOLLOWUP_AR,
        body_en=RAMADAN_FOLLOWUP_AR,
        category="ramadan",
    ),
    "invoice_delivery": EmailTemplate(
        template_id="invoice_delivery",
        subject_ar="فاتورتكم الإلكترونية — {invoice_number}",
        subject_en="Your E-Invoice — {invoice_number}",
        body_ar=INVOICE_DELIVERY_AR,
        body_en=INVOICE_DELIVERY_EN,
        category="invoice",
    ),
}

WHATSAPP_TEMPLATES: dict[str, WhatsAppTemplate] = {
    "initial_outreach": WhatsAppTemplate(
        template_id="initial_outreach",
        message_ar=WA_INITIAL_AR,
        message_en=WA_INITIAL_AR,
        category="outreach",
    ),
    "followup": WhatsAppTemplate(
        template_id="followup",
        message_ar=WA_FOLLOWUP_AR,
        message_en=WA_FOLLOWUP_AR,
        category="follow_up",
    ),
    "ramadan": WhatsAppTemplate(
        template_id="ramadan",
        message_ar=WA_RAMADAN_AR,
        message_en=WA_RAMADAN_AR,
        category="ramadan",
    ),
    "invoice_delivery": WhatsAppTemplate(
        template_id="invoice_delivery",
        message_ar=WA_INVOICE_DELIVERY_AR,
        message_en=WA_INVOICE_DELIVERY_AR,
        category="invoice",
    ),
    "prayer_reminder": WhatsAppTemplate(
        template_id="prayer_reminder",
        message_ar=WA_PRAYER_REMINDER,
        message_en=WA_PRAYER_REMINDER,
        category="notification",
    ),
}


# ── Render Helper ──────────────────────────────────────────────────────────

def render_template(
    template_id: str,
    channel: str,
    variables: dict[str, Any],
    locale: str = "ar",
) -> dict[str, str]:
    """
    Render a template by substituting variables.
    يعرض القالب عن طريق استبدال المتغيرات.

    Returns: {"subject": str, "body": str} for email
             {"message": str} for WhatsApp
    """
    if channel == "email":
        tmpl = EMAIL_TEMPLATES.get(template_id)
        if not tmpl:
            raise ValueError(f"Email template '{template_id}' not found")
        if locale == "ar":
            subject = tmpl.subject_ar.format_map(variables)
            body = tmpl.body_ar.format_map(variables)
        else:
            subject = tmpl.subject_en.format_map(variables)
            body = tmpl.body_en.format_map(variables)
        return {"subject": subject, "body": body, "channel": "email", "locale": locale}

    if channel == "whatsapp":
        tmpl_wa = WHATSAPP_TEMPLATES.get(template_id)
        if not tmpl_wa:
            raise ValueError(f"WhatsApp template '{template_id}' not found")
        if locale == "ar":
            message = tmpl_wa.message_ar.format_map(variables)
        else:
            message = tmpl_wa.message_en.format_map(variables)
        return {"message": message, "channel": "whatsapp", "locale": locale}

    raise ValueError(f"Unknown channel: {channel}. Use 'email' or 'whatsapp'.")


def list_templates(channel: str | None = None) -> list[dict[str, str]]:
    """
    List available templates.
    يسرد القوالب المتاحة.
    """
    result: list[dict[str, str]] = []
    if channel in (None, "email"):
        for tmpl in EMAIL_TEMPLATES.values():
            result.append({
                "template_id": tmpl.template_id,
                "channel": "email",
                "category": tmpl.category,
                "subject_ar": tmpl.subject_ar,
            })
    if channel in (None, "whatsapp"):
        for tmpl in WHATSAPP_TEMPLATES.values():
            result.append({
                "template_id": tmpl.template_id,
                "channel": "whatsapp",
                "category": tmpl.category,
            })
    return result
