"""Dealix platform-security readiness evaluator (Omega V3).

Deterministic, offline, evidence-bound. Evaluates the four platform-security
capabilities from ``config/security/platform_security_readiness_v1.json``
against injected environment evidence. HOLD is the default; READY requires
every required evidence item. Config presence alone is never operational
proof. No network access, no secret exfiltration: reasons reference key
names and shape only, never values.
"""

from __future__ import annotations

import json
import os
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Mapping

REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_PATH = REPO_ROOT / "config" / "security" / "platform_security_readiness_v1.json"
FALCO_PROFILE_PATH = REPO_ROOT / "config" / "security" / "falco_profile_v1.yaml"
RECEIPT_SCHEMA = "dealix.platform_security_receipt.v1"

CAPABILITY_IDS = (
    "customer_identity_oidc",
    "secrets_openbao",
    "runtime_falco",
    "deps_renovate",
)

_FAKE_MARKERS = (
    "example",
    "fake",
    "changeme",
    "placeholder",
    "your-idp",
    "your_idp",
    "localhost",
    "127.0.0.1",
    "test",
    "demo",
    "sample",
)

_SECRET_PATTERNS = (
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"ghp_[A-Za-z0-9]{20,}"),
    re.compile(r"github_pat_[A-Za-z0-9_]{20,}"),
    re.compile(r"xox[bap]-[A-Za-z0-9-]{10,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def _looks_fake(value: str) -> bool:
    lowered = value.strip().lower()
    return any(marker in lowered for marker in _FAKE_MARKERS)


def _is_https_url(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered.startswith("https://") and len(lowered) > len("https://x")


def _evidence(key: str, kind: str, present: bool) -> dict[str, Any]:
    return {"type": kind, "key": key, "present": bool(present)}


def _eval_oidc(env: Mapping[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    evidence: list[dict[str, Any]] = []
    checks: dict[str, bool] = {}

    issuer = (env.get("DEALIX_OIDC_ISSUER") or "").strip()
    audience = (env.get("DEALIX_OIDC_AUDIENCE") or "").strip()
    jwks = (env.get("DEALIX_OIDC_JWKS_URL") or "").strip()
    pkce = (env.get("DEALIX_OIDC_PKCE_ENABLED") or "").strip().lower()
    rbac = (env.get("DEALIX_OIDC_RBAC_MAPPING") or "").strip()
    tenant = (env.get("DEALIX_OIDC_TENANT_BOUNDARY") or "").strip().lower()

    checks["issuer_https_nonfake"] = bool(issuer) and _is_https_url(issuer) and not _looks_fake(issuer)
    checks["audience_set_nonplaceholder"] = bool(audience) and not _looks_fake(audience)
    checks["jwks_url_https_nonfake"] = bool(jwks) and _is_https_url(jwks) and not _looks_fake(jwks)
    checks["pkce_enabled"] = pkce in ("1", "true", "yes")
    checks["rbac_mapping_present"] = bool(rbac) and not _looks_fake(rbac)
    checks["tenant_boundary_attested"] = tenant in ("1", "true", "yes")

    for name, ok in checks.items():
        if not ok:
            reasons.append(f"missing_or_invalid:{name}")
    for key in (
        "DEALIX_OIDC_ISSUER",
        "DEALIX_OIDC_AUDIENCE",
        "DEALIX_OIDC_JWKS_URL",
        "DEALIX_OIDC_PKCE_ENABLED",
        "DEALIX_OIDC_RBAC_MAPPING",
        "DEALIX_OIDC_TENANT_BOUNDARY",
    ):
        evidence.append(_evidence(key, "env", bool((env.get(key) or "").strip())))

    if not any((env.get(k) or "").strip() for k in ("DEALIX_OIDC_ISSUER", "DEALIX_OIDC_JWKS_URL")):
        reasons.append("absent_env")
    elif not checks["issuer_https_nonfake"] or not checks["jwks_url_https_nonfake"]:
        reasons.append("fake_or_nonhttps_identity_material_cannot_ready")

    status = "READY" if all(checks.values()) else "HOLD"
    return {"status": status, "reasons": sorted(set(reasons)), "evidence": evidence}


def _eval_openbao(env: Mapping[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    evidence: list[dict[str, Any]] = []
    authority = (env.get("OPENBAO_ADOPTION_AUTHORITY") or "").strip().lower()
    endpoint = (env.get("OPENBAO_ENDPOINT") or "").strip()
    scope = (env.get("OPENBAO_SCOPE") or "").strip().lower()
    no_migration = (env.get("OPENBAO_NO_MIGRATION_ATTESTED") or "").strip().lower()
    single_source = (env.get("OPENBAO_SINGLE_SOURCE_ATTESTED") or "").strip().lower()

    evidence.extend(
        [
            _evidence("OPENBAO_ADOPTION_AUTHORITY", "env", bool(authority)),
            _evidence("OPENBAO_ENDPOINT", "env", bool(endpoint)),
            _evidence("OPENBAO_SCOPE", "env", bool(scope)),
        ]
    )
    if authority != "approved":
        reasons.append("missing_explicit_authority")
        return {"status": "HOLD", "reasons": reasons, "evidence": evidence}
    if scope not in ("transit-only", "transit_only", "sign-verify", "sign_verify"):
        reasons.append("scope_not_transit_or_sign_verify_only")
    if endpoint and (not _is_https_url(endpoint) or _looks_fake(endpoint)):
        reasons.append("fake_or_nonhttps_endpoint_cannot_ready")
    if no_migration not in ("1", "true", "yes"):
        reasons.append("migration_boundary_not_attested")
    if single_source not in ("1", "true", "yes"):
        reasons.append("single_source_of_truth_not_attested")
    status = "READY" if not reasons else "HOLD"
    return {"status": status, "reasons": reasons, "evidence": evidence}


def _read_falco_profile() -> dict[str, Any]:
    try:
        text = FALCO_PROFILE_PATH.read_text(encoding="utf-8")
    except OSError:
        return {"missing": True}
    data: dict[str, Any] = {}
    for line in text.splitlines():
        if ":" not in line or line.lstrip().startswith("#"):
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip().strip("\"'")
        if raw.lower() in ("true", "false"):
            data[key] = raw.lower() == "true"
        elif key in ("enabled", "privileged", "host_docker_socket", "host_network"):
            data[key] = raw.lower() == "true"
        else:
            data[key] = raw
    return data


def _eval_falco(env: Mapping[str, str]) -> dict[str, Any]:
    reasons: list[str] = []
    profile = _read_falco_profile()
    evidence = [
        _evidence("FALCO_MODE", "env", bool((env.get("FALCO_MODE") or "").strip())),
        _evidence("FALCO_EBPF_EVIDENCE", "env", bool((env.get("FALCO_EBPF_EVIDENCE") or "").strip())),
        _evidence(str(FALCO_PROFILE_PATH.name), "file", not profile.get("missing", False)),
    ]
    if profile.get("missing", False):
        reasons.append("profile_missing")
        return {"status": "HOLD", "reasons": reasons, "evidence": evidence}
    if profile.get("enabled", True) is True:
        reasons.append("profile_not_disabled")
    if profile.get("privileged", True) is True:
        reasons.append("profile_privileged")
    mode = (env.get("FALCO_MODE") or "").strip().lower()
    ebpf = (env.get("FALCO_EBPF_EVIDENCE") or "").strip().lower()
    if mode != "lab":
        reasons.append("lab_mode_not_attested")
    if ebpf not in ("present", "verified", "1", "true", "yes"):
        reasons.append("missing_kernel_driver_ebpf_evidence")
    status = "READY" if not reasons else "HOLD"
    return {"status": status, "reasons": reasons, "evidence": evidence}


def _eval_renovate(env: Mapping[str, str]) -> dict[str, Any]:
    del env  # policy is file-bound; env carries no renovate authority.
    reasons = ["deferred_to_dependabot_equivalent"]
    evidence = [
        _evidence(".github/dependabot.yml", "file", (REPO_ROOT / ".github" / "dependabot.yml").exists()),
        _evidence("renovate.json", "file", (REPO_ROOT / "renovate.json").exists()),
    ]
    return {"status": "HOLD", "reasons": reasons, "evidence": evidence}


def _scan_secret_material() -> list[str]:
    violations: list[str] = []
    targets = [
        CONTRACT_PATH,
        FALCO_PROFILE_PATH,
        REPO_ROOT / "scripts" / "verify_platform_security_readiness.py",
        Path(__file__),
    ]
    for target in targets:
        try:
            text = target.read_text(encoding="utf-8")
        except OSError:
            continue
        for pattern in _SECRET_PATTERNS:
            if pattern.search(text):
                violations.append(f"secret_material_in:{target.name}")
                break
    return violations


def _scan_renovate_automerge() -> list[str]:
    violations: list[str] = []
    candidate = REPO_ROOT / "renovate.json"
    if not candidate.exists():
        return violations
    try:
        data = json.loads(candidate.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        violations.append("renovate_config_unparseable")
        return violations
    if data.get("automerge") is True or data.get("automergeType"):
        violations.append("renovate_automerge_forbidden")
    return violations


def evaluate(env: Mapping[str, str] | None = None, base_commit: str = "") -> dict[str, Any]:
    """Evaluate all capabilities. Pure apart from reading repo files; no network."""
    source = dict(os.environ) if env is None else dict(env)
    contract: dict[str, Any] = {}
    try:
        contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        contract = {}

    capabilities = {
        "customer_identity_oidc": _eval_oidc(source),
        "secrets_openbao": _eval_openbao(source),
        "runtime_falco": _eval_falco(source),
        "deps_renovate": _eval_renovate(source),
    }
    violations = _scan_secret_material() + _scan_renovate_automerge()
    overall = "READY" if all(c["status"] == "READY" for c in capabilities.values()) and not violations else "HOLD"
    return {
        "schema": RECEIPT_SCHEMA,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "base_commit": base_commit or (os.environ.get("DEALIX_BASE_COMMIT") or ""),
        "contract_schema": contract.get("schema", ""),
        "capabilities": capabilities,
        "violations": sorted(violations),
        "overall": overall,
    }


def receipt_is_closed(receipt: Mapping[str, Any]) -> bool:
    """A receipt is closed/evidence-bound iff it carries exactly the canonical
    capability ids, each with status + reasons + evidence, and no value payloads."""
    if receipt.get("schema") != RECEIPT_SCHEMA:
        return False
    caps = receipt.get("capabilities")
    if not isinstance(caps, dict) or set(caps.keys()) != set(CAPABILITY_IDS):
        return False
    for cap in caps.values():
        if not isinstance(cap, dict):
            return False
        if cap.get("status") not in ("READY", "HOLD"):
            return False
        if not isinstance(cap.get("reasons"), list) or not isinstance(cap.get("evidence"), list):
            return False
        for item in cap["evidence"]:
            if not isinstance(item, dict) or set(item.keys()) != {"type", "key", "present"}:
                return False
    return isinstance(receipt.get("violations"), list) and receipt.get("overall") in ("READY", "HOLD")
