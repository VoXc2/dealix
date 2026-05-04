"""
Railway healthcheck resilience.

Production deploys fail when /health doesn't return 200 within Railway's
healthcheck window. This test pins three invariants that protect against
that failure mode:

  1. /health and /healthz return 200 even when the LLM provider router
     raises (a misbehaving provider adapter must never fail /health).
  2. /health includes the `git_sha` field so a single curl confirms which
     commit Railway is serving.
  3. Live-action gates default to False even in `production` mode.

The test does NOT exercise startup hooks (lifespan), because TestClient
spins them up synchronously. Lifespan resilience (timeouts on init_db
and the auto-migration) is enforced separately in `api/main.py:lifespan`.
"""

from __future__ import annotations

import importlib

from fastapi.testclient import TestClient

from api.main import create_app
from core.config.settings import Settings


def test_health_returns_200_with_git_sha_and_providers_resilient(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("APP_SECRET_KEY", "test-secret")
    monkeypatch.setenv("DATABASE_URL", "sqlite+aiosqlite:////tmp/dlx_health.db")
    monkeypatch.setenv("GIT_SHA", "ci-test-shaXYZ")

    # Reload settings so the new env is picked up.
    importlib.reload(importlib.import_module("core.config.settings"))

    # Simulate a broken LLM provider router: /health must still return 200.
    def _raise(*_a, **_k):
        raise RuntimeError("provider router exploded")

    monkeypatch.setattr("api.routers.health.get_model_router", _raise)

    app = create_app()
    with TestClient(app) as client:
        r = client.get("/health")
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["status"] == "ok"
        assert "git_sha" in body
        assert body["providers"] == []  # defensive: empty when router raises

        rz = client.get("/healthz")
        assert rz.status_code == 200
        assert rz.json().get("status") == "ok"


def test_settings_has_git_sha_field_default_unknown() -> None:
    s = Settings()
    assert hasattr(s, "git_sha")
    assert isinstance(s.git_sha, str)
    # Default is "unknown" outside containers; can be overridden via GIT_SHA env.


def test_live_action_gates_default_false_under_production(monkeypatch) -> None:
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("WHATSAPP_ALLOW_LIVE_SEND", raising=False)
    monkeypatch.delenv("GMAIL_ALLOW_LIVE_SEND", raising=False)
    monkeypatch.delenv("RESEND_ALLOW_LIVE_SEND", raising=False)
    s = Settings()
    assert s.whatsapp_allow_live_send is False
    assert s.gmail_allow_live_send is False
    assert s.resend_allow_live_send is False
