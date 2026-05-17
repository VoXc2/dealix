"""Layer 1 — Readiness Gates.

Six go/no-go gates (Sales, Marketing, Support, Delivery, Affiliate/Partner,
Governance). Most criteria are operator-confirmed checklist booleans
supplied via ``AssuranceInputs.gate_answers``. A handful are DERIVED
automatically from real sources (config presence, claim policy, the live
approval store) so the gates are genuinely wired, not pure passthrough.

A criterion with no answer is ``None`` (unknown) and the gate cannot pass.
"""
from __future__ import annotations

from auto_client_acquisition.assurance_os.adapters import (
    ApprovalAdapter,
    ClaimAdapter,
)
from auto_client_acquisition.assurance_os.config_loader import load_config
from auto_client_acquisition.assurance_os.models import (
    AssuranceInputs,
    GateCriterion,
    GateResult,
)

# (gate_id, name_en, name_ar, [(criterion_id, label_en, label_ar), ...])
GATE_SPECS: list[tuple[str, str, str, list[tuple[str, str, str]]]] = [
    (
        "gate1_sales", "Sales Ready", "جاهزية المبيعات",
        [
            ("gate1_leads_enter", "Test leads enter the system", "leads تجريبية تدخل النظام"),
            ("gate1_leads_scored", "100% of leads get a lead score", "كل lead له score"),
            ("gate1_leads_staged", "100% of leads get a stage", "كل lead له stage"),
            ("gate1_leads_next_action", "100% of leads get a next action", "كل lead له next action"),
            ("gate1_qualified_a_approval_task", "Qualified-A generates an approval task", "Qualified A يولد approval task"),
            ("gate1_meeting_brief", "Meeting booked generates a meeting brief", "Meeting booked يولد meeting brief"),
            ("gate1_meeting_notes_required", "Meeting done is blocked without notes", "Meeting done مرفوض بلا notes"),
            ("gate1_scope_needs_approval", "Scope cannot be sent without approval", "Scope لا يُرسل بلا approval"),
            ("gate1_invoice_needs_scope", "Invoice needs an approved scope", "Invoice يحتاج scope معتمد"),
        ],
    ),
    (
        "gate2_marketing", "Marketing Ready", "جاهزية التسويق",
        [
            ("gate2_cta_utm", "Every CTA carries a UTM", "كل CTA له UTM"),
            ("gate2_risk_score_source", "Risk Score captures source", "Risk Score يلتقط المصدر"),
            ("gate2_proof_pack_creates_lead", "Proof Pack request creates a lead", "طلب Proof Pack يخلق lead"),
            ("gate2_campaign_id", "Every campaign has a campaign_id", "كل حملة لها campaign_id"),
            ("gate2_newsletter_live", "Newsletter sequence is live", "تسلسل النشرة شغّال"),
            ("gate2_dashboard_source_meeting", "Dashboard shows source -> lead -> meeting", "لوحة تعرض المصدر حتى الاجتماع"),
        ],
    ),
    (
        "gate3_support", "Support Ready", "جاهزية الدعم",
        [
            ("gate3_kb_30_faqs", "30 FAQs in the knowledge base", "30 سؤال في قاعدة المعرفة"),
            ("gate3_easy_from_kb", "80% of easy questions answered from KB", "80% من الأسئلة السهلة تُجاب من KB"),
            ("gate3_high_risk_escalated", "100% of security/refund/scope escalated", "كل سؤال حساس يُصعّد"),
            ("gate3_answer_has_source", "Every answer has a source", "كل إجابة لها مصدر"),
            ("gate3_unknown_creates_gap", "Unknown question creates a knowledge gap", "سؤال مجهول يخلق knowledge gap"),
        ],
    ),
    (
        "gate4_delivery", "Delivery Ready", "جاهزية التسليم",
        [
            ("gate4_onboarding_form", "Onboarding form is ready", "نموذج onboarding جاهز"),
            ("gate4_inputs_checklist", "Required-inputs checklist is ready", "قائمة المدخلات المطلوبة جاهزة"),
            ("gate4_proof_pack_template", "Proof Pack template is ready", "قالب Proof Pack جاهز"),
            ("gate4_sections_present", "Source/evidence/approval sections present", "أقسام المصدر/الدليل/الموافقة موجودة"),
            ("gate4_founder_review", "Final Proof Pack needs founder review", "Proof Pack النهائي يحتاج مراجعة الفاوندر"),
            ("gate4_value_confirmation", "Value confirmation after delivery", "تأكيد القيمة بعد التسليم"),
        ],
    ),
    (
        "gate5_affiliate_partner", "Affiliate / Partner Ready", "جاهزية الشركاء والمسوّقين",
        [
            ("gate5_partner_application", "Partner application exists", "نموذج طلب الشريك موجود"),
            ("gate5_affiliate_rules", "Affiliate rules exist", "قواعد المسوّق موجودة"),
            ("gate5_approved_messages", "Approved messages exist", "رسائل معتمدة موجودة"),
            ("gate5_forbidden_claims", "Forbidden claims are defined", "الادعاءات الممنوعة مُعرّفة"),
            ("gate5_disclosure_text", "Disclosure text is present", "نص الإفصاح موجود"),
            ("gate5_referral_tracking", "Referral tracking exists", "تتبّع الإحالات موجود"),
            ("gate5_commission_after_paid", "Commission only after invoice_paid", "العمولة فقط بعد invoice_paid"),
        ],
    ),
    (
        "gate6_governance", "Governance Ready", "جاهزية الحوكمة",
        [
            ("gate6_approval_policy", "approval_policy.yaml exists", "ملف approval_policy.yaml موجود"),
            ("gate6_stage_transitions", "stage_transitions.yaml exists", "ملف stage_transitions.yaml موجود"),
            ("gate6_claim_policy", "claim_policy.yaml exists", "ملف claim_policy.yaml موجود"),
            ("gate6_no_high_risk_auto_send", "No high-risk auto-send", "لا إرسال آلي عالي الخطورة"),
            ("gate6_evidence_events", "Evidence events are working", "أحداث الدليل تعمل"),
            ("gate6_agent_run_logs", "Agent run logs are working", "سجلات تشغيل الوكلاء تعمل"),
            ("gate6_monthly_audit", "Monthly governance audit is scheduled", "تدقيق حوكمة شهري مجدول"),
        ],
    ),
]


