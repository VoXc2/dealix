"""Complete bilingual reports module — Arabic/English with RTL/LTR handling."""

from __future__ import annotations

import html
from dataclasses import dataclass, field
from typing import Any
from xml.sax.saxutils import escape as xml_escape

BILINGUAL_REPORT_KEYS: tuple[str, ...] = (
    "summary_ar",
    "summary_en",
    "governance_notes_ar",
    "governance_notes_en",
    "recommendations_ar",
    "recommendations_en",
    "conclusion_ar",
    "conclusion_en",
)

# RTL/LTR direction indicators
RTL_MARK = "\u200F"  # RIGHT-TO-LEFT MARK
LTR_MARK = "\u200E"  # LEFT-TO-RIGHT MARK
RTL_EMBEDDING = "\u202B"
POP_DIRECTIONAL_FORMATTING = "\u202C"


def bilingual_report_complete(fields: dict[str, str]) -> tuple[bool, tuple[str, ...]]:
    """Check that all required bilingual fields are populated.

    Args:
        fields: Dictionary of field_name -> value.

    Returns:
        (is_complete, missing_fields)
    """
    missing = tuple(k for k in BILINGUAL_REPORT_KEYS if not (fields.get(k) or "").strip())
    return (len(missing) == 0, missing)


def is_rtl(text: str) -> bool:
    """Check if text is primarily RTL (Arabic, Hebrew, etc.)."""
    if not text:
        return False
    rtl_count = 0
    total = 0
    for c in text[:500]:
        if '\u0600' <= c <= '\u06FF' or '\u0750' <= c <= '\u077F' or '\u08A0' <= c <= '\u08FF':
            rtl_count += 1
            total += 1
        elif c.isalpha():
            total += 1
    return total > 0 and (rtl_count / total) > 0.4


def ensure_rtl_direction(text: str) -> str:
    """Ensure Arabic text has proper RTL markers."""
    if is_rtl(text):
        return f"{RTL_EMBEDDING}{text}{POP_DIRECTIONAL_FORMATTING}"
    return text


def fix_mixed_direction(text: str) -> str:
    """Fix mixed RTL/LTR text for proper display."""
    if not text:
        return text
    lines = text.split('\n')
    fixed = []
    for line in lines:
        if is_rtl(line):
            fixed.append(ensure_rtl_direction(line))
        else:
            fixed.append(line)
    return '\n'.join(fixed)


@dataclass
class BilingualSection:
    """A bilingual section with Arabic and English content."""

    title_ar: str
    title_en: str
    body_ar: str
    body_en: str

    def to_html(self) -> str:
        """Render as HTML with proper RTL/LTR handling."""
        ar_html = (
            f'<div dir="rtl" lang="ar" class="section-arabic">\n'
            f'  <h3>{html.escape(self.title_ar)}</h3>\n'
            f'  <p>{html.escape(self.body_ar)}</p>\n'
            f'</div>'
        )
        en_html = (
            f'<div dir="ltr" lang="en" class="section-english">\n'
            f'  <h3>{html.escape(self.title_en)}</h3>\n'
            f'  <p>{html.escape(self.body_en)}</p>\n'
            f'</div>'
        )
        return f'{ar_html}\n{en_html}'

    def to_markdown(self) -> str:
        """Render as Markdown with direction annotations."""
        return (
            f'**{self.title_ar}**  \n'
            f'{self.body_ar}  \n\n'
            f'**{self.title_en}**  \n'
            f'{self.body_en}  \n'
        )


