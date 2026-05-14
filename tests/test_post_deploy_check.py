"""Post-Deploy Self-Check — Wave 16 (A12)."""
from __future__ import annotations

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

ADMIN_HEADER = "X-Admin-API-Key"


def test_post_deploy_check_requires_admin_key():
    resp = client.get("/api/v1/founder/post-deploy-check")
    assert resp.status_code in {401, 403}


def test_post_deploy_check_returns_aggregate_shape(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_post_deploy_check_shape")
    resp = client.get(
        "/api/v1/founder/post-deploy-check",
        headers={ADMIN_HEADER: "test_post_deploy_check_shape"},
    )
    assert resp.status_code == 200
    body = resp.json()
    for field in ("generated_at", "summary", "checks", "governance_decision", "is_estimate"):
        assert field in body, f"missing field: {field}"
    assert body["governance_decision"] == "allow"
    assert body["is_estimate"] is False
    summary = body["summary"]
    for key in ("passed", "failed", "total", "all_green"):
        assert key in summary
    assert summary["total"] == summary["passed"] + summary["failed"]
    assert summary["total"] == len(body["checks"])


def test_post_deploy_check_module_imports_all_ok(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_post_deploy_check_imports")
    resp = client.get(
        "/api/v1/founder/post-deploy-check",
        headers={ADMIN_HEADER: "test_post_deploy_check_imports"},
    )
    assert resp.status_code == 200
    checks = resp.json()["checks"]
    import_checks = [c for c in checks if c["name"].startswith("import:")]
    assert len(import_checks) >= 15
    failed = [c for c in import_checks if not c["ok"]]
    assert failed == [], f"module imports failing: {failed}"


def test_post_deploy_check_governance_envelope_ok(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_post_deploy_check_gov")
    resp = client.get(
        "/api/v1/founder/post-deploy-check",
        headers={ADMIN_HEADER: "test_post_deploy_check_gov"},
    )
    body = resp.json()
    gov = next(c for c in body["checks"] if c["name"] == "governance_envelope")
    assert gov["ok"] is True
    assert "BLOCK" in gov["detail"]


def test_post_deploy_check_doctrine_count_at_least_six(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_post_deploy_check_doctrine")
    resp = client.get(
        "/api/v1/founder/post-deploy-check",
        headers={ADMIN_HEADER: "test_post_deploy_check_doctrine"},
    )
    body = resp.json()
    doctrine = next(c for c in body["checks"] if c["name"] == "doctrine_guard_count")
    assert doctrine["ok"] is True
    assert "doctrine guard tests" in doctrine["detail"]


def test_post_deploy_check_warnings_filter_installed(monkeypatch):
    monkeypatch.setenv("ADMIN_API_KEYS", "test_post_deploy_check_warnings")
    resp = client.get(
        "/api/v1/founder/post-deploy-check",
        headers={ADMIN_HEADER: "test_post_deploy_check_warnings"},
    )
    body = resp.json()
    wfilter = next(c for c in body["checks"] if c["name"] == "warnings_filter")
    assert wfilter["ok"] is True
