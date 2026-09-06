from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import openai_realtime_webhook as voice_router
from dealix.voice_ai.front_desk import VoiceWebhookResult


def _client() -> TestClient:
    app = FastAPI()
    app.include_router(voice_router.router)
    return TestClient(app)


def test_public_webhook_surface_has_no_readiness_endpoint():
    response = _client().get("/api/v1/webhooks/openai/voice-readiness")
    assert response.status_code == 404


def test_realtime_webhook_requires_both_secrets(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_WEBHOOK_SECRET", raising=False)
    response = _client().post("/api/v1/webhooks/openai/realtime", content=b"{}")
    assert response.status_code == 503
    assert response.json()["detail"] == "voice_ai_credentials_not_configured"


def test_verified_provider_handler_result_is_returned_without_call_id(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-api-key")
    monkeypatch.setenv("OPENAI_WEBHOOK_SECRET", "test-webhook-secret")
    monkeypatch.setenv("VOICE_AI_ENABLED", "true")

    def fake_handler(raw_body, headers, config):
        assert raw_body == "{}"
        assert config.model == "gpt-realtime-2.1"
        return VoiceWebhookResult(
            event_type="response.completed",
            action="ignored",
            call_id="provider-call-id-should-not-be-returned",
            start_sideband=False,
        )

    monkeypatch.setattr(voice_router, "handle_openai_realtime_webhook", fake_handler)
    response = _client().post(
        "/api/v1/webhooks/openai/realtime",
        content=b"{}",
        headers={"content-type": "application/json"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "ok": True,
        "event_type": "response.completed",
        "action": "ignored",
        "sideband_started": False,
    }
    assert "provider-call-id" not in response.text