@dataclass
class BilingualReport:
    """Complete bilingual report."""

    title_ar: str
    title_en: str
    date_ar: str
    date_en: str
    sections: list[BilingualSection] = field(default_factory=list)
    metadata: dict[str, str] = field(default_factory=dict)

    def add_section(self, title_ar: str, title_en: str, body_ar: str, body_en: str) -> None:
        self.sections.append(BilingualSection(
            title_ar=title_ar,
            title_en=title_en,
            body_ar=body_ar,
            body_en=body_en,
        ))

    def to_html(self, include_styles: bool = True) -> str:
        """Render complete bilingual report as HTML."""
        style_block = ""
        if include_styles:
            style_block = """
            <style>
                body { font-family: 'Noto Sans', 'Cairo', sans-serif; max-width: 800px; margin: auto; padding: 20px; }
                .section-arabic { margin: 20px 0; padding: 10px; border-right: 3px solid #1a73e8; }
                .section-english { margin: 20px 0; padding: 10px; border-left: 3px solid #1a73e8; }
                .header { text-align: center; border-bottom: 2px solid #ccc; padding-bottom: 10px; }
                h3 { color: #1a73e8; }
                .meta { font-size: 0.9em; color: #666; }
            </style>
            """
        sections_html = '\n'.join(s.to_html() for s in self.sections)
        meta_html = ""
        if self.metadata:
            meta_items = ''.join(
                f"<p><strong>{k}:</strong> {v}</p>" for k, v in self.metadata.items()
            )
            meta_html = f'<div class="meta">{meta_items}</div>'

        return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"><title>{html.escape(self.title_en)}</title>{style_block}</head>
<body>
<div class="header">
  <h1 dir="rtl">{html.escape(self.title_ar)}</h1>
  <h2>{html.escape(self.title_en)}</h2>
  <p dir="rtl">{html.escape(self.date_ar)} | {html.escape(self.date_en)}</p>
