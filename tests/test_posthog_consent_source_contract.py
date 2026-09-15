"""Public analytics must be explicit-opt-in and privacy-safe."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROVIDER = ROOT / "apps/web/lib/analytics/posthog.tsx"
TRACKED = ROOT / "apps/web/components/analytics/TrackedLink.tsx"


def test_posthog_init_is_guarded_by_explicit_local_consent() -> None:
    src = PROVIDER.read_text(encoding="utf-8")
    assert 'ANALYTICS_CONSENT_KEY = "dealix.analytics_consent.v1"' in src
    assert 'consent !== "granted"' in src
    assert 'posthog.init' in src
    assert 'const persisted = persistConsent(value)' in src
    assert '"denied"' in src


def test_posthog_privacy_safe_defaults_disable_automatic_collection() -> None:
    src = PROVIDER.read_text(encoding="utf-8")
    for contract in (
        "autocapture: false",
        "capture_pageview: false",
        "capture_pageleave: false",
        "disable_session_recording: true",
        'person_profiles: "identified_only"',
    ):
        assert contract in src


def test_tracked_links_fail_closed_before_analytics_opt_in() -> None:
    src = TRACKED.read_text(encoding="utf-8")
    assert "analyticsConsentGranted" in src
    assert "if (!analyticsConsentGranted()) return" in src
    assert src.index("if (!analyticsConsentGranted()) return") < src.index("posthog.capture")


def test_consent_copy_rejects_direct_identifiers_and_session_replay() -> None:
    src = PROVIDER.read_text(encoding="utf-8")
    assert "لا نرسل الاسم أو البريد أو الهاتف أو نصوص النماذج" in src
    assert "no session replay, autocapture, or direct identifiers" in src


def test_consent_storage_failures_fail_closed_without_initializing_analytics() -> None:
    src = PROVIDER.read_text(encoding="utf-8")
    assert "try {" in src
    assert "window.localStorage.getItem" in src
    assert "window.localStorage.setItem" in src
    assert "return false;" in src
    assert 'value === "granted" && !persisted ? "denied" : value' in src
