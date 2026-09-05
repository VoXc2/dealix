from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/railway_frontend_dns_gate.py"
SPEC = importlib.util.spec_from_file_location("railway_frontend_dns_gate", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

SHA = "a" * 40
CANDIDATE = {
    "service": "dealix-apps-web",
    "role": "canonical_public_web",
    "repository": "Dealix-sa/dealix",
    "root_directory": "apps/web",
    "config_file": "/apps/web/railway.toml",
}


def _receipt(**overrides):
    payload = {
        "schema": "dealix.railway-frontdoor-evidence.v1",
        **CANDIDATE,
        "deployment_sha": SHA,
        "deployment_status": "SUCCESS",
        "service_id": "svc-canonical-web",
        "environment_id": "env-production",
        "deployment_id": "dep-exact-sha",
        "captured_at": "2026-09-03T12:00:00Z",
        "evidence_refs": ["railway:read-only:service-status"],
        "domains": {
            "dealix.me": {
                "routing_verified": True,
                "ownership_verified": True,
                "certificate_verified": True,
            },
            "www.dealix.me": {
                "routing_verified": True,
                "ownership_verified": True,
                "certificate_verified": True,
            },
        },
    }
    payload.update(overrides)
    return payload


def _evaluate(*, status=200, server="cloudflare", receipt=None, accepted_sha=None):
    return MODULE.evaluate_frontdoor(
        frontend_base="https://dealix.me",
        status=status,
        server=server,
        candidate=CANDIDATE,
        provider_receipt=receipt,
        accepted_sha=accepted_sha,
    )


def test_http_200_from_unknown_origin_is_hold_not_pass() -> None:
    result = _evaluate()
    assert result["route_reachable"] is True
    assert result["service_identity_proven_by_http_probe"] is False
    assert result["canonical_origin_verified"] is False
    assert result["layer_4_ok"] is False
    assert result["verdict"] == "HOLD"


def test_redirect_from_unknown_origin_is_hold_not_pass() -> None:
    result = _evaluate(status=302, server="nginx")
    assert result["route_reachable"] is True
    assert result["canonical_origin_verified"] is False
    assert result["verdict"] == "HOLD"


def test_github_server_signal_is_fail_even_with_receipt() -> None:
    result = _evaluate(server="GitHub.com", receipt=_receipt(), accepted_sha=SHA)
    assert result["legacy_server_signal"] is True
    assert result["canonical_origin_verified"] is False
    assert result["verdict"] == "FAIL"


def test_exact_provider_receipt_and_route_are_required_for_pass() -> None:
    result = _evaluate(receipt=_receipt(), accepted_sha=SHA)
    assert result["provider_receipt_valid"] is True
    assert result["canonical_origin_verified"] is True
    assert result["layer_4_ok"] is True
    assert result["verdict"] == "PASS"


def test_mismatched_deployment_sha_is_hold() -> None:
    result = _evaluate(receipt=_receipt(deployment_sha="b" * 40), accepted_sha=SHA)
    assert result["provider_receipt_valid"] is False
    assert result["canonical_origin_verified"] is False
    assert result["verdict"] == "HOLD"
    assert any("does not match accepted SHA" in error for error in result["evidence_errors"])


def test_missing_domain_evidence_is_hold() -> None:
    result = _evaluate(receipt=_receipt(domains={}), accepted_sha=SHA)
    assert result["provider_receipt_valid"] is False
    assert result["verdict"] == "HOLD"


def test_repo_root_config_file_is_hold_not_pass() -> None:
    result = _evaluate(receipt=_receipt(config_file="/railway.toml"), accepted_sha=SHA)
    assert result["provider_receipt_valid"] is False
    assert result["canonical_origin_verified"] is False
    assert result["verdict"] == "HOLD"
    assert any("config_file mismatch" in error for error in result["evidence_errors"])