def _derived_criteria() -> dict[str, bool]:
    """Criteria the Assurance System can verify itself from real sources."""
    cfg = load_config()
    derived: dict[str, bool] = {
        "gate6_approval_policy": bool(cfg.approval_policy),
        "gate6_stage_transitions": bool(cfg.stage_transitions),
        "gate6_claim_policy": bool(cfg.claim_policy),
    }

    claim = ClaimAdapter().forbidden_claims()
    derived["gate5_forbidden_claims"] = bool(claim.is_known and claim.value)

    stats = ApprovalAdapter().live_stats()
    if stats.is_known:
        derived["gate6_no_high_risk_auto_send"] = stats.value["high_risk_auto_send"] == 0
    return derived


def evaluate_gates(inputs: AssuranceInputs) -> list[GateResult]:
    """Evaluate all 6 readiness gates."""
    derived = _derived_criteria()
    results: list[GateResult] = []
    for gate_id, name_en, name_ar, crit_specs in GATE_SPECS:
        criteria: list[GateCriterion] = []
        for cid, label_en, label_ar in crit_specs:
            if cid in derived:
                passed: bool | None = derived[cid]
            else:
                passed = inputs.gate_answers.get(cid)
            criteria.append(GateCriterion(cid, label_en, label_ar, passed))
        unknown = sum(1 for c in criteria if c.passed is None)
        gate_passed = unknown == 0 and all(c.passed for c in criteria)
        results.append(
            GateResult(gate_id, name_en, name_ar, criteria, gate_passed, unknown)
        )
    return results
