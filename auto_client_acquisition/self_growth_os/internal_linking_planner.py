"""Internal-linking planner — builds a link graph over our own
``landing/*.html`` and surfaces orphan pages, missing CTAs, and
broken relative links.

This is a measurement module — it never modifies pages. Output
is a structured report consumable by the API and the founder's
weekly review.

Out of scope:
  - Third-party links (we don't follow them; we don't validate them)
  - Anchor-text quality scoring (no NLP here)
  - Authority transfer modelling (no PageRank-style math)
"""
from __future__ import annotations

import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[2]
LANDING = REPO_ROOT / "landing"

SKIP_PAGES = {"posthog_snippet.html"}

# Pages considered "core" for the internal-link audit. Each MUST be
# linked from at least one other page; orphan core pages are bugs.
CORE_PAGES = {
    "index.html",
    "status.html",
    "pricing.html",
    "trust-center.html",
    "founder.html",
    "marketers.html",
}

# Pages considered "service-page-class" — each must contain a CTA.
SERVICE_LIKE_PAGES_PREFIX = (
    "growth-",
    "data-",
    "executive-",
    "partnership-",
    "agency-",
    "saudi-",
    "proof-pack",
)

CTA_PATTERNS = [
    re.compile(r'<a[^>]*class=["\'][^"\']*\bbtn\b[^"\']*["\']', re.IGNORECASE),
    re.compile(r'data-analytics=["\']cta_', re.IGNORECASE),
    re.compile(r'احجز[^<]{0,30}تجربة', re.DOTALL),
    re.compile(r'احجز[^<]{0,30}جلسة', re.DOTALL),
    re.compile(r'\bbook[ -]?(a[ -]?)?demo\b', re.IGNORECASE),
]

LINK_PATTERN = re.compile(r'<a\s+[^>]*href=["\']([^"\']+)["\']', re.IGNORECASE)


def _is_local_link(href: str) -> tuple[bool, str | None]:
    """Returns (is_local_landing_link, normalized_target_filename_or_anchor)."""
    if not href or href.startswith(("mailto:", "tel:", "javascript:")):
        return False, None
    parsed = urlparse(href)
    if parsed.scheme and parsed.scheme not in {"", "http", "https"}:
        return False, None
    # External (different host) — not in scope
    if parsed.netloc:
        return False, None
    path = parsed.path or ""
    if path in {"", "/"}:
        return True, "index.html"
    # Strip leading slash, anchor handling
    fname = path.lstrip("/").rstrip("/")
    if not fname:
        return True, "index.html"
    if "#" in fname:
        fname = fname.split("#", 1)[0]
    if not fname:
        return True, "index.html"
    if not fname.endswith(".html"):
        # Could be an asset; landing pages all end in .html.
        return False, None
    return True, fname


def _scan_page(html: str) -> tuple[list[str], bool]:
    """Return (linked_pages, has_cta)."""
    targets: list[str] = []
    for m in LINK_PATTERN.finditer(html):
        is_local, target = _is_local_link(m.group(1))
        if is_local and target:
            targets.append(target)
    has_cta = any(p.search(html) for p in CTA_PATTERNS)
    return targets, has_cta


def _is_service_like(page_name: str) -> bool:
    return any(page_name.startswith(prefix) for prefix in SERVICE_LIKE_PAGES_PREFIX)


def build_graph() -> dict:
    """Walk landing/**/*.html (recursive), build a link graph, and return a
    typed report.

    Pages in subdirectories (e.g. ``landing/free-tools/lead-score-calculator.html``)
    are keyed by their POSIX path relative to ``landing/`` (e.g.
    ``free-tools/lead-score-calculator.html``) so absolute-path hrefs like
    ``/free-tools/lead-score-calculator.html`` resolve correctly against
    the page set.
    """
    pages: dict[str, dict] = {}
    for path in sorted(LANDING.glob("**/*.html")):
        if path.name in SKIP_PAGES:
            continue
        try:
            html = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel_key = path.relative_to(LANDING).as_posix()
        targets, has_cta = _scan_page(html)
        pages[rel_key] = {
            "outbound": targets,
            "outbound_unique": sorted(set(targets)),
            "outbound_count": len(targets),
            "has_cta": has_cta,
        }

    # Compute inbound link counts.
    inbound: Counter[str] = Counter()
    for src, info in pages.items():
        for target in info["outbound"]:
            if target == src:
                continue  # self-links don't count
            inbound[target] += 1
    for name in pages:
        pages[name]["inbound_count"] = inbound.get(name, 0)

    # Detect issues.
    orphan_core: list[str] = []
    service_pages_without_cta: list[str] = []
    broken_relative_links: list[dict] = []
    page_set = set(pages.keys())
    for name, info in pages.items():
        if name in CORE_PAGES and info["inbound_count"] == 0:
            orphan_core.append(name)
        if _is_service_like(name) and not info["has_cta"]:
            service_pages_without_cta.append(name)
        for target in info["outbound_unique"]:
            if target not in page_set:
                broken_relative_links.append({"from": name, "to": target})

    return {
        "schema_version": 1,
        "summary": {
            "pages": len(pages),
            "core_pages_audited": sum(1 for p in pages if p in CORE_PAGES),
            "orphan_core_count": len(orphan_core),
            "service_pages_without_cta_count": len(service_pages_without_cta),
            "broken_relative_links_count": len(broken_relative_links),
        },
        "issues": {
            "orphan_core_pages": orphan_core,
            "service_pages_without_cta": service_pages_without_cta,
            "broken_relative_links": broken_relative_links,
        },
        "graph": pages,
    }


def is_clean() -> bool:
    """True iff there are no orphan core pages, no service pages without
    CTA, and no broken relative links."""
    g = build_graph()
    s = g["summary"]
    return (
        s["orphan_core_count"] == 0
        and s["service_pages_without_cta_count"] == 0
        and s["broken_relative_links_count"] == 0
    )
