"""Customer Onboarding System — governs the client journey from payment to first value.

Tracks the 5-step onboarding sequence:
1. WELCOME — welcome email + WhatsApp + intake form sent
2. INTAKE — intake session scheduled/completed
3. SETUP — platform access configured
4. FIRST_VALUE — first deliverable approved and delivered
5. ANCHORED — client using system weekly

Constitutional gates:
- APPROVAL_FIRST: all communications drafted for founder approval
- NO_LIVE_SEND: no auto-send without founder action
"""

from __future__ import annotations

import json
import logging
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, Field

log = logging.getLogger(__name__)

ONBOARDING_STAGES = [
    "WELCOME",
    "INTAKE_SCHEDULED",
    "INTAKE_COMPLETED",
    "SETUP",
    "FIRST_VALUE",
    "ANCHORED",
]

# SLA targets per stage (business hours)
STAGE_SLA_HOURS = {
    "WELCOME": 2,           # Within 2 hours of payment
    "INTAKE_SCHEDULED": 24, # Intake call booked within 24 hours
    "INTAKE_COMPLETED": 72, # Call done within 3 business days
    "SETUP": 48,            # Platform access within 48 hours
    "FIRST_VALUE": 168,     # First deliverable in 7 days
    "ANCHORED": 336,        # Client anchored in 14 days
}

INTAKE_QUESTIONS_AR = [
    "ما هو الهدف الرئيسي من هذا البرنامج بالنسبة لك؟",
    "ما هي أكبر نقطة ألم تواجهها الآن في عملياتك؟",
    "كم عدد الـ leads التي تتعامل معها شهرياً؟",
    "ما هو متوسط وقت إغلاق الصفقة لديك؟",
    "هل لديك CRM حالياً؟ أي نظام؟",
    "من في الفريق سيستخدم النتائج؟",
    "ما هو المقياس الذي ستعرف به أن هذا البرنامج نجح؟",
    "ما هي القيود أو الحدود الهامة التي يجب أن نعرفها؟",
]

INTAKE_QUESTIONS_EN = [
    "What is your primary goal from this program?",
    "What is the biggest pain point in your operations right now?",
    "How many leads do you handle per month?",
    "What is your average deal close time?",
    "Do you have a current CRM? Which system?",
    "Who in the team will use the results?",
    "What metric will tell you this program succeeded?",
    "What constraints or boundaries should we know about?",
]


class OnboardingStep(BaseModel):
    stage: str
    status: str  # pending | in_progress | completed | overdue
    started_at: datetime | None = None
    completed_at: datetime | None = None
    sla_deadline: datetime | None = None
    notes: str = ""
    action_required_ar: str = ""
    action_required_en: str = ""


