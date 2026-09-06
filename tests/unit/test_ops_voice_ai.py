from __future__ import annotations

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers import ops_voice_ai


def test_ops_readiness_is_non_secret_and_explicit_about_recording(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "secret-api-key")
    monkeypatch.setenv("OPENAI_WEBHOOK_SECRET", "secret-webhook-key")
    monkeypatch.setenv("VOICE_AI_ENABLED", "false")

    app = FastAPI()
    app.include_router(ops_voice_ai.router)
    response = TestClient(app).get("/api/v1/ops/voice-ai/readiness")

    assert response.status_code == 200
    data = response.json()
    assert data["openai_api_key_configured"] is True
    assert data["webhook_secret_configured"] is True
    assert data["enabled"] is False
    assert data["raw_recording_persistence"] is False
    assert data["live_voice"] == "cedar"
    assert data["model"] == "gpt-realtime-2.1"
    assert data["model_locked"] is True
    assert "secret-api-key" not in response.text
    assert "secret-webhook-key" not in response.text
