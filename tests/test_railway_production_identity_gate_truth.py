from __future__ import annotations

import importlib.util
import urllib.error
from datetime import UTC, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/railway_production_identity_gate.py"
SPEC = importlib.util.spec_from_file_location("railway_production_identity_gate", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

SHA = "a" * 40
NOW = datetime(2026, 9, 5, 3, 0, tzinfo=UTC)
PROVIDER_AUTHORITY = {
    "provider": "railway",
    "project_id": "03e6bb4b-bdf5-4aa7-86ed-bc94fa293c0e",
    "environment_id": "38e3d38f-53b2-44fa-a3f9-ef91d863bd83",
    "environment_name": "production",
    "evidence_mode": "read_only_provider_receipt",
}
WEB_CANDIDATE = {
    "service": "dealix-apps-web",
    "role": "canonical_public_web",
    "repository": "Dealix-sa/dealix",
    "root_directory": "apps/web",
    "config_file": "/apps/web/railway.toml",
}
API_CANDIDATE = {
    "service": "dealix-api",
    "role": "canonical_api",
    "repository": "Dealix-sa/dealix",
    "root_directory": ".",
}


def _stamp(value: datetime = NOW) -> str:
    return value.astimezone(UTC).isoformat().replace("+00:00", "Z")


def _domain() -> dict[str, bool]:
    return {
        "routing_verified": True,
        "ownership_verified": True,
        "certificate_verified": True,
    }


def _web_receipt(**overrides):
    payload = {
        "schema": "dealix.railway-frontdoor-evidence.v1",
        **WEB_CANDIDATE,
        "provider": PROVIDER_AUTHORITY["provider"],
        "project_id": PROVIDER_AUTHORITY["project_id"],
        "environment_id": PROVIDER_AUTHORITY["environment_id"],
        "environment_name": PROVIDER_AUTHORITY["environment_name"],
        "deployment_sha": SHA,
        "deployment_status": "SUCCESS",
        "service_id": "svc-web",
        "deployment_id": "dep-web",
        "captured_at": _stamp(),
        "evidence_refs": ["railway:web:read-only"],
        "domains": {"dealix.me": _domain(), "www.dealix.me": _domain()},
    }
    payload.update(overrides)
    return payload


def _api_receipt(**overrides):
    payload = {
        "schema": "dealix.railway-api-evidence.v1",
        **API_CANDIDATE,
        "provider": PROVIDER_AUTHORITY["provider"],
        "project_id": PROVIDER_AUTHORITY["project_id"],
        "environment_id": PROVIDER_AUTHORITY["environment_id"],
        "environment_name": PROVIDER_AUTHORITY["environment_name"],
        "deployment_sha": SHA,
        "deployment_status": "SUCCESS",
        "service_id": "svc-api",
        "deployment_id": "dep-api",
        "captured_at": _stamp(),
        "evidence_refs": ["railway:api:read-only"],
        "domains": {"api.dealix.me": _domain()},
    }
    payload.update(overrides)
    return payload


def _evaluate(
    *,
    web_receipt=None,
    api_receipt=None,
    web_status=200,
    api_status=200,
    web_server="cloudflare",
):
    return MODULE.evaluate_production_identity(
        web_status=web_status,
        web_server=web_server,
        api_status=api_status,
        web_receipt=web_receipt,
        api_receipt=api_receipt,
        accepted_sha=SHA,
        web_candidate=WEB_CANDIDATE,
        api_candidate=API_CANDIDATE,
        provider_authority=PROVIDER_AUTHORITY,
        evaluated_at=NOW,
    )


def test_source_matrix_binds_canonical_railway_project_and_environment() -> None:
    assert MODULE._provider_authority() == PROVIDER_AUTHORITY


def test_source_matrix_binds_canonical_web_service_scoped_config() -> None:
    web_candidate, _ = MODULE._canonical_candidates()
    assert web_candidate["config_file"] == "/apps/web/railway.toml"


def test_exact_web_and_api_receipts_on_same_release_sha_pass() -> None:
    result = _evaluate(web_receipt=_web_receipt(), api_receipt=_api_receipt())
    assert result["web"]["canonical_origin_verified"] is True
    assert result["api"]["canonical_origin_verified"] is True
    assert result["same_release_sha_required"] is True
    assert result["production_green"] is True
    assert result["verdict"] == "PASS"
    assert result["provider_authority"]["project_id"] == PROVIDER_AUTHORITY["project_id"]


def test_repo_root_web_config_is_hold_not_pass() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(config_file="/railway.toml"),
        api_receipt=_api_receipt(),
    )
    assert result["web"]["provider_receipt_valid"] is False
    assert result["web"]["canonical_origin_verified"] is False
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "web: provider receipt config_file mismatch" in item
        for item in result["evidence_errors"]
    )


