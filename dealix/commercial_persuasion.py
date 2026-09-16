"""Evidence-governed buyer decision planning for Saudi B2B opportunities.

The module composes Commercial Intelligence evidence with the canonical
negotiation engine.  It creates an internal, reviewable persuasion plan; it
does not send messages, expose an unapproved price, or make a commercial
commitment.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any

from dealix.commercial_intelligence import EvidenceLevel, SourcePolicyStatus
from dealix.company_os.negotiation_engine import (
    NegotiationContext,
    build_negotiation_plan,
)


class BuyerRole(StrEnum):
    ECONOMIC_BUYER = "economic_buyer"
    REVENUE_OWNER = "revenue_owner"
    FINANCE = "finance"
    TECHNOLOGY_DATA = "technology_data"
    LEGAL_GOVERNANCE = "legal_governance"
    CHAMPION_END_USER = "champion_end_user"


class EvidenceUse(StrEnum):
    BLOCKED = "blocked"
    HYPOTHESIS_ONLY = "hypothesis_only"
    DISCOVERY_ONLY = "discovery_only"
    CUSTOMER_CONTEXT = "customer_context"
    INTERNAL_OUTCOME = "internal_outcome"
    PUBLISHABLE_PROOF = "publishable_proof"


class PricingDecision(StrEnum):
    CATALOG_RECONCILIATION_REQUIRED = "catalog_reconciliation_required"
    EXPERIMENT_PENDING = "experiment_pending"
    FOUNDER_APPROVED = "founder_approved"


DEFAULT_BUYER_ROLES = tuple(BuyerRole)

_EVIDENCE_RANK = {
    EvidenceLevel.L0_UNKNOWN: 0,
    EvidenceLevel.L1_HYPOTHESIS: 1,
    EvidenceLevel.L2_PUBLIC_SIGNAL: 2,
    EvidenceLevel.L3_FIRST_PARTY: 3,
    EvidenceLevel.L4_VERIFIED: 4,
    EvidenceLevel.L5_MEASURED_OUTCOME: 5,
}
_PUBLISHABLE_PROOF_TYPES = {
    "client_approved_case_study",
    "dealix_measured_outcome",
}
_FORBIDDEN_PROMISE = re.compile(
    r"(?:\bguarantee(?:d)?\b|\b100\s*%\s*(?:roi|return)\b|"
    r"\bdouble\s+(?:your\s+)?revenue\b|نضمن|مضمون(?:ة)?|"
    r"عائد\s*100\s*%|نضاعف\s+(?:لك\s+)?(?:الإيراد|المبيعات))",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class PersuasionEvidence:
    claim: str
    signal_type: str
    evidence_ref: str
    evidence_level: EvidenceLevel
    confidence: int
    source_policy_status: SourcePolicyStatus
    publication_consent_ref: str | None = None
    stale: bool = False

    def __post_init__(self) -> None:
        for field_name in ("claim", "signal_type", "evidence_ref"):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must not be empty")
        if not 0 <= self.confidence <= 100:
            raise ValueError("confidence must be between 0 and 100")


@dataclass(frozen=True)
class BuyerDecisionContext:
    opportunity_id: str
    account_name: str
    opportunity_title: str
    offer_id: str
    objective: str
    metric: str
    proof_target: str
    evidence_level: EvidenceLevel
    opportunity_score: int
    evidence: tuple[PersuasionEvidence, ...]
    buyer_roles: tuple[BuyerRole, ...] = DEFAULT_BUYER_ROLES
    known_objections: tuple[str, ...] = ()
    relationship_permission_state: str = "research_only"
    pricing_decision: PricingDecision = PricingDecision.CATALOG_RECONCILIATION_REQUIRED
    requested_discount_pct: float = 0.0
    non_standard_terms_requested: bool = False

    def __post_init__(self) -> None:
        for field_name in (
            "opportunity_id",
            "account_name",
            "opportunity_title",
            "offer_id",
            "objective",
            "metric",
            "proof_target",
        ):
            if not getattr(self, field_name).strip():
                raise ValueError(f"{field_name} must not be empty")
        if not 0 <= self.opportunity_score <= 100:
            raise ValueError("opportunity_score must be between 0 and 100")
        if not 0 <= self.requested_discount_pct <= 100:
            raise ValueError("requested_discount_pct must be between 0 and 100")
        if not self.buyer_roles:
            raise ValueError("at least one buyer role is required")


@dataclass(frozen=True)
class BuyerDecisionPlan:
    plan_id: str
    opportunity_id: str
    mode: str
    persuasion_thesis_ar: str
    offer_architecture: dict[str, Any]
    truth_map: tuple[dict[str, Any], ...]
    buying_committee: tuple[dict[str, Any], ...]
    objection_responses: tuple[dict[str, Any], ...]
    negotiation: dict[str, Any]
    proof_design: dict[str, Any]
    approval_queue: tuple[dict[str, Any], ...]
    recommended_sequence: tuple[str, ...]
    blockers: tuple[str, ...]
    validation_routes: tuple[str, ...]
    price_included: bool
    external_action_allowed: bool
    external_commitment_made: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_BUYER_FRAMES: dict[BuyerRole, dict[str, Any]] = {
    BuyerRole.ECONOMIC_BUYER: {
        "decision_question_ar": "هل يستحق الخلل التشغيلي تجربة محدودة بقرار توقف أو توسع واضح؟",
        "value_frame_ar": ("قرار تنفيذي مبني على خط أساس ودليل خلال المدة المعتمدة، لا مشروع تحول مفتوح."),
        "questions_ar": (
            "ما القرار الذي تريدون أن يصبح أسهل بعد المدة المعتمدة؟",
            "من يملك قرار التوسع أو الإيقاف بعد ظهور الدليل؟",
        ),
        "proof_required": "executive_before_after_baseline_and_decision_log",
    },
    BuyerRole.REVENUE_OWNER: {
        "decision_question_ar": "أين تتوقف الفرص ومن يملك الخطوة التالية فعلياً؟",
        "value_frame_ar": (
            "رؤية موحدة للفرصة والمالك والخطوة التالية والدليل فوق الأدوات الحالية."
        ),
        "questions_ar": (
            "كم فرصة نشطة لا تحمل مالكاً أو خطوة تالية موثقة؟",
            "كيف تقيسون زمن الاستجابة والمتابعات الفائتة اليوم؟",
        ),
        "proof_required": "pipeline_ownership_and_follow_up_baseline",
    },
    BuyerRole.FINANCE: {
        "decision_question_ar": "هل النطاق والتكلفة وآلية القياس قابلة للمراجعة قبل أي توسع؟",
        "value_frame_ar": (
            "نطاق واحد، سعر معتمد، تكلفة معلومة، ومقارنة قبل/بعد بلا وعد بعائد مضمون."
        ),
        "questions_ar": (
            "ما تكلفة الوقت أو الفرص الضائعة وفق بياناتكم أنتم؟",
            "ما شرط الصرف وما آلية قبول المخرجات والفوترة؟",
        ),
        "proof_required": "approved_price_scope_acceptance_and_cost_baseline",
    },
    BuyerRole.TECHNOLOGY_DATA: {
        "decision_question_ar": "هل يمكن الاختبار فوق الأنظمة الحالية بأقل صلاحية ومسار رجوع؟",
        "value_frame_ar": (
            "طبقة قرار لا تستبدل CRM؛ يبدأ الوصول بقراءة محدودة بعد خريطة بيانات وموافقة."
        ),
        "questions_ar": (
            "ما النظام المصدر وما الحقول الدنيا اللازمة للتجربة؟",
            "من يعتمد الصلاحيات والاحتفاظ والحذف ومسار الرجوع؟",
        ),
        "proof_required": "data_map_access_approval_audit_and_rollback_test",
    },
    BuyerRole.LEGAL_GOVERNANCE: {
        "decision_question_ar": "هل الغرض والصلاحيات والاحتفاظ والمعالجة الخارجية محددة تعاقدياً؟",
        "value_frame_ar": ("غرض محدد، أقل بيانات ممكنة، سجل تدقيق، وموافقات بشرية لكل إجراء حساس."),
        "questions_ar": (
            "من جهة التحكم ومن جهة المعالجة وما الغرض المحدد؟",
            "هل يلزم تقييم أثر أو اتفاقية معالجة أو مراجعة نقل بيانات؟",
        ),
        "proof_required": "counsel_reviewed_data_processing_and_retention_pack",
    },
    BuyerRole.CHAMPION_END_USER: {
        "decision_question_ar": "هل يقل الغموض والعمل المتكرر دون إضافة عبء إداري جديد؟",
        "value_frame_ar": (
            "إجراء يومي واضح يحدد المالك والخطوة التالية ويترك القرار النهائي للإنسان."
        ),
        "questions_ar": (
            "أين تضيع المتابعة في يوم العمل الحقيقي؟",
            "ما التنبيه أو الملخص الذي يختصر عملاً دون أن يزعج الفريق؟",
        ),
        "proof_required": "user_workflow_baseline_and_adoption_feedback",
    },
}


_OBJECTION_PLAYBOOK: dict[str, dict[str, Any]] = {
    "existing_stack": {
        "response_ar": (
            "وجود Odoo أو CRM نقطة قوة؛ Dealix لا يطلب استبداله. السؤال الذي نختبره: "
            "هل كل فرصة لها مالك وخطوة تالية ودليل وقرار في الوقت المناسب؟"
        ),
        "diagnostic_question_ar": "أرني عشر فرص حديثة: كم واحدة بلا مالك أو خطوة تالية موثقة؟",
        "proof_required": "ten_opportunity_workflow_audit",
        "red_line": "no_unverified_integration_or_replacement_claim",
        "approval_required": False,
    },
    "people_vs_process": {
        "response_ar": (
            "قد يكون السبب في الفريق أو العملية أو البيانات. لن نفترض؛ سنفصل الفرضيات بخط "
            "أساس حسب المرحلة والمالك وزمن الاستجابة ثم نختبر تدخلاً واحداً."
        ),
        "diagnostic_question_ar": "هل الخلل يتكرر مع أفراد محددين أم عند مرحلة أو نوع فرصة محدد؟",
        "proof_required": "stage_owner_response_time_baseline",
        "red_line": "no_employee_blame_without_evidence",
        "approval_required": False,
    },
    "price": {
        "response_ar": (
            "لن نعالج اعتراض السعر بخصم عشوائي. نربط النطاق بخط الأساس، ثم نختار: "
            "نطاق أصغر، تنفيذ مرحلي، أو سعر معتمد مقابل التزام واضح."
        ),
        "diagnostic_question_ar": "هل العائق هو الميزانية، توقيت الدفع، أم أن قيمة النطاق لم تُثبت بعد؟",
        "proof_required": "approved_scope_price_and_acceptance_criteria",
        "red_line": "no_discount_without_give_get_and_approval",
        "approval_required": True,
    },
    "guarantee": {
        "response_ar": (
            "لا نضمن إيراداً لا نتحكم في جميع أسبابه. نلتزم بطريقة عمل قابلة للتحقق: "
            "خط أساس، تدخل محدد، قياس، تقرير دليل، ثم قرار توقف أو توسع."
        ),
        "diagnostic_question_ar": "ما المؤشر التشغيلي الذي يمكننا قياسه دون تحويله إلى وعد مالي؟",
        "proof_required": "baseline_intervention_measurement_stop_go",
        "red_line": "no_revenue_roi_or_sales_guarantee",
        "approval_required": True,
    },
    "security_data": {
        "response_ar": (
            "لا يبدأ أي وصول للبيانات قبل تحديد الغرض والحقول الدنيا والصلاحيات والاحتفاظ "
            "ومسار الحذف والرجوع وموافقة أصحاب الصلاحية."
        ),
        "diagnostic_question_ar": "ما البيانات الدنيا التي تكفي لإثبات الفرضية ومن يعتمد الوصول إليها؟",
        "proof_required": "data_map_and_security_review",
        "red_line": "no_security_or_compliance_claim_without_evidence",
        "approval_required": True,
    },
    "in_house_ai": {
        "response_ar": (
            "امتلاك AI داخلي لا يحسم الحوكمة التشغيلية. نقيس من يملك الإجراء، وما الدليل، "
            "وأين الموافقة، وكيف يحدث الرجوع عند الخطأ."
        ),
        "diagnostic_question_ar": "أي إجراء يستطيع نظامكم تنفيذه اليوم، وما سجل دليله وموافقته؟",
        "proof_required": "action_ownership_approval_and_audit_map",
        "red_line": "no_claim_that_ai_replaces_the_team",
        "approval_required": False,
    },
    "authority": {
        "response_ar": (
            "يمكننا تجهيز تشخيص ومسودة نطاق، لكن لا نلتزم بسعر أو عقد أو وصول بيانات "
            "دون صاحب القرار والمراجعين المختصين."
        ),
        "diagnostic_question_ar": "من يملك القرار التجاري ومن يراجع البيانات والعقد؟",
        "proof_required": "buying_committee_and_decision_process",
        "red_line": "no_commitment_without_authority",
        "approval_required": True,
    },
    "timing": {
        "response_ar": (
            "نخفض مخاطرة الوقت بتجربة بمدة خاصة بالعميل لعملية واحدة، بمعايير دخول وخروج وقرار "
            "أسبوعي؛ لا نبدأ تحولاً مفتوحاً."
        ),
        "diagnostic_question_ar": "ما الموعد الذي يجعل قراراً موثقاً مفيداً لكم فعلياً؟",
        "proof_required": "mutually_approved_30_day_workplan",
        "red_line": "no_unapproved_start_or_delivery_commitment",
        "approval_required": False,
    },
    "competitor": {
        "response_ar": (
            "نقارن على معيار القرار لا على الشعارات: مصدر الدليل، وضوح الصلاحيات، سرعة "
            "الوصول لخط أساس، وقابلية التوقف والرجوع."
        ),
        "diagnostic_question_ar": "ما معايير المقارنة الثلاثة التي ستحدد القرار لديكم؟",
        "proof_required": "buyer_owned_evaluation_scorecard",
        "red_line": "no_defamation_or_unverified_competitor_claim",
        "approval_required": False,
    },
    "unclassified": {
        "response_ar": (
            "قبل الرد بحجة جاهزة، نحتاج فهم الاعتراض: هل يتعلق بالقيمة أم الدليل أم "
            "المخاطر أم الصلاحية أم التوقيت؟"
        ),
        "diagnostic_question_ar": "ما الذي يجب أن يصبح واضحاً حتى تستطيعوا اتخاذ الخطوة التالية؟",
        "proof_required": "objection_classification_and_first_party_validation",
        "red_line": "no_assumption_presented_as_fact",
        "approval_required": False,
    },
}


def classify_evidence(item: PersuasionEvidence) -> EvidenceUse:
    """Classify evidence by safe customer-facing use."""
    if item.source_policy_status is SourcePolicyStatus.BLOCKED:
        return EvidenceUse.BLOCKED
    if _FORBIDDEN_PROMISE.search(item.claim):
        return EvidenceUse.BLOCKED
    if item.stale or item.source_policy_status in {
        SourcePolicyStatus.RESEARCH_ONLY,
        SourcePolicyStatus.REVIEW_REQUIRED,
    }:
        return EvidenceUse.DISCOVERY_ONLY
    if item.evidence_level in {EvidenceLevel.L0_UNKNOWN, EvidenceLevel.L1_HYPOTHESIS}:
        return EvidenceUse.HYPOTHESIS_ONLY
    if item.evidence_level is EvidenceLevel.L2_PUBLIC_SIGNAL:
        return EvidenceUse.DISCOVERY_ONLY
    if item.evidence_level is EvidenceLevel.L5_MEASURED_OUTCOME:
        if item.signal_type in _PUBLISHABLE_PROOF_TYPES:
            return (
                EvidenceUse.PUBLISHABLE_PROOF
                if item.publication_consent_ref
                else EvidenceUse.INTERNAL_OUTCOME
            )
    return EvidenceUse.CUSTOMER_CONTEXT


def _objection_category(text: str) -> str:
    lowered = text.casefold()
    checks = (
        ("existing_stack", ("odoo", "crm", "hubspot", "zoho", "نظامنا", "عندنا نظام")),
        ("people_vs_process", ("الموظف", "الموظفين", "الفريق", "people", "sales team")),
        ("price", ("السعر", "خصم", "ميزانية", "غالي", "أرخص", "price", "discount", "budget")),
        ("guarantee", ("اضمن", "ضمان", "مضمون", "guarantee", "promise", "roi")),
        ("security_data", ("أمن", "بيانات", "خصوصية", "pdpl", "security", "data", "privacy")),
        ("in_house_ai", ("ذكاء", "ai", "chatgpt", "نبني داخلي")),
        ("authority", ("المدير غير", "صاحب القرار", "صلاحية", "authority", "decision maker")),
        ("timing", ("وقت", "الآن", "اليوم", "تأجيل", "timing", "today", "later")),
        ("competitor", ("منافس", "البديل", "competitor", "alternative")),
    )
    for category, labels in checks:
        if any(label in lowered for label in labels):
            return category
    return "unclassified"


def _truth_map(evidence: tuple[PersuasionEvidence, ...]) -> tuple[dict[str, Any], ...]:
    allowed_use_ar = {
        EvidenceUse.BLOCKED: "محظور؛ لا يدخل في الحجة أو العرض.",
        EvidenceUse.HYPOTHESIS_ONLY: "فرضية داخلية تُحوّل إلى سؤال اكتشاف.",
        EvidenceUse.DISCOVERY_ONLY: "إشارة عامة؛ تُستخدم لفتح سؤال لا لإثبات مشكلة العميل.",
        EvidenceUse.CUSTOMER_CONTEXT: "سياق عميل يمكن استخدامه معه مع إظهار المرجع.",
        EvidenceUse.INTERNAL_OUTCOME: "نتيجة داخلية؛ لا تُنشر قبل موافقة موثقة.",
        EvidenceUse.PUBLISHABLE_PROOF: "دليل قابل للاستخدام ضمن حدود موافقة النشر.",
    }
    rows: list[dict[str, Any]] = []
    for item in evidence:
        disposition = classify_evidence(item)
        rows.append(
            {
                "claim": item.claim,
                "signal_type": item.signal_type,
                "evidence_ref": item.evidence_ref,
                "evidence_level": item.evidence_level.value,
                "confidence": item.confidence,
                "disposition": disposition.value,
                "allowed_use_ar": allowed_use_ar[disposition],
                "publication_consent_ref": item.publication_consent_ref,
                "stale": item.stale,
            }
        )
    return tuple(rows)


def build_buyer_decision_plan(context: BuyerDecisionContext) -> BuyerDecisionPlan:
    """Create a multi-stakeholder, proof-led persuasion plan."""
    truth_map = _truth_map(context.evidence)
    usable_refs = tuple(
        row["evidence_ref"]
        for row in truth_map
        if row["disposition"]
        in {EvidenceUse.CUSTOMER_CONTEXT.value, EvidenceUse.PUBLISHABLE_PROOF.value}
    )
    publishable_refs = tuple(
        row["evidence_ref"]
        for row in truth_map
        if row["disposition"] == EvidenceUse.PUBLISHABLE_PROOF.value
    )

    committee = tuple(
        {
            "role": role.value,
            **_BUYER_FRAMES[role],
            "usable_evidence_refs": usable_refs,
            "message_status": "internal_draft",
        }
        for role in context.buyer_roles
    )
    objection_rows: list[dict[str, Any]] = []
    for objection in context.known_objections:
        category = _objection_category(objection)
        objection_rows.append(
            {
                "objection": objection,
                "category": category,
                **_OBJECTION_PLAYBOOK[category],
                "response_status": "internal_draft",
            }
        )

    negotiation = build_negotiation_plan(
        NegotiationContext(
            account_name=context.account_name,
            offer_id=context.offer_id,
            customer_problem=context.opportunity_title,
            known_objections=context.known_objections,
            list_price_sar=None,
            approved_floor_sar=None,
            max_discount_without_approval_pct=0,
            requested_discount_pct=context.requested_discount_pct,
            non_standard_terms_requested=context.non_standard_terms_requested,
            evidence_refs=usable_refs,
        )
    ).to_dict()

    blockers: list[str] = []
    approvals: list[dict[str, Any]] = []
    if context.pricing_decision is not PricingDecision.FOUNDER_APPROVED:
        blockers.append("launch_offer_and_price_not_founder_approved")
        approvals.append(
            {
                "id": "approve_first_launch_offer_and_price",
                "owner": "founder",
                "question_ar": (
                    "هل تعتمد عرض Revenue Command Pilot بمدة ومعايير قبول خاصة بالعميل ونطاقه وسعره "
                    "بعد مراجعة خمس محادثات مؤهلة وتوحيد الكتالوج؟"
                ),
                "blocks": ("public_price", "commercial_proposal", "checkout"),
            }
        )
    if _EVIDENCE_RANK[context.evidence_level] < _EVIDENCE_RANK[EvidenceLevel.L3_FIRST_PARTY]:
        blockers.append("first_party_customer_validation_required")
        approvals.append(
            {
                "id": "validate_customer_problem",
                "owner": "revenue_owner",
                "question_ar": "هل أكد العميل المشكلة وخط الأساس والهدف بمرجع موثق؟",
                "blocks": ("customer_problem_claim", "proposal_generation"),
            }
        )
    if not publishable_refs:
        blockers.append("no_publishable_dealix_outcome_proof")
    if context.relationship_permission_state not in {"consented", "active", "customer_initiated"}:
        blockers.append("relationship_permission_not_verified")
    if context.requested_discount_pct > 0 or context.non_standard_terms_requested:
        approvals.append(
            {
                "id": "approve_commercial_exception",
                "owner": "founder",
                "question_ar": (
                    "هل تعتمد الاستثناء مقابل خفض نطاق أو دفع مقدم أو مدة تعاقدية "
                    "واضحة مع حماية هامش الربح؟"
                ),
                "blocks": ("discount", "non_standard_terms"),
            }
        )
    if any(row["disposition"] == EvidenceUse.INTERNAL_OUTCOME.value for row in truth_map):
        approvals.append(
            {
                "id": "approve_proof_publication",
                "owner": "client_and_founder",
                "question_ar": "هل توجد موافقة نشر محددة النطاق ومثبتة لهذا الدليل؟",
                "blocks": ("case_study", "testimonial", "public_metric"),
            }
        )
    approvals.append(
        {
            "id": "approve_external_draft",
            "owner": "founder",
            "question_ar": "هل الأدلة والنبرة والقناة والمستلم صحيحة قبل أي إجراء خارجي؟",
            "blocks": ("external_send", "calendar_booking", "commercial_commitment"),
        }
    )

    return BuyerDecisionPlan(
        plan_id=f"bdp_{context.opportunity_id}",
        opportunity_id=context.opportunity_id,
        mode="internal_draft_only",
        persuasion_thesis_ar=(
            f"مع {context.account_name} لا نبيع وعوداً عامة؛ نربط هدف «{context.objective}» "
            "بخط أساس وتدخل واحد ودليل وقرار توسع أو توقف خلال المدة المعتمدة."
        ),
        offer_architecture={
            "recommended_motion": "revenue_command_pilot_30d",
            "duration_days": 30,
            "one_icp": True,
            "one_revenue_workflow": True,
            "one_evidence_baseline": True,
            "weekly_executive_readout": True,
            "final_stop_expand_decision": True,
            "price_status": context.pricing_decision.value,
            "price_sar": None,
            "public_checkout_allowed": False,
        },
        truth_map=truth_map,
        buying_committee=committee,
        objection_responses=tuple(objection_rows),
        negotiation=negotiation,
        proof_design={
            "metric": context.metric,
            "baseline": "first_party_baseline_required",
            "intervention": "one_workflow_only",
            "target": context.proof_target,
            "measurement": "before_after_with_evidence_refs",
            "decision": "stop_expand_or_redesign",
            "guaranteed_outcome": False,
            "publishable_proof_refs": publishable_refs,
        },
        approval_queue=tuple(approvals),
        recommended_sequence=(
            "confirm_permission_and_buying_committee",
            "validate_problem_and_baseline_with_first_party_evidence",
            "map_role_specific_decision_questions",
            "run_18_minute_evidence_demo",
            "agree_30_day_proof_design_and_acceptance_criteria",
            "obtain_founder_price_terms_and_external_draft_approval",
            "measure_then_decide_stop_expand_or_redesign",
        ),
        blockers=tuple(dict.fromkeys(blockers)),
        validation_routes=(
            "commercial_intelligence",
            "sales_arena",
            "revenue_lab",
            "approval_center",
            "proof_ledger",
        ),
        price_included=False,
        external_action_allowed=False,
        external_commitment_made=False,
    )


__all__ = [
    "BuyerDecisionContext",
    "BuyerDecisionPlan",
    "BuyerRole",
    "DEFAULT_BUYER_ROLES",
    "EvidenceUse",
    "PersuasionEvidence",
    "PricingDecision",
    "build_buyer_decision_plan",
    "classify_evidence",
]
