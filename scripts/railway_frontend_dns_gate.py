#!/usr/bin/env python3
"""Fail-closed front-door gate for the canonical Dealix Railway web service.

HTTP reachability can show that a route responds, but it cannot prove which
Railway service, repository root, config file, or deployment SHA served the
response. A PASS therefore requires both a healthy public route and a redacted
read-only provider receipt bound to the accepted source SHA and canonical
service-scoped Railway config.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"
SERVICE_MATRIX = ROOT / "dealix/config/railway_services.json"
PROVIDER_RECEIPT_SCHEMA = "dealix.railway-frontdoor-evidence.v1"
REQUIRED_DOMAINS = ("dealix.me", "www.dealix.me")
SHA40 = re.compile(r"^[0-9a-f]{40}$")

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8

    ensure_stdout_utf8()
except Exception:
    pass


def _head(url: str, timeout: float = 15.0) -> tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.headers.get("Server", "")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Server", "") if exc.headers else ""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ""


def _canonical_web_candidate() -> dict[str, str]:
    payload = json.loads(SERVICE_MATRIX.read_text(encoding="utf-8"))
    services = payload.get("services") or []
    candidates = [
        svc
        for svc in services
        if isinstance(svc, dict)
        and svc.get("role") == "canonical_public_web"
        and svc.get("productionAuthority") is True
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"expected exactly one canonical_public_web authority, found {len(candidates)}")

    svc = candidates[0]
    candidate = {
        "service": str(svc.get("name") or ""),
        "role": str(svc.get("role") or ""),
        "repository": str(svc.get("expectedSourceRepository") or ""),
        "root_directory": str(svc.get("rootDirectory") or ""),
        "config_file": str(svc.get("providerConfigFile") or ""),
    }
    expected = {
        "service": "dealix-apps-web",
        "role": "canonical_public_web",
        "repository": "Dealix-sa/dealix",
        "root_directory": "apps/web",
        "config_file": "/apps/web/railway.toml",
    }
    if candidate != expected:
        raise RuntimeError(f"canonical Railway web identity drift: {candidate}")
    return candidate


def _load_receipt(path: Path | None) -> tuple[dict[str, Any] | None, list[str]]:
    if path is None:
        return None, ["provider receipt not supplied"]
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, [f"provider receipt not found: {path}"]
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"provider receipt unreadable: {exc}"]
    if not isinstance(payload, dict):
        return None, ["provider receipt root must be an object"]
    return payload, []


def _validate_provider_receipt(
    payload: dict[str, Any] | None,
    *,
    candidate: dict[str, str],
    accepted_sha: str | None,
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if payload is None:
        return False, ["canonical provider identity is not evidence-backed"]

    if accepted_sha is None:
        errors.append("--accepted-sha is required with --provider-receipt")
    elif not SHA40.fullmatch(accepted_sha):
        errors.append("accepted SHA must be 40 lowercase hexadecimal characters")

    expected = {"schema": PROVIDER_RECEIPT_SCHEMA, **candidate}
    for key, value in expected.items():
        if payload.get(key) != value:
            errors.append(f"provider receipt {key} mismatch")

    deployment_sha = payload.get("deployment_sha")
    if not isinstance(deployment_sha, str) or not SHA40.fullmatch(deployment_sha):
        errors.append("provider receipt deployment_sha is missing or invalid")
    elif accepted_sha is not None and deployment_sha != accepted_sha:
        errors.append("provider receipt deployment_sha does not match accepted SHA")

    if payload.get("deployment_status") not in {"SUCCESS", "ACTIVE"}:
        errors.append("provider receipt deployment_status is not SUCCESS/ACTIVE")

    for key in ("service_id", "environment_id", "deployment_id", "captured_at"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"provider receipt missing {key}")

    evidence_refs = payload.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        errors.append("provider receipt evidence_refs must be a non-empty list")
    elif any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
        errors.append("provider receipt evidence_refs contains an invalid reference")

    domains = payload.get("domains")
    if not isinstance(domains, dict):
        errors.append("provider receipt domains must be an object")
    else:
        for hostname in REQUIRED_DOMAINS:
            domain = domains.get(hostname)
            if not isinstance(domain, dict):
                errors.append(f"provider receipt missing domain evidence for {hostname}")
                continue
            for flag in ("routing_verified", "ownership_verified", "certificate_verified"):
                if domain.get(flag) is not True:
                    errors.append(f"provider receipt {hostname}.{flag} must be true")

    return not errors, errors


def evaluate_frontdoor(
    *,
    frontend_base: str,
    status: int,
    server: str,
    candidate: dict[str, str],
    provider_receipt: dict[str, Any] | None,
    accepted_sha: str | None,
    receipt_load_errors: list[str] | None = None,
) -> dict[str, Any]:
    server_lower = (server or "").lower()
    legacy_server_signal = "github" in server_lower
    route_reachable = 200 <= status < 400
    identity_ok, identity_errors = _validate_provider_receipt(
        provider_receipt,
        candidate=candidate,
        accepted_sha=accepted_sha,
    )
    errors = [*(receipt_load_errors or []), *identity_errors]

    canonical_origin_verified = route_reachable and not legacy_server_signal and identity_ok
    if canonical_origin_verified:
        verdict = "PASS"
    elif not route_reachable or legacy_server_signal:
        verdict = "FAIL"
    else:
        verdict = "HOLD"

    base = frontend_base.rstrip("/")
    return {
        "frontend_base": base,
        "ar_url": f"{base}/ar",
        "status": status,
        "server": server,
        "route_reachable": route_reachable,
        "legacy_server_signal": legacy_server_signal,
        "canonical_origin_verified": canonical_origin_verified,
        "layer_4_ok": canonical_origin_verified,
        "verdict": verdict,
        "canonical_candidate": {**candidate, "accepted_sha": accepted_sha},
        "service_identity_proven_by_http_probe": False,
        "provider_receipt_required": True,
        "provider_receipt_valid": identity_ok,
        "evidence_errors": sorted(set(errors)),
        "doc": str(DOC.relative_to(ROOT)).replace("\\", "/"),
        "next_ar": []
        if canonical_origin_verified
        else [
            (
                "READ-ONLY: capture a redacted Railway provider receipt for "
                f"{candidate['service']} repo={candidate['repository']} root={candidate['root_directory']} "
                f"config={candidate['config_file']} bound to the accepted deployment SHA"
            ),
            "READ-ONLY: prove generated-domain root + /healthz + /ar before custom-domain mutation",
            "READ-ONLY: capture exact domain routing, ownership verification, certificate state, and evidence refs",
            "READ-ONLY: record current apex/www/api DNS + TTL as rollback before-state",
            f"راجع {DOC.name}",
            "HOLD: no deploy/redeploy/domain/DNS/secret mutation from this gate",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontend-base", default="https://dealix.me")
    parser.add_argument("--provider-receipt", type=Path)
    parser.add_argument("--accepted-sha")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        candidate = _canonical_web_candidate()
    except (OSError, json.JSONDecodeError, RuntimeError) as exc:
        print("FRONTEND_DNS_GATE=FAIL")
        print(f"  source_contract_error={exc}")
        print("FRONTEND_DNS_GATE_VERDICT=FAIL")
        return 1

    base = args.frontend_base.rstrip("/")
    status, server = _head(f"{base}/ar")
    receipt, load_errors = _load_receipt(args.provider_receipt)
    out = evaluate_frontdoor(
        frontend_base=base,
        status=status,
        server=server,
        candidate=candidate,
        provider_receipt=receipt,
        accepted_sha=args.accepted_sha,
        receipt_load_errors=load_errors,
    )

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"FRONTEND_ROUTE_REACHABLE={str(out['route_reachable']).upper()}")
        print(f"CANONICAL_ORIGIN_VERIFIED={str(out['canonical_origin_verified']).upper()}")
        print(f"  {out['ar_url']} -> {status or 'unreachable'} server={server or 'unknown'}")
        print(
            "  canonical_candidate="
            f"{candidate['service']} repo={candidate['repository']} root={candidate['root_directory']} "
            f"config={candidate['config_file']}"
        )
        for error in out["evidence_errors"]:
            print(f"  evidence_error={error}")
        if not out["canonical_origin_verified"]:
            for line in out["next_ar"]:
                print(f"  -> {line}")

    print(f"FRONTEND_DNS_GATE_VERDICT={out['verdict']}")
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
