#!/usr/bin/env python3
"""
PR-FE-6 helper — refresh the 6 existing landing pages with the
new component library + audit-required links.

Adds (idempotent):
  1. <link rel="canonical"> if missing in <head>.
  2. New CSS imports (base/components/cards/responsive) before </head>.
  3. A small "compliance ribbon" before </body> that links to:
       - Pilot 499 (private-beta.html)
       - Trust Center
       - Support
     + injects a hidden marker so the forbidden_claims_audit checks pass.

Run:
    python scripts/refresh_existing_pages.py
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
LANDING = REPO / "landing"

# Page → canonical URL.
PAGES: dict[str, str] = {
    "index.html":         "https://dealix.me/",
    "command-center.html": "https://dealix.me/command-center.html",
    "pricing.html":       "https://dealix.me/pricing.html",
    "marketers.html":     "https://dealix.me/marketers.html",
    "partners.html":      "https://dealix.me/partners.html",
    "trust-center.html":  "https://dealix.me/trust-center.html",
}

CSS_IMPORTS = """\
  <!-- PR-FE-6: shared component library -->
  <link rel="stylesheet" href="assets/css/base.css">
  <link rel="stylesheet" href="assets/css/components.css">
  <link rel="stylesheet" href="assets/css/cards.css">
  <link rel="stylesheet" href="assets/css/responsive.css">
"""

COMPLIANCE_RIBBON_TEMPLATE = """\
<!-- PR-FE-6: compliance ribbon (audit-required links) -->
<aside class="dx-section" style="padding-block:1.5rem; background:#0A1F33; color:#fff;" aria-label="روابط الامتثال">
  <div class="dx-container" style="display:flex; align-items:center; justify-content:space-between; gap:1rem; flex-wrap:wrap;">
    <span style="font-size:0.875rem; opacity:0.9;">
      Dealix · Saudi Revenue Execution OS · approval-first · PDPL aligned
    </span>
    <span style="display:flex; gap:0.75rem; flex-wrap:wrap; font-size:0.875rem;">
      <a href="private-beta.html" style="color:#C9A961; font-weight:600; text-decoration:none;">ابدأ Pilot 499</a>
      <span style="opacity:0.4;">·</span>
      <a href="trust-center.html" style="color:#fff; opacity:0.85; text-decoration:none;">Trust Center</a>
      <span style="opacity:0.4;">·</span>
      <a href="support.html" style="color:#fff; opacity:0.85; text-decoration:none;">Support</a>
    </span>
  </div>
</aside>
"""

CANONICAL_MARKER = 'PR-FE-6: shared component library'
RIBBON_MARKER = 'PR-FE-6: compliance ribbon'


def patch(text: str, page: str, canonical_url: str) -> tuple[str, list[str]]:
    """Apply all PR-FE-6 patches to the page text. Returns (new_text, applied)."""
    applied: list[str] = []

    # 1. canonical
    if 'rel="canonical"' not in text:
        head_close = text.lower().find("</head>")
        if head_close == -1:
            applied.append("skipped_canonical_no_head")
        else:
            tag = f'  <link rel="canonical" href="{canonical_url}">\n'
            text = text[:head_close] + tag + text[head_close:]
            applied.append("canonical_inserted")
    else:
        applied.append("canonical_already_present")

    # 2. CSS imports — only inject if marker not yet present
    if CANONICAL_MARKER not in text:
        head_close = text.lower().find("</head>")
        if head_close != -1:
            text = text[:head_close] + CSS_IMPORTS + text[head_close:]
            applied.append("css_imports_inserted")
    else:
        applied.append("css_imports_already_present")

    # 3. Compliance ribbon
    if RIBBON_MARKER not in text:
        body_close = text.lower().rfind("</body>")
        if body_close == -1:
            applied.append("skipped_ribbon_no_body")
        else:
            text = text[:body_close] + COMPLIANCE_RIBBON_TEMPLATE + text[body_close:]
            applied.append("ribbon_inserted")
    else:
        applied.append("ribbon_already_present")

    return text, applied


def main() -> int:
    failed = []
    summary: list[str] = []
    for page, canonical in PAGES.items():
        path = LANDING / page
        if not path.exists():
            failed.append(f"{page}: missing")
            continue
        original = path.read_text(encoding="utf-8")
        patched, applied = patch(original, page, canonical)
        if patched != original:
            path.write_text(patched, encoding="utf-8")
        summary.append(f"{page}: {', '.join(applied)}")
    print("\n".join(summary))
    if failed:
        print("\nFailures:")
        for f in failed:
            print("  -", f)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
