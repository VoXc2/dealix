"""GEO/AIO readiness audit — how AI engines see Dealix today.

This is a *measurement* module, not a content generator. It scans
``landing/*.html`` for the structural signals AI search engines
(ChatGPT, Perplexity, Gemini) cite — without ever scraping any
third-party site.

Per 2026 GEO research, AI engines preferentially cite content with:
  - clear ``<meta name="description">``
  - structured FAQ blocks (``itemtype="FAQPage"`` or h2-then-question pattern)
  - schema.org JSON-LD (``application/ld+json``)
  - canonical link
  - Open Graph + Twitter Card metadata
  - explicit ``<html lang>`` so the engine knows the language

This module gives each landing page a per-signal readiness check
and surfaces an actionable gap list. It NEVER:
  - calls AI engines directly
  - writes content
  - touches any non-Dealix site
  - claims a guaranteed ranking improvement
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
LANDING = REPO_ROOT / "landing"

SKIP_PAGES = {"posthog_snippet.html"}


_PATTERNS: dict[str, re.Pattern] = {
    "title": re.compile(r"<title[^>]*>[^<]+</title>", re.IGNORECASE | re.DOTALL),
    "meta_description": re.compile(
        r'<meta\s+[^>]*name=["\']description["\'][^>]*content=["\'][^"\']+["\']',
        re.IGNORECASE | re.DOTALL,
    ),
    "html_lang": re.compile(r'<html[^>]*\blang=["\'][^"\']+["\']', re.IGNORECASE),
    "html_dir": re.compile(r'<html[^>]*\bdir=["\'][^"\']+["\']', re.IGNORECASE),
    "canonical": re.compile(r'<link\s+[^>]*rel=["\']canonical["\']', re.IGNORECASE),
    "og_title": re.compile(r'<meta\s+[^>]*property=["\']og:title["\']', re.IGNORECASE),
    "og_description": re.compile(
        r'<meta\s+[^>]*property=["\']og:description["\']', re.IGNORECASE
    ),
    "twitter_card": re.compile(
        r'<meta\s+[^>]*name=["\']twitter:card["\']', re.IGNORECASE
    ),
    "json_ld": re.compile(
        r'<script[^>]*type=["\']application/ld\+json["\']', re.IGNORECASE
    ),
    "faq_schema": re.compile(
        r'(itemtype=["\'][^"\']*FAQPage[^"\']*["\']|"@type"\s*:\s*"FAQPage")',
        re.IGNORECASE,
    ),
    "faq_block_pattern": re.compile(
        r'<(h\d)[^>]*>[^<]{5,200}\?\s*</\1>', re.IGNORECASE | re.DOTALL
    ),
}


def _has(pattern_key: str, html: str) -> bool:
    return _PATTERNS[pattern_key].search(html) is not None


def _count(pattern_key: str, html: str) -> int:
    return len(list(_PATTERNS[pattern_key].finditer(html)))


def _audit_page(html: str) -> dict[str, object]:
    return {
        "title": _has("title", html),
        "meta_description": _has("meta_description", html),
        "html_lang": _has("html_lang", html),
        "html_dir": _has("html_dir", html),
        "canonical": _has("canonical", html),
        "og_title": _has("og_title", html),
        "og_description": _has("og_description", html),
        "twitter_card": _has("twitter_card", html),
        "json_ld": _has("json_ld", html),
        "faq_schema_jsonld": _has("faq_schema", html),
        "question_headings_count": _count("faq_block_pattern", html),
    }


# Weights (sum = 100) — informed by 2026 GEO research:
#   ~40 points for entity clarity (title, meta, lang, canonical)
#   ~30 points for AI-citation structure (JSON-LD, FAQ schema, question headings)
#   ~30 points for social-share signals (OG, twitter — these get re-cited too)
_WEIGHTS = {
    "title": 10,
    "meta_description": 12,
    "html_lang": 6,
    "html_dir": 4,
    "canonical": 8,
    "og_title": 8,
    "og_description": 8,
    "twitter_card": 6,
    "json_ld": 18,
    "faq_schema_jsonld": 8,
    "question_headings": 12,
}


def _score(audit: dict[str, object]) -> int:
    score = 0
    for key, weight in _WEIGHTS.items():
        if key == "question_headings":
            count = int(audit.get("question_headings_count", 0))
            score += weight if count >= 3 else (weight // 2 if count >= 1 else 0)
            continue
        score += weight if audit.get(key) else 0
    return score


def _gaps(audit: dict[str, object]) -> list[str]:
    out: list[str] = []
    if not audit.get("json_ld"):
        out.append("missing_json_ld")
    if not audit.get("faq_schema_jsonld") and int(audit.get("question_headings_count", 0)) < 3:
        out.append("low_faq_signal")
    if not audit.get("meta_description"):
        out.append("missing_meta_description")
    if not audit.get("canonical"):
        out.append("missing_canonical")
    if not audit.get("og_title") or not audit.get("og_description"):
        out.append("missing_og")
    if not audit.get("twitter_card"):
        out.append("missing_twitter_card")
    return out


def audit_all() -> dict:
    """Audit every landing page; return summary + per-page detail."""
    pages: list[dict] = []
    for path in sorted(LANDING.glob("*.html")):
        if path.name in SKIP_PAGES:
            continue
        try:
            html = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        audit = _audit_page(html)
        pages.append(
            {
                "path": path.name,
                "score": _score(audit),
                "audit": audit,
                "gaps": _gaps(audit),
            }
        )

    if not pages:
        return {"summary": {"pages": 0}, "pages": []}

    avg = sum(p["score"] for p in pages) / len(pages)
    pages_with_json_ld = sum(1 for p in pages if p["audit"].get("json_ld"))
    pages_with_faq = sum(
        1 for p in pages if p["audit"].get("faq_schema_jsonld")
        or int(p["audit"].get("question_headings_count", 0)) >= 3
    )
    return {
        "schema_version": 1,
        "summary": {
            "pages": len(pages),
            "average_score": round(avg, 1),
            "pages_with_json_ld": pages_with_json_ld,
            "pages_with_faq_signal": pages_with_faq,
            "perimeter_clean": all(p["audit"].get("title") and p["audit"].get("meta_description") for p in pages),
        },
        "weights": dict(_WEIGHTS),
        "pages": pages,
    }


def top_priority_pages(limit: int = 5) -> list[dict]:
    """Return up to `limit` pages with the lowest readiness score —
    these are the highest-leverage targets to author next."""
    report = audit_all()
    pages = sorted(report.get("pages") or [], key=lambda p: p["score"])
    return pages[: max(1, limit)]
