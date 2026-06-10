"""
Partner Tiers — tier definitions and benefits for the partner program.
مستويات الشركاء — تعريفات المستويات والمزايا لبرنامج الشركاء.
"""

PARTNER_TIERS = {
    "bronze": {
        "commission_rate": 0.10,
        "min_referrals": 0,
        "min_deal_value_sar": 0,
        "features": [
            "10% commission on referrals",
            "Basic white-label portal",
            "Monthly performance report",
            "Email support",
            "Access to partner dashboard",
            "Standard referral links",
        ],
        "benefits_ar": [
            "عمولة 10% على الإحالات",
            "بوابة علامة بيضاء أساسية",
            "تقرير أداء شهري",
            "دعم عبر البريد الإلكتروني",
            "الوصول إلى لوحة تحكم الشريك",
            "روابط إحالة قياسية",
        ],
        "commission_payout": "monthly",
        "support_level": "email",
        "white_label": False,
    },
    "silver": {
        "commission_rate": 0.15,
        "min_referrals": 5,
        "min_deal_value_sar": 50000,
        "features": [
            "15% commission on referrals",
            "White-label portal with custom domain",
            "Weekly performance reports",
            "Priority email & chat support",
            "Co-branded marketing materials",
            "Advanced referral analytics",
            "Quarterly business review",
            "Access to sales enablement kit",
        ],
        "benefits_ar": [
            "عمولة 15% على الإحالات",
            "بوابة علامة بيضاء مع نطاق مخصص",
            "تقارير أداء أسبوعية",
            "دعم ذو أولوية عبر البريد والدردشة",
            "مواد تسويقية مشتركة العلامة",
            "تحليلات إحالة متقدمة",
            "مراجعة أعمال ربع سنوية",
            "الوصول لحزمة تمكين المبيعات",
        ],
        "commission_payout": "biweekly",
        "support_level": "priority",
        "white_label": True,
    },
    "gold": {
        "commission_rate": 0.20,
        "min_referrals": 15,
        "min_deal_value_sar": 200000,
        "features": [
            "20% commission on referrals",
            "Full white-label with custom branding",
            "Real-time performance dashboard",
            "Dedicated partner manager",
            "Joint go-to-market campaigns",
            "Co-branded case studies",
            "Monthly strategic planning",
            "Early access to new features",
            "API access for integration",
            "Invitation to partner events",
        ],
        "benefits_ar": [
            "عمولة 20% على الإحالات",
            "علامة بيضاء كاملة مع علامة تجارية مخصصة",
            "لوحة أداء فورية",
            "مدير شركاء مخصص",
            "حملات تسويق مشتركة",
            "دراسات حالة مشتركة",
            "تخطيط استراتيجي شهري",
            "وصول مبكر للميزات الجديدة",
            "وصول API للتكامل",
            "دعوة لفعاليات الشركاء",
        ],
        "commission_payout": "weekly",
        "support_level": "dedicated",
        "white_label": True,
    },
    "platinum": {
        "commission_rate": 0.25,
        "min_referrals": 30,
        "min_deal_value_sar": 500000,
        "features": [
            "25% commission on referrals",
            "Enterprise white-label solution",
            "Executive dashboard with forecasting",
            "Dedicated success team",
            "Strategic partnership status",
            "Co-investment in marketing",
            "Executive sponsor access",
            "Custom integration support",
            "Revenue sharing opportunities",
            "Board-level reporting",
            "Exclusive partner advisory council",
            "First access to new markets",
        ],
        "benefits_ar": [
            "عمولة 25% على الإحالات",
            "حل علامة بيضاء للمؤسسات",
            "لوحة تنفيذية مع توقعات",
            "فريق نجاح مخصص",
            "شراكة استراتيجية",
            "استثمار مشترك في التسويق",
            "وصول للراعي التنفيذي",
            "دعم تكامل مخصص",
            "فرص تقاسم الإيرادات",
            "تقارير على مستوى مجلس الإدارة",
            "مجلس استشاري حصري للشركاء",
            "وصول أول للأسواق الجديدة",
        ],
        "commission_payout": "daily",
        "support_level": "executive",
        "white_label": True,
    },
}

TIER_ORDER = ["bronze", "silver", "gold", "platinum"]

COMMISSION_RATES = {
    "bronze": 0.10,
    "silver": 0.15,
    "gold": 0.20,
    "platinum": 0.25,
}

MINIMUM_REFERRALS = {
    "bronze": 0,
    "silver": 5,
    "gold": 15,
    "platinum": 30,
}


def get_tier_for_referrals(referral_count: int) -> str:
    for tier in reversed(TIER_ORDER):
        if referral_count >= MINIMUM_REFERRALS[tier]:
            return tier
    return "bronze"


def get_commission_rate(tier: str) -> float:
    return COMMISSION_RATES.get(tier, 0.10)


def get_features(tier: str, locale: str = "en") -> list[str]:
    tier_info = PARTNER_TIERS.get(tier, PARTNER_TIERS["bronze"])
    if locale == "ar":
        return tier_info.get("benefits_ar", tier_info["features"])
    return tier_info["features"]
