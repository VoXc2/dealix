"""Current-authority Dealix pricing-path artifact generator.

Dealix has one first-launch product path, not a public seven-tier price ladder.
The artifact is internal-review only and carries no quote, invoice, checkout, or
payment authority. ``highlight`` is accepted for API compatibility but cannot
restore a retired package/tier.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)

CURRENT_PATH: list[dict[str, Any]] = [
    {
        "stage": "entry",
        "name_ar": "Free Mini Diagnostic",
        "name_en": "Free Mini Diagnostic",
        "price_authority": "free_entry_no_payment",
        "summary_ar": (
            "تشخيص minimum-data ينتج leak hypothesis وwritten diagnosis و"
            "missing-evidence report وPilot hypothesis؛ لا Lead persistence أو دفع تلقائي."
        ),
        "summary_en": (
            "Minimum-data diagnostic producing a leak hypothesis, written diagnosis, "
            "missing-evidence report, and Pilot hypothesis; no automatic lead persistence or payment."
        ),
    },
    {
        "stage": "paid_motion",
        "name_ar": "Revenue Command Pilot — 30 يومًا",
        "name_en": "Revenue Command Pilot — 30 days",
        "price_authority": "customer_specific_quote_after_qualified_discovery",
        "summary_ar": (
            "Workflow واحد + baseline + owner + approved data boundary + approval path + "
            "acceptance criteria + weekly/final Proof."
        ),
        "summary_en": (
            "One workflow + baseline + owner + approved data boundary + approval path + "
            "acceptance criteria + weekly/final Proof."
        ),
    },
    {
        "stage": "decision",
        "name_ar": "Stop / Expand / Redesign",
        "name_en": "Stop / Expand / Redesign",
        "price_authority": "no_automatic_expansion",
        "summary_ar": "التوسع ليس package تلقائيًا؛ يقرر من source-backed Proof ونطاق جديد معتمد.",
        "summary_en": "Expansion is not an automatic package; it is earned by source-backed Proof and a newly approved scope.",
    },
]


def generate_pricing_page(highlight: str | None = None) -> dict[str, Any]:
    """Compose the current one-product buying/pricing-path artifact."""
    del highlight

    title_ar = "مسار شراء Dealix — منتج واحد، Quote خاص بالعميل"
    title_en = "Dealix Buying Path — One Product, Customer-Specific Quote"

    items_ar = [
        f"{row['name_ar']}: {row['summary_ar']}"
        for row in CURRENT_PATH
    ]
    items_en = [
        f"{row['name_en']}: {row['summary_en']}"
        for row in CURRENT_PATH
    ]

    sections_ar = [
        {
            "title": "السلطة الحالية",
            "items": [
                "Dealix — Saudi-first AI Business Operating System.",
                "أول wedge: Revenue + Proof + Command.",
                "لا سعر عام ثابت للـPilot، ولا self-serve checkout، ولا package ladder عام.",
            ],
        },
        {"title": "مسار الشراء", "items": items_ar},
        {
            "title": "بوابة السعر",
            "items": [
                "السعر الفعلي يأتي من customer-specific quote بعد qualified discovery.",
                "مراجعة النطاق والهامش والقدرة والموافقات تسبق اعتماد العرض.",
                "هذا artifact لا يصدر Quote أو Invoice أو Payment request.",
            ],
        },
        {
            "title": "حدود النتيجة",
            "items": [
                "لا ضمان إيراد أو ROI أو conversion أو نتيجة سوقية محددة.",
                "أي expansion يحتاج Proof ونطاقًا وموافقة جديدة.",
            ],
        },
    ]
    sections_en = [
        {
            "title": "Current authority",
            "items": [
                "Dealix — Saudi-first AI Business Operating System.",
                "First wedge: Revenue + Proof + Command.",
                "No public fixed Pilot price, self-serve checkout, or public package ladder.",
            ],
        },
        {"title": "Buying path", "items": items_en},
        {
            "title": "Price gate",
            "items": [
                "The actual price comes from a customer-specific quote after qualified discovery.",
                "Scope, margin, capacity, and approval review precede quote approval.",
                "This artifact does not issue a quote, invoice, or payment request.",
            ],
        },
        {
            "title": "Outcome boundary",
            "items": [
                "No promise of revenue, ROI, conversion, or a specific market outcome.",
                "Any expansion requires Proof, a new scope, and a new approval decision.",
            ],
        },
    ]

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs = [
        "launch_authority=revenue_command_pilot_30d",
        "price_authority=customer_specific_quote_after_qualified_discovery",
        "public_fixed_price=false",
        "live_checkout=false",
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
        "\n---\n"
        "> Quote-only after qualified discovery — no live checkout or outcome promise.\n"
        "> Quote خاص بالعميل بعد Discovery — لا Checkout حي ولا وعد بنتيجة.\n"
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
        + "\n".join(f"- {item}" for item in items_ar)
        + "\n\n> السعر: customer-specific quote بعد qualified discovery فقط.\n"
    )
    markdown_en = (
        f"# {title_en}\n\n"
        + "\n".join(f"- {item}" for item in items_en)
        + "\n\n> Price: customer-specific quote after qualified discovery only.\n"
    )

    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "ladder": CURRENT_PATH,
        "manifest": {
            "artifact_type": "pricing_page",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "highlight": None,
            "tier_count": 1,
            "product_count": 1,
            "public_fixed_price": False,
            "quote_only": True,
            "live_checkout": False,
            "price_authority": "customer_specific_quote_after_qualified_discovery",
        },
    }
