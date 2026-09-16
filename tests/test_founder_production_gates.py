"""Founder production gates — unified Railway + GTM + weekly blockers."""

from __future__ import annotations

from dealix.commercial_ops.founder_production_gates import build_founder_production_gates
from dealix.commercial_ops.railway_production import probe_trust_layer


def test_build_founder_production_gates_offline() -> None:
    blob = build_founder_production_gates(skip_live=True)
    assert blob["verdict"] in ("PASS", "WARN", "FAIL")
    assert blob["railway"]["repo"]["ok"]
    assert "gtm_surfaces_repo" in blob
    assert "commands" in blob


def test_probe_trust_layer_stale_healthz(monkeypatch) -> None:
    """Minimal healthz is stale only when the dedicated identity endpoint is unavailable."""
    responses = {
        "/healthz": {"probed": True, "status": 200, "ok": True, "snippet": '{"status":"ok"}'},
        "/version": {"probed": True, "status": 404, "ok": False},
        "/api/v1/meta": {"probed": True, "status": 200, "ok": True, "snippet": "{}"},
        "/health": {"probed": True, "status": 200, "ok": True, "snippet": "{}"},
    }

    def fake_probe_get(_api_base, path, *, timeout_sec=12.0, max_bytes=4096):
        return responses[path]

    monkeypatch.setattr(
        "dealix.commercial_ops.railway_production.probe_get", fake_probe_get
    )
    blob = probe_trust_layer("https://api.dealix.me")
    assert blob["deploy_stale_hint_ar"]
    assert blob["ok"] is False


def test_probe_trust_layer_accepts_minimal_healthz_with_live_version(monkeypatch) -> None:
    responses = {
        "/healthz": {"probed": True, "status": 200, "ok": True, "snippet": '{"status":"ok","service":"dealix"}'},
        "/version": {"probed": True, "status": 200, "ok": True, "snippet": '{"git_sha":"' + ("a" * 40) + '"}'},
        "/api/v1/meta": {"probed": True, "status": 200, "ok": True, "snippet": "{}"},
        "/health": {"probed": True, "status": 200, "ok": True, "snippet": '{"git_sha":"' + ("a" * 40) + '"}'},
    }

    def fake_probe_get(_api_base, path, *, timeout_sec=12.0, max_bytes=4096):
        return responses[path]

    monkeypatch.setattr(
        "dealix.commercial_ops.railway_production.probe_get", fake_probe_get
    )
    blob = probe_trust_layer("https://api.dealix.me")
    assert blob["deploy_stale_hint_ar"] == ""
    assert blob["ok"] is True
