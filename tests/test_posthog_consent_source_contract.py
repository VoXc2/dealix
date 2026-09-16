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



def test_consent_choice_is_reachable_and_reversible_after_initial_decision() -> None:
    src = PROVIDER.read_text(encoding="utf-8")
    assert "const [preferencesOpen, setPreferencesOpen] = useState(false)" in src
    assert 'aria-label="Analytics privacy preferences"' in src
    assert "setPreferencesOpen(true)" in src
    assert 'consent !== "loading" && !preferencesOpen' in src
    assert "Decline / Revoke" in src
    assert "سحب الموافقة" in src


def test_runtime_consent_override_blocks_capture_immediately_on_revoke() -> None:
    src = PROVIDER.read_text(encoding="utf-8")
    assert "let runtimeConsentOverride: AnalyticsConsent | null = null" in src
    assert 'if (runtimeConsentOverride !== null) return runtimeConsentOverride === "granted"' in src
    assert "runtimeConsentOverride = effectiveConsent" in src
    assert 'if (effectiveConsent === "denied")' in src
    denied_block = src.split('if (effectiveConsent === "denied")', 1)[1]
    assert "posthog.opt_out_capturing()" in denied_block
    assert "posthog.reset()" in denied_block
