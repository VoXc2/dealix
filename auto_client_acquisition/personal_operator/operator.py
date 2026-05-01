"""Arabic Personal Strategic Operator core.

This module powers a Boardy-style operator for Sami, but specialized for Dealix:
- Arabic-first daily strategic brief
- relationship and intro suggestions
- accept / skip / draft / schedule actions
- project-aware next steps
- safe execution guardrails
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from enum import StrEnum
from typing import Any
from uuid import uuid4


class OpportunityType(StrEnum):
    CUSTOMER = "customer"
    PARTNER = "partner"
    ADVISOR = "advisor"
    INVESTOR = "investor"
    TALENT = "talent"
    MEDIA = "media"
    TECHNICAL = "technical"
    INTERNAL_PROJECT = "internal_project"


class ApprovalDecision(StrEnum):
    ACCEPT = "accept"
    SKIP = "skip"
    DRAFT = "draft"
    SCHEDULE = "schedule"
    NEEDS_RESEARCH = "needs_research"


@dataclass(frozen=True)
class OperatorProfile:
    user_id: str
    name: str
    language: str = "ar"
    timezone: str = "Asia/Riyadh"
    primary_goal: str = "Launch Dealix as the Saudi B2B Revenue OS"
    style: str = "direct, strategic, Arabic-first, execution-focused"
    preferred_channels: list[str] = field(default_factory=lambda: ["whatsapp", "gmail", "calendar", "github"])
    current_priorities: list[str] = field(default_factory=list)
    avoid: list[str] = field(default_factory=lambda: ["cold WhatsApp without opt-in", "auto LinkedIn DM", "sending without approval"])


@dataclass(frozen=True)
class StrategicOpportunity:
    title: str
    opportunity_type: OpportunityType
    person_or_company: str
    why_now: str
    strategic_value: str
    recommended_action: str
    suggested_message_ar: str
    risk_notes: list[str] = field(default_factory=list)
    evidence: list[str] = field(default_factory=list)
    score: int = 70
    id: str = field(default_factory=lambda: f"opp_{uuid4().hex[:12]}")

    def to_card(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "type": self.opportunity_type.value,
            "person_or_company": self.person_or_company,
            "score": self.score,
            "why_now": self.why_now,
            "strategic_value": self.strategic_value,
            "recommended_action": self.recommended_action,
            "message_ar": self.suggested_message_ar,
            "risk_notes": self.risk_notes,
            "evidence": self.evidence,
            "actions": [
                {"key": ApprovalDecision.ACCEPT.value, "label_ar": "قبول"},
                {"key": ApprovalDecision.SKIP.value, "label_ar": "تخطي"},
                {"key": ApprovalDecision.DRAFT.value, "label_ar": "اكتب رسالة"},
                {"key": ApprovalDecision.SCHEDULE.value, "label_ar": "احجز اجتماع"},
            ],
        }


@dataclass(frozen=True)
class DailyBrief:
    greeting: str
    top_decisions: list[str]
    opportunities: list[StrategicOpportunity]
    risks: list[str]
    launch_readiness: dict[str, Any]
    generated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def to_dict(self) -> dict[str, Any]:
        return {
            "generated_at": self.generated_at.isoformat(),
            "greeting": self.greeting,
            "top_decisions": self.top_decisions,
            "opportunities": [item.to_card() for item in self.opportunities],
            "risks": self.risks,
            "launch_readiness": self.launch_readiness,
        }


def default_sami_profile() -> OperatorProfile:
    return OperatorProfile(
        user_id="sami",
        name="سامي",
        current_priorities=[
            "Merge v3 Autonomous Revenue OS foundation",
            "Build Arabic Personal Operator with Accept/Skip flow",
            "Launch private beta for Saudi B2B founders",
            "Connect Supabase project memory and WhatsApp approvals",
        ],
    )


def suggest_opportunities(profile: OperatorProfile | None = None) -> list[StrategicOpportunity]:
    profile = profile or default_sami_profile()
    return [
        StrategicOpportunity(
            title="تشغيل بوتك الشخصي العربي",
            opportunity_type=OpportunityType.INTERNAL_PROJECT,
            person_or_company="Dealix Personal Operator",
            why_now="لأن PR v3 صار عنده Revenue Memory وProject Intelligence، والطبقة الناقصة الآن هي واجهة تنفيذ شخصية لك.",
            strategic_value="يحول Dealix من نظام داخلي إلى مساعد يومي يقرر ويقترح وينفذ بموافقتك.",
            recommended_action="اعتمد بناء Personal Operator كأول تجربة تشغيلية قبل بيعها للعملاء.",
            suggested_message_ar="ابدأ بتشغيل النسخة الأولى: daily brief + فرص استراتيجية + قبول/تخطي + draft للرسائل.",
            risk_notes=["لا ترسل أي رسالة خارجية تلقائياً قبل الموافقة", "ابدأ بـ Gmail draft وCalendar draft فقط"],
            evidence=["Revenue Memory موجود", "Project Intelligence موجود", "v3 API router موجود"],
            score=96,
        ),
        StrategicOpportunity(
            title="إطلاق Private Beta محدود",
            opportunity_type=OpportunityType.CUSTOMER,
            person_or_company="10 مؤسسين B2B سعوديين",
            why_now="المنتج صار لديه قصة واضحة: Saudi Revenue OS + Personal Operator + Market Radar.",
            strategic_value="يجلب feedback حقيقي وcase studies قبل الإطلاق العام.",
            recommended_action="جهز قائمة 10 مؤسسين وابدأ بدعوة شخصية مع وعد واضح: 7 أيام لاكتشاف فرص نمو.",
            suggested_message_ar="أبغى أعطيك وصول مبكر لتجربة Dealix: نظام يكتشف فرص B2B ويقترح لك next actions بالعربي. هل يناسبك نجربه 7 أيام؟",
            risk_notes=["لا توسع قبل وجود onboarding واضح", "لا تعد بنتائج مضمونة قبل قياس pilot"],
            evidence=["Command Center snapshot", "Market Radar demo", "Revenue Science forecast"],
            score=91,
        ),
        StrategicOpportunity(
            title="شريك Supabase/DevOps لإغلاق جاهزية الإنتاج",
            opportunity_type=OpportunityType.TECHNICAL,
            person_or_company="Supabase/Postgres engineer",
            why_now="أضفنا schema للـ project memory، والمرحلة القادمة تحتاج تنفيذ embeddings/jobs/RLS بشكل production.",
            strategic_value="يقلل مخاطر البيانات والـ launch ويجعل البوت يفهم المشروع فعلياً.",
            recommended_action="ابحث عن مهندس Supabase/pgvector لمراجعة migration وRLS وembedding pipeline.",
            suggested_message_ar="أبغى رأيك التقني في schema لـ Supabase/pgvector لمشروع AI Revenue OS. هل تقدر تراجع معي readiness خلال 30 دقيقة؟",
            risk_notes=["RLS يجب اختباره قبل بيانات عملاء حقيقية", "لا تخزن أسرار أو tokens داخل embeddings"],
            evidence=["supabase migration added", "project_intelligence.py added"],
            score=88,
        ),
    ]


def launch_readiness_score() -> dict[str, Any]:
    checks = {
        "core_api": 80,
        "revenue_memory": 75,
        "personal_operator": 45,
        "supabase_vector_memory": 55,
        "whatsapp_approval_flow": 35,
        "gmail_calendar_execution": 25,
        "frontend_command_center": 45,
        "tests_ci": 40,
        "observability": 45,
        "security_pdpl": 55,
        "billing_pricing": 50,
        "onboarding": 35,
    }
    score = round(sum(checks.values()) / len(checks), 1)
    stage = "private_beta_ready_after_fixes" if score >= 70 else "foundation_ready_not_launch_ready"
    return {
        "score": score,
        "stage": stage,
        "checks": checks,
        "next_critical_path": [
            "Merge PR #125 after tests",
            "Add Personal Operator persistence + WhatsApp buttons",
            "Connect Supabase embeddings pipeline",
            "Add Gmail draft + Calendar schedule with approval",
            "Ship private beta to 10 founders",
        ],
    }


def build_daily_brief(profile: OperatorProfile | None = None) -> DailyBrief:
    profile = profile or default_sami_profile()
    return DailyBrief(
        greeting=f"صباح الخير {profile.name}. هذا موجزك التنفيذي لليوم.",
        top_decisions=[
            "ادمج PR v3 بعد إضافة اختبارات smoke أساسية.",
            "ابدأ Personal Operator كواجهة التشغيل اليومية قبل أي توسع في الميزات.",
            "لا تطلق عام قبل WhatsApp approval + Gmail draft + Calendar schedule.",
        ],
        opportunities=suggest_opportunities(profile),
        risks=[
            "الخطر الأكبر: كثرة الأدوات بدون workflow إنتاجي واضح.",
            "الخطر الثاني: إرسال رسائل تلقائية قبل ضبط الموافقات والامتثال.",
            "الخطر الثالث: إطلاق عام قبل وجود onboarding وتجربة pilot قابلة للقياس.",
        ],
        launch_readiness=launch_readiness_score(),
    )


def draft_intro_message(opportunity: StrategicOpportunity, tone: str = "warm") -> dict[str, Any]:
    opener = "السلام عليكم" if tone == "formal" else "هلا"
    body = (
        f"{opener}، عندي مشروع اسمه Dealix نبنيه كـ Saudi B2B Revenue OS. "
        f"سبب تواصلي أن {opportunity.why_now} "
        "أبغى آخذ رأيك/نصيحتك بشكل مختصر، وليس عرض بيع طويل. يناسبك مكالمة 20 دقيقة؟"
    )
    return {
        "channel": "gmail_or_whatsapp_after_approval",
        "subject": f"رأيك في Dealix — {opportunity.title}",
        "body_ar": body,
        "approval_required": True,
        "risk_notes": opportunity.risk_notes,
    }


def draft_follow_up(meeting_title: str, outcome: str, next_step: str) -> dict[str, Any]:
    return {
        "subject": f"متابعة: {meeting_title}",
        "body_ar": (
            "شكراً على وقتك اليوم.\n\n"
            f"أبرز ما خرجت به: {outcome}\n"
            f"الخطوة المقترحة: {next_step}\n\n"
            "إذا مناسب، أرسل لك ملخص قصير أو نحدد موعد متابعة الأسبوع القادم."
        ),
        "approval_required": True,
        "recommended_send_window": (datetime.now(UTC) + timedelta(hours=2)).isoformat(),
    }


def apply_decision(opportunity: StrategicOpportunity, decision: ApprovalDecision) -> dict[str, Any]:
    if decision == ApprovalDecision.ACCEPT:
        return {"status": "accepted", "next_action": "draft_message", "message": draft_intro_message(opportunity)}
    if decision == ApprovalDecision.SKIP:
        return {"status": "skipped", "next_action": "learn_preference", "note": "سنقلل فرص مشابهة لاحقاً."}
    if decision == ApprovalDecision.DRAFT:
        return {"status": "draft_ready", "message": draft_intro_message(opportunity)}
    if decision == ApprovalDecision.SCHEDULE:
        return {"status": "schedule_requested", "next_action": "create_calendar_draft", "duration_minutes": 30}
    return {"status": "needs_research", "next_action": "collect_more_context"}
