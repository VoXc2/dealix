"""Platform-security readiness gates (Omega V3).

Deterministic, offline: absent env => HOLD, fake issuer/JWKS cannot READY,
no secret material in config, Falco disabled/nonprivileged, Renovate
no-automerge, receipt closed/evidence-bound. No network access.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import yaml

from dealix.platform_security.readiness import (
    CAPABILITY_IDS,
    evaluate,
    receipt_is_closed,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
EMPTY_ENV: dict[str, str] = {}

FULL_OIDC_ENV = {
    "DEALIX_OIDC_ISSUER": "https://login.customerbank-riyadh.sa/realms/dealix",
    "DEALIX_OIDC_AUDIENCE": "dealix-customer-portal",
    "DEALIX_OIDC_JWKS_URL": "https://login.customerbank-riyadh.sa/realms/dealix/protocol/openid-connect/certs",
    "DEALIX_OIDC_PKCE_ENABLED": "1",
    "DEALIX_OIDC_RBAC_MAPPING": "viewer,sales_rep,sales_manager,tenant_admin",
    "DEALIX_OIDC_TENANT_BOUNDARY": "1",
}


def _oidc(env):
    return evaluate(env=env)["capabilities"]["customer_identity_oidc"]


def test_absent_env_all_hold():
    receipt = evaluate(env=EMPTY_ENV)
    assert receipt["overall"] == "HOLD"
    for cap_id in CAPABILITY_IDS:
        assert receipt["capabilities"][cap_id]["status"] == "HOLD"
    assert receipt_is_closed(receipt)


def test_fake_issuer_cannot_ready():
    env = dict(FULL_OIDC_ENV, DEALIX_OIDC_ISSUER="https://fake-idp.example.com/realms/x")
    cap = _oidc(env)
    assert cap["status"] == "HOLD"
    assert "fake_or_nonhttps_identity_material_cannot_ready" in cap["reasons"]


def test_fake_jwks_cannot_ready():
    env = dict(FULL_OIDC_ENV, DEALIX_OIDC_JWKS_URL="https://localhost:8443/certs")
    cap = _oidc(env)
    assert cap["status"] == "HOLD"


def test_nonhttps_issuer_cannot_ready():
    env = dict(FULL_OIDC_ENV, DEALIX_OIDC_ISSUER="http://idp.internal/certs")
    assert _oidc(env)["status"] == "HOLD"


def test_missing_pkce_rbac_tenant_cannot_ready():
    env = {
        "DEALIX_OIDC_ISSUER": FULL_OIDC_ENV["DEALIX_OIDC_ISSUER"],
        "DEALIX_OIDC_AUDIENCE": FULL_OIDC_ENV["DEALIX_OIDC_AUDIENCE"],
        "DEALIX_OIDC_JWKS_URL": FULL_OIDC_ENV["DEALIX_OIDC_JWKS_URL"],
    }
    cap = _oidc(env)
    assert cap["status"] == "HOLD"
    assert "missing_or_invalid:pkce_enabled" in cap["reasons"]
    assert "missing_or_invalid:rbac_mapping_present" in cap["reasons"]
    assert "missing_or_invalid:tenant_boundary_attested" in cap["reasons"]


def test_full_valid_oidc_evidence_readies_identity_only():
    receipt = evaluate(env=FULL_OIDC_ENV)
    assert receipt["capabilities"]["customer_identity_oidc"]["status"] == "READY"
    # Other capabilities stay HOLD: config presence is not operational proof.
    assert receipt["capabilities"]["secrets_openbao"]["status"] == "HOLD"
    assert receipt["capabilities"]["runtime_falco"]["status"] == "HOLD"
    assert receipt["capabilities"]["deps_renovate"]["status"] == "HOLD"
    assert receipt["overall"] == "HOLD"
    assert receipt_is_closed(receipt)


def test_openbao_hold_without_authority_and_ready_with_full_authority():
    assert evaluate(env=EMPTY_ENV)["capabilities"]["secrets_openbao"]["status"] == "HOLD"
    transit_only = {
        "OPENBAO_ADOPTION_AUTHORITY": "approved",
        "OPENBAO_ENDPOINT": "https://openbao.internal-vault-riyadh.sa:8200",
        "OPENBAO_SCOPE": "transit-only",
        "OPENBAO_NO_MIGRATION_ATTESTED": "1",
        "OPENBAO_SINGLE_SOURCE_ATTESTED": "1",
    }
    cap = evaluate(env=transit_only)["capabilities"]["secrets_openbao"]
    assert cap["status"] == "READY", cap["reasons"]
    missing_boundary = dict(transit_only, OPENBAO_NO_MIGRATION_ATTESTED="")
    assert evaluate(env=missing_boundary)["capabilities"]["secrets_openbao"]["status"] == "HOLD"


def test_no_secret_material_in_new_contracts():
    secret_re = re.compile(r"sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----")
    targets = [
        REPO_ROOT / "config" / "security" / "platform_security_readiness_v1.json",
        REPO_ROOT / "config" / "security" / "falco_profile_v1.yaml",
        REPO_ROOT / "dealix" / "platform_security" / "readiness.py",
        REPO_ROOT / "scripts" / "verify_platform_security_readiness.py",
    ]
    for target in targets:
        assert target.exists(), f"missing {target}"
        assert not secret_re.search(target.read_text(encoding="utf-8")), f"secret material in {target}"


def test_falco_profile_disabled_nonprivileged_and_hold_without_evidence():
    profile = yaml.safe_load((REPO_ROOT / "config" / "security" / "falco_profile_v1.yaml").read_text())
    assert profile["enabled"] is False
    assert profile["privileged"] is False
    assert profile.get("host_docker_socket") is False
    assert profile.get("host_network") is False
    cap = evaluate(env=EMPTY_ENV)["capabilities"]["runtime_falco"]
    assert cap["status"] == "HOLD"
    assert "missing_kernel_driver_ebpf_evidence" in cap["reasons"]


def test_renovate_hold_deferred_and_no_automerge_file():
    cap = evaluate(env=EMPTY_ENV)["capabilities"]["deps_renovate"]
    assert cap["status"] == "HOLD"
    assert "deferred_to_dependabot_equivalent" in cap["reasons"]
    assert (REPO_ROOT / ".github" / "dependabot.yml").exists()
    candidate = REPO_ROOT / "renovate.json"
    if candidate.exists():
        data = json.loads(candidate.read_text(encoding="utf-8"))
        assert data.get("automerge") is not True


def test_receipt_closed_and_evidence_bound():
    receipt = evaluate(env=FULL_OIDC_ENV)
    assert receipt_is_closed(receipt)
    assert set(receipt["capabilities"].keys()) == set(CAPABILITY_IDS)
    for cap in receipt["capabilities"].values():
        for item in cap["evidence"]:
            assert set(item.keys()) == {"type", "key", "present"}
    tampered = json.loads(json.dumps(receipt))
    tampered["capabilities"]["extra_capability"] = {"status": "READY", "reasons": [], "evidence": []}
    assert not receipt_is_closed(tampered)
