# Bilingual Reporting Standards — معايير التقارير ثنائية اللغة

## Overview

Dealix generates bilingual reports in Arabic (primary) and English (secondary)
with proper RTL/LTR handling, PDF support, and consistent formatting.

## Report Structure

### Required Fields
- `summary_ar` / `summary_en` — Executive summary in both languages
- `governance_notes_ar` / `governance_notes_en` — Governance and compliance notes
- `recommendations_ar` / `recommendations_en` — Actionable recommendations
- `conclusion_ar` / `conclusion_en` — Concluding remarks

### Section Architecture
```
Header
├── Arabic title (right-aligned, bold)
├── English title (left-aligned)
├── Date (Arabic + English)
└── Logo (optional)

Body
├── Executive Summary (Arabic first, then English)
├── Analysis (bilingual sections)
├── Recommendations (action items)
├── Governance Notes (PDPL compliance)
└── Footer
```

## RTL/LTR Handling

### Direction Detection
```python
from auto_client_acquisition.saudi_layer.bilingual_reports import is_rtl

is_rtl("مرحباً بالعالم")  # True
is_rtl("Hello World")      # False
```

### Mixed Content Fixing
```python
from auto_client_acquisition.saudi_layer.bilingual_reports import fix_mixed_direction

text = "Dealix: نقدم حلولاً متكاملة"
fixed = fix_mixed_direction(text)
# Adds proper RTL/LTR markers
```

### HTML Direction Attributes
- Arabic sections: `dir="rtl" lang="ar"`
- English sections: `dir="ltr" lang="en"`
- Each bilingual pair should be clearly separated

### CSS for Arabic Text
```python
from auto_client_acquisition.saudi_layer.bilingual_reports import wrap_arabic_css

css = wrap_arabic_css()
"""
.arabic-text {
    direction: rtl;
    text-align: right;
    font-family: 'Cairo', 'Noto Naskh Arabic', serif;
    line-height: 1.8;
}
"""
```

## PDF Generation

### HTML-to-PDF Pipeline
```python
from auto_client_acquisition.saudi_layer.bilingual_reports import (
    generate_bilingual_pdf_html, BilingualReport
)

report = BilingualReport(...)
html = generate_bilingual_pdf_html(report, logo_url="/logo.png")

# Convert to PDF (using wkhtmltopdf or WeasyPrint)
# wkhtmltopdf --encoding UTF-8 report.html report.pdf
```

### PDF Requirements
- **Page Size**: A4
- **Margins**: 2cm
- **Font Family**: Noto Sans (Latin) + Cairo (Arabic)
- **Font Size**: 12pt body, 18pt titles, 14pt subtitles
- **Encoding**: UTF-8
- **Line Height**: 1.6 English, 1.8 Arabic
- **Color Scheme**: Primary #1a73e8, Text #333, Background #fff

## Report Generation API

### Programmatic Report Creation
```python
from auto_client_acquisition.saudi_layer.bilingual_reports import (
    BilingualReport, BilingualSection, create_default_bilingual_report
)

# Create from scratch
report = BilingualReport(
    title_ar="تقرير تحليل السوق",
    title_en="Market Analysis Report",
    date_ar="١ يناير ٢٠٢٥م",
    date_en="January 1, 2025",
)

report.add_section(
    title_ar="ملخص تنفيذي",
    title_en="Executive Summary",
    body_ar="يقدم هذا التقرير تحليلاً شاملاً...",
    body_en="This report provides a comprehensive analysis...",
)

# Create with templates
report = create_default_bilingual_report(
    title_ar="تقرير ديلكس",
    title_en="Dealix Report",
    include_sections=["executive_summary", "analysis", "recommendations"]
)

# Export formats
html = report.to_html()        # Complete HTML with styles
markdown = report.to_markdown()  # Markdown format
data = report.to_dict()          # Dictionary format
```

### Validation
```python
from auto_client_acquisition.saudi_layer.bilingual_reports import (
    BILINGUAL_REPORT_KEYS, bilingual_report_complete
)

fields = {
    "summary_ar": "...",
    "summary_en": "...",
    # ...
}
is_complete, missing = bilingual_report_complete(fields)
```

## Output Formats

### HTML Output
```html
<div dir="rtl" lang="ar" class="section-arabic">
  <h3>ملخص تنفيذي</h3>
  <p>نص التقرير بالعربية...</p>
</div>
<div dir="ltr" lang="en" class="section-english">
  <h3>Executive Summary</h3>
  <p>Report text in English...</p>
</div>
```

### Markdown Output
```markdown
**ملخص تنفيذي**
نص التقرير بالعربية...

**Executive Summary**
Report text in English...
```

## Code Reference

- **Module**: `auto_client_acquisition/saudi_layer/bilingual_reports.py`
- **Classes**: `BilingualReport`, `BilingualSection`
- **Functions**: `bilingual_report_complete()`, `create_default_bilingual_report()`, `generate_bilingual_pdf_html()`, `is_rtl()`, `fix_mixed_direction()`, `wrap_arabic_css()`
- **Constants**: `BILINGUAL_REPORT_KEYS`
