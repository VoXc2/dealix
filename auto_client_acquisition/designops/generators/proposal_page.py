"""Current-authority bilingual Revenue Command Pilot proposal generator.

The public/first-launch Dealix motion is one quote-only 30-day Pilot. Legacy
``recommended_service`` and ``price_band_sar`` inputs remain in the function
signature for API compatibility, but they cannot create a public/fixed-price
proposal. Every artifact remains internal-review / approval-required and has no
send, invoice, payment, or publication authority.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)

_FOUNDER_SEND_RULE_AR = "المؤسس يجب أن يرسل هذا العرض يدويًا — لا إرسال آلي."
_FOUNDER_SEND_RULE_EN = "Founder must manually send this proposal — no auto-send."
CURRENT_SERVICE = "Revenue Command Pilot"
CURRENT_TIMELINE_DAYS = 30
PRICE_AUTHORITY = "quote_after_discovery"

_RETIRED_INPUT_TOKENS = (
    "4,999",
    "15,000",
    "1,500",
    "2,999",
    "499 ر.س",
    "499 sar",
    "sprint 499",
    "data pack 1500",
    "growth 2999",
    "/ar/risk-score",
    "/ar/proof-pack",
    "first-paid-diagnostic",
    "10-lead-audit",
)


def _assert_no_retired_claims(parts: list[str]) -> None:
    text = "\n".join(parts).casefold()
    for token in _RETIRED_INPUT_TOKENS:
        if token.casefold() in text:
            raise ValueError(f"retired_commercial_authority:{token}")


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
    """Compose an internal-review proposal for the current 30-day Pilot.

    ``recommended_service``, ``timeline_days`` and ``price_band_sar`` are
    accepted only to avoid breaking existing callers. The artifact normalizes
    them to the current launch authority instead of propagating legacy offers.
    """
    del recommended_service, timeline_days, price_band_sar

    deliverables = list(deliverables or [])
    blocked_actions = list(blocked_actions or [])
    proof_plan = list(proof_plan or [])
    _assert_no_retired_claims(
        [
            customer_handle,
            scope_ar,
            scope_en,
            *deliverables,
            *blocked_actions,
            *proof_plan,
        ]
    )

    title_ar = f"مسودة عرض Dealix — {customer_handle}"
    title_en = f"Dealix Draft Proposal — {customer_handle}"

    approval_required_actions = [
        "إرسال العرض أو أي رسالة إلى العميل أو شركائه",
        "اعتماد السعر أو الخصم أو أي concession",
        "إصدار فاتورة أو طلب دفع أو تفعيل مسار دفع",
        "نشر اسم العميل أو Case Study أو Proof Pack خارجيًا",
        "أي تغيير إنتاج أو DNS أو Secret أو بيانات حساسة",
    ]
    approval_required_actions_en = [
        "Sending this proposal or any message to the customer or their partners",
        "Approving price, discount, or any commercial concession",
        "Issuing an invoice/payment request or enabling a payment path",
        "Publishing the customer name, case study, or Proof Pack externally",
        "Any production, DNS, secret, or sensitive-data change",
    ]

    current_deliverables = deliverables or [
        "One approved revenue workflow",
        "Baseline + source / missing-evidence report",
        "Approval path + acceptance criteria",
        "Weekly Proof Pack",
        "Weekly executive readout",
        "Final Proof Pack + outcome review",
    ]
    current_proof_plan = proof_plan or [
        "Baseline → source reference → tracked action/delivery → measured outcome",
        "Payment/Revenue/Delivery/Customer Value/Publication Permission remain separate states",
        "Missing or stale evidence remains Unknown/Blocked, never invented",
    ]

    sections_ar = [
        {"title": "المشكلة لدى العميل", "body": scope_ar or "—"},
        {
            "title": "المنتج والمسار الحالي",
            "body": (
                "Dealix — Saudi-first AI Business Operating System. "
                "الحركة المدفوعة الأولى: Revenue Command Pilot لمدة 30 يومًا فقط."
            ),
        },
        {"title": "النطاق", "body": scope_ar or "—"},
        {"title": "المخرجات", "items": current_deliverables},
        {"title": "المدة", "body": "30 يومًا"},
        {
            "title": "السعر",
            "body": (
                "Quote خاص بالعميل بعد qualified discovery ومراجعة النطاق والهامش "
                "والقدرة والموافقات. لا يوجد سعر عام ثابت في هذا artifact."
            ),
        },
        {
            "title": "الدفع",
            "items": [
                "هذا artifact لا يصدر فاتورة ولا Payment request ولا ينشئ Revenue state.",
                "طريقة الدفع والجهة المصدرة والشروط والضرائب/الفوترة تحدد للحالة المعتمدة فقط.",
                "لا live charge أو checkout ذاتي في مسار الإطلاق الحالي.",
            ],
        },
        {"title": "إجراءات تتطلب موافقة", "items": approval_required_actions},
        {
            "title": "إجراءات محظورة/مقيّدة",
            "items": blocked_actions
            or [
                "Cold WhatsApp",
                "Mass LinkedIn automation",
                "Unapproved external send",
                "Unverified customer/revenue claims",
            ],
        },
        {
            "title": "حدود النتيجة",
            "items": [
                "لا ضمان لإيراد أو ROI أو conversion أو نتيجة سوقية محددة.",
                "الالتزام هو بالنطاق المعتمد والعمل والأدلة المتفق عليها.",
            ],
        },
        {"title": "خطة الإثبات", "items": current_proof_plan},
        {
            "title": "الخطوة التالية",
            "items": [
                _FOUNDER_SEND_RULE_AR,
                "المسودة تنتظر مراجعة واعتمادًا خاصًا بالعميل قبل أي مشاركة.",
            ],
        },
    ]

    sections_en = [
        {"title": "Customer problem", "body": scope_en or "-"},
        {
            "title": "Current product path",
            "body": (
                "Dealix — Saudi-first AI Business Operating System. "
                "The first paid motion is one 30-day Revenue Command Pilot."
            ),
        },
        {"title": "Scope", "body": scope_en or "-"},
        {"title": "Deliverables", "items": current_deliverables},
        {"title": "Timeline", "body": "30 days"},
        {
            "title": "Price",
            "body": (
                "Customer-specific quote after qualified discovery and review of scope, "
                "margin, capacity, and approvals. This artifact carries no public fixed price."
            ),
        },
        {
            "title": "Payment",
            "items": [
                "This artifact does not issue an invoice/payment request or create revenue state.",
                "Payment method, issuer, terms, and tax/invoicing treatment are approved per customer case.",
                "No live charge or self-serve checkout in the current first-launch path.",
            ],
        },
        {"title": "Approval-required actions", "items": approval_required_actions_en},
        {
            "title": "Blocked/restricted actions",
            "items": blocked_actions
            or [
                "Cold WhatsApp",
                "Mass LinkedIn automation",
                "Unapproved external send",
                "Unverified customer/revenue claims",
            ],
        },
        {
            "title": "Outcome boundary",
            "items": [
                "No promise of revenue, ROI, conversion, or a specific market outcome.",
                "The commitment is the approved scope, work, and agreed evidence path.",
            ],
        },
        {"title": "Proof plan", "items": current_proof_plan},
        {
            "title": "Next step",
            "items": [
                _FOUNDER_SEND_RULE_EN,
                "This draft requires customer-specific review and approval before sharing.",
            ],
        },
    ]

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs = [
        f"customer_handle={customer_handle}",
        "launch_authority=revenue_command_pilot_30d",
        "price_authority=customer_specific_quote_after_qualified_discovery",
        "timeline_days=30",
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
    md_full += (
        "\n\n---\n\n"
        f"> {_FOUNDER_SEND_RULE_AR}\n"
        f"> {_FOUNDER_SEND_RULE_EN}\n"
        "> quote-only — no live charge — no outcome promise.\n"
        "> عرض سعر خاص بالعميل فقط — لا خصم حي — لا وعد بنتيجة.\n"
    )

    html = render_artifact_html(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )

    markdown_ar = (
        f"# {title_ar}\n\n"
        f"{scope_ar or '—'}\n\n"
        "Revenue Command Pilot — 30 يومًا — Quote خاص بالعميل بعد Discovery.\n\n"
        f"> {_FOUNDER_SEND_RULE_AR}\n"
        "> لا live charge — لا وعد بإيراد أو ROI.\n"
    )
    markdown_en = (
        f"# {title_en}\n\n"
        f"{scope_en or '-'}\n\n"
        "Revenue Command Pilot — customer-specific duration — customer-specific quote after discovery.\n\n"
        f"> {_FOUNDER_SEND_RULE_EN}\n"
        "> no live charge — no revenue or ROI promise.\n"
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
            "recommended_service": CURRENT_SERVICE,
            "timeline_days": CURRENT_TIMELINE_DAYS,
            "price_band_sar": PRICE_AUTHORITY,
            "price_authority": "customer_specific_quote_after_qualified_discovery",
            "quote_only": True,
            "manual_payment": False,
            "payment_path_status": "blocked_until_customer_specific_approval",
            "no_live_charge": True,
            "no_guarantees": True,
        },
    }