def test_web_pass_cannot_hide_stale_api_sha() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(),
        api_receipt=_api_receipt(deployment_sha="b" * 40),
    )
    assert result["web"]["canonical_origin_verified"] is True
    assert result["api"]["canonical_origin_verified"] is False
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "api: provider receipt deployment_sha does not match accepted SHA" in item
        for item in result["evidence_errors"]
    )


def test_cross_project_receipt_is_hold_not_pass() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(project_id="different-project"),
        api_receipt=_api_receipt(),
    )
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "web: provider receipt project_id mismatch" in item
        for item in result["evidence_errors"]
    )


def test_cross_environment_receipt_is_hold_not_pass() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(environment_id="preview-environment"),
        api_receipt=_api_receipt(),
    )
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "web: provider receipt environment_id mismatch" in item
        for item in result["evidence_errors"]
    )


def test_stale_receipt_is_hold_not_pass() -> None:
    stale = _stamp(NOW - timedelta(hours=2))
    result = _evaluate(
        web_receipt=_web_receipt(captured_at=stale),
        api_receipt=_api_receipt(),
    )
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "web: provider receipt is stale" in item
        for item in result["evidence_errors"]
    )


def test_far_future_receipt_is_hold_not_pass() -> None:
    future = _stamp(NOW + timedelta(minutes=10))
    result = _evaluate(
        web_receipt=_web_receipt(captured_at=future),
        api_receipt=_api_receipt(),
    )
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "web: provider receipt captured_at is too far in the future" in item
        for item in result["evidence_errors"]
    )


def test_missing_api_provider_receipt_is_hold_not_pass() -> None:
    result = _evaluate(web_receipt=_web_receipt())
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"


def test_unhealthy_api_is_fail_even_with_exact_receipt() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(),
        api_receipt=_api_receipt(),
        api_status=503,
    )
    assert result["api"]["provider_receipt_valid"] is True
    assert result["api"]["health_reachable"] is False
    assert result["production_green"] is False
    assert result["verdict"] == "FAIL"


def test_legacy_web_server_signal_is_fail_even_with_exact_receipts() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(),
        api_receipt=_api_receipt(),
        web_server="GitHub.com",
    )
    assert result["web"]["legacy_server_signal"] is True
    assert result["production_green"] is False
    assert result["verdict"] == "FAIL"


def test_api_identity_mismatch_is_hold() -> None:
    result = _evaluate(
        web_receipt=_web_receipt(),
        api_receipt=_api_receipt(repository="VoXc2/dealix"),
    )
    assert result["production_green"] is False
    assert result["verdict"] == "HOLD"
    assert any(
        "api: provider receipt repository mismatch" in item
        for item in result["evidence_errors"]
    )


def test_identity_probe_sends_canonical_trust_headers(monkeypatch) -> None:
    captured: dict[str, object] = {}

    class Response:
        status = 200
        headers = {"Server": "cloudflare"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def fake_urlopen(req, timeout):
        captured["headers"] = {str(k).lower(): v for k, v in req.header_items()}
        captured["timeout"] = timeout
        return Response()

    monkeypatch.setattr(MODULE.urllib.request, "urlopen", fake_urlopen)
    status, server = MODULE._probe("https://api.example.test/healthz", method="GET", timeout=7.0)
    assert status == 200
    assert server == "cloudflare"
    assert captured["headers"]["user-agent"] == "Dealix-Production-Trust/1.0"
    assert captured["headers"]["accept"] == "application/json"
    assert captured["timeout"] == 7.0


def test_identity_probe_keeps_real_403_as_failure(monkeypatch) -> None:
    def fake_urlopen(req, timeout):
        raise urllib.error.HTTPError(req.full_url, 403, "Forbidden", None, None)

    monkeypatch.setattr(MODULE.urllib.request, "urlopen", fake_urlopen)
    status, _server = MODULE._probe("https://api.example.test/healthz", method="GET")
    assert status == 403
