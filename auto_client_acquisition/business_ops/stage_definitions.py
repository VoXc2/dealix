"""
Wave 9 - Customer Journey Stage Definitions
22-stage journey from target_identified → case_study_candidate
HARD RULES: no revenue before payment_confirmed, no public proof without permission,
            no delivery without payment, no cold WhatsApp.
"""
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional


class JourneyStage(str, Enum):
    TARGET_IDENTIFIED = "target_identified"
    ICP_QUALIFIED = "icp_qualified"
    WARM_INTRO_DRAFTED = "warm_intro_drafted"
    OUTREACH_APPROVED = "outreach_approved"          # approval_required
    OUTREACH_SENT = "outreach_sent"                  # approved_manual only
    RESPONSE_RECEIVED = "response_received"
    DISCOVERY_SCHEDULED = "discovery_scheduled"
    DISCOVERY_COMPLETED = "discovery_completed"
    FIT_SCORED = "fit_scored"
    OFFER_PRESENTED = "offer_presented"
    PROPOSAL_SENT = "proposal_sent"
    NEGOTIATION = "negotiation"
    VERBAL_AGREEMENT = "verbal_agreement"
    CONTRACT_SENT = "contract_sent"
    CONTRACT_SIGNED = "contract_signed"
    INVOICE_ISSUED = "invoice_issued"
    PAYMENT_CONFIRMED = "payment_confirmed"          # delivery gate
    ONBOARDING_STARTED = "onboarding_started"
    DELIVERY_IN_PROGRESS = "delivery_in_progress"
    DELIVERY_COMPLETED = "delivery_completed"
    RESULT_DOCUMENTED = "result_documented"
    CASE_STUDY_CANDIDATE = "case_study_candidate"   # requires client permission


@dataclass
class StageDefinition:
    stage: JourneyStage
    label_en: str
    label_ar: str
    action_mode: str   # suggest_only / draft_only / approval_required / approved_manual / blocked
    gate_conditions: List[str] = field(default_factory=list)
    exit_conditions: List[str] = field(default_factory=list)
    hard_rules: List[str] = field(default_factory=list)
    owner: str = "founder"
    estimated_days: Optional[int] = None


