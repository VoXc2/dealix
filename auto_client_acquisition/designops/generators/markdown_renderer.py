"""Markdown renderer for DesignOps artifacts.

Bilingual document: Arabic block first, then ``---``, then English
block. Footer carries the approval banner. Pure templating — no
external calls.
"""
from __future__ import annotations

from typing import Any


def _section_md(section: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    title = section.get("title", "")
    body = section.get("body", "")
    items = section.get("items") or []
    if title:
        lines.append(f"## {title}")
    if body:
        lines.append(str(body))
    for it in items:
        lines.append(f"- {it}")
    if title or body or items:
        lines.append("")
    return lines


def render_artifact_markdown(
    title_ar: str,
    title_en: str,
    sections_ar: list[dict],
    sections_en: list[dict],
    approval_status: str,
    audience: str,
    evidence_refs: list[str],
) -> str:
    """Compose a bilingual markdown artifact.

    Arabic block is rendered first (Arabic primary), separator,
    English block, then a footer with approval + audience banners
    and evidence references.
    """
    lines: list[str] = []

    # Arabic primary block
    lines.append(f"# {title_ar}")
    lines.append("")
    lines.append(
        f"> **حالة الموافقة:** `{approval_status}`  "
        f"**الجمهور:** `{audience}`"
    )
    lines.append(
        "> مراجعة المؤسس مطلوبة قبل أي مشاركة — لا إرسال آلي."
    )
    lines.append("")
    for s in sections_ar:
        lines.extend(_section_md(s))

    lines.append("---")
    lines.append("")

    # English secondary block
    lines.append(f"# {title_en}")
    lines.append("")
    lines.append(
        f"> **Approval status:** `{approval_status}`  "
        f"**Audience:** `{audience}`"
    )
    lines.append(
        "> Founder approval required before sharing — no auto-send."
    )
    lines.append("")
    for s in sections_en:
        lines.extend(_section_md(s))

    lines.append("---")
    lines.append("")
    lines.append("## Evidence references / المراجع")
    if evidence_refs:
        for ref in evidence_refs:
            lines.append(f"- `{ref}`")
    else:
        lines.append("- (no evidence references / لا مراجع بعد)")
    lines.append("")
    lines.append(
        "> ⚠️ Founder approval required before sharing — "
        "مراجعة المؤسس مطلوبة قبل المشاركة."
    )
    return "\n".join(lines)
