"""
Dealix Pricing Service — 3-tier SaaS pricing for the Saudi market.
خدمة التسعير لـ Dealix — 3 مستويات للسوق السعودي.

Tiers:
┌──────────────┬──────────────────────────────────────────────────────────────┐
│ Starter      │ 1,499 ريال/شهر — Salla/Zid SMBs (20-50 موظف)               │
│ Pro          │ 4,999 ريال/شهر — Mid-market (50-200 موظف)                   │
│ Enterprise   │ Custom — ALLaM + Unifonic + KSA hosting + discovery call     │
└──────────────┴──────────────────────────────────────────────────────────────┘

ICP: B2B companies with 20–200 employees in KSA.
Strategy: Salla/Zid first → Starter → upgrade path to Pro/Enterprise.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional


# ── Enums ─────────────────────────────────────────────────────────────────────


class PlanTier(str, Enum):
    """
    Dealix subscription plan tiers.
    مستويات خطط اشتراك Dealix.
    """
    STARTER = "starter"
    PRO = "pro"
    ENTERPRISE = "enterprise"


class BillingCycle(str, Enum):
    """
    Billing cycle options.
    خيارات دورة الفوترة.
    """
    MONTHLY = "monthly"
    ANNUAL = "annual"     # 2 months free (≈ 16.7% discount)


# ── Plan definitions ──────────────────────────────────────────────────────────


@dataclass(frozen=True)
class PlanFeatures:
    """
    Feature set for a Dealix plan.
    مجموعة المميزات لخطة Dealix.
    """
    # Core
    ai_agents: int                  # Number of concurrent AI sales agents
    leads_per_month: int            # Max outbound leads/contacts per month
    whatsapp_messages_per_month: int
    sms_messages_per_month: int

    # Integrations
    salla_integration: bool
    zid_integration: bool
    crm_seats: int                  # CRM user seats included
    api_access: bool

    # AI / LLM
    llm_provider: str               # "openai" | "groq" | "allam" | "all"
    arabic_dialect_support: bool
    saudi_compliance: bool          # PDPL-compliant data storage

    # Infrastructure
    data_residency_ksa: bool        # Data stored in KSA (sovereign)
    dedicated_support: bool
    sla_hours: int                  # Support SLA response time in hours

    # Enterprise only
    custom_llm_model: bool = False
    unifonic_managed: bool = False  # Managed Unifonic account
    allam_access: bool = False      # HUMAIN ALLaM sovereign LLM
    discovery_call: bool = False    # Sales engineering call included
    custom_contract: bool = False


@dataclass(frozen=True)
class Plan:
    """
    A Dealix subscription plan.
    خطة اشتراك Dealix.
    """
    tier: PlanTier
    name_ar: str
    name_en: str
    description_ar: str
    description_en: str

    # Pricing in SAR
    monthly_price_sar: Optional[Decimal]  # None = custom pricing
    annual_price_sar: Optional[Decimal]   # None = custom pricing
    setup_fee_sar: Decimal = Decimal("0")

    # Pricing in halalas (SAR × 100) for Moyasar
    @property
    def monthly_price_halalas(self) -> Optional[int]:
        if self.monthly_price_sar is None:
            return None
        return int(self.monthly_price_sar * 100)

    @property
    def annual_price_halalas(self) -> Optional[int]:
        if self.annual_price_sar is None:
            return None
        return int(self.annual_price_sar * 100)

    @property
    def annual_savings_sar(self) -> Optional[Decimal]:
        """Savings vs paying monthly for 12 months."""
        if self.monthly_price_sar is None or self.annual_price_sar is None:
            return None
        return (self.monthly_price_sar * 12) - self.annual_price_sar

    features: PlanFeatures = field(default_factory=lambda: PlanFeatures(
        ai_agents=0, leads_per_month=0, whatsapp_messages_per_month=0,
        sms_messages_per_month=0, salla_integration=False, zid_integration=False,
        crm_seats=0, api_access=False, llm_provider="", arabic_dialect_support=False,
        saudi_compliance=False, data_residency_ksa=False, dedicated_support=False,
        sla_hours=48,
    ))


# ── Plan catalog ──────────────────────────────────────────────────────────────


PLANS: dict[PlanTier, Plan] = {

    PlanTier.STARTER: Plan(
        tier=PlanTier.STARTER,
        name_ar="Starter — المبتدئ",
        name_en="Starter",
        description_ar=(
            "مثالي للمتاجر الإلكترونية الصغيرة على Salla وزد. "
            "ابدأ أتمتة المبيعات بـ 1,499 ريال شهرياً."
        ),
        description_en=(
            "Ideal for Salla/Zid SMB stores (20–50 employees). "
            "Start automating sales for 1,499 SAR/month."
        ),
        monthly_price_sar=Decimal("1499.00"),
        annual_price_sar=Decimal("14990.00"),   # 2 months free ≈ 1,249/mo
        setup_fee_sar=Decimal("0"),
        features=PlanFeatures(
            ai_agents=1,
            leads_per_month=500,
            whatsapp_messages_per_month=2_000,
            sms_messages_per_month=500,
            salla_integration=True,
            zid_integration=True,
            crm_seats=3,
            api_access=False,
            llm_provider="openai",
            arabic_dialect_support=True,
            saudi_compliance=True,
            data_residency_ksa=False,
            dedicated_support=False,
            sla_hours=48,
        ),
    ),

    PlanTier.PRO: Plan(
        tier=PlanTier.PRO,
        name_ar="Pro — الاحترافي",
        name_en="Pro",
        description_ar=(
            "للشركات المتوسطة (50-200 موظف). "
            "وكلاء مبيعات متعددون، تكاملات متقدمة، وأولوية الدعم."
        ),
        description_en=(
            "For mid-market companies (50–200 employees). "
            "Multi-agent, advanced integrations, priority support."
        ),
        monthly_price_sar=Decimal("4999.00"),
        annual_price_sar=Decimal("49990.00"),   # 2 months free ≈ 4,166/mo
        setup_fee_sar=Decimal("0"),
        features=PlanFeatures(
            ai_agents=5,
            leads_per_month=3_000,
            whatsapp_messages_per_month=15_000,
            sms_messages_per_month=3_000,
            salla_integration=True,
            zid_integration=True,
            crm_seats=15,
            api_access=True,
            llm_provider="openai",
            arabic_dialect_support=True,
            saudi_compliance=True,
            data_residency_ksa=False,
            dedicated_support=False,
            sla_hours=12,
        ),
    ),

    PlanTier.ENTERPRISE: Plan(
        tier=PlanTier.ENTERPRISE,
        name_ar="Enterprise — المؤسسي",
        name_en="Enterprise",
        description_ar=(
            "حلول مخصصة للمؤسسات الكبيرة مع نموذج ALLaM السيادي، "
            "يونيفونيك المُدار، واستضافة في المملكة. تواصل مع فريق المبيعات."
        ),
        description_en=(
            "Custom solutions for large enterprises: ALLaM sovereign LLM, "
            "managed Unifonic, KSA data residency. Contact sales for pricing."
        ),
        monthly_price_sar=None,   # Custom pricing
        annual_price_sar=None,    # Custom pricing
        setup_fee_sar=Decimal("0"),
        features=PlanFeatures(
            ai_agents=999,        # Unlimited
            leads_per_month=999_999,
            whatsapp_messages_per_month=999_999,
            sms_messages_per_month=999_999,
            salla_integration=True,
            zid_integration=True,
            crm_seats=999,
            api_access=True,
            llm_provider="all",
            arabic_dialect_support=True,
            saudi_compliance=True,
            data_residency_ksa=True,
            dedicated_support=True,
            sla_hours=2,
            custom_llm_model=True,
            unifonic_managed=True,
            allam_access=True,
            discovery_call=True,
            custom_contract=True,
        ),
    ),
}


# ── Pricing service ───────────────────────────────────────────────────────────


class PricingService:
    """
    Dealix pricing logic: plan lookup, billing calculation, upgrade paths.
    منطق التسعير في Dealix: البحث عن الخطة، حساب الفوترة، مسارات الترقية.

    Usage:
        pricing = PricingService()
        plan = pricing.get_plan(PlanTier.STARTER)
        quote = pricing.quote(PlanTier.PRO, BillingCycle.ANNUAL)
        eligible = pricing.is_salla_eligible(PlanTier.STARTER)
    """

    def get_plan(self, tier: PlanTier) -> Plan:
        """
        Get a plan by tier.
        الحصول على خطة بواسطة المستوى.
        """
        plan = PLANS.get(tier)
        if not plan:
            raise ValueError(f"Unknown plan tier: {tier}")
        return plan

    def get_all_plans(self) -> list[Plan]:
        """
        Get all plans sorted by tier.
        الحصول على جميع الخطط مرتبة حسب المستوى.
        """
        return [PLANS[tier] for tier in PlanTier]

    def quote(
        self,
        tier: PlanTier,
        billing_cycle: BillingCycle = BillingCycle.MONTHLY,
    ) -> dict:
        """
        Generate a pricing quote for a plan.
        إنشاء عرض سعر لخطة.

        Returns:
            dict with pricing details, features, and Moyasar-ready amount in halalas
        """
        plan = self.get_plan(tier)

        if tier == PlanTier.ENTERPRISE:
            return {
                "tier": tier.value,
                "plan_name_ar": plan.name_ar,
                "plan_name_en": plan.name_en,
                "billing_cycle": billing_cycle.value,
                "price_sar": None,
                "price_halalas": None,
                "pricing_type": "custom",
                "contact_url": "https://dealix.sa/contact-sales",
                "discovery_call": True,
                "description_ar": plan.description_ar,
                "description_en": plan.description_en,
            }

        if billing_cycle == BillingCycle.ANNUAL:
            price_sar = plan.annual_price_sar
            price_halalas = plan.annual_price_halalas
            savings = plan.annual_savings_sar
        else:
            price_sar = plan.monthly_price_sar
            price_halalas = plan.monthly_price_halalas
            savings = None

        return {
            "tier": tier.value,
            "plan_name_ar": plan.name_ar,
            "plan_name_en": plan.name_en,
            "billing_cycle": billing_cycle.value,
            "price_sar": float(price_sar) if price_sar else None,
            "price_halalas": price_halalas,
            "pricing_type": "fixed",
            "annual_savings_sar": float(savings) if savings else None,
            "description_ar": plan.description_ar,
            "description_en": plan.description_en,
            "features": {
                "ai_agents": plan.features.ai_agents,
                "leads_per_month": plan.features.leads_per_month,
                "whatsapp_messages_per_month": plan.features.whatsapp_messages_per_month,
                "sms_messages_per_month": plan.features.sms_messages_per_month,
                "salla_integration": plan.features.salla_integration,
                "zid_integration": plan.features.zid_integration,
                "crm_seats": plan.features.crm_seats,
                "api_access": plan.features.api_access,
                "llm_provider": plan.features.llm_provider,
                "arabic_dialect_support": plan.features.arabic_dialect_support,
                "saudi_compliance": plan.features.saudi_compliance,
                "data_residency_ksa": plan.features.data_residency_ksa,
                "dedicated_support": plan.features.dedicated_support,
                "sla_hours": plan.features.sla_hours,
                "allam_access": plan.features.allam_access,
            },
        }

    def is_salla_eligible(self, tier: PlanTier) -> bool:
        """
        Check if a plan includes Salla integration.
        التحقق مما إذا كانت الخطة تشمل تكامل Salla.
        """
        return PLANS[tier].features.salla_integration

    def is_zid_eligible(self, tier: PlanTier) -> bool:
        """
        Check if a plan includes Zid integration.
        التحقق مما إذا كانت الخطة تشمل تكامل زد.
        """
        return PLANS[tier].features.zid_integration

    def has_allam_access(self, tier: PlanTier) -> bool:
        """
        Check if a plan includes ALLaM sovereign LLM access.
        التحقق مما إذا كانت الخطة تشمل وصولاً لنموذج ALLaM.

        Only Enterprise tier includes ALLaM by default.
        خطة المؤسسي فقط تشمل ALLaM بشكل افتراضي.
        """
        return PLANS[tier].features.allam_access

    def upgrade_path(self, current_tier: PlanTier) -> Optional[Plan]:
        """
        Get the next upgrade tier for a plan.
        الحصول على مستوى الترقية التالي للخطة.

        Returns None if already at top tier (Enterprise).
        يرجع None إذا كانت الخطة الحالية هي الأعلى.
        """
        tiers = list(PlanTier)
        current_idx = tiers.index(current_tier)
        if current_idx + 1 < len(tiers):
            return PLANS[tiers[current_idx + 1]]
        return None

    def calculate_proration(
        self,
        current_tier: PlanTier,
        new_tier: PlanTier,
        days_remaining: int,
        days_in_cycle: int = 30,
    ) -> dict:
        """
        Calculate prorated upgrade credit/charge.
        حساب الرسوم أو الرصيد النسبي عند ترقية الخطة.

        Args:
            current_tier: Current plan
            new_tier: Target upgrade plan
            days_remaining: Days left in current billing cycle
            days_in_cycle: Total days in cycle (default: 30)

        Returns:
            dict with credit_sar, charge_sar, net_sar
        """
        current_plan = self.get_plan(current_tier)
        new_plan = self.get_plan(new_tier)

        if current_plan.monthly_price_sar is None or new_plan.monthly_price_sar is None:
            return {
                "proration_type": "custom",
                "message": "Enterprise pricing requires manual calculation",
                "contact_url": "https://dealix.sa/contact-sales",
            }

        daily_current = current_plan.monthly_price_sar / days_in_cycle
        daily_new = new_plan.monthly_price_sar / days_in_cycle

        credit_sar = daily_current * days_remaining
        charge_sar = daily_new * days_remaining
        net_sar = charge_sar - credit_sar

        return {
            "proration_type": "calculated",
            "current_tier": current_tier.value,
            "new_tier": new_tier.value,
            "days_remaining": days_remaining,
            "credit_sar": float(round(credit_sar, 2)),
            "charge_sar": float(round(charge_sar, 2)),
            "net_charge_sar": float(round(net_sar, 2)),
            "net_charge_halalas": int(net_sar * 100),
        }

    def pricing_table(self) -> list[dict]:
        """
        Returns a structured pricing table for all plans.
        إرجاع جدول تسعير منظم لجميع الخطط.

        Suitable for rendering a pricing page or API response.
        مناسب لعرض صفحة التسعير أو استجابة API.
        """
        return [self.quote(tier) for tier in PlanTier]


# ── Singleton ─────────────────────────────────────────────────────────────────

_pricing_service: Optional[PricingService] = None


def get_pricing_service() -> PricingService:
    """
    FastAPI dependency / singleton accessor.
    اعتمادية FastAPI / وصول للـ Singleton.

    Usage:
        @router.get("/pricing")
        async def get_pricing(pricing: PricingService = Depends(get_pricing_service)):
            return pricing.pricing_table()
    """
    global _pricing_service
    if _pricing_service is None:
        _pricing_service = PricingService()
    return _pricing_service
