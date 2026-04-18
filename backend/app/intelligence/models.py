"""
نماذج البيانات لمحرك الاستخبارات — Dealix Lead Intelligence Engine
Data models for the Lead Intelligence Engine (Pydantic v2, Python 3.11+).

Arabic-friendly encoding throughout; all string fields accept full Unicode.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, HttpUrl, field_validator


# ─────────────────────────── Enumerations ───────────────────────────────────


class Sector(str, Enum):
    """القطاعات المستهدفة حسب الأولوية الربحية."""

    ECOMMERCE = "ecommerce"                # تجارة إلكترونية
    DIGITAL_AGENCY = "digital_agency"     # وكالات رقمية
    REAL_ESTATE = "real_estate"           # عقارات
    B2B_SAAS = "b2b_saas"                # برمجيات B2B
    HEALTHCARE = "healthcare"             # رعاية صحية
    FINANCIAL_SERVICES = "financial_services"  # خدمات مالية
    GOVERNMENT = "government"             # حكومي / شبه حكومي
    RETAIL = "retail"                     # تجزئة
    LOGISTICS = "logistics"               # لوجستيات
    EDUCATION = "education"               # تعليم
    TECHNOLOGY = "technology"             # تقنية
    TELECOM = "telecom"                   # اتصالات
    ENERGY = "energy"                     # طاقة
    OTHER = "other"


class Region(str, Enum):
    """المناطق الإدارية في المملكة العربية السعودية."""

    RIYADH = "riyadh"              # الرياض
    MAKKAH = "makkah"              # مكة المكرمة
    MADINAH = "madinah"            # المدينة المنورة
    EASTERN = "eastern"            # المنطقة الشرقية
    ASIR = "asir"                  # عسير
    TABUK = "tabuk"                # تبوك
    QASSIM = "qassim"              # القصيم
    HAIL = "hail"                  # حائل
    JAZAN = "jazan"                # جازان
    NAJRAN = "najran"              # نجران
    BAHA = "baha"                  # الباحة
    NORTHERN_BORDERS = "northern_borders"   # الحدود الشمالية
    JOUF = "jouf"                  # الجوف


class LeadStatus(str, Enum):
    """مراحل دورة حياة الـ lead."""

    NEW = "new"
    ENRICHING = "enriching"
    QUALIFIED = "qualified"
    CONTACTED = "contacted"
    MEETING = "meeting"
    PROPOSAL = "proposal"
    NEGOTIATION = "negotiation"
    CLOSED_WON = "closed_won"
    CLOSED_LOST = "closed_lost"
    DISQUALIFIED = "disqualified"


class EstablishmentType(str, Enum):
    """نوع المنشأة."""

    MICRO = "micro"          # أقل من 5 موظفين
    SMALL = "small"          # 5–49
    MEDIUM = "medium"        # 50–249
    LARGE = "large"          # 250+
    CORPORATION = "corporation"   # شركة مساهمة


class SignalType(str, Enum):
    """أنواع الإشارات البيعية."""

    HIRING = "hiring"                    # توظيف نشط
    FUNDING = "funding"                  # تمويل جديد
    TECH_CHANGE = "tech_change"          # تغيير تقني
    TENDER_WIN = "tender_win"            # فوز بمناقصة
    EXPANSION = "expansion"              # توسع جغرافي
    LEADERSHIP_CHANGE = "leadership_change"  # تغيير قيادي
    NEWS_MENTION = "news_mention"        # ذكر إعلامي
    CONTENT_ENGAGEMENT = "content_engagement"  # تفاعل محتوى
    PRODUCT_LAUNCH = "product_launch"   # إطلاق منتج
    PARTNERSHIP = "partnership"          # شراكة جديدة


# ─────────────────────────── Sub-models ─────────────────────────────────────


class SocialHandles(BaseModel):
    """روابط ومعرّفات وسائل التواصل الاجتماعي."""

    linkedin: str | None = Field(None, description="رابط LinkedIn للشركة")
    twitter: str | None = Field(None, description="معرّف X (Twitter) بدون @")
    instagram: str | None = Field(None, description="معرّف Instagram بدون @")
    youtube: str | None = Field(None, description="رابط قناة YouTube")
    tiktok: str | None = Field(None, description="معرّف TikTok")

    model_config = {"json_encoders": {}, "populate_by_name": True}


class FundingEvent(BaseModel):
    """جولة تمويل."""

    round_type: str = Field(..., description="نوع الجولة: Seed, Series A, Series B…")
    amount_usd: float | None = Field(None, description="المبلغ بالدولار الأمريكي")
    amount_sar: float | None = Field(None, description="المبلغ بالريال السعودي")
    investors: list[str] = Field(default_factory=list, description="أسماء المستثمرين")
    announced_at: datetime | None = None
    source_url: str | None = None


class TenderWin(BaseModel):
    """فوز بمناقصة حكومية (Etimad)."""

    tender_id: str | None = None
    title_ar: str = Field(..., description="عنوان المناقصة بالعربية")
    title_en: str | None = None
    entity: str = Field(..., description="الجهة الحكومية")
    value_sar: float | None = None
    awarded_at: datetime | None = None
    source_url: str | None = None


class HiringSignal(BaseModel):
    """إشارة توظيف."""

    job_title: str
    job_title_ar: str | None = None
    department: str | None = None
    location: str | None = None
    posted_at: datetime | None = None
    source: str = Field(..., description="linkedin_jobs | bayt | taqat | indeed")
    url: str | None = None
    seniority: str | None = Field(None, description="junior | mid | senior | director | vp | c_level")


class NewsEvent(BaseModel):
    """خبر أو حدث إعلامي."""

    headline: str
    headline_ar: str | None = None
    summary: str | None = None
    source_name: str | None = None
    url: str | None = None
    published_at: datetime | None = None
    sentiment: str | None = Field(None, description="positive | neutral | negative")
    signal_type: SignalType | None = None


class Signal(BaseModel):
    """
    إشارة بيعية — وحدة البيانات الأساسية لنظام الـ intent scoring.
    A single intent signal attached to a Company or Lead.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    signal_type: SignalType
    title: str
    description: str | None = None
    score_contribution: float = Field(0.0, ge=0, le=100, description="مساهمة هذه الإشارة في النتيجة الكلية")
    source: str | None = None
    detected_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = {"populate_by_name": True}


