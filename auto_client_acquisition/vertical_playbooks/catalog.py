"""Hand-curated 5-vertical playbook catalog."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class Vertical(StrEnum):
    AGENCY = "agency"
    B2B_SERVICES = "b2b_services"
    SAAS = "saas"
    TRAINING_CONSULTING = "training_consulting"
    LOCAL_SERVICES = "local_services"


@dataclass(frozen=True)
class Playbook:
    vertical: Vertical
    name_ar: str
    name_en: str
    icp_ar: str
    icp_en: str
    common_pains_ar: list[str]
    common_pains_en: list[str]
    best_first_offer_ar: str
    best_first_offer_en: str
    diagnostic_questions_ar: list[str]
    diagnostic_questions_en: list[str]
    safe_channels: list[str]
    forbidden_channels: list[str]
    message_pattern_ar: str
    message_pattern_en: str
    proof_metric: str
    blocked_actions: list[str] = field(default_factory=list)
    upsell_path: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "vertical": self.vertical.value,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "icp_ar": self.icp_ar,
            "icp_en": self.icp_en,
            "common_pains_ar": list(self.common_pains_ar),
            "common_pains_en": list(self.common_pains_en),
            "best_first_offer_ar": self.best_first_offer_ar,
            "best_first_offer_en": self.best_first_offer_en,
            "diagnostic_questions_ar": list(self.diagnostic_questions_ar),
            "diagnostic_questions_en": list(self.diagnostic_questions_en),
            "safe_channels": list(self.safe_channels),
            "forbidden_channels": list(self.forbidden_channels),
            "message_pattern_ar": self.message_pattern_ar,
            "message_pattern_en": self.message_pattern_en,
            "proof_metric": self.proof_metric,
            "blocked_actions": list(self.blocked_actions),
            "upsell_path": self.upsell_path,
        }


_AGENCY = Playbook(
    vertical=Vertical.AGENCY,
    name_ar="وكالة تسويق B2B سعوديّة",
    name_en="Saudi B2B marketing agency",
    icp_ar="وكالات 5-30 موظف، عملاء B2B، تبيع خدمات شهريّة (3K-15K SAR/شهر).",
    icp_en="Agencies 5-30 staff, B2B clients, monthly retainers (3K-15K SAR).",
    common_pains_ar=[
        "متابعة العملاء بطيئة (>4 ساعات)",
        "صعوبة في إثبات ROI للعميل النهائي",
        "كثرة الـ leads المنخفضة الجودة",
        "تكاليف تشغيل عالية مقابل عوائد متوسّطة",
    ],
    common_pains_en=[
        "Slow lead follow-up (>4 hours)",
        "Hard to prove ROI to end-clients",
        "Too many low-quality leads",
        "High ops cost vs average margins",
    ],
    best_first_offer_ar="Pilot 499 ريال (7 أيام) → عرض الردود التلقائيّة + Proof Pack.",
    best_first_offer_en="499 SAR Pilot (7 days) → fast-response drafts + Proof Pack.",
    diagnostic_questions_ar=[
        "كم عميل B2B لديكم حالياً، ومتوسّط حجم العقد الشهري؟",
        "ما متوسّط زمن الردّ على lead جديد؟",
        "ما القناة التي يأتي منها معظم leads (موقع، إعلانات، شراكات)؟",
    ],
    diagnostic_questions_en=[
        "How many B2B clients today + average monthly contract?",
        "Average response time on a new lead?",
        "Where do most leads come from (web, ads, partners)?",
    ],
    safe_channels=["website_form", "email_inbound", "warm_intro", "founder_linkedin_manual"],
    forbidden_channels=["cold_whatsapp", "scraped_linkedin", "purchased_lead_lists"],
    message_pattern_ar=(
        "فتح بسؤال عن قطاع العميل → تأكيد فهم نقطة الألم → عرض القيمة "
        "بالعربيّة → دعوة لمكالمة ٢٠ دقيقة."
    ),
    message_pattern_en=(
        "Open with sector question → confirm pain point → state value in "
        "Arabic-first language → invite a 20-min call."
    ),
    proof_metric="qualified_opportunities_per_pilot_week",
    blocked_actions=["send_cold_whatsapp", "auto_dm_linkedin", "buy_followers"],
    upsell_path="Executive Growth OS 2,999 SAR/mo بعد أوّل Proof Pack موقَّع.",
)

_B2B_SERVICES = Playbook(
    vertical=Vertical.B2B_SERVICES,
    name_ar="خدمات B2B عامّة (محاسبة، استشارات، توظيف)",
    name_en="General B2B services (accounting, consulting, recruitment)",
    icp_ar="مكاتب 10-100 موظف، عملاء شركات، مبيعات تتمّ عبر العلاقات.",
    icp_en="Firms 10-100 staff, corporate clients, sales via relationships.",
    common_pains_ar=[
        "ضعف الوضوح في pipeline الأعمال",
        "اعتماد كامل على شخص واحد للمبيعات",
        "صعوبة في تتبّع متابعات متعدّدة في وقت واحد",
        "بطء توثيق النتائج لاستخدامها مع عملاء جدد",
    ],
    common_pains_en=[
        "Pipeline visibility is weak",
        "Reliance on a single salesperson",
        "Hard to juggle multiple follow-ups",
        "Slow at documenting results to reuse with new clients",
    ],
    best_first_offer_ar="Free Diagnostic 60 دقيقة → خريطة قمع البيع + 3 توصيات تحسين.",
    best_first_offer_en="Free 60-min Diagnostic → pipeline map + 3 improvement recs.",
    diagnostic_questions_ar=[
        "كم عميل في pipeline حالياً، وفي أيّ مرحلة؟",
        "من المسؤول عن المتابعة، وما عدد المتابعات اليوميّة؟",
        "هل تستخدمون نظام CRM؟ ما درجة استخدامه الفعليّة؟",
    ],
    diagnostic_questions_en=[
        "How many pipeline accounts + their current stage?",
        "Who follows up + daily touch volume?",
        "Do you use a CRM? Real adoption rate?",
    ],
    safe_channels=["warm_intro", "email_inbound", "phone_call_requested", "partner_referral"],
    forbidden_channels=["cold_whatsapp", "scraped_linkedin"],
    message_pattern_ar=(
        "افتتاحيّة بمعرفة مشتركة (إن وُجدت) → اقتراح ١٥ دقيقة لتقييم pipeline "
        "→ مشاركة Diagnostic يدوي مجاني."
    ),
    message_pattern_en=(
        "Open with shared connection (if any) → 15-min pipeline review "
        "→ share manual free Diagnostic."
    ),
    proof_metric="pipeline_visibility_score_delta",
    blocked_actions=["send_cold_whatsapp", "auto_dm_linkedin"],
    upsell_path="Data to Revenue 1,500 SAR (one-shot) → Executive Growth OS recurring.",
)

_SAAS = Playbook(
    vertical=Vertical.SAAS,
    name_ar="SaaS B2B سعودي/خليجي",
    name_en="Saudi/Gulf B2B SaaS",
    icp_ar="فِرَق منتج 10-50 شخص، MRR 50K-500K SAR، تبيع لـ SMEs أو enterprise.",
    icp_en="Product teams 10-50, MRR 50K-500K SAR, sell to SMEs or enterprise.",
    common_pains_ar=[
        "تحويل trial → paid منخفض",
        "إعادة الاستخدام بعد الشهر الأول ضعيفة",
        "صعوبة في صياغة نسخة عربيّة تنفيذيّة (ليست MSA)",
        "Onboarding يدوي غير قابل للتوسّع",
    ],
    common_pains_en=[
        "Low trial → paid conversion",
        "Weak month-2 retention",
        "Hard to produce Saudi-executive Arabic copy (not MSA)",
        "Manual onboarding doesn't scale",
    ],
    best_first_offer_ar="Diagnostic مجاني → خريطة activation + 3 درافت إيميل تأهيل.",
    best_first_offer_en="Free Diagnostic → activation map + 3 onboarding email drafts.",
    diagnostic_questions_ar=[
        "ما معدّل تحويل trial → paid حالياً؟",
        "ما متوسّط time-to-first-value للمستخدم؟",
        "هل عندكم نسخة عربيّة تنفيذيّة (ليست MSA حرفيّاً)؟",
    ],
    diagnostic_questions_en=[
        "Current trial → paid conversion rate?",
        "Average time-to-first-value?",
        "Do you have Saudi-executive Arabic copy (not literal MSA)?",
    ],
    safe_channels=[
        "in_product_message",
        "email_inbound",
        "founder_linkedin_manual",
        "warm_intro",
    ],
    forbidden_channels=["cold_whatsapp", "scraped_linkedin"],
    message_pattern_ar=(
        "افتح بإحصائيّة عن سوق SaaS العربي → اربط بنقطة ألم محدّدة → "
        "عرض Diagnostic مجاني."
    ),
    message_pattern_en=(
        "Open with Arab SaaS market stat → tie to specific pain → "
        "offer free Diagnostic."
    ),
    proof_metric="trial_to_paid_conversion_delta",
    blocked_actions=["send_cold_whatsapp", "auto_dm_linkedin", "fake_trial_users"],
    upsell_path="Executive Growth OS 2,999 SAR/mo + Partnership Growth.",
)

_TRAINING_CONSULTING = Playbook(
    vertical=Vertical.TRAINING_CONSULTING,
    name_ar="شركات تدريب/استشارات",
    name_en="Training / consulting firms",
    icp_ar="شركات 3-30 موظف، تبيع programs/ساعات، عملاء شركات أو حكومي.",
    icp_en="Firms 3-30 staff, sell programs/hours, corporate or govt clients.",
    common_pains_ar=[
        "العملاء يطلبون proof قبل التعاقد، ولا يوجد سجل واضح",
        "اعتماد على CEO للمبيعات",
        "صعوبة في تطوير عرض متكرّر بعد الـ pilot الأوّل",
    ],
    common_pains_en=[
        "Clients ask for proof but there's no clean record",
        "CEO-dependent sales",
        "Hard to repeat the offer after a successful first pilot",
    ],
    best_first_offer_ar="Pilot 499 ريال → بناء Proof Pack من 3 جلسات سابقة.",
    best_first_offer_en="499 SAR Pilot → build a Proof Pack from 3 past sessions.",
    diagnostic_questions_ar=[
        "كم برنامج/استشارة سلّمتم آخر 12 شهر؟",
        "ما درجة رضا العملاء (إن وُجدت)؟ هل لديكم cases مكتوبة؟",
        "كيف تتلقّون leads جدد حالياً؟",
    ],
    diagnostic_questions_en=[
        "Programs/consulting engagements delivered last 12 months?",
        "Client satisfaction score (if any)? Written cases?",
        "Where do new leads come from today?",
    ],
    safe_channels=["website_form", "warm_intro", "email_inbound", "phone_call_requested"],
    forbidden_channels=["cold_whatsapp", "scraped_linkedin", "automated_invites"],
    message_pattern_ar=(
        "ابدأ بسؤال عن آخر برنامج سلّموه → اطلب رابط/صورة لمخرجاته → "
        "عرض Pilot لتحويلها إلى Proof Pack."
    ),
    message_pattern_en=(
        "Ask about their last program → request a link/photo of outputs → "
        "offer a Pilot to convert into a Proof Pack."
    ),
    proof_metric="proof_pack_signed_per_quarter",
    blocked_actions=["send_cold_whatsapp", "fake_testimonials"],
    upsell_path="Executive Growth OS 2,999 SAR/mo + Partnership Growth.",
)

_LOCAL_SERVICES = Playbook(
    vertical=Vertical.LOCAL_SERVICES,
    name_ar="خدمات محلّيّة (مطاعم، عيادات، صيانة)",
    name_en="Local services (restaurants, clinics, maintenance)",
    icp_ar="أعمال 3-50 موظف، خدمة محلّيّة، عملاؤها أفراد أو شركات صغيرة.",
    icp_en="Businesses 3-50 staff, local service, B2C or small B2B.",
    common_pains_ar=[
        "ردّ بطيء على واتساب الواردة",
        "ضياع leads لأنّ المتابعة ضعيفة",
        "اعتماد على موقع جوجل دون استراتيجيّة محتوى",
    ],
    common_pains_en=[
        "Slow reply to inbound WhatsApp",
        "Lost leads from weak follow-up",
        "Reliance on Google profile without a content strategy",
    ],
    best_first_offer_ar="Diagnostic مجاني 30 دقيقة → خطّة ردّ سريع + 3 درافت ردود.",
    best_first_offer_en="Free 30-min Diagnostic → fast-reply plan + 3 reply drafts.",
    diagnostic_questions_ar=[
        "كم رسالة واتساب تستلمون يومياً، وكم الردّ يأخذ؟",
        "هل عندكم قائمة عملاء سابقين تواصلتم معهم آخر 90 يوم؟",
        "ما القناة التي تأتي منها أكثر leads (جوجل، إعلانات، إحالة)؟",
    ],
    diagnostic_questions_en=[
        "Daily WhatsApp volume + average reply time?",
        "Past-customer list contacted in the last 90 days?",
        "Top lead source (Google, ads, referrals)?",
    ],
    safe_channels=["whatsapp_inbound_only", "google_business_listing", "warm_referral"],
    forbidden_channels=["cold_whatsapp", "purchased_phone_lists", "scraped_directories"],
    message_pattern_ar=(
        "اعرض قيمة محدّدة في 30 ثانية (مثال: ٤٠٪ من عملاء عيادتك يتركوك "
        "بسبب الردّ البطيء) → اقترح Diagnostic مجاني."
    ),
    message_pattern_en=(
        "State a specific value in 30s (e.g., 40% of clinic patients leave "
        "due to slow reply) → offer a free Diagnostic."
    ),
    proof_metric="reply_time_minutes_p50_delta",
    blocked_actions=["send_cold_whatsapp", "buy_phone_lists", "scrape_local_directories"],
    upsell_path="Growth Starter 990 SAR (after S1) → Executive Growth OS later.",
)


PLAYBOOKS: dict[Vertical, Playbook] = {
    Vertical.AGENCY: _AGENCY,
    Vertical.B2B_SERVICES: _B2B_SERVICES,
    Vertical.SAAS: _SAAS,
    Vertical.TRAINING_CONSULTING: _TRAINING_CONSULTING,
    Vertical.LOCAL_SERVICES: _LOCAL_SERVICES,
}


def list_playbooks() -> list[str]:
    return [v.value for v in Vertical]


def get_playbook(vertical: Vertical | str) -> dict[str, Any]:
    v = vertical if isinstance(vertical, Vertical) else Vertical(vertical)
    return PLAYBOOKS[v].to_dict()


# Common Saudi sector strings → vertical mapping. Used by `recommend_for`
# to bridge between free-text sector input and our static catalog.
_SECTOR_HINTS: dict[str, Vertical] = {
    "agency": Vertical.AGENCY,
    "marketing": Vertical.AGENCY,
    "advertising": Vertical.AGENCY,
    "saas": Vertical.SAAS,
    "software": Vertical.SAAS,
    "tech": Vertical.SAAS,
    "consulting": Vertical.TRAINING_CONSULTING,
    "training": Vertical.TRAINING_CONSULTING,
    "education": Vertical.TRAINING_CONSULTING,
    "restaurant": Vertical.LOCAL_SERVICES,
    "clinic": Vertical.LOCAL_SERVICES,
    "maintenance": Vertical.LOCAL_SERVICES,
    "local": Vertical.LOCAL_SERVICES,
    "accounting": Vertical.B2B_SERVICES,
    "recruitment": Vertical.B2B_SERVICES,
    "legal": Vertical.B2B_SERVICES,
    "logistics": Vertical.B2B_SERVICES,
}


def recommend_for(sector_hint: str) -> dict[str, Any]:
    """Best-effort hint-to-playbook mapping. Falls back to b2b_services
    when the hint doesn't clearly match a vertical."""
    if not sector_hint or not isinstance(sector_hint, str):
        return get_playbook(Vertical.B2B_SERVICES)
    hint_lower = sector_hint.lower()
    for token, vertical in _SECTOR_HINTS.items():
        if token in hint_lower:
            return get_playbook(vertical)
    return get_playbook(Vertical.B2B_SERVICES)


def summary() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "verticals_total": len(Vertical),
        "verticals": [
            {
                "vertical": v.value,
                "name_ar": PLAYBOOKS[v].name_ar,
                "name_en": PLAYBOOKS[v].name_en,
                "first_offer_ar": PLAYBOOKS[v].best_first_offer_ar,
            }
            for v in Vertical
        ],
        "guardrails": {
            "no_cold_outreach": True,
            "no_scraping": True,
            "no_purchased_lists": True,
        },
    }
