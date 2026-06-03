"""Tests for self_growth_os.search_radar.

The radar is a STATIC + LOCAL signal composer. It must:
  - load and validate docs/registry/SEED_KEYWORDS.yaml
  - reject any forbidden marketing token in any keyword
  - produce a deterministic priority ranking from local-only signals
  - never claim it called an external search API
  - keep both Arabic and English keywords visible at the top
"""
from __future__ import annotations

import pytest
import yaml
from httpx import ASGITransport, AsyncClient

from auto_client_acquisition.self_growth_os import search_radar
from auto_client_acquisition.self_growth_os.safe_publishing_gate import (
    FORBIDDEN_PATTERNS,
)

REQUIRED_KEYS = {"keyword", "language", "sector_hint", "suggested_bundle_id"}
ALLOWED_BUNDLES = {
    "growth_starter",
    "data_to_revenue",
    "executive_growth_os",
    "partnership_growth",
    "full_control_tower",
    "internal",
}


def test_seed_yaml_loads_and_validates_schema():
    raw = yaml.safe_load(search_radar.SEED_PATH.read_text(encoding="utf-8"))
    keywords = raw.get("keywords") or []
    assert keywords, "SEED_KEYWORDS.yaml must contain a non-empty 'keywords' list"
    assert len(keywords) >= 20, (
        f"expected >=20 seed keywords, got {len(keywords)}"
    )
    for idx, entry in enumerate(keywords):
        missing = REQUIRED_KEYS - set(entry.keys())
        assert not missing, f"keywords[{idx}] missing keys: {missing}"
        assert entry["language"] in {"ar", "en"}, (
            f"keywords[{idx}].language invalid: {entry['language']!r}"
        )
        assert entry["suggested_bundle_id"] in ALLOWED_BUNDLES, (
            f"keywords[{idx}].suggested_bundle_id not in matrix bundles: "
            f"{entry['suggested_bundle_id']!r}"
        )


def test_no_forbidden_tokens_in_any_keyword():
    """Any keyword carrying نضمن / guaranteed / blast / scrape /
    cold outreach must NEVER ship in the radar."""
    keywords = search_radar.load_seed_keywords()
    for entry in keywords:
        for token, pattern in FORBIDDEN_PATTERNS:
            assert not pattern.search(entry["keyword"]), (
                f"keyword {entry['keyword']!r} contains forbidden token {token!r}"
            )


def test_build_search_radar_returns_at_least_ten_keywords():
    report = search_radar.build_search_radar()
    assert report["schema_version"] == 1
    assert report["keywords_total"] >= 20
    assert len(report["top_priority_keywords"]) >= 10
    # Ranking is deterministic — re-running yields identical scores.
    again = search_radar.build_search_radar()
    pairs1 = [(r["keyword"], r["priority_score"]) for r in report["all_keywords"]]
    pairs2 = [(r["keyword"], r["priority_score"]) for r in again["all_keywords"]]
    assert pairs1 == pairs2, "search_radar ranking is not deterministic"


def test_data_sources_field_explicitly_says_manually_curated():
    report = search_radar.build_search_radar()
    sources = report["data_sources"]
    assert "manually-curated" in sources["disclosure"]
    assert "no external search API" in sources["disclosure"]
    assert sources["external_search_api_used"] is False


def test_guardrails_block_external_api_and_volume_invention():
    report = search_radar.build_search_radar()
    g = report["guardrails"]
    assert g["no_external_api"] is True
    assert g["no_volume_estimates_without_source"] is True
    assert g["manual_review_required"] is True
    assert g["no_scraping"] is True
    assert g["opt_in_only"] is True


def test_top_priority_is_bilingual():
    """Guard against the radar collapsing to one language."""
    report = search_radar.build_search_radar()
    langs = {r["language"] for r in report["top_priority_keywords"]}
    assert "ar" in langs, "top priorities must include >=1 Arabic keyword"
    assert "en" in langs, "top priorities must include >=1 English keyword"


def test_every_top_keyword_carries_a_why():
    report = search_radar.build_search_radar()
    for r in report["top_priority_keywords"]:
        assert r["why"], f"missing why for {r['keyword']!r}"
        assert isinstance(r["why"], list)
        assert all(isinstance(x, str) and x for x in r["why"])


# ─── API endpoint tests ─────────────────────────────────────────────


@pytest.mark.asyncio
async def test_router_status_endpoint_returns_no_external_api_guardrail():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/search-radar/status")
    assert r.status_code == 200
    payload = r.json()
    assert payload["module"] == "self_growth_os.search_radar"
    assert payload["guardrails"]["no_external_api"] is True
    assert payload["data_sources"]["external_search_api_used"] is False
    assert "manually-curated" in payload["data_sources"]["disclosure"]


@pytest.mark.asyncio
async def test_router_report_endpoint_returns_full_payload():
    from api.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        r = await client.get("/api/v1/search-radar/report")
    assert r.status_code == 200
    payload = r.json()
    assert payload["keywords_total"] >= 20
    assert len(payload["top_priority_keywords"]) >= 10
    assert payload["data_sources"]["external_search_api_used"] is False
