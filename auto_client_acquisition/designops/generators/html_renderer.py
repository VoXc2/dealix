"""HTML renderer for DesignOps artifacts.

Builds a self-contained Arabic-first / English-secondary HTML document
using the Dealix design tokens (palette mirrored from
``landing/founder-dashboard.html``). NO external CDN — every style is
embedded inline so the artifact is portable + safe to share offline.
"""
from __future__ import annotations

import html as _html
from typing import Any


_DEALIX_CSS = """
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{font-family:'IBM Plex Sans Arabic','Segoe UI',Tahoma,Arial,sans-serif;background:#f8fafc;color:#0f172a;line-height:1.6}
.wrap{max-width:880px;margin:0 auto;padding:24px 16px 64px}
.banner{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:16px;padding:10px 14px;background:#fef3c7;border:1px solid #fde68a;border-radius:10px;font-size:13px;color:#92400e}
.chip{display:inline-block;font-size:12px;padding:3px 10px;border-radius:999px;background:#e2e8f0;color:#475569;font-weight:600}
.chip.approval{background:#fee2e2;color:#991b1b}
.chip.audience{background:#dbeafe;color:#1e3a8a}
.hdr h1{font-size:24px;margin:0 0 4px;color:#0f172a}
.hdr .en{font-size:14px;color:#64748b;direction:ltr;text-align:left;margin-bottom:18px}
.section{background:#ffffff;border:1px solid #e2e8f0;border-radius:14px;padding:18px;margin:14px 0}
.section h2{font-size:16px;margin:0 0 8px;color:#0f172a}
.section h2 .en{display:block;font-size:11px;color:#64748b;font-weight:500;direction:ltr;text-align:left;margin-top:2px}
.section ul{margin:8px 0;padding-inline-start:20px}
.section li{margin:3px 0}
.section.en{direction:ltr;text-align:left}
.divider{border:0;border-top:1px dashed #e2e8f0;margin:24px 0}
.footer{margin-top:24px;padding:14px;border-top:1px solid #e2e8f0;color:#64748b;font-size:13px}
.footer .approval-line{margin-top:8px;color:#991b1b;font-weight:600}
.evidence{margin:6px 0 0;padding:0;list-style:none;font-family:'Inter',monospace;font-size:12px;direction:ltr;text-align:left}
.evidence li{padding:2px 0;color:#475569}
.kv{display:flex;justify-content:space-between;gap:12px;padding:6px 0;border-bottom:1px dashed #e2e8f0;font-size:14px}
.kv:last-child{border-bottom:0}
.kv .k{color:#64748b;font-size:13px}
.kv .v{font-weight:600;color:#0f172a}
""".strip()


def _esc(value: Any) -> str:
    if value is None:
        return ""
    return _html.escape(str(value), quote=True)


def _render_section(section: dict[str, Any], *, ltr: bool = False) -> str:
    title = _esc(section.get("title", ""))
    body = section.get("body", "")
    items = section.get("items") or []
    cls = "section en" if ltr else "section"
    parts: list[str] = [f'<div class="{cls}">']
    if title:
        parts.append(f"<h2>{title}</h2>")
    if body:
        # body is plain text; preserve line breaks
        safe = _esc(body).replace("\n", "<br>")
        parts.append(f"<p>{safe}</p>")
    if items:
        parts.append("<ul>")
        for it in items:
            parts.append(f"<li>{_esc(it)}</li>")
        parts.append("</ul>")
    parts.append("</div>")
    return "".join(parts)


def render_artifact_html(
    title_ar: str,
    title_en: str,
    sections_ar: list[dict],
    sections_en: list[dict],
    approval_status: str,
    audience: str,
    evidence_refs: list[str],
) -> str:
    """Compose a bilingual self-contained HTML artifact.

    The document is ``<html lang="ar" dir="rtl">`` (Arabic primary).
    English sections are rendered LTR inside the same document.

    No external CDN, no JS, no analytics — pure inline CSS.
    """
    sections_ar_html = "".join(_render_section(s, ltr=False) for s in sections_ar)
    sections_en_html = "".join(_render_section(s, ltr=True) for s in sections_en)

    evidence_items = "".join(
        f"<li>- {_esc(ref)}</li>" for ref in (evidence_refs or [])
    ) or "<li>(no evidence references)</li>"

    return (
        '<!DOCTYPE html>\n'
        '<html lang="ar" dir="rtl">\n'
        '<head>\n'
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="robots" content="noindex,nofollow">\n'
        f'<title>{_esc(title_ar)} — {_esc(title_en)}</title>\n'
        f'<style>{_DEALIX_CSS}</style>\n'
        '</head>\n'
        '<body>\n'
        '<div class="wrap">\n'
        '<div class="banner">'
        f'<span class="chip approval">{_esc(approval_status)}</span>'
        f'<span class="chip audience">{_esc(audience)}</span>'
        '<span>مراجعة المؤسس مطلوبة قبل المشاركة / Founder approval required before sharing</span>'
        '</div>\n'
        '<div class="hdr">'
        f'<h1>{_esc(title_ar)}</h1>'
        f'<div class="en">{_esc(title_en)}</div>'
        '</div>\n'
        f'{sections_ar_html}\n'
        '<hr class="divider">\n'
        f'{sections_en_html}\n'
        '<div class="footer">'
        '<div><strong>Evidence references / المراجع:</strong></div>'
        f'<ul class="evidence">{evidence_items}</ul>'
        '<div class="approval-line">مراجعة المؤسس مطلوبة قبل المشاركة — Founder approval required before sharing.</div>'
        '</div>\n'
        '</div>\n'
        '</body>\n'
        '</html>\n'
    )