STAGES: List[StageDefinition] = [
    StageDefinition(
        stage=JourneyStage.TARGET_IDENTIFIED,
        label_en="Target Identified",
        label_ar="تحديد الهدف",
        action_mode="suggest_only",
        gate_conditions=["company name known", "sector known"],
        exit_conditions=["added to pipeline"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.ICP_QUALIFIED,
        label_en="ICP Qualified",
        label_ar="مؤهل ICP",
        action_mode="suggest_only",
        gate_conditions=["target_identified"],
        exit_conditions=["ICP score >= 60", "sector in target_verticals"],
        hard_rules=["no outreach before ICP check"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.WARM_INTRO_DRAFTED,
        label_en="Warm Intro Drafted",
        label_ar="مسودة تعريف دافئ",
        action_mode="draft_only",
        gate_conditions=["icp_qualified"],
        exit_conditions=["draft reviewed by founder"],
        hard_rules=["no cold WhatsApp", "draft only - not sent automatically"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.OUTREACH_APPROVED,
        label_en="Outreach Approved",
        label_ar="الوصول معتمد",
        action_mode="approval_required",
        gate_conditions=["warm_intro_drafted", "founder review"],
        exit_conditions=["founder explicitly approves send"],
        hard_rules=["no auto-send", "approval_required before send"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.OUTREACH_SENT,
        label_en="Outreach Sent",
        label_ar="تم إرسال التواصل",
        action_mode="approved_manual",
        gate_conditions=["outreach_approved"],
        exit_conditions=["confirmation of send"],
        hard_rules=["manual send only", "no WhatsApp cold outreach", "no LinkedIn automation"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.RESPONSE_RECEIVED,
        label_en="Response Received",
        label_ar="تم استلام الرد",
        action_mode="suggest_only",
        gate_conditions=["outreach_sent"],
        exit_conditions=["reply logged"],
        estimated_days=7,
    ),
    StageDefinition(
        stage=JourneyStage.DISCOVERY_SCHEDULED,
        label_en="Discovery Scheduled",
        label_ar="موعد الاكتشاف محدد",
        action_mode="draft_only",
        gate_conditions=["response_received"],
        exit_conditions=["meeting confirmed"],
        estimated_days=3,
    ),
    StageDefinition(
        stage=JourneyStage.DISCOVERY_COMPLETED,
        label_en="Discovery Completed",
        label_ar="اكتشاف مكتمل",
        action_mode="suggest_only",
        gate_conditions=["discovery_scheduled"],
        exit_conditions=["pain points documented", "fit score calculated"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.FIT_SCORED,
        label_en="Fit Scored",
        label_ar="تم تسجيل الملاءمة",
        action_mode="suggest_only",
        gate_conditions=["discovery_completed"],
        exit_conditions=["fit_score calculated", "offer recommended"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.OFFER_PRESENTED,
        label_en="Offer Presented",
        label_ar="تم تقديم العرض",
        action_mode="approval_required",
        gate_conditions=["fit_scored", "fit_score >= 50"],
        exit_conditions=["offer shown to prospect"],
        hard_rules=["no guaranteed claims", "no misleading pricing"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.PROPOSAL_SENT,
        label_en="Proposal Sent",
        label_ar="تم إرسال الاقتراح",
        action_mode="approval_required",
        gate_conditions=["offer_presented"],
        exit_conditions=["proposal document sent"],
        estimated_days=2,
    ),
    StageDefinition(
        stage=JourneyStage.NEGOTIATION,
        label_en="Negotiation",
        label_ar="التفاوض",
        action_mode="suggest_only",
        gate_conditions=["proposal_sent"],
        exit_conditions=["terms agreed or rejected"],
        estimated_days=5,
    ),
    StageDefinition(
        stage=JourneyStage.VERBAL_AGREEMENT,
        label_en="Verbal Agreement",
        label_ar="اتفاق شفهي",
        action_mode="suggest_only",
        gate_conditions=["negotiation"],
        exit_conditions=["verbal yes documented"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.CONTRACT_SENT,
        label_en="Contract Sent",
        label_ar="تم إرسال العقد",
        action_mode="approval_required",
        gate_conditions=["verbal_agreement"],
        exit_conditions=["contract doc sent"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.CONTRACT_SIGNED,
        label_en="Contract Signed",
        label_ar="تم توقيع العقد",
        action_mode="approved_manual",
        gate_conditions=["contract_sent"],
        exit_conditions=["signed doc received"],
        estimated_days=3,
    ),
    StageDefinition(
        stage=JourneyStage.INVOICE_ISSUED,
        label_en="Invoice Issued",
        label_ar="تم إصدار الفاتورة",
        action_mode="approval_required",
        gate_conditions=["contract_signed"],
        exit_conditions=["ZATCA-compliant invoice sent"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.PAYMENT_CONFIRMED,
        label_en="Payment Confirmed",
        label_ar="تم تأكيد الدفع",
        action_mode="approved_manual",
        gate_conditions=["invoice_issued"],
        exit_conditions=["payment verified in system"],
        hard_rules=["delivery blocked until payment_confirmed", "no fake revenue"],
        estimated_days=3,
    ),
    StageDefinition(
        stage=JourneyStage.ONBOARDING_STARTED,
        label_en="Onboarding Started",
        label_ar="بدأ الإعداد",
        action_mode="suggest_only",
        gate_conditions=["payment_confirmed"],
        exit_conditions=["onboarding checklist started"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.DELIVERY_IN_PROGRESS,
        label_en="Delivery In Progress",
        label_ar="التسليم جارٍ",
        action_mode="suggest_only",
        gate_conditions=["onboarding_started"],
        exit_conditions=["delivery milestones tracked"],
        estimated_days=7,
    ),
    StageDefinition(
        stage=JourneyStage.DELIVERY_COMPLETED,
        label_en="Delivery Completed",
        label_ar="التسليم مكتمل",
        action_mode="suggest_only",
        gate_conditions=["delivery_in_progress"],
        exit_conditions=["client accepted deliverables"],
        estimated_days=1,
    ),
    StageDefinition(
        stage=JourneyStage.RESULT_DOCUMENTED,
        label_en="Result Documented",
        label_ar="تم توثيق النتيجة",
        action_mode="suggest_only",
        gate_conditions=["delivery_completed"],
        exit_conditions=["measured outcome recorded"],
        hard_rules=["no fake results", "only real measured data"],
        estimated_days=3,
    ),
    StageDefinition(
        stage=JourneyStage.CASE_STUDY_CANDIDATE,
        label_en="Case Study Candidate",
        label_ar="مرشح دراسة حالة",
        action_mode="approval_required",
        gate_conditions=["result_documented", "client_permission_granted"],
        exit_conditions=["case study draft ready"],
        hard_rules=["no public proof without explicit client permission"],
        estimated_days=7,
    ),
]

STAGE_MAP = {s.stage: s for s in STAGES}


def get_stage(stage: JourneyStage) -> StageDefinition:
    return STAGE_MAP[stage]


def get_stage_index(stage: JourneyStage) -> int:
    for i, s in enumerate(STAGES):
        if s.stage == stage:
            return i
    return -1
