"""Mini Diagnostic generator.

Wraps the v5 ``diagnostic_engine.generate_diagnostic`` bilingual
narrative inside Dealix design-token HTML + bilingual markdown.

NO LLM. NO external HTTP. Pure composition.
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.designops.generators.html_renderer import (
    render_artifact_html,
)
from auto_client_acquisition.designops.generators.markdown_renderer import (
    render_artifact_markdown,
)


def _split_bilingual(markdown_ar_en: str) -> tuple[str, str]:
    """Best-effort split of the engine's combined markdown into AR / EN.

    The diagnostic_engine renders Arabic primary then English secondary.
    The English block always starts with the heading
    ``## Executive summary (English)``. We split on that header.
    """
    needle = "## Executive summary (English)"
    if needle in markdown_ar_en:
        ar, en = markdown_ar_en.split(needle, 1)
        return ar.strip(), (needle + en).strip()
    # Fallback: deliver full markdown as both blocks
    return markdown_ar_en, markdown_ar_en


def generate_mini_diagnostic(
    company: str,
    sector: str,
    region: str,
    pipeline_state: str,
    language: str = "bilingual",
) -> dict[str, Any]:
    """Generate a bilingual mini-diagnostic artifact.

    Returns a dict with keys ``markdown_ar``, ``markdown_en``,
    ``html``, and ``manifest``.
    """
    # Defensive import: even if diagnostic_engine is missing we still
    # produce a manifest stub. In the current cherry-pick the engine
    # is present, but the try/except keeps the module robust.
    try:
        from auto_client_acquisition.diagnostic_engine import (
            DiagnosticRequest,
            generate_diagnostic,
        )

        result = generate_diagnostic(
            DiagnosticRequest(
                company=company,
                sector=sector,
                region=region,
                pipeline_state=pipeline_state,
            )
        )
        markdown_ar, markdown_en = _split_bilingual(result.markdown_ar_en)
        recommended = result.recommended_bundle
    except Exception:  # noqa: BLE001 — defensive
        markdown_ar = (
            f"# تشخيص مصغّر — {company}\n\n"
            f"القطاع: {sector} / {region}\n\n"
            "لا بيانات بعد / no data yet."
        )
        markdown_en = (
            f"# Mini Diagnostic — {company}\n\n"
            f"Sector: {sector} / {region}\n\n"
            "no data yet."
        )
        recommended = "growth_starter"

    title_ar = f"تشخيص مصغّر — {company}"
    title_en = f"Mini Diagnostic — {company}"

    sections_ar = [
        {
            "title": "السياق",
            "body": f"الشركة: {company}\nالقطاع: {sector}\nالمنطقة: {region}",
        },
        {"title": "الوضع الحالي", "body": pipeline_state or "غير محدّد"},
        {"title": "الموجز", "body": markdown_ar},
        {
            "title": "الخطوة التالية",
            "items": [
                f"التوصية: ابدؤوا بـ `{recommended}`.",
                "مراجعة المؤسس قبل أي إرسال — لا إرسال آلي.",
            ],
        },
    ]
    sections_en = [
        {
            "title": "Context",
            "body": f"Company: {company}\nSector: {sector}\nRegion: {region}",
        },
        {"title": "Current state", "body": pipeline_state or "not provided"},
        {"title": "Brief", "body": markdown_en},
        {
            "title": "Next step",
            "items": [
                f"Recommendation: start with `{recommended}`.",
                "Founder review required before any send — no auto-send.",
            ],
        },
    ]

    approval_status = "approval_required"
    audience = "internal_review"
    evidence_refs: list[str] = [
        f"diagnostic_engine.generate_diagnostic(company={company!r})",
        f"recommended_bundle={recommended}",
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
    html = render_artifact_html(
        title_ar=title_ar,
        title_en=title_en,
        sections_ar=sections_ar,
        sections_en=sections_en,
        approval_status=approval_status,
        audience=audience,
        evidence_refs=evidence_refs,
    )

    # We also expose AR-only and EN-only markdown for convenience.
    return {
        "markdown_ar": markdown_ar,
        "markdown_en": markdown_en,
        "markdown": md_full,
        "html": html,
        "manifest": {
            "artifact_type": "mini_diagnostic",
            "approval_status": approval_status,
            "safe_to_send": False,
            "evidence_refs": evidence_refs,
            "audience": audience,
            "language": language,
        },
    }
