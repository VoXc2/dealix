"""Proof Pack renderer — customer-facing HTML/PDF/email for a Sprint Proof Pack.

Pure functions over the Proof Pack dict produced by the Sprint orchestrator
(`delivery_factory.delivery_sprint.step6_proof_pack`): ``{"sections": {...14...},
"score": int, "tier": str, ...}``. Mirrors the Trust Pack renderer shape and
reuses the shared markdown→PDF renderer. No external sends.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from auto_client_acquisition.proof_architecture_os.proof_pack_v2 import (
    PROOF_PACK_V2_SECTIONS,
)

_DISCLAIMER = (
    "Estimated outcomes are not guaranteed outcomes / "
    "النتائج التقديرية ليست نتائج مضمونة."
)

# Ordered (key, English title, Arabic title) for the 14 canonical sections.
_SECTION_TITLES: tuple[tuple[str, str, str], ...] = (
    ("executive_summary", "Executive Summary", "الملخص التنفيذي"),
    ("problem", "Problem", "المشكلة"),
    ("inputs", "Inputs", "المدخلات"),
    ("source_passports", "Source Passports", "جوازات المصدر"),
    ("work_completed", "Work Completed", "العمل المُنجَز"),
    ("outputs", "Outputs", "المخرجات"),
    ("quality_scores", "Quality Scores", "درجات الجودة"),
    ("governance_decisions", "Governance Decisions", "قرارات الحوكمة"),
    ("blocked_risks", "Blocked & Risks", "المحجوب والمخاطر"),
    ("value_metrics", "Value Metrics", "مقاييس القيمة"),
    ("limitations", "Limitations", "القيود والحدود"),
    ("recommended_next_step", "Recommended Next Step", "الخطوة التالية الموصى بها"),
    ("retainer_expansion_path", "Retainer / Expansion Path", "مسار التوسّع والاشتراك"),
    ("capital_assets_created", "Capital Assets Created", "الأصول المُنشأة"),
)


def _sections(pack: dict[str, Any] | None) -> dict[str, str]:
    return dict(((pack or {}).get("sections") or {}))


def _has_content(sections: dict[str, str]) -> bool:
    return any((sections.get(k) or "").strip() for k in PROOF_PACK_V2_SECTIONS)


def _not_generated_notice(customer_handle: str, generated_at: str) -> str:
    body = (
        "> This engagement has not produced a scored Proof Pack. Run the "
        + "Sprint with the customer's data first. No proof is fabricated — "
        + "an empty pack is reported honestly as empty."
    )
    return "\n".join(
        [
            f"# Dealix Proof Pack — {customer_handle}",
            "",
            f"_Generated: {generated_at}_",
            "",
            "> **Proof Pack not yet generated / لم يُولَّد Proof Pack بعد.**",
            ">",
            body,
            "",
            "---",
            f"_{_DISCLAIMER}_",
        ]
    )


def proof_pack_to_markdown(
    pack: dict[str, Any] | None, *, customer_handle: str
) -> str:
    """Render a Proof Pack dict to a bilingual customer-facing markdown report.

    An empty/missing pack renders a clearly-marked "not yet generated" notice
    rather than a fabricated pack.
    """
    customer_handle = customer_handle or "(customer)"
    generated_at = datetime.now(timezone.utc).isoformat()
    sections = _sections(pack)
    if not _has_content(sections):
        return _not_generated_notice(customer_handle, generated_at)

    score = (pack or {}).get("score")
    tier = (pack or {}).get("tier", "")
    lines = [
        f"# Dealix Proof Pack — {customer_handle}",
        "",
        f"_Generated: {generated_at}_",
        "",
        f"**Proof score / درجة الإثبات:** {score if score is not None else '—'}/100"
        f"  ·  **Tier / المستوى:** {tier or '—'}",
        "",
    ]
    for key, title_en, title_ar in _SECTION_TITLES:
        lines.append(f"## {title_en} / {title_ar}")
        lines.append("")
        lines.append((sections.get(key) or "").strip() or "_—_")
        lines.append("")
    lines.append("---")
    lines.append(f"_{_DISCLAIMER}_")
    return "\n".join(lines)


def proof_pack_to_pdf(
    pack: dict[str, Any] | None, *, customer_handle: str
) -> bytes | None:
    """Render the Proof Pack to PDF bytes. Returns None when no PDF renderer
    is available — the caller falls back to the markdown."""
    from auto_client_acquisition.proof_to_market.pdf_renderer import (
        render_markdown_to_pdf,
    )

    md = proof_pack_to_markdown(pack, customer_handle=customer_handle)
    return render_markdown_to_pdf(
        md, title=f"Dealix Proof Pack — {customer_handle or '(customer)'}"
    )


def proof_pack_email_body(
    pack: dict[str, Any] | None, *, customer_handle: str
) -> str:
    """A short bilingual cover note the founder copies into their own mailbox.

    This is render-only — it never sends. Approval-first stands.
    """
    customer_handle = customer_handle or "(customer)"
    sections = _sections(pack)
    generated = _has_content(sections)
    score = (pack or {}).get("score")
    next_step = (sections.get("recommended_next_step") or "").strip()

    if not generated:
        not_ready = (
            "Proof Pack not yet generated. Run the Sprint with the "
            + "customer's data before sending. / لم يُولَّد Proof Pack بعد."
        )
        return "\n".join(
            [
                f"Subject / الموضوع: Dealix — {customer_handle}",
                "",
                not_ready,
            ]
        )

    score_str = score if score is not None else "—"
    body_ar = (
        f"مرحباً، مرفق Proof Pack الخاص بـ{customer_handle} من Revenue Proof "
        + f"Sprint. درجة الإثبات: {score_str}/100."
    )
    body_en = (
        f"Hello — attached is the Proof Pack for {customer_handle} from the "
        + f"Revenue Proof Sprint. Proof score: {score_str}/100."
    )
    return "\n".join(
        [
            f"Subject / الموضوع: Dealix Proof Pack — {customer_handle}",
            "",
            body_ar,
            (f"الخطوة التالية الموصى بها: {next_step}" if next_step else ""),
            "",
            body_en,
            "",
            _DISCLAIMER,
        ]
    )


__all__ = [
    "proof_pack_email_body",
    "proof_pack_to_markdown",
    "proof_pack_to_pdf",
]
