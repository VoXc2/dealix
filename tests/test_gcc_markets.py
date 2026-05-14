"""GCC Market Intel — Wave 19 public endpoint."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app
from auto_client_acquisition.governance_os.gcc_markets import (
    GCC_MARKETS,
    get_market,
)

client = TestClient(app)


def test_gcc_markets_endpoint_is_public_no_admin_key_required():
    resp = client.get("/api/v1/gcc-markets")
    assert resp.status_code == 200
    body = resp.json()
    assert body["governance_decision"] == "allow"


def test_gcc_markets_endpoint_lists_four_priority_markets():
    body = client.get("/api/v1/gcc-markets").json()
    assert body["market_count"] == 4
    assert len(body["markets"]) == 4
    countries = {m["country"] for m in body["markets"]}
    assert countries == {"SA", "AE", "QA", "KW"}


def test_saudi_is_the_only_active_market_today():
    body = client.get("/api/v1/gcc-markets").json()
    active = [m for m in body["markets"] if m["dealix_status"] == "active"]
    assert len(active) == 1
    assert active[0]["country"] == "SA"


def test_every_market_carries_bilingual_labels_and_framework_articles():
    body = client.get("/api/v1/gcc-markets").json()
    for m in body["markets"]:
        assert m["country_ar"].strip()
        assert m["country_en"].strip()
        assert m["country_ar"] != m["country_en"]
        assert len(m["framework_articles"]) >= 3, (
            f"{m['country']} should map ≥ 3 articles; got {len(m['framework_articles'])}"
        )


def test_markdown_endpoint_is_bilingual_and_lists_all_markets():
    resp = client.get("/api/v1/gcc-markets/markdown")
    assert resp.status_code == 200
    body = resp.text
    assert "GCC Market Posture" in body
    assert "موقفنا الإقليمي" in body
    assert "Estimated outcomes are not guaranteed outcomes" in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body
    for m in GCC_MARKETS:
        assert m.country_en in body, f"markdown missing {m.country}"
        assert m.country_ar in body, f"markdown missing {m.country} AR"


def test_legacy_alias_lookup_resolves_lowercase_country_codes():
    assert get_market("sa") is not None
    assert get_market("ae") is not None
    assert get_market("XX") is None


def test_market_status_values_are_doctrine_safe():
    """Only 'active' / 'pilot_ready' / 'future_market' allowed — no marketing fluff."""
    allowed = {"active", "pilot_ready", "future_market"}
    body = client.get("/api/v1/gcc-markets").json()
    for m in body["markets"]:
        assert m["dealix_status"] in allowed, (
            f"{m['country']}.dealix_status = {m['dealix_status']!r} not in {allowed}"
        )