class OnboardingRecord(BaseModel):
    onboarding_id: str = Field(default_factory=lambda: f"onb_{uuid.uuid4().hex[:12]}")
    account_id: str
    company_name: str
    contact_name: str
    contact_phone: str
    service_tier: str  # sprint_499 | data_pack_1500 | managed_ops_2999 | etc
    payment_confirmed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    current_stage: str = "WELCOME"
    steps: list[OnboardingStep] = Field(default_factory=list)

    # Intake data
    intake_session_at: datetime | None = None
    intake_answers: dict[str, str] = Field(default_factory=dict)
    assigned_founder: str = "founder"

    # Communication drafts (approval required before sending)
    welcome_draft_ar: str = ""
    welcome_draft_en: str = ""

    def is_on_track(self) -> bool:
        current_step = self._get_current_step()
        if not current_step or not current_step.sla_deadline:
            return True
        return datetime.now(UTC) <= current_step.sla_deadline

    def _get_current_step(self) -> OnboardingStep | None:
        for step in self.steps:
            if step.stage == self.current_stage:
                return step
        return None

    def to_dict(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class OnboardingOrchestrator:
    """Manages the onboarding journey for new Dealix customers."""

    def create_onboarding(
        self,
        account_id: str,
        company_name: str,
        contact_name: str,
        contact_phone: str,
        service_tier: str,
    ) -> OnboardingRecord:
        """Create a new onboarding record after payment confirmed."""
        now = datetime.now(UTC)

        steps = []
        for stage in ONBOARDING_STAGES:
            sla_hours = STAGE_SLA_HOURS.get(stage, 48)
            sla_deadline = now + timedelta(hours=sla_hours)

            action_ar, action_en = self._get_stage_action(stage, company_name)

            steps.append(OnboardingStep(
                stage=stage,
                status="pending" if stage != "WELCOME" else "in_progress",
                sla_deadline=sla_deadline,
                action_required_ar=action_ar,
                action_required_en=action_en,
            ))

        # Mark first step as started
        steps[0].started_at = now

        record = OnboardingRecord(
            account_id=account_id,
            company_name=company_name,
            contact_name=contact_name,
            contact_phone=contact_phone,
            service_tier=service_tier,
            steps=steps,
            welcome_draft_ar=self._build_welcome_ar(contact_name, company_name, service_tier),
            welcome_draft_en=self._build_welcome_en(contact_name, company_name, service_tier),
        )

        log.info("onboarding_created account=%s tier=%s", account_id, service_tier.replace("\n", "").replace("\r", ""))
        return record

    def advance_stage(self, record: OnboardingRecord, completed_stage: str) -> OnboardingRecord:
        """Mark a stage as completed and advance to next."""
        now = datetime.now(UTC)

        for step in record.steps:
            if step.stage == completed_stage:
                step.status = "completed"
                step.completed_at = now
                break

        # Find next stage
        try:
            current_idx = ONBOARDING_STAGES.index(completed_stage)
            if current_idx + 1 < len(ONBOARDING_STAGES):
                next_stage = ONBOARDING_STAGES[current_idx + 1]
                record.current_stage = next_stage
                for step in record.steps:
                    if step.stage == next_stage:
                        step.status = "in_progress"
                        step.started_at = now
                        break
        except ValueError:  # completed_stage not in ONBOARDING_STAGES — no-op
            pass

        return record

    def get_overdue_steps(self, record: OnboardingRecord) -> list[OnboardingStep]:
        now = datetime.now(UTC)
        return [
            s for s in record.steps
            if s.status in ("pending", "in_progress")
            and s.sla_deadline
            and now > s.sla_deadline
        ]

    def get_intake_form(self) -> dict[str, Any]:
        """Returns the intake session question template."""
        return {
            "questions_ar": INTAKE_QUESTIONS_AR,
            "questions_en": INTAKE_QUESTIONS_EN,
            "duration_minutes": 45,
            "format_ar": "مكالمة فيديو أو هاتف — مدة 45 دقيقة",
            "format_en": "Video or phone call — 45 minutes",
            "instructions_ar": "سجّل الإجابات في ملف الاستلام ثم أضفها إلى نظام التتبع",
            "instructions_en": "Record answers in intake file then add to tracking system",
        }

    def _get_stage_action(self, stage: str, company_name: str) -> tuple[str, str]:
        actions = {
            "WELCOME": (
                f"أرسل رسالة ترحيب + نموذج الاستلام لـ {company_name} بعد الموافقة",
                f"Send welcome message + intake form to {company_name} after approval",
            ),
            "INTAKE_SCHEDULED": (
                f"تأكيد موعد جلسة الاستلام مع {company_name}",
                f"Confirm intake session date with {company_name}",
            ),
            "INTAKE_COMPLETED": (
                "توثيق نتائج الجلسة وبناء خريطة الألم",
                "Document session outcomes and build pain map",
            ),
            "SETUP": (
                "إعداد الوصول للمنصة + تسليم credentials",
                "Configure platform access + deliver credentials",
            ),
            "FIRST_VALUE": (
                "تسليم أول مخرج موافق عليه + قياس النتيجة",
                "Deliver first approved output + measure result",
            ),
            "ANCHORED": (
                "تأكيد الاستخدام الأسبوعي + جدول OKR الشهري",
                "Confirm weekly usage + schedule monthly OKR",
            ),
        }
        return actions.get(stage, ("", ""))

    def _build_welcome_ar(self, contact_name: str, company_name: str, tier: str) -> str:
        tier_names = {
            "sprint_499": "برنامج التحول الأسبوعي",
            "data_pack_1500": "حزمة البيانات",
            "managed_ops_2999": "Managed Ops الأساسي",
            "managed_ops_4999": "Managed Ops المتقدم",
            "custom_ai_15000": "مشروع AI المخصص",
        }
        tier_name = tier_names.get(tier, "برنامج Dealix")
        return f"""مرحباً {contact_name}،

شكراً لثقتك بـ Dealix ✅

تم تأكيد اشتراكك في {tier_name} لـ {company_name}.

الخطوة التالية: جلسة الاستلام (45 دقيقة) — سنحدد الوقت المناسب خلال 24 ساعة.

في هذه الجلسة سنرسم خريطة الألم الدقيقة ونحدد أهداف الأسبوع الأول.

هل تفضل مكالمة فيديو أم هاتف؟

— فريق Dealix

⚠️ ملاحظة: هذه المسودة تتطلب موافقة المؤسس قبل الإرسال"""

    def _build_welcome_en(self, contact_name: str, company_name: str, tier: str) -> str:
        tier_names = {
            "sprint_499": "Weekly Transformation Sprint",
            "data_pack_1500": "Data Intelligence Pack",
            "managed_ops_2999": "Managed Ops Basic",
            "managed_ops_4999": "Managed Ops Advanced",
            "custom_ai_15000": "Custom AI Project",
        }
        tier_name = tier_names.get(tier, "Dealix Program")
        return f"""Hi {contact_name},

Thank you for trusting Dealix ✅

Your {tier_name} subscription for {company_name} has been confirmed.

Next step: Intake session (45 min) — we'll schedule within 24 hours.

In this session, we'll map your exact pain points and set Week 1 goals.

Do you prefer video call or phone?

— Dealix Team

⚠️ Note: This draft requires founder approval before sending"""
