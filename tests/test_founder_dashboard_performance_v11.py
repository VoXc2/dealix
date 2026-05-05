"""V11 Phase 1 — founder dashboard cache + degraded handling perf test.

Asserts:
- Two calls within the same minute bucket: 2nd is ≥10x faster than 1st
- Cache marker fields are present
- Degraded payload bypasses cache (next call rebuilds)
- No exception leaks; bilingual ``next_action_*`` populated
- Cache layer never returns secrets
"""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.founder_v10 import (
    cached_dashboard_payload,
    reset_cache,
)


def _slow_builder() -> dict[str, Any]:
    import time
    time.sleep(0.05)  # 50ms — fast enough to keep tests <1s, slow enough to measure
    return {
        "title_ar": "ل",
        "title_en": "L",
        "degraded": False,
        "degraded_sections": [],
        "next_action_ar": "x",
        "next_action_en": "y",
    }


def _degraded_builder() -> dict[str, Any]:
    return {
        "title_ar": "ل",
        "title_en": "L",
        "degraded": True,
        "degraded_sections": ["reliability"],
        "next_action_ar": "راجع القسم المتأخر، لكن التشغيل الأساسي مستمر",
        "next_action_en": "Review the degraded section; core operations continue.",
    }


def test_second_call_uses_cache_and_is_faster() -> None:
    reset_cache()
    import time

    t1 = time.perf_counter()
    p1 = cached_dashboard_payload(_slow_builder)
    e1 = time.perf_counter() - t1

    t2 = time.perf_counter()
    p2 = cached_dashboard_payload(_slow_builder)
    e2 = time.perf_counter() - t2

    assert p1["cache_hit"] is False
    assert p1["source"] == "live"
    assert p2["cache_hit"] is True
    assert p2["source"] == "cache"
    assert e2 * 10 < e1, (
        f"cache hit was not ≥10× faster: 1st={e1*1000:.1f}ms 2nd={e2*1000:.1f}ms"
    )


def test_degraded_payload_is_not_cached() -> None:
    reset_cache()
    p1 = cached_dashboard_payload(_degraded_builder)
    p2 = cached_dashboard_payload(_degraded_builder)

    assert p1["degraded"] is True
    assert p2["cache_hit"] is False, "degraded payloads must never be cached"
    assert p2["source"] == "live"


def test_payload_has_required_v11_markers() -> None:
    reset_cache()
    p = cached_dashboard_payload(_slow_builder)
    for key in ("cache_hit", "source", "elapsed_ms"):
        assert key in p, f"missing v11 marker: {key}"
    assert isinstance(p["elapsed_ms"], int)
    assert p["elapsed_ms"] >= 0


def test_no_secrets_leak_into_cached_payload() -> None:
    """The cache layer is generic; ensure it doesn't accidentally
    inject anything resembling secrets into the response."""
    reset_cache()
    p = cached_dashboard_payload(_slow_builder)
    serialized = repr(p).lower()
    forbidden_prefixes = ("sk_live_", "ghp_", "aiza", "anthropic_api", "moyasar_secret")
    for token in forbidden_prefixes:
        assert token not in serialized, f"forbidden token in payload: {token}"


def test_real_dashboard_builder_runs_without_crash() -> None:
    """Smoke-level: the real builder must never raise, even if a
    sub-section is unavailable. Degraded sections are reported, not
    raised."""
    from auto_client_acquisition.founder_v10 import build_dashboard_payload

    reset_cache()
    p = build_dashboard_payload()
    # Even if every section fails, these top-level fields exist.
    for key in ("schema_version", "generated_at", "live_gates", "guardrails",
                "degraded", "degraded_sections", "next_action_ar", "next_action_en"):
        assert key in p, f"missing top-level field: {key}"
    assert isinstance(p["degraded_sections"], list)
