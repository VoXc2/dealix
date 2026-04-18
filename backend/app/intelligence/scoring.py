"""
LeadScorer — Explainable Lead Scoring Engine
============================================
Implements the Dealix weighted scoring formula:

  DealixScore = w1·ICP + w2·Intent + w3·Timing + w4·Budget + w5·Authority + w6·Engagement

Each dimension is scored 0-100, then weighted and summed to produce a final 0-100 score.
Full explainability: every contributing factor is logged with its individual contribution.

Formula weights (learnable via feedback loop on closed deals):
  ICP        : 25%  — match with ideal customer profile
  Intent     : 25%  — hiring, funding, tech changes, news
  Timing     : 15%  — recency of signals (last 90 days)
  Budget     : 15%  — revenue proxies + funding + tenders
  Authority  : 10%  — seniority of known contacts
  Engagement : 10%  — interaction with Dealix (emails, WhatsApp, LinkedIn)
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any

from .models import (
    Company,
    Contact,
    DiscoveryCriteria,
    Lead,
    ScoreBreakdown,
    Sector,
    Signal,
    SignalType,
)
from .enrichment import EnrichmentResult


# ─────────────────────────── ICP Profile ─────────────────────────────────────

# Default ICP: Saudi B2B companies with growth signals, digital presence,
# decision-maker access, and budget capacity for SaaS 990-9,990 SAR/month.

ICP_SECTOR_SCORES: dict[Sector, float] = {
    Sector.ECOMMERCE: 100.0,       # Primary target
    Sector.DIGITAL_AGENCY: 95.0,   # Primary target
    Sector.B2B_SAAS: 90.0,         # Primary target
    Sector.REAL_ESTATE: 85.0,      # High value
    Sector.HEALTHCARE: 80.0,       # High margin
    Sector.RETAIL: 70.0,
    Sector.TECHNOLOGY: 75.0,
    Sector.FINANCIAL_SERVICES: 65.0,  # Longer cycle
    Sector.LOGISTICS: 60.0,
    Sector.EDUCATION: 55.0,
    Sector.TELECOM: 50.0,
    Sector.ENERGY: 45.0,
    Sector.GOVERNMENT: 30.0,       # Long cycle, low priority
    Sector.OTHER: 20.0,
}

ICP_SIZE_SCORES: dict[str, float] = {
    "10-49": 70.0,    # Small but growing — likely open to SaaS
    "50-199": 100.0,  # Sweet spot
    "200-499": 95.0,  # Still good
    "500-999": 80.0,  # Enterprise — longer cycle
    "1000+": 50.0,    # Very enterprise
    "1-9": 40.0,      # Too small
}

# Weights for the scoring formula (must sum to 1.0)
SCORE_WEIGHTS = {
    "icp": 0.25,
    "intent": 0.25,
    "timing": 0.15,
    "budget": 0.15,
    "authority": 0.10,
    "engagement": 0.10,
}

SENIORITY_AUTHORITY_SCORES = {
    "c_level": 100.0,
    "vp": 85.0,
    "director": 70.0,
    "manager": 50.0,
    "individual_contributor": 20.0,
}


class LeadScorer:
    """
    محرك تسجيل النقاط — Explainable Lead Scoring Engine.

    يحسب نتيجة من 0 إلى 100 مع شرح كامل لكل عامل.
    Computes a 0-100 score with full per-factor explainability.

    Usage::

        scorer = LeadScorer()
        breakdown = scorer.score(company, enrichment_result)
        print(f"Total: {breakdown.total_score}")
        print(f"Why: {breakdown.score_rationale}")
    """

    def __init__(self, weights: dict[str, float] | None = None) -> None:
        """
        Args:
            weights: تجاوز أوزان الصيغة الافتراضية.
                     يجب أن يكون مجموعها 1.0.
        """
        self.weights = weights or SCORE_WEIGHTS
        self._validate_weights()

    def score(
        self,
        company: Company,
        enrichment_result: EnrichmentResult | None = None,
        engagement_data: dict[str, Any] | None = None,
    ) -> ScoreBreakdown:
        """
        احسب نتيجة Lead الكاملة مع الشرح.

        Args:
            company: الشركة المُثرّاة
            enrichment_result: نتيجة الإثراء (تتضمن الإشارات)
            engagement_data: بيانات تفاعل قناة الاتصال (email opens, WhatsApp reads...)

        Returns:
            ScoreBreakdown كامل مع كل العوامل والشرح.
        """
        contributing: list[str] = []
        penalizing: list[str] = []

        # ── 1. ICP Score ──────────────────────────────────────────────────────
        icp_score, icp_factors = self._score_icp(company)
        contributing.extend([f"ICP: {f}" for f in icp_factors["positive"]])
        penalizing.extend([f"ICP: {f}" for f in icp_factors["negative"]])

        # ── 2. Intent Score ───────────────────────────────────────────────────
        signals = []
        if enrichment_result:
            signals = enrichment_result.signals
        elif company.signals:
            signals = company.signals

        intent_score, intent_factors = self._score_intent(company, signals)
        contributing.extend([f"Intent: {f}" for f in intent_factors["positive"]])
        penalizing.extend([f"Intent: {f}" for f in intent_factors["negative"]])

        # ── 3. Timing Score ───────────────────────────────────────────────────
        timing_score, timing_factors = self._score_timing(company, signals)
        contributing.extend([f"Timing: {f}" for f in timing_factors["positive"]])
        penalizing.extend([f"Timing: {f}" for f in timing_factors["negative"]])

        # ── 4. Budget Score ───────────────────────────────────────────────────
        budget_score, budget_factors = self._score_budget(company)
        contributing.extend([f"Budget: {f}" for f in budget_factors["positive"]])
        penalizing.extend([f"Budget: {f}" for f in budget_factors["negative"]])

        # ── 5. Authority Score ────────────────────────────────────────────────
        authority_score, authority_factors = self._score_authority(company)
        contributing.extend([f"Authority: {f}" for f in authority_factors["positive"]])
        penalizing.extend([f"Authority: {f}" for f in authority_factors["negative"]])

        # ── 6. Engagement Score ───────────────────────────────────────────────
        engagement_score, engagement_factors = self._score_engagement(
            company, engagement_data or {}
        )
        contributing.extend([f"Engagement: {f}" for f in engagement_factors["positive"]])
        penalizing.extend([f"Engagement: {f}" for f in engagement_factors["negative"]])

        # ── Weighted Total ────────────────────────────────────────────────────
        total = (
            self.weights["icp"] * icp_score
            + self.weights["intent"] * intent_score
            + self.weights["timing"] * timing_score
            + self.weights["budget"] * budget_score
            + self.weights["authority"] * authority_score
            + self.weights["engagement"] * engagement_score
        )
        total = round(min(100.0, max(0.0, total)), 1)

        # ── Build Rationale ───────────────────────────────────────────────────
        rationale = self._build_rationale(
            company, total, icp_score, intent_score, timing_score,
            budget_score, authority_score, engagement_score
        )

        return ScoreBreakdown(
            icp_score=round(icp_score, 1),
            intent_score=round(intent_score, 1),
            timing_score=round(timing_score, 1),
            budget_score=round(budget_score, 1),
            authority_score=round(authority_score, 1),
            engagement_score=round(engagement_score, 1),
            total_score=total,
            contributing_signals=contributing[:10],  # Top 10
            penalizing_factors=penalizing[:5],
            score_rationale=rationale,
        )

    def score_lead(
        self,
        lead: Lead,
        enrichment_result: EnrichmentResult | None = None,
    ) -> Lead:
        """
        تحديث نتيجة Lead الكاملة في مكانها وتعيين فئة الأولوية.

        Args:
            lead: كائن Lead المراد تسجيله
            enrichment_result: نتيجة الإثراء

        Returns:
            نفس كائن Lead مع تحديث نتيجة الـ score.
        """
        lead.score = self.score(lead.company, enrichment_result)
        lead.set_priority_tier()
        lead.updated_at = datetime.utcnow()
        return lead

    # ─────────────────────────── Dimension Scorers ───────────────────────────

    def _score_icp(self, company: Company) -> tuple[float, dict[str, list[str]]]:
        """
        نتيجة ICP: مدى تطابق الشركة مع ملف العميل المثالي.

        يقيس:
        - القطاع (الأوزان محددة بناءً على أولوية الربح)
        - حجم الموظفين (Sweet spot: 50-499)
        - الحضور الرقمي (موقع، سوشيال)
        - البيانات الرسمية (سجل تجاري، رقم ضريبي)
        """
        score = 0.0
        positives: list[str] = []
        negatives: list[str] = []

        # Sector score (max 50 pts)
        sector_score = ICP_SECTOR_SCORES.get(company.sector, 20.0)
        score += sector_score * 0.5
        positives.append(f"القطاع: {company.sector.value} ({sector_score:.0f}%)")

        # Size score (max 30 pts)
        emp = company.employee_count or 0
        if 50 <= emp <= 499:
            size_score = 100.0
            positives.append(f"الحجم المثالي: {emp} موظف")
        elif 10 <= emp < 50:
            size_score = 65.0
            positives.append(f"شركة صغيرة: {emp} موظف")
        elif 500 <= emp < 2000:
            size_score = 75.0
            positives.append(f"شركة كبيرة: {emp} موظف")
        elif emp >= 2000:
            size_score = 40.0
            negatives.append(f"شركة ضخمة جداً ({emp}+) — دورة مبيعات طويلة")
        else:
            size_score = 20.0
            negatives.append("عدد الموظفين غير معروف")

        score += size_score * 0.3

        # Digital presence (max 20 pts)
        digital_score = 0.0
        if company.website or company.domain:
            digital_score += 50
            positives.append("لديه موقع إلكتروني")
        if company.social_handles.linkedin:
            digital_score += 30
            positives.append("حضور على LinkedIn")
        if company.tech_stack:
            digital_score += 20
            positives.append(f"تقنيات معروفة: {len(company.tech_stack)} تقنية")

        score += digital_score * 0.2

        return min(100.0, score), {"positive": positives, "negative": negatives}

    def _score_intent(
        self,
        company: Company,
        signals: list[Signal],
    ) -> tuple[float, dict[str, list[str]]]:
        """
        نتيجة Intent: مدى استعداد الشركة للشراء الآن.

        يقيس:
        - تمويل جديد (قوي جداً: بودجة جديدة)
        - توظيف نشط (نمو = بودجة)
        - فوز بمناقصة (بودجة موثّقة)
        - تغيير تقني (نافذة شراء)
        - أخبار إيجابية
        """
        score = 0.0
        positives: list[str] = []
        negatives: list[str] = []

        # From enrichment signals
        for signal in signals:
            contribution = signal.score_contribution

            if signal.signal_type == SignalType.FUNDING:
                score += min(contribution, 40.0)
                positives.append(f"تمويل: {signal.title} (+{contribution:.0f})")

            elif signal.signal_type == SignalType.HIRING:
                score += min(contribution, 20.0)
                positives.append(f"توظيف: {signal.title} (+{contribution:.0f})")

            elif signal.signal_type == SignalType.TENDER_WIN:
                score += min(contribution, 30.0)
                positives.append(f"مناقصة: {signal.title} (+{contribution:.0f})")

            elif signal.signal_type == SignalType.TECH_CHANGE:
                score += min(contribution, 15.0)
                positives.append(f"تقنية: {signal.title} (+{contribution:.0f})")

            elif signal.signal_type == SignalType.EXPANSION:
                score += min(contribution, 20.0)
                positives.append(f"توسع: {signal.title} (+{contribution:.0f})")

            elif signal.signal_type == SignalType.NEWS_MENTION:
                score += min(contribution, 10.0)

            elif signal.signal_type == SignalType.PARTNERSHIP:
                score += min(contribution, 15.0)
                positives.append(f"شراكة: {signal.title} (+{contribution:.0f})")

        # From company data directly
        if company.funding_events:
            recent = [
                f for f in company.funding_events
                if f.announced_at and f.announced_at > datetime.utcnow() - timedelta(days=365)
            ]
            if recent:
                latest = max(recent, key=lambda f: f.announced_at)
                bonus = min(30.0, (latest.amount_usd or 1_000_000) / 1_000_000 * 2)
                score += bonus
                positives.append(f"تمويل حديث: {latest.round_type} (+{bonus:.0f})")

        if company.hiring_signals:
            score += min(20.0, len(company.hiring_signals) * 3)

        if company.tender_wins:
            tender_total = sum(t.value_sar or 0 for t in company.tender_wins)
            if tender_total > 0:
                bonus = min(25.0, 10 + 5 * math.log10(max(tender_total / 1_000_000, 1)))
                score += bonus
                positives.append(f"إجمالي المناقصات: {tender_total:,.0f} ر.س (+{bonus:.0f})")

        if not signals and not company.funding_events and not company.hiring_signals:
            negatives.append("لا توجد إشارات نية واضحة")

        return min(100.0, score), {"positive": positives, "negative": negatives}

    def _score_timing(
        self,
        company: Company,
        signals: list[Signal],
    ) -> tuple[float, dict[str, list[str]]]:
        """
        نتيجة Timing: حداثة الإشارات (آخر 90 يوم = ذروة الاهتمام).

        منطق الحداثة:
        - آخر 30 يوم: 100%
        - 31-60 يوم: 80%
        - 61-90 يوم: 50%
        - أكثر من 90 يوم: 20%
        """
        positives: list[str] = []
        negatives: list[str] = []

        if not signals:
            negatives.append("لا توجد إشارات حديثة")
            return 10.0, {"positive": positives, "negative": negatives}

        now = datetime.utcnow()
        total_weighted = 0.0
        signal_count = 0

        for signal in signals:
            days_old = (now - signal.detected_at).days

            if days_old <= 30:
                recency = 1.0
            elif days_old <= 60:
                recency = 0.8
            elif days_old <= 90:
                recency = 0.5
            elif days_old <= 180:
                recency = 0.2
            else:
                recency = 0.1

            total_weighted += signal.score_contribution * recency
            signal_count += 1

        if signal_count == 0:
            return 10.0, {"positive": positives, "negative": negatives}

        # Normalize: average weighted contribution → timing score
        avg_weighted = total_weighted / signal_count
        timing_score = min(100.0, avg_weighted * 3)  # Scale factor

        # Most recent signal
        most_recent = min(signals, key=lambda s: (datetime.utcnow() - s.detected_at).days)
        days_ago = (datetime.utcnow() - most_recent.detected_at).days

        if days_ago <= 30:
            positives.append(f"آخر إشارة منذ {days_ago} يوم — فرصة حارة")
        elif days_ago <= 90:
            positives.append(f"آخر إشارة منذ {days_ago} يوم")
        else:
            negatives.append(f"آخر إشارة منذ {days_ago} يوم — أكثر من 90 يوم")

        return timing_score, {"positive": positives, "negative": negatives}

    def _score_budget(self, company: Company) -> tuple[float, dict[str, list[str]]]:
        """
        نتيجة Budget: القدرة المالية المقدّرة للشركة.

        يقيس:
        - الإيرادات المقدّرة (revenue estimate)
        - رأس المال المسجّل
        - إجمالي قيمة المناقصات الحكومية
        - التمويل المُعلن (Funding)
        - عدد الموظفين × متوسط تكلفة الصناعة
        """
        score = 0.0
        positives: list[str] = []
        negatives: list[str] = []

        # Revenue-based scoring
        revenue = company.revenue_estimate_sar or 0
        if revenue > 0:
            # Log scale: 10M SAR → 40pts, 100M → 60pts, 1B → 80pts
            rev_score = min(80.0, 20 + 20 * math.log10(max(revenue / 1_000_000, 1)))
            score += rev_score * 0.5
            positives.append(f"إيرادات مقدّرة: {revenue/1_000_000:.0f}م ر.س")
        else:
            negatives.append("إيرادات غير معروفة")

        # Employee-based proxy (avg 150K SAR/employee/year → budget capacity)
        emp = company.employee_count or 0
        if emp > 0:
            emp_proxy_sar = emp * 150_000
            emp_score = min(60.0, 10 + 15 * math.log10(max(emp / 10, 1)))
            score += emp_score * 0.2
            positives.append(f"قوة عاملة: {emp} موظف (proxy: {emp_proxy_sar/1_000_000:.0f}م ر.س)")

        # Tender wins (proven government budget)
        tender_total = sum(t.value_sar or 0 for t in company.tender_wins)
        if tender_total > 0:
            tender_score = min(80.0, 20 + 20 * math.log10(max(tender_total / 1_000_000, 1)))
            score += tender_score * 0.2
            positives.append(f"مناقصات حكومية: {tender_total/1_000_000:.0f}م ر.س")

        # Recent funding
        recent_funding = [
            f for f in company.funding_events
            if f.announced_at and f.announced_at > datetime.utcnow() - timedelta(days=730)
        ]
        if recent_funding:
            total_usd = sum(f.amount_usd or 0 for f in recent_funding)
            if total_usd > 0:
                fund_score = min(80.0, 20 + 20 * math.log10(max(total_usd / 1_000_000, 1)))
                score += fund_score * 0.1
                positives.append(f"تمويل مُعلن: ${total_usd/1_000_000:.0f}م")

        if score == 0:
            negatives.append("لا توجد بيانات مالية متاحة")
            score = 15.0  # Minimum

        return min(100.0, score), {"positive": positives, "negative": negatives}

    def _score_authority(self, company: Company) -> tuple[float, dict[str, list[str]]]:
        """
        نتيجة Authority: هل نعرف صانعي القرار؟ وما مستواهم؟

        يقيس:
        - وجود جهات اتصال C-level / VP / Director
        - عدد صانعي القرار المعروفين
        - هل لديهم LinkedIn / بريد إلكتروني؟
        """
        score = 0.0
        positives: list[str] = []
        negatives: list[str] = []

        # CEO known
        if company.ceo_name:
            score += 20.0
            positives.append(f"المدير التنفيذي معروف: {company.ceo_name}")

        # Decision makers
        dms = company.decision_makers
        if not dms:
            negatives.append("لا يوجد صانعو قرار معروفون")
            score = max(score, 10.0)
        else:
            # Score based on highest seniority
            max_authority = max(
                SENIORITY_AUTHORITY_SCORES.get(dm.seniority or "individual_contributor", 20.0)
                for dm in dms
            )
            score += max_authority * 0.5
            positives.append(f"أعلى مستوى: {max_authority:.0f}%")

            # Count bonus
            dm_count_score = min(30.0, len(dms) * 10)
            score += dm_count_score
            positives.append(f"{len(dms)} جهة اتصال معروفة")

            # Contact info quality
            with_email = sum(1 for dm in dms if dm.email)
            with_linkedin = sum(1 for dm in dms if dm.linkedin_url)
            if with_email > 0:
                score += 10.0
                positives.append(f"بريد إلكتروني متاح لـ {with_email} جهة")
            if with_linkedin > 0:
                score += 5.0

        return min(100.0, score), {"positive": positives, "negative": negatives}

    def _score_engagement(
        self,
        company: Company,
        engagement_data: dict[str, Any],
    ) -> tuple[float, dict[str, list[str]]]:
        """
        نتيجة Engagement: مستوى التفاعل مع Dealix.

        يقيس:
        - فتح البريد الإلكتروني
        - قراءة رسائل WhatsApp
        - مشاهدة ملفات LinkedIn
        - النقر على الروابط
        - الاستجابة لمحاولات التواصل
        """
        score = 0.0
        positives: list[str] = []
        negatives: list[str] = []

        if not engagement_data:
            negatives.append("لا يوجد تاريخ تفاعل بعد (lead جديد)")
            return 0.0, {"positive": positives, "negative": negatives}

        # Email engagement
        email_opens = engagement_data.get("email_opens", 0)
        if email_opens > 0:
            score += min(20.0, email_opens * 5)
            positives.append(f"فتح {email_opens} بريد إلكتروني")

        email_clicks = engagement_data.get("email_clicks", 0)
        if email_clicks > 0:
            score += min(20.0, email_clicks * 10)
            positives.append(f"نقر على {email_clicks} رابط في البريد")

        # WhatsApp
        wa_reads = engagement_data.get("whatsapp_reads", 0)
        if wa_reads > 0:
            score += min(25.0, wa_reads * 8)
            positives.append(f"قرأ {wa_reads} رسالة WhatsApp")

        wa_replies = engagement_data.get("whatsapp_replies", 0)
        if wa_replies > 0:
            score += min(30.0, wa_replies * 15)
            positives.append(f"ردّ على {wa_replies} رسالة WhatsApp")

        # LinkedIn
        linkedin_views = engagement_data.get("linkedin_profile_views", 0)
        if linkedin_views > 0:
            score += min(15.0, linkedin_views * 5)
            positives.append(f"شاهد الملف على LinkedIn {linkedin_views} مرة")

        return min(100.0, score), {"positive": positives, "negative": negatives}

    # ─────────────────────────── Utils ───────────────────────────────────────

    def _build_rationale(
        self,
        company: Company,
        total: float,
        icp: float,
        intent: float,
        timing: float,
        budget: float,
        authority: float,
        engagement: float,
    ) -> str:
        """بناء شرح موجز لنتيجة التسجيل."""
        tier = "🔴 بارد" if total < 40 else ("🟡 دافئ" if total < 60 else ("🟠 ساخن" if total < 80 else "🔥 حارّ جداً"))

        weakest = min(
            [("ICP", icp), ("Intent", intent), ("Timing", timing),
             ("Budget", budget), ("Authority", authority), ("Engagement", engagement)],
            key=lambda x: x[1]
        )
        strongest = max(
            [("ICP", icp), ("Intent", intent), ("Timing", timing),
             ("Budget", budget), ("Authority", authority), ("Engagement", engagement)],
            key=lambda x: x[1]
        )

        return (
            f"{company.name} | {tier} | إجمالي: {total:.0f}/100\n"
            f"الأقوى: {strongest[0]} ({strongest[1]:.0f}) | "
            f"الأضعف: {weakest[0]} ({weakest[1]:.0f})\n"
            f"ICP:{icp:.0f} Intent:{intent:.0f} Timing:{timing:.0f} "
            f"Budget:{budget:.0f} Authority:{authority:.0f} Engagement:{engagement:.0f}"
        )

    def _validate_weights(self) -> None:
        """التحقق من أن مجموع الأوزان يساوي 1.0."""
        total = sum(self.weights.values())
        if not (0.99 <= total <= 1.01):
            raise ValueError(
                f"Score weights must sum to 1.0, got {total:.3f}. "
                f"Weights: {self.weights}"
            )

    def explain(self, breakdown: ScoreBreakdown) -> str:
        """طباعة شرح قابل للقراءة لنتيجة التسجيل."""
        lines = [
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"  Dealix Score: {breakdown.total_score:.1f} / 100",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            f"  ICP          {breakdown.icp_score:>6.1f}  ×  {self.weights['icp']:.0%}",
            f"  Intent       {breakdown.intent_score:>6.1f}  ×  {self.weights['intent']:.0%}",
            f"  Timing       {breakdown.timing_score:>6.1f}  ×  {self.weights['timing']:.0%}",
            f"  Budget       {breakdown.budget_score:>6.1f}  ×  {self.weights['budget']:.0%}",
            f"  Authority    {breakdown.authority_score:>6.1f}  ×  {self.weights['authority']:.0%}",
            f"  Engagement   {breakdown.engagement_score:>6.1f}  ×  {self.weights['engagement']:.0%}",
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━",
            "  Contributing signals:",
        ]
        for s in breakdown.contributing_signals[:5]:
            lines.append(f"    ✓ {s}")
        if breakdown.penalizing_factors:
            lines.append("  Penalizing factors:")
            for s in breakdown.penalizing_factors[:3]:
                lines.append(f"    ✗ {s}")
        lines.append("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        return "\n".join(lines)