</div>
{meta_html}
{sections_html}
</body>
</html>"""

    def to_markdown(self) -> str:
        """Render as bilingual Markdown."""
        lines = [
            f"# {self.title_ar}",
            f"# {self.title_en}",
            f"",
            f"*{self.date_ar} — {self.date_en}*",
            f"",
        ]
        for s in self.sections:
            lines.append("---")
            lines.append(s.to_markdown())
        return '\n'.join(lines)

    def to_dict(self) -> dict[str, Any]:
        """Export to flat dictionary."""
        result: dict[str, Any] = {
            "title_ar": self.title_ar,
            "title_en": self.title_en,
            "date_ar": self.date_ar,
            "date_en": self.date_en,
            "metadata": self.metadata,
            "sections": [{
                "title_ar": s.title_ar,
                "title_en": s.title_en,
                "body_ar": s.body_ar,
                "body_en": s.body_en,
            } for s in self.sections],
        }
        return result


def wrap_arabic_css() -> str:
    """CSS class for Arabic text blocks."""
    return """
    .arabic-text {
        direction: rtl;
        text-align: right;
        font-family: 'Cairo', 'Noto Naskh Arabic', 'Traditional Arabic', serif;
        line-height: 1.8;
    }
    .bilingual-pair {
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }
    .bilingual-pair > div {
        flex: 1;
        min-width: 280px;
    }
    """


def create_default_bilingual_report(
    title_ar: str = "تقرير ديلكس",
    title_en: str = "Dealix Report",
    include_sections: list[str] | None = None,
) -> BilingualReport:
    """Create a bilingual report with default templates.

    Args:
        title_ar: Arabic title.
        title_en: English title.
        include_sections: List of section keys to include.

    Returns:
        BilingualReport with placeholder sections.
    """
    from datetime import UTC, datetime

    now = datetime.now(UTC)
    months_ar = [
        "يناير", "فبراير", "مارس", "أبريل", "مايو", "يونيو",
        "يوليو", "أغسطس", "سبتمبر", "أكتوبر", "نوفمبر", "ديسمبر",
    ]
    date_ar = f"{now.day} {months_ar[now.month - 1]} {now.year}م"
    date_en = now.strftime("%B %d, %Y")

    report = BilingualReport(
        title_ar=title_ar,
        title_en=title_en,
        date_ar=date_ar,
        date_en=date_en,
    )

    default_sections = include_sections or ["executive_summary", "analysis", "recommendations"]

    templates: dict[str, tuple[str, str, str, str]] = {
        "executive_summary": (
            "ملخص تنفيذي",
            "Executive Summary",
            "هذا التقرير يقدم تحليلاً شاملاً للفرص المتاحة بناءً على بيانات السوق ومعايير الأداء.",
            "This report provides a comprehensive analysis of available opportunities based on market data and performance criteria.",
        ),
        "analysis": (
            "التحليل",
            "Analysis",
            "بناءً على البيانات المتاحة، تم تحليل أداء القطاع وتحديد نقاط القوة وفرص التحسين.",
            "Based on available data, sector performance was analyzed and strengths and improvement opportunities identified.",
        ),
        "recommendations": (
            "التوصيات",
            "Recommendations",
            "نوصي بالتركيز على المبادرات التالية لتحقيق أفضل النتائج في السوق السعودي.",
            "We recommend focusing on the following initiatives to achieve the best results in the Saudi market.",
        ),
        "governance": (
            "ملاحظات الحوكمة",
            "Governance Notes",
            "جميع التوصيات مبنية على أدلة متاحة وفق سياسات الحوكمة المعتمدة.",
            "All recommendations are based on available evidence per approved governance policies.",
        ),
    }

    for key in default_sections:
        if key in templates:
            report.add_section(*templates[key])

    return report


def generate_bilingual_pdf_html(
    report: BilingualReport,
    logo_url: str | None = None,
) -> str:
    """Generate printer-friendly HTML suitable for PDF conversion.

    Args:
        report: The bilingual report.
        logo_url: Optional logo URL for the header.

    Returns:
        HTML string for PDF generation.
    """
    logo_html = f'<img src="{logo_url}" height="50" alt="Logo">' if logo_url else ""
    sections_html = '\n'.join(s.to_html() for s in report.sections)

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    @page {{ size: A4; margin: 2cm; }}
    body {{ font-family: 'Noto Sans', 'Cairo', sans-serif; font-size: 12pt; line-height: 1.6; }}
    .header {{ text-align: center; margin-bottom: 30px; }}
    .header h1 {{ font-size: 18pt; margin: 5px 0; }}
    .header h2 {{ font-size: 14pt; color: #555; margin: 5px 0; }}
    .header img {{ margin-bottom: 10px; }}
    .section {{ margin: 15px 0; padding: 10px; page-break-inside: avoid; }}
    .arabic {{ direction: rtl; text-align: right; }}
    .english {{ direction: ltr; text-align: left; }}
    .meta {{ font-size: 10pt; color: #666; margin: 20px 0; padding: 10px; border: 1px solid #ddd; }}
</style>
</head>
<body>
<div class="header">
    {logo_html}
    <h1 class="arabic">{html.escape(report.title_ar)}</h1>
    <h2>{html.escape(report.title_en)}</h2>
    <p class="arabic">{html.escape(report.date_ar)} | {html.escape(report.date_en)}</p>
</div>
{sections_html}
</body>
</html>"""


def extract_bilingual_field(fields: dict[str, str], ar_key: str, en_key: str) -> tuple[str, str]:
    """Extract Arabic and English values from a field dict.

    Args:
        fields: Dictionary of field_name -> value.
        ar_key: Key for Arabic content.
        en_key: Key for English content.

    Returns:
        (arabic, english) tuple.
    """
    ar_val = fields.get(ar_key, "").strip()
    en_val = fields.get(en_key, "").strip()
    return ar_val, en_val


__all__ = [
    "BILINGUAL_REPORT_KEYS",
    "BilingualReport",
    "BilingualSection",
    "bilingual_report_complete",
    "create_default_bilingual_report",
    "extract_bilingual_field",
    "fix_mixed_direction",
    "generate_bilingual_pdf_html",
    "is_rtl",
    "wrap_arabic_css",
]
