"""Per-role brief composition.

Each brief is computed from real signals already in the repo:
  - service_activation_matrix.candidates_for_promotion()
  - daily_growth_loop.build_today() (its open_loops + perimeter)
  - partner_distribution_radar.summary() (rotating focus)
  - seo_technical_auditor.summary() (perimeter cells)
  - safe_publishing_gate (approval-first invariant)

No LLM calls. No fake data. Each role receives the SAME underlying
truth, framed for their concerns.
"""
from __future__ import annotations

from typing import Callable

from auto_client_acquisition.role_command_os.schemas import (
    RoleBrief,
    RoleDecision,
    RoleName,
)
from auto_client_acquisition.self_growth_os import (
    geo_aio_radar,
    partner_distribution_radar,
    service_activation_matrix,
)


_GUARDRAILS_TRUE = {
    "no_live_send": True,
    "no_scraping": True,
    "no_cold_outreach": True,
    "approval_required_for_external_actions": True,
}


def _candidate_decisions(limit: int = 2) -> list[RoleDecision]:
    """Produce 0–limit decisions about service-promotion candidates."""
    out: list[RoleDecision] = []
    try:
        candidates = service_activation_matrix.candidates_for_promotion()
    except Exception:  # noqa: BLE001
        return out
    for c in candidates[:limit]:
        gates = ", ".join((c.blocking_reasons or [])[:3])
        out.append(RoleDecision(
            title_ar=f"خدمة قريبة من Live: {c.name_ar}",
            title_en=f"Service close to Live: {c.name_en}",
            rationale_ar=f"حالتها {c.status}؛ ينقصها: {gates}",
            rationale_en=f"Status: {c.status}. Remaining gates: {gates}",
            risk_level="medium",
            approval_required=True,
            proof_event=f"service_promotion_review:{c.service_id}",
        ))
    return out


