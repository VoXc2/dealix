"""Search radar — deterministic keyword priority composer.

This module is *measurement + composition*, not a search-API wrapper.
It reads a manually-curated seed list (``docs/registry/SEED_KEYWORDS.yaml``)
and ranks each keyword using ONLY local signals:

  - which weak landing pages (from ``geo_aio_radar.audit_all``) the
    keyword is relevant to (token overlap with the page filename)
  - which Service Activation Matrix bundle the founder already
    associated the keyword with

There is NO call to Google Search Console, Ahrefs, SEMrush, or any
other external search API — the founder has not authorized B4 in
the Decision Pack. There is NO scraping. There are NO synthetic
search-volume numbers. The radar is opt-in: it composes a report
the founder reviews, never auto-publishing anything.

Forbidden marketing tokens (نضمن, guaranteed, blast, scrape,
cold outreach) are rejected at module-load time so a polluted
seed file fails fast instead of silently shipping.
"""
from __future__ import annotations

import datetime as _dt
import re
from pathlib import Path
from typing import Any

import yaml

from auto_client_acquisition.self_growth_os import (
    geo_aio_radar,
    service_activation_matrix,
)
from auto_client_acquisition.self_growth_os.safe_publishing_gate import (
    FORBIDDEN_PATTERNS,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
SEED_PATH = REPO_ROOT / "docs" / "registry" / "SEED_KEYWORDS.yaml"

ALLOWED_LANGUAGES = {"ar", "en"}

REQUIRED_KEYS = ("keyword", "language", "sector_hint", "suggested_bundle_id")

DATA_SOURCE_DISCLOSURE = "manually-curated, no external search API"


def _has_forbidden_token(text: str) -> list[str]:
    found: list[str] = []
    for token, pattern in FORBIDDEN_PATTERNS:
        if pattern.search(text):
            found.append(token)
    return found


def load_seed_keywords() -> list[dict[str, Any]]:
    """Return the validated seed keyword list.

    Raises ``FileNotFoundError`` if the YAML is missing and
    ``ValueError`` if the structure or vocabulary is invalid.
    """
    if not SEED_PATH.exists():
        raise FileNotFoundError(f"seed keywords not found at {SEED_PATH}")
    with SEED_PATH.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    raw = data.get("keywords") or []
    if not isinstance(raw, list) or not raw:
        raise ValueError("SEED_KEYWORDS.yaml must contain a non-empty 'keywords' list")

    cleaned: list[dict[str, Any]] = []
    for idx, entry in enumerate(raw):
        if not isinstance(entry, dict):
            raise ValueError(f"keywords[{idx}] is not a mapping")
        for key in REQUIRED_KEYS:
            if key not in entry or entry[key] in (None, ""):
                raise ValueError(f"keywords[{idx}] missing required key: {key}")
        kw = str(entry["keyword"]).strip()
        lang = str(entry["language"]).strip().lower()
        if lang not in ALLOWED_LANGUAGES:
            raise ValueError(
                f"keywords[{idx}].language must be 'ar' or 'en'; got {lang!r}"
            )
        forbidden = _has_forbidden_token(kw)
        if forbidden:
            raise ValueError(
                f"keywords[{idx}] keyword contains forbidden tokens: {forbidden}"
            )
        cleaned.append(
            {
                "keyword": kw,
                "language": lang,
                "sector_hint": str(entry["sector_hint"]).strip(),
                "suggested_bundle_id": str(entry["suggested_bundle_id"]).strip(),
            }
        )
    return cleaned


_TOKEN_RE = re.compile(r"[A-Za-z؀-ۿ]{3,}")


def _tokens(text: str) -> set[str]:
    return {t.lower() for t in _TOKEN_RE.findall(text or "")}


def _weak_pages() -> list[dict[str, Any]]:
    """Return GEO/AIO weak pages (score below the cohort average)."""
    report = geo_aio_radar.audit_all() or {}
    pages = report.get("pages") or []
    if not pages:
        return []
    avg = (report.get("summary") or {}).get("average_score") or 0
    # weak = at-or-below average score
    weak = [p for p in pages if p.get("score", 0) <= avg]
    return weak


def _bundle_keyword_index() -> dict[str, set[str]]:
    """Map bundle_id -> set of tokens drawn from matrix service names.

    Pure local lookup over the YAML the validator already polices.
    """
    out: dict[str, set[str]] = {}
    try:
        matrix = service_activation_matrix.load_matrix()
    except FileNotFoundError:
        return out
    for svc in matrix.get("services", []) or []:
        bundle = str(svc.get("bundle", "")).strip()
        if not bundle:
            continue
        tokens = _tokens(
            " ".join(
                str(svc.get(k, "") or "")
                for k in (
                    "service_id",
                    "name_ar",
                    "name_en",
                    "capability_group",
                )
            )
        )
        out.setdefault(bundle, set()).update(tokens)
    return out


def _score_keyword(
    entry: dict[str, Any],
    weak_pages: list[dict[str, Any]],
    bundle_index: dict[str, set[str]],
) -> tuple[int, list[str]]:
    """Return (priority_score, why_reasons).

    priority = (weak_page_match * 2) + (bundle_keyword_match * 1)
    """
    kw_tokens = _tokens(entry["keyword"])
    why: list[str] = []

    weak_page_match = 0
    matched_pages: list[str] = []
    for page in weak_pages:
        page_name = str(page.get("path", ""))
        page_tokens = _tokens(page_name.replace("-", " ").replace("_", " "))
        if kw_tokens & page_tokens:
            weak_page_match += 1
            matched_pages.append(page_name)

    bundle_id = entry["suggested_bundle_id"]
    bundle_tokens = bundle_index.get(bundle_id, set())
    bundle_keyword_match = len(kw_tokens & bundle_tokens)

    score = (weak_page_match * 2) + bundle_keyword_match

    if weak_page_match:
        why.append(
            f"weak_page_match={weak_page_match} ({', '.join(matched_pages[:3])})"
        )
    if bundle_keyword_match:
        why.append(
            f"bundle_token_overlap={bundle_keyword_match} (bundle={bundle_id})"
        )
    if not why:
        why.append(f"baseline_seed (bundle={bundle_id}, sector={entry['sector_hint']})")
    return score, why


def build_search_radar(top_n: int = 10) -> dict[str, Any]:
    """Compose the deterministic search radar report.

    This is the single typed entry point used by the API router and
    the tests. It returns a plain dict so it serializes cleanly via
    FastAPI without a Pydantic model dance.
    """
    keywords = load_seed_keywords()
    weak_pages = _weak_pages()
    bundle_index = _bundle_keyword_index()

    scored: list[dict[str, Any]] = []
    for entry in keywords:
        score, why = _score_keyword(entry, weak_pages, bundle_index)
        scored.append(
            {
                "keyword": entry["keyword"],
                "language": entry["language"],
                "sector_hint": entry["sector_hint"],
                "suggested_bundle": entry["suggested_bundle_id"],
                "priority_score": score,
                "why": why,
            }
        )
    # deterministic ranking: higher score first, then keyword text alpha
    scored.sort(key=lambda r: (-r["priority_score"], r["keyword"]))

    top = scored[: max(1, top_n)]
    return {
        "schema_version": 1,
        "generated_at": _dt.datetime.now(_dt.UTC).isoformat(timespec="seconds"),
        "keywords_total": len(scored),
        "top_priority_keywords": top,
        "all_keywords": scored,
        "data_sources": {
            "disclosure": DATA_SOURCE_DISCLOSURE,
            "seed_file": str(SEED_PATH.relative_to(REPO_ROOT)),
            "weak_pages_signal": "auto_client_acquisition.self_growth_os.geo_aio_radar.audit_all",
            "bundle_signal": "auto_client_acquisition.self_growth_os.service_activation_matrix.load_matrix",
            "external_search_api_used": False,
        },
        "guardrails": {
            "no_external_api": True,
            "no_volume_estimates_without_source": True,
            "manual_review_required": True,
            "no_scraping": True,
            "opt_in_only": True,
        },
    }


def status() -> dict[str, Any]:
    """Cheap probe for the dashboard. No file IO beyond seed YAML existence."""
    return {
        "module": "self_growth_os.search_radar",
        "seed_file_present": SEED_PATH.exists(),
        "seed_file_path": str(SEED_PATH.relative_to(REPO_ROOT)),
        "data_sources": {
            "disclosure": DATA_SOURCE_DISCLOSURE,
            "external_search_api_used": False,
        },
        "guardrails": {
            "no_external_api": True,
            "no_volume_estimates_without_source": True,
            "manual_review_required": True,
            "no_scraping": True,
            "opt_in_only": True,
        },
    }