# ─────────────────────────── Core Models ────────────────────────────────────


class Contact(BaseModel):
    """
    جهة اتصال (صانع قرار) داخل الشركة.
    Decision-maker / key contact within a target company.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    full_name: str = Field(..., description="الاسم الكامل")
    full_name_ar: str | None = Field(None, description="الاسم بالعربية")
    title: str | None = Field(None, description="المسمى الوظيفي")
    title_ar: str | None = None
    seniority: str | None = Field(
        None,
        description="c_level | vp | director | manager | individual_contributor",
    )
    department: str | None = None
    email: str | None = None
    phone: str | None = Field(None, description="بصيغة E.164 مثل +966501234567")
    linkedin_url: str | None = None
    twitter_handle: str | None = None
    is_decision_maker: bool = False
    is_champion: bool = Field(False, description="هل هو مدافع داخلي عن المشروع؟")
    notes: str | None = None
    enriched_at: datetime | None = None
    source: str | None = None

    @field_validator("phone", mode="before")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Basic Saudi phone normalisation (+966 prefix)."""
        if v is None:
            return v
        v = v.strip().replace(" ", "").replace("-", "")
        if v.startswith("05") and len(v) == 10:
            # 0501234567 → +966501234567 (keep the 5, replace leading 0 with +966)
            return "+966" + v[1:]  # +966 + 501234567 = +966501234567
        return v


