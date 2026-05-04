#!/usr/bin/env python3
"""Technical SEO auditor for the static landing site.

Scans every ``landing/*.html`` page and emits a JSON report listing
required-but-missing technical-SEO elements:

  - ``<title>``
  - ``<meta name="description">``
  - ``<meta name="viewport">``
  - canonical link
  - ``<html lang="…" dir="…">``
  - Open Graph title + description
  - Twitter card

The audit is intentionally minimal and *honest*: it surfaces what's
missing without inventing scores or claiming Google rankings. No
external HTTP requests are made.

Output: ``docs/SEO_AUDIT_REPORT.json``

Exit codes:
  0 — all required elements present (advisory items may still be missing)
  1 — at least one *required* element is missing on at least one page

Pair with ``tests/test_seo_audit.py`` to lock the perimeter in CI.
"""
from __future__ import annotations

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parents[1]
LANDING = REPO / "landing"
OUTPUT = REPO / "docs" / "SEO_AUDIT_REPORT.json"

# Pages that aren't true content pages and shouldn't be audited as such.
SKIP_PAGES = {
    "posthog_snippet.html",  # snippet include, not a page
}

# Pages that legitimately don't need an `og:title` / `og:description`
# (they're internal redirects or single-purpose readiness placeholders).
ADVISORY_ONLY_PAGES = {
    "launch-readiness.html",
}

REQUIRED_CHECKS = [
    "title",
    "meta_description",
    "meta_viewport",
    "html_lang",
    "html_dir",
]
ADVISORY_CHECKS = [
    "canonical",
    "og_title",
    "og_description",
    "twitter_card",
]


@dataclass
class PageReport:
    path: str
    present: dict[str, bool] = field(default_factory=dict)
    missing_required: list[str] = field(default_factory=list)
    missing_advisory: list[str] = field(default_factory=list)


def _has(pattern: str, html: str) -> bool:
    return re.search(pattern, html, flags=re.IGNORECASE | re.DOTALL) is not None


def _audit(html: str) -> dict[str, bool]:
    return {
        "title": _has(r"<title[^>]*>[^<]+</title>", html),
        "meta_description": _has(
            r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'][^"\']+["\']',
            html,
        ),
        "meta_viewport": _has(
            r'<meta\s+[^>]*name=["\']viewport["\']', html
        ),
        "html_lang": _has(r'<html[^>]*\blang=["\'][^"\']+["\']', html),
        "html_dir": _has(r'<html[^>]*\bdir=["\'][^"\']+["\']', html),
        "canonical": _has(
            r'<link\s+[^>]*rel=["\']canonical["\']', html
        ),
        "og_title": _has(
            r'<meta\s+[^>]*property=["\']og:title["\']', html
        ),
        "og_description": _has(
            r'<meta\s+[^>]*property=["\']og:description["\']', html
        ),
        "twitter_card": _has(
            r'<meta\s+[^>]*name=["\']twitter:card["\']', html
        ),
    }


def _iter_pages() -> Iterable[Path]:
    for p in sorted(LANDING.glob("*.html")):
        if p.name in SKIP_PAGES:
            continue
        yield p


def audit_all() -> tuple[list[PageReport], dict[str, int]]:
    reports: list[PageReport] = []
    for path in _iter_pages():
        html = path.read_text(encoding="utf-8")
        present = _audit(html)
        rep = PageReport(path=path.name, present=present)
        for k in REQUIRED_CHECKS:
            if not present.get(k):
                rep.missing_required.append(k)
        # Advisory checks are skipped for explicitly listed pages.
        if path.name not in ADVISORY_ONLY_PAGES:
            for k in ADVISORY_CHECKS:
                if not present.get(k):
                    rep.missing_advisory.append(k)
        reports.append(rep)

    summary = {
        "total_pages": len(reports),
        "pages_with_required_gap": sum(1 for r in reports if r.missing_required),
        "pages_with_advisory_gap": sum(1 for r in reports if r.missing_advisory),
    }
    return reports, summary


def main() -> int:
    reports, summary = audit_all()
    payload = {
        "schema_version": 1,
        "summary": summary,
        "required_checks": REQUIRED_CHECKS,
        "advisory_checks": ADVISORY_CHECKS,
        "skipped_pages": sorted(SKIP_PAGES),
        "advisory_only_pages": sorted(ADVISORY_ONLY_PAGES),
        "pages": [
            {
                "path": r.path,
                "present": r.present,
                "missing_required": r.missing_required,
                "missing_advisory": r.missing_advisory,
            }
            for r in reports
        ],
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"OK: wrote {OUTPUT.relative_to(REPO)} "
        f"(pages={summary['total_pages']}, "
        f"required_gap={summary['pages_with_required_gap']}, "
        f"advisory_gap={summary['pages_with_advisory_gap']})"
    )
    return 1 if summary["pages_with_required_gap"] else 0


if __name__ == "__main__":
    sys.exit(main())