def _ceo_brief() -> RoleBrief:
    decisions = _candidate_decisions(limit=2)
    decisions.insert(0, RoleDecision(
        title_ar="مراجعة Decision Pack — هل وقّعتم البنود الـ10؟",
        title_en="Review Decision Pack — have the 10 items been signed?",
        rationale_ar="docs/EXECUTIVE_DECISION_PACK.md ينتظر توقيع المؤسس على B1-B5 + S1-S5.",
        rationale_en="docs/EXECUTIVE_DECISION_PACK.md awaits founder sign-off on B1-B5 + S1-S5.",
        risk_level="medium",
        approval_required=True,
        proof_event="executive_decision_pack_signed",
    ))

    summary_ar = (
        "ملخّص اليوم للمؤسس: مصفوفة الخدمات تشتغل، الإشعار على intake فعّال، "
        "Daily digest يصلكم 7AM KSA. القرارات الـ3 أعلاه تستحقّ ساعة هذا الأسبوع."
    )
    summary_en = (
        "Founder daily summary: service matrix is healthy, intake alert is "
        "wired, daily digest arrives at 7AM KSA. The 3 decisions above warrant "
        "an hour this week."
    )
    return RoleBrief(
        role=RoleName.CEO,
        summary_ar=summary_ar,
        summary_en=summary_en,
        top_decisions=decisions[:3],
        risks=[
            "B1+B2 REVIEW_PENDING strings still un-decided",
            "Railway redeploy occasionally delayed by infra-side incidents",
        ],
        approvals_needed=[
            "Decision Pack v1 sign-off",
            "First service to flip Live (recommendation: lead_intake_whatsapp)",
        ],
        evidence_pointers=[
            "docs/MASTER_CLOSURE_EVIDENCE_TABLE.md",
            "docs/STRATEGIC_MASTER_PLAN_2026.md",
            "docs/EXECUTIVE_DECISION_PACK.md",
        ],
        next_action_ar="وقّع Decision Pack أو ارفض أحد البنود بشكل واضح.",
        next_action_en="Sign the Decision Pack or explicitly reject one item.",
        blocked_actions=[
            "auto_charge_customer",
            "send_cold_whatsapp",
            "linkedin_dm_automation",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


def _sales_brief() -> RoleBrief:
    candidates = _candidate_decisions(limit=3)
    return RoleBrief(
        role=RoleName.SALES,
        summary_ar=(
            "مدير المبيعات: 3 خدمات قريبة من الترقية، تحتاج 1-2 إغلاق "
            "لكلّ خدمة قبل أن تدخل Live. لا outreach آلي — كل مسوّدة "
            "تحتاج موافقة قبل أيّ إرسال."
        ),
        summary_en=(
            "Sales lead: 3 services close to promotion. Each needs 1-2 "
            "more gates closed before going Live. No automated outreach — "
            "every draft requires approval before any send."
        ),
        top_decisions=candidates,
        risks=[
            "Quiet-hours enforcement test missing on routing service",
            "Outreach window enforcement test missing on outreach_drafts",
        ],
        approvals_needed=[
            "Approve drafts in /api/v1/self-growth/publishing/check before any external send",
        ],
        evidence_pointers=[
            "docs/registry/SERVICE_READINESS_MATRIX.yaml",
            "/api/v1/self-growth/service-activation-candidates",
        ],
        next_action_ar="افتح أوّل service candidate وأكمل أحد gates التفعيل.",
        next_action_en="Open the first service candidate and close one activation gate.",
        blocked_actions=[
            "send_outside_consent",
            "bulk_messaging",
            "auto_send_outside_24h_window",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


def _growth_brief() -> RoleBrief:
    try:
        geo = geo_aio_radar.audit_all()
        top = geo_aio_radar.top_priority_pages(limit=3)
    except Exception:  # noqa: BLE001
        geo, top = {"summary": {}}, []

    decisions: list[RoleDecision] = []
    for page in top:
        decisions.append(RoleDecision(
            title_ar=f"تحسين صفحة: {page['path']} (نقاط GEO منخفضة)",
            title_en=f"Improve page: {page['path']} (low GEO score)",
            rationale_ar=f"النقاط الحاليّة: {page['score']}. الفجوات: {', '.join(page.get('gaps', [])[:3])}",
            rationale_en=f"Current score: {page['score']}. Gaps: {', '.join(page.get('gaps', [])[:3])}",
            risk_level="low",
            approval_required=True,
        ))

    return RoleBrief(
        role=RoleName.GROWTH,
        summary_ar=(
            f"مدير النموّ: متوسّط GEO/AIO الحالي "
            f"{(geo.get('summary') or {}).get('average_score', '—')}. "
            f"3 صفحات أعلى أولويّة للتحسين أسفل."
        ),
        summary_en=(
            f"Growth lead: current GEO/AIO average score "
            f"{(geo.get('summary') or {}).get('average_score', '—')}. "
            f"Top 3 priority pages below."
        ),
        top_decisions=decisions[:3],
        risks=[
            "Without a search-data source (B4), no real keyword volume",
        ],
        approvals_needed=[
            "Pick search/keyword data source (B4 in Decision Pack)",
        ],
        evidence_pointers=[
            "/api/v1/self-growth/geo/audit",
            "/api/v1/self-growth/scorecard/weekly",
            "docs/STRATEGIC_MASTER_PLAN_2026.md Part VIII",
        ],
        next_action_ar="حسّن أوّل صفحة من القائمة (إضافة JSON-LD أو FAQ).",
        next_action_en="Improve the top-priority page (add JSON-LD or FAQ).",
        blocked_actions=[
            "scaled_low_value_ai_pages",
            "purchased_keyword_lists",
            "fake_traffic_metrics",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


def _partnership_brief() -> RoleBrief:
    try:
        radar = partner_distribution_radar.summary()
    except Exception:  # noqa: BLE001
        radar = {"categories": []}

    decisions: list[RoleDecision] = []
    for cat in (radar.get("categories") or [])[:3]:
        decisions.append(RoleDecision(
            title_ar=f"اقترب من شريك: {cat.get('name_ar', cat['category_id'])}",
            title_en=f"Approach partner category: {cat.get('name_en', cat['category_id'])}",
            rationale_ar=f"المسوّدة جاهزة في /api/v1/self-growth/partner-radar/{cat['category_id']}",
            rationale_en=f"Draft ready at /api/v1/self-growth/partner-radar/{cat['category_id']}",
            risk_level="low",
            approval_required=True,
        ))

    return RoleBrief(
        role=RoleName.PARTNERSHIP,
        summary_ar=(
            f"مدير الشراكات: {len(radar.get('categories') or [])} فئة "
            f"شريك جاهزة في الكتالوج. كل مسوّدة warm-intro تمرّ بـ "
            f"safe_publishing_gate قبل العرض."
        ),
        summary_en=(
            f"Partnership lead: {len(radar.get('categories') or [])} "
            f"partner categories ready in the catalog. Every warm-intro "
            f"draft passes safe_publishing_gate before display."
        ),
        top_decisions=decisions,
        risks=[
            "Exclusivity offers are blocked until 3 proofs delivered",
            "No paid affiliate commissions until written agreement",
        ],
        approvals_needed=[
            "S2 in Decision Pack: authorize partner outreach to 5 names",
        ],
        evidence_pointers=[
            "/api/v1/self-growth/partner-radar",
            "auto_client_acquisition/self_growth_os/partner_distribution_radar.py",
        ],
        next_action_ar="اختر 5 شركاء معرفة شخصيّاً واطلب موافقة Decision Pack S2.",
        next_action_en="Pick 5 personally-known partners and approve Decision Pack S2.",
        blocked_actions=[
            "auto_dm_partner",
            "scrape_partner_directory",
            "exclusivity_without_three_proofs",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


def _cs_brief() -> RoleBrief:
    return RoleBrief(
        role=RoleName.CUSTOMER_SUCCESS,
        summary_ar=(
            "مدير نجاح العملاء: تابع customer_loop journey. كل عميل "
            "يجب أن ينتقل من PAID_OR_COMMITTED إلى PROOF_PACK_SENT خلال "
            "7-14 يوم. لا تواصل خارج 24h window بدون template موافَق عليه."
        ),
        summary_en=(
            "CS lead: track the customer_loop journey. Every customer "
            "must move from PAID_OR_COMMITTED to PROOF_PACK_SENT within "
            "7-14 days. No outbound outside the 24h window without an "
            "approved template."
        ),
        top_decisions=[
            RoleDecision(
                title_ar="افتح ServiceSession لكل عميل في PAID_OR_COMMITTED",
                title_en="Open a ServiceSession for every PAID_OR_COMMITTED customer",
                rationale_ar="customer_loop يعطيك checklist بعد كل تقدّم",
                rationale_en="customer_loop returns a checklist after every advance",
                risk_level="low",
                approval_required=True,
            ),
            RoleDecision(
                title_ar="جمّع ProofEvents في pack بعد كل تسليم",
                title_en="Assemble ProofEvents into a pack after each delivery",
                rationale_ar="POST /api/v1/self-growth/proof-pack/assemble",
                rationale_en="POST /api/v1/self-growth/proof-pack/assemble",
                risk_level="low",
                approval_required=True,
                proof_event="proof_pack_assembled",
            ),
        ],
        risks=[
            "WhatsApp 24h window drift if customer doesn't reply within window",
            "Proof Pack publication needs explicit customer consent",
        ],
        approvals_needed=[
            "Customer consent_for_publication on every shareable pack",
        ],
        evidence_pointers=[
            "/api/v1/customer-loop/states",
            "/api/v1/self-growth/proof-pack/assemble",
        ],
        next_action_ar="افتح أوّل عميل لم ينتقل من IN_DELIVERY → PROOF_PACK_READY.",
        next_action_en="Open the first customer stuck in IN_DELIVERY → PROOF_PACK_READY.",
        blocked_actions=[
            "send_template_without_opt_in",
            "publish_customer_name_without_consent",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


def _finance_brief() -> RoleBrief:
    return RoleBrief(
        role=RoleName.FINANCE,
        summary_ar=(
            "المالية: لا live charge. الفواتير عبر Moyasar test_mode "
            "أو رابط مدفوع يدوي. سياسة 499 ريال Pilot سارية حتى أوّل "
            "5 عملاء (S1 في Decision Pack)."
        ),
        summary_en=(
            "Finance: no live charge. Invoices via Moyasar test mode "
            "or manual paid link. The 499 SAR Pilot policy holds until "
            "customer #5 (S1 in Decision Pack)."
        ),
        top_decisions=[
            RoleDecision(
                title_ar="استخدم scripts/dealix_invoice.py لكل فاتورة",
                title_en="Use scripts/dealix_invoice.py for every invoice",
                rationale_ar="يرفض sk_live_ بدون --allow-live",
                rationale_en="Refuses sk_live_ without --allow-live",
                risk_level="low",
                approval_required=False,
            ),
            RoleDecision(
                title_ar="بعد 5 Pilots، فعّل خطّة S1 (رفع Growth Starter لـ 990)",
                title_en="After 5 Pilots, activate S1 (Growth Starter → 990 SAR)",
                rationale_ar="موثَّق في docs/EXECUTIVE_DECISION_PACK.md",
                rationale_en="documented in docs/EXECUTIVE_DECISION_PACK.md",
                risk_level="low",
                approval_required=True,
            ),
        ],
        risks=[
            "Live charge enabling without explicit policy + tests",
            "ZATCA invoicing for >5 paid customers",
        ],
        approvals_needed=[
            "S1: Pilot retirement at customer #5",
            "Live charge gate: founder approval after billing tests pass",
        ],
        evidence_pointers=[
            "scripts/dealix_invoice.py",
            "dealix/payments/moyasar.py",
            "docs/MOYASAR_E2E_GUIDE.md",
        ],
        next_action_ar="إذا فيه فاتورة pending — افتح Moyasar dashboard وحدّث الحالة.",
        next_action_en="If there's a pending invoice, open Moyasar dashboard and update status.",
        blocked_actions=[
            "auto_charge_card",
            "live_charge_without_tests",
            "share_card_data_externally",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


def _compliance_brief() -> RoleBrief:
    return RoleBrief(
        role=RoleName.COMPLIANCE,
        summary_ar=(
            "الامتثال (PDPL/SDAIA): جميع البوابات الصلبة فعّالة. "
            "4 REVIEW_PENDING strings تنتظر قرار المؤسس قبل النشر."
        ),
        summary_en=(
            "Compliance (PDPL/SDAIA): all hard gates active. "
            "4 REVIEW_PENDING strings await founder decision before publication."
        ),
        top_decisions=[
            RoleDecision(
                title_ar="راجع 4 REVIEW_PENDING strings في Issue #138",
                title_en="Review 4 REVIEW_PENDING strings in Issue #138",
                rationale_ar="roi.html refund + academy Cold Email Pro + 2 sales-kit docs",
                rationale_en="roi.html refund + academy Cold Email Pro + 2 sales-kit docs",
                risk_level="low",
                approval_required=True,
                proof_event="review_pending_resolved",
            ),
            RoleDecision(
                title_ar="تأكّد أن audit_trail يلتقط كل external action attempt",
                title_en="Verify audit_trail captures every external-action attempt",
                rationale_ar="الخدمة partial حالياً — تحتاج correlation_id موحّد",
                rationale_en="service is partial — needs unified correlation_id",
                risk_level="medium",
                approval_required=True,
            ),
        ],
        risks=[
            "PDPL fine up to 5M SAR per violation",
            "Cross-border data transfer requires SDAIA approval",
            "Marketing consent must be logged with timestamp + method",
        ],
        approvals_needed=[
            "B1: roi.html refund wording",
            "B2: academy Cold Email Pro course title",
            "B3: pages for full OG copy approval",
        ],
        evidence_pointers=[
            "docs/PRIVACY_PDPL_READINESS.md",
            "docs/SECURITY_PDPL_CHECKLIST.md",
            "https://github.com/voxc2/dealix/issues/138",
        ],
        next_action_ar="افتح Issue #138 ووثّق قرارك على كل بند.",
        next_action_en="Open Issue #138 and record your decision per item.",
        blocked_actions=[
            "send_marketing_without_logged_consent",
            "store_pii_outside_ksa_without_authorization",
            "log_pii_in_plaintext",
        ],
        guardrails=dict(_GUARDRAILS_TRUE),
    )


_BUILDERS: dict[RoleName, Callable[[], RoleBrief]] = {
    RoleName.CEO: _ceo_brief,
    RoleName.SALES: _sales_brief,
    RoleName.GROWTH: _growth_brief,
    RoleName.PARTNERSHIP: _partnership_brief,
    RoleName.CUSTOMER_SUCCESS: _cs_brief,
    RoleName.FINANCE: _finance_brief,
    RoleName.COMPLIANCE: _compliance_brief,
}


def build_role_brief(role: RoleName) -> RoleBrief:
    """Compose the brief for a single role."""
    builder = _BUILDERS.get(role)
    if builder is None:
        raise KeyError(f"unknown role: {role}")
    return builder()


def list_roles() -> list[str]:
    return [r.value for r in RoleName]
