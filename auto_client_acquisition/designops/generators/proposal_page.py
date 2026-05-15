"""Proposal page generator.

Composes a bilingual proposal that always carries the manual-payment
fallback, no-live-charge / no-guarantees disclaimers, and the hard
rule: "Founder must manually send this proposal — no auto-send."
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)

# Hard line baked into every proposal.
_FOUNDER_SEND_RULE_AR = (
    "المؤسس يجب أن يرسل هذا العرض يدويًا — لا إرسال آلي."
)
_FOUNDER_SEND_RULE_EN = (
    "Founder must manually send this proposal — no auto-send."
)


def generate_proposal_page(
    customer_handle: str,
    recommended_service: str,
    scope_ar: str,
    scope_en: str,
    deliverables: list[str],
    timeline_days: int,
    price_band_sar: str,
    blocked_actions: list[str],
    proof_plan: list[str],
) -> dict[str, Any]:
    """Compose a bilingual proposal artifact."""
    deliverables = list(deliverables or [])
    blocked_actions = list(blocked_actions or [])
    proof_plan = list(proof_plan or [])

    title_ar = f"عرض Dealix — {customer_handle}"
    title_en = f"Dealix Proposal — {customer_handle}"

    approval_required_actions = [
        "إرسال أيّ رسالة إلى العميل أو شركاء العميل",
        "نشر دراسة حالة أو Proof Pack خارجيًّا",
        "إصدار فاتورة (تحت Moyasar test mode فقط)",
    ]
    approval_required_actions_en = [
        "Sending any message to the customer or their partners",
        "Publishing a case study or Proof Pack externally",
        "Issuing an invoice (Moyasar test-mode only)",
    ]

    sections_ar = [
        {
            "title": "المشكلة لدى العميل",
            "body": scope_ar or "—",
        },
        {
            "title": "الوضع الحاليّ",
            "body": (
                f"العميل: {customer_handle}\n"
                f"الخدمة الموصى بها: {recommended_service}"
            ),
        },
        {
            "title": "خدمة Dealix الموصى بها",
            "body": (
                f"`{recommended_service}` — تركيز على إثبات قبل التوسّع."
            ),
        },
        {"title": "النطاق", "body": scope_ar or "—"},
        {"title": "المخرجات", "items": deliverables or ["—"]},
        {"title": "المدّة", "body": f"{timeline_days} يومًا"},
        {
            "title": "إجراءات تتطلّب موافقة",
            "items": approval_required_actions,
        },
        {
            "title": "إجراءات محظورة",
            "items": blocked_actions or ["لا إجراءات محظورة محدّدة بعد."],
        },
        {
            "title": "خيار التسعير",
            "body": f"السعر التقريبيّ: {price_band_sar} ريال (نطاق توجيهيّ).",
        },
        {
            "title": "الدفع",
            "items": [
                "الدفع اليدويّ هو الإطار الافتراضيّ — لا خصم آليّ.",
                "Moyasar test-mode invoice فقط — لا شحنة حيّة.",
                "فاتورة تجريبيّة بإشراف المؤسس قبل أيّ تأكيد.",
            ],
        },
        {
            "title": "الضمانات",
            "items": [
                "❌ لا ضمانات بأرقام أو ترتيب أو إيرادات.",
                "❌ لا التزامات تسويقيّة.",
                "✅ التزام بالعمل + Proof Pack موثَّق.",
            ],
        },
        {"title": "خطّة الإثبات", "items": proof_plan or ["—"]},
        {
            "title": "الخطوة التالية",
            "items": [
                _FOUNDER_SEND_RULE_AR,
                "ينتظر هذا العرض موافقة المؤسس قبل المشاركة.",
            ],
        },
    ]

    sections_en = [
        {"title": "Customer problem", "body": scope_en or "-"},
        {
            "title": "Current situation",
            "body": (
                f"Customer: {customer_handle}\n"
                f"Recommended service: {recommended_service}"
            ),
        },
        {
            "title": "Recommended Dealix service",
            "body": (
                f"`{recommended_service}` — proof-before-scale focus."
            ),
        },
        {"title": "Scope", "body": scope_en or "-"},
        {"title": "Deliverables", "items": deliverables or ["-"]},
        {"title": "Timeline", "body": f"{timeline_days} days"},
        {
            "title": "Approval-required actions",
            "items": approval_required_actions_en,
        },
        {
            "title": "Blocked actions",
            "items": blocked_actions or ["No explicit blocked actions yet."],
        },
        {
            "title": "Price option",
            "body": f"Indicative price band: {price_band_sar} SAR.",
        },
        {
            "title": "Payment",
            "items": [
                "Manual payment is the default mode — no auto-charge.",
                "Moyasar test-mode invoice only — no live charge.",
                "Test invoice issued under founder supervision before any confirmation.",
            ],
        },
        {
            "title": "Guarantees",
            "items": [
                "No guarantees on numbers, ranking, or revenue.",
                "No marketing commitments.",
                "Commitment is on the work + a documented Proof Pack.",
            ],
        },
        {"title": "Proof plan", "items": proof_plan or ["-"]},
        {
            "title": "Next step",
            "items": [
                _FOUNDER_SEND_RULE_EN,
                "This proposal waits for founder approval before sharing.",
            ],
        },
    ]

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs = [
        f"customer_handle={customer_handle}",
        f"recommended_service={recommended_service}",
        f"timeline_days={timeline_days}",
        f"price_band_sar={price_band_sar}",
    ]

    md_full = render_artifact_markdown(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )
    # Append the hard rules to the markdown so safety_gate / tests see them.
    rules_block = (
        "\n\n---\n\n"
        f"> {_FOUNDER_SEND_RULE_AR}\n"
        f"> {_FOUNDER_SEND_RULE_EN}\n"
        "> manual payment — no live charge — no guarantees.\n"
        "> الدفع يدويّ — لا شحنة حيّة — لا ضمانات.\n"
    )
    md_full += rules_block

    html = render_artifact_html(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )

    # AR / EN convenience strings always include the hard-rule lines.
    markdown_ar = (
        f"# {title_ar}\n\n"
        f"{scope_ar or '—'}\n\n"
        f"> {_FOUNDER_SEND_RULE_AR}\n"
        "> الدفع يدويّ — لا شحنة حيّة — لا ضمانات.\n"
    )
    markdown_en = (
        f"# {title_en}\n\n"
        f"{scope_en or '-'}\n\n"
        f"> {_FOUNDER_SEND_RULE_EN}\n"
        "> manual payment — no live charge — no guarantees.\n"
    )

    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "manifest": {
            "artifact_type": "proposal_page",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "customer_handle": customer_handle,
            "recommended_service": recommended_service,
            "timeline_days": timeline_days,
            "price_band_sar": price_band_sar,
            "manual_payment": True,
            "no_live_charge": True,
            "no_guarantees": True,
        },
    }
