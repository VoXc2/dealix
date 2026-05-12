"""Tests for Sentry PII scrubber (dealix.observability.sentry._scrub_event).

The scrubber is the final guard before any event leaves Dealix for Sentry.
Failures here are PII leaks — hard fail.
"""
from __future__ import annotations

import pytest

from dealix.observability.sentry import _scrub_event


# Helper — minimal valid Sentry event shape

def _evt(**overrides):
    base = {
        "event_id": "abc",
        "level": "error",
        "culprit": "api.routers.foo",
        "request": {"url": "https://api.dealix.me/api/v1/leads", "headers": {}},
    }
    base.update(overrides)
    return base


# ── Headers scrubber ────────────────────────────────────────────

def test_strips_authorization_header():
    evt = _evt(request={
        "url": "https://api.dealix.me/api/v1/leads",
        "headers": {"Authorization": "Bearer sk_test_xxx", "User-Agent": "curl"},
    })
    out = _scrub_event(evt, {})
    assert out is not None
    assert out["request"]["headers"]["Authorization"] == "<redacted>"
    assert out["request"]["headers"]["User-Agent"] == "curl"


def test_strips_cookie_and_api_key_headers():
    evt = _evt(request={
        "url": "https://api.dealix.me/api/v1/leads",
        "headers": {"Cookie": "session=xyz", "X-API-Key": "k_live"},
    })
    out = _scrub_event(evt, {})
    assert out["request"]["headers"]["Cookie"] == "<redacted>"
    assert out["request"]["headers"]["X-API-Key"] == "<redacted>"


def test_case_insensitive_header_match():
    evt = _evt(request={
        "url": "https://api.dealix.me/x",
        "headers": {"authorization": "Bearer t", "X-MOYASAR-SIGNATURE": "abc"},
    })
    out = _scrub_event(evt, {})
    assert out["request"]["headers"]["authorization"] == "<redacted>"
    assert out["request"]["headers"]["X-MOYASAR-SIGNATURE"] == "<redacted>"


# ── Sensitive paths — full blackout of query + body ─────────────

@pytest.mark.parametrize("path", [
    "/api/v1/admin/users",
    "/api/v1/auth/login",
    "/api/v1/webhooks/moyasar",
    "/api/v1/checkout",
])
def test_sensitive_path_redacts_data_and_query(path):
    evt = _evt(request={
        "url": f"https://api.dealix.me{path}?token=abc",
        "headers": {},
        "query_string": "token=abc&key=xyz",
        "data": {"email": "user@example.com", "card_number": "4111111111111111"},
        "cookies": {"session": "abc"},
    })
    out = _scrub_event(evt, {})
    assert out["request"]["query_string"] == "<redacted>"
    assert out["request"]["data"] == "<redacted>"
    assert out["request"]["cookies"] == "<redacted>"


def test_non_sensitive_path_keeps_data():
    evt = _evt(request={
        "url": "https://api.dealix.me/api/v1/leads",
        "headers": {},
        "data": {"company": "Acme"},
    })
    out = _scrub_event(evt, {})
    # Data on non-sensitive paths is NOT scrubbed at the request level
    # (only individual sensitive fields are scrubbed via extras/contexts).
    assert out["request"]["data"] == {"company": "Acme"}


# ── Field-name scrubber (deep) ──────────────────────────────────

def test_scrubs_sensitive_keys_in_extras():
    evt = _evt(extra={
        "email": "user@example.com",
        "password": "p4ssword",
        "company": "Acme",
        "nested": {"api_key": "secret123", "ok": "yes"},
    })
    out = _scrub_event(evt, {})
    assert out["extra"]["email"] == "<redacted>"
    assert out["extra"]["password"] == "<redacted>"
    assert out["extra"]["company"] == "Acme"
    assert out["extra"]["nested"]["api_key"] == "<redacted>"
    assert out["extra"]["nested"]["ok"] == "yes"


def test_scrubs_sensitive_keys_in_lists():
    evt = _evt(contexts={
        "users": [{"email": "a@b.com", "name": "x"}, {"email": "c@d.com", "name": "y"}],
    })
    out = _scrub_event(evt, {})
    for user in out["contexts"]["users"]:
        assert user["email"] == "<redacted>"
        assert user["name"] in ("x", "y")


# ── Drop test-originating events ────────────────────────────────

def test_drops_event_from_tests_path():
    evt = _evt(culprit="tests/test_something.py")
    out = _scrub_event(evt, {})
    assert out is None


def test_drops_event_with_test_underscore_culprit():
    evt = _evt(culprit="my_module:/test_function_name")
    out = _scrub_event(evt, {})
    assert out is None


def test_does_not_drop_production_culprit():
    evt = _evt(culprit="api.routers.pricing:moyasar_webhook")
    out = _scrub_event(evt, {})
    assert out is not None


# ── Defensive: malformed event shouldn't crash ───────────────────

def test_handles_event_without_request():
    evt = {"event_id": "abc", "level": "error", "culprit": "foo"}
    out = _scrub_event(evt, {})
    assert out is not None  # still emitted, no exception


def test_handles_unparseable_url():
    evt = _evt(request={"url": "not://a real url://", "headers": {}})
    # Should not raise even if urlparse returns something odd
    out = _scrub_event(evt, {})
    assert out is not None