class Company(BaseModel):
    """
    بيانات الشركة المستهدفة — الوحدة المركزية في pipeline الاكتشاف.
    Central entity for the discovery + enrichment pipeline.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))

    # ── Identity ──────────────────────────────────────────────────────────
    name: str = Field(..., description="اسم الشركة بالإنجليزية")
    name_ar: str | None = Field(None, description="اسم الشركة بالعربية")
    domain: str | None = Field(None, description="النطاق الإلكتروني مثل example.com")
    website: str | None = None
    logo_url: str | None = None

    # ── Sector & Geography ────────────────────────────────────────────────
    sector: Sector = Sector.OTHER
    sub_sector: str | None = None
    region: Region | None = None
    city: str | None = None
    city_ar: str | None = None
    address: str | None = None

    # ── Official Registration (Saudi) ─────────────────────────────────────
    registration_number: str | None = Field(
        None, description="رقم السجل التجاري (10 أرقام)"
    )
    vat_number: str | None = Field(
        None, description="الرقم الضريبي (VAT) — 15 رقماً يبدأ بـ 3"
    )
    isic_code: str | None = Field(
        None, description="رمز النشاط ISIC الرباعي"
    )
    establishment_type: EstablishmentType | None = None
    founded_year: int | None = None
    capital_sar: float | None = Field(None, description="رأس المال المسجّل بالريال")

    # ── Size & Financials ──────────────────────────────────────────────────
    employee_count: int | None = None
    employee_count_range: str | None = Field(
        None, description="مثل '50-200' أو '200+'"
    )
    revenue_estimate_sar: float | None = Field(
        None, description="تقدير الإيرادات السنوية بالريال"
    )
    gosi_employees: int | None = Field(
        None, description="عدد الموظفين المسجلين في GOSI (proxy موثوق)"
    )

    # ── Contacts ───────────────────────────────────────────────────────────
    ceo_name: str | None = None
    ceo_name_ar: str | None = None
    decision_makers: list[Contact] = Field(default_factory=list)

    # ── Tech & Digital ─────────────────────────────────────────────────────
    tech_stack: list[str] = Field(
        default_factory=list,
        description="التقنيات المكتشفة مثل ['Shopify', 'Klaviyo', 'HubSpot']",
    )
    ecommerce_platform: str | None = Field(
        None, description="Salla | Zid | Shopify | WooCommerce | Magento | Custom"
    )
    crm_platform: str | None = None
    marketing_tools: list[str] = Field(default_factory=list)

    # ── Signals ────────────────────────────────────────────────────────────
    funding_events: list[FundingEvent] = Field(default_factory=list)
    hiring_signals: list[HiringSignal] = Field(default_factory=list)
    tender_wins: list[TenderWin] = Field(default_factory=list)
    last_news_events: list[NewsEvent] = Field(default_factory=list)
    signals: list[Signal] = Field(default_factory=list)

    # ── Social ─────────────────────────────────────────────────────────────
    social_handles: SocialHandles = Field(default_factory=SocialHandles)

    # ── Meta ───────────────────────────────────────────────────────────────
    data_sources: list[str] = Field(
        default_factory=list, description="المصادر التي أثرت هذا السجل"
    )
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    enriched: bool = False

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }


class ScoreBreakdown(BaseModel):
    """
    تفصيل نتيجة التسجيل مع قابلية الشرح.
    Explainable score breakdown — each dimension separately.
    """

    icp_score: float = Field(0.0, ge=0, le=100, description="تطابق مع ICP")
    intent_score: float = Field(0.0, ge=0, le=100, description="نية الشراء")
    timing_score: float = Field(0.0, ge=0, le=100, description="توقيت الإشارات (آخر 90 يوم)")
    budget_score: float = Field(0.0, ge=0, le=100, description="القدرة المالية المقدّرة")
    authority_score: float = Field(0.0, ge=0, le=100, description="مستوى صانعي القرار")
    engagement_score: float = Field(0.0, ge=0, le=100, description="مستوى التفاعل مع Dealix")

    # Weighted total
    total_score: float = Field(0.0, ge=0, le=100, description="النتيجة الإجمالية (0-100)")

    # Explainability
    contributing_signals: list[str] = Field(
        default_factory=list,
        description="الإشارات التي رفعت النتيجة",
    )
    penalizing_factors: list[str] = Field(
        default_factory=list,
        description="العوامل التي خفضت النتيجة",
    )
    score_rationale: str | None = Field(
        None, description="شرح موجز لنتيجة التسجيل"
    )


class Lead(BaseModel):
    """
    Lead مؤهّل — الناتج النهائي لمحرك الاستخبارات.
    A fully enriched + scored lead ready for outreach.
    """

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    company: Company
    primary_contact: Contact | None = None

    # ── Scoring ────────────────────────────────────────────────────────────
    score: ScoreBreakdown = Field(default_factory=ScoreBreakdown)
    priority_tier: str | None = Field(
        None,
        description="hot (80-100) | warm (60-79) | cool (40-59) | cold (<40)",
    )

    # ── Pipeline ──────────────────────────────────────────────────────────
    status: LeadStatus = LeadStatus.NEW
    assigned_agent: str | None = None
    playbook: str | None = None

    # ── Outreach History ──────────────────────────────────────────────────
    outreach_attempts: int = 0
    last_outreach_at: datetime | None = None
    last_response_at: datetime | None = None

    # ── Metadata ──────────────────────────────────────────────────────────
    tags: list[str] = Field(default_factory=list)
    notes: str | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def dealix_score(self) -> float:
        """الوصول السريع للنتيجة الإجمالية."""
        return self.score.total_score

    def set_priority_tier(self) -> None:
        """تحديد فئة الأولوية بناءً على النتيجة الإجمالية."""
        s = self.score.total_score
        if s >= 80:
            self.priority_tier = "hot"
        elif s >= 60:
            self.priority_tier = "warm"
        elif s >= 40:
            self.priority_tier = "cool"
        else:
            self.priority_tier = "cold"

    model_config = {
        "populate_by_name": True,
        "json_encoders": {datetime: lambda v: v.isoformat()},
    }


# ─────────────────────────── Criteria / Filters ─────────────────────────────


class DiscoveryCriteria(BaseModel):
    """
    معايير اكتشاف الـ leads — تُمرَّر إلى IntelligenceOrchestrator.discover().
    Criteria passed to the orchestrator's discover() method.
    """

    sectors: list[Sector] = Field(default_factory=list)
    regions: list[Region] = Field(default_factory=list)
    min_employees: int | None = None
    max_employees: int | None = None
    min_revenue_sar: float | None = None
    isic_codes: list[str] = Field(default_factory=list)
    has_ecommerce: bool | None = None
    keywords: list[str] = Field(
        default_factory=list,
        description="كلمات مفتاحية للبحث في اسم الشركة / النشاط",
    )
    limit: int = Field(50, ge=1, le=500)
    min_score: float = Field(0.0, ge=0, le=100)
