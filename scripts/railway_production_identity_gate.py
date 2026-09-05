#!/usr/bin/env python3
"""Fail-closed composite Railway production identity gate for Dealix.

Production Green requires both canonical public web and canonical API provider
identity to be bound to the same accepted release SHA, canonical Railway project,
and current production environment. HTTP reachability alone never proves service
identity, and stale provider receipts are never accepted as current production
truth. The canonical web receipt must also prove the service-scoped Railway
config file so a repo-root backend pre-deploy hook cannot false-green the web.
"""

from __future__ import annotations

import argparse
import json
import re
import urllib.error
import urllib.request
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SERVICE_MATRIX = ROOT / "dealix/config/railway_services.json"
SHA40 = re.compile(r"^[0-9a-f]{40}$")
RECEIPT_MAX_AGE = timedelta(minutes=30)
RECEIPT_FUTURE_SKEW = timedelta(minutes=5)

WEB_SPEC = {
    "schema": "dealix.railway-frontdoor-evidence.v1",
    "service": "dealix-apps-web",
    "role": "canonical_public_web",
    "repository": "Dealix-sa/dealix",
    "root_directory": "apps/web",
    "config_file": "/apps/web/railway.toml",
    "domains": ("dealix.me", "www.dealix.me"),
}
API_SPEC = {
    "schema": "dealix.railway-api-evidence.v1",
    "service": "dealix-api",
    "role": "canonical_api",
    "repository": "Dealix-sa/dealix",
    "root_directory": ".",
    "domains": ("api.dealix.me",),
}


def _probe(url: str, *, method: str, timeout: float = 15.0) -> tuple[int, str]:
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.headers.get("Server", "")
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Server", "") if exc.headers else ""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, ""


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


def _service_matrix() -> dict[str, Any]:
    payload = json.loads(SERVICE_MATRIX.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RuntimeError("Railway service matrix root must be an object")
    return payload


def _provider_authority() -> dict[str, str]:
    payload = _service_matrix()
    authority = payload.get("productionProviderAuthority")
    if not isinstance(authority, dict):
        raise RuntimeError("Railway production provider authority is missing")

    candidate = {
        "provider": str(authority.get("provider") or ""),
        "project_id": str(authority.get("projectId") or ""),
        "environment_id": str(authority.get("environmentId") or ""),
        "environment_name": str(authority.get("environmentName") or ""),
        "evidence_mode": str(authority.get("evidenceMode") or ""),
    }
    if candidate["provider"] != "railway":
        raise RuntimeError("canonical production provider must be railway")
    if not candidate["project_id"] or not candidate["environment_id"]:
        raise RuntimeError("canonical Railway project/environment id is missing")
    if candidate["environment_name"] != "production":
        raise RuntimeError("canonical Railway environment must be production")
    if candidate["evidence_mode"] != "read_only_provider_receipt":
        raise RuntimeError("canonical Railway evidence mode must be read_only_provider_receipt")
    return candidate


def _canonical_candidates() -> tuple[dict[str, str], dict[str, str]]:
    payload = _service_matrix()
    services = payload.get("services") or []
    if not isinstance(services, list):
        raise RuntimeError("Railway service matrix services must be a list")

    def one(role: str, expected: dict[str, Any]) -> dict[str, str]:
        matches = [
            svc
            for svc in services
            if isinstance(svc, dict)
            and svc.get("role") == role
            and svc.get("productionAuthority") is True
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"expected exactly one {role} production authority, found {len(matches)}"
            )
        svc = matches[0]
        candidate = {
            "service": str(svc.get("name") or ""),
            "role": str(svc.get("role") or ""),
            "repository": str(svc.get("expectedSourceRepository") or ""),
            "root_directory": str(svc.get("rootDirectory") or ""),
        }
        expected_candidate = {
            "service": str(expected["service"]),
            "role": str(expected["role"]),
            "repository": str(expected["repository"]),
            "root_directory": str(expected["root_directory"]),
        }
        if "config_file" in expected:
            candidate["config_file"] = str(svc.get("providerConfigFile") or "")
            expected_candidate["config_file"] = str(expected["config_file"])
        if candidate != expected_candidate:
            raise RuntimeError(
                f"canonical Railway identity drift for {role}: {candidate}"
            )
        return candidate

    return one("canonical_public_web", WEB_SPEC), one("canonical_api", API_SPEC)


def _parse_captured_at(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    raw = value.strip()
    if raw.endswith("Z"):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(UTC)


def _validate_receipt(
    payload: dict[str, Any] | None,
    *,
    spec: dict[str, Any],
    provider_authority: dict[str, str],
    accepted_sha: str | None,
    now: datetime | None = None,
) -> tuple[bool, list[str]]:
    errors: list[str] = []
    if payload is None:
        return False, ["canonical provider identity is not evidence-backed"]

    if accepted_sha is None:
        errors.append("--accepted-sha is required with provider receipts")
    elif not SHA40.fullmatch(accepted_sha):
        errors.append("accepted SHA must be 40 lowercase hexadecimal characters")

    for key in ("schema", "service", "role", "repository", "root_directory"):
        if payload.get(key) != spec[key]:
            errors.append(f"provider receipt {key} mismatch")

    if "config_file" in spec and payload.get("config_file") != spec["config_file"]:
        errors.append("provider receipt config_file mismatch")

    provider_pairs = {
        "provider": provider_authority["provider"],
        "project_id": provider_authority["project_id"],
        "environment_id": provider_authority["environment_id"],
        "environment_name": provider_authority["environment_name"],
    }
    for key, expected in provider_pairs.items():
        if payload.get(key) != expected:
            errors.append(f"provider receipt {key} mismatch")

    deployment_sha = payload.get("deployment_sha")
    if not isinstance(deployment_sha, str) or not SHA40.fullmatch(deployment_sha):
        errors.append("provider receipt deployment_sha is missing or invalid")
    elif accepted_sha is not None and deployment_sha != accepted_sha:
        errors.append("provider receipt deployment_sha does not match accepted SHA")

    if payload.get("deployment_status") not in {"SUCCESS", "ACTIVE"}:
        errors.append("provider receipt deployment_status is not SUCCESS/ACTIVE")

    for key in ("service_id", "deployment_id"):
        value = payload.get(key)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"provider receipt missing {key}")

    captured_at = _parse_captured_at(payload.get("captured_at"))
    if captured_at is None:
        errors.append("provider receipt captured_at is missing or invalid")
    else:
        current = (now or datetime.now(UTC)).astimezone(UTC)
        if captured_at > current + RECEIPT_FUTURE_SKEW:
            errors.append("provider receipt captured_at is too far in the future")
        elif current - captured_at > RECEIPT_MAX_AGE:
            errors.append("provider receipt is stale")

    evidence_refs = payload.get("evidence_refs")
    if not isinstance(evidence_refs, list) or not evidence_refs:
        errors.append("provider receipt evidence_refs must be a non-empty list")
    elif any(not isinstance(ref, str) or not ref.strip() for ref in evidence_refs):
        errors.append("provider receipt evidence_refs contains an invalid reference")

    domains = payload.get("domains")
    if not isinstance(domains, dict):
        errors.append("provider receipt domains must be an object")
    else:
        for hostname in spec["domains"]:
            domain = domains.get(hostname)
            if not isinstance(domain, dict):
                errors.append(
                    f"provider receipt missing domain evidence for {hostname}"
                )
                continue
            for flag in (
                "routing_verified",
                "ownership_verified",
                "certificate_verified",
            ):
                if domain.get(flag) is not True:
                    errors.append(
                        f"provider receipt {hostname}.{flag} must be true"
                    )

    return not errors, errors


def evaluate_production_identity(
    *,
    web_status: int,
    web_server: str,
    api_status: int,
    web_receipt: dict[str, Any] | None,
    api_receipt: dict[str, Any] | None,
    accepted_sha: str | None,
    web_receipt_load_errors: list[str] | None = None,
    api_receipt_load_errors: list[str] | None = None,
    web_candidate: dict[str, str] | None = None,
    api_candidate: dict[str, str] | None = None,
    provider_authority: dict[str, str] | None = None,
    evaluated_at: datetime | None = None,
) -> dict[str, Any]:
    if web_candidate is None or api_candidate is None:
        web_candidate, api_candidate = _canonical_candidates()
    if provider_authority is None:
        provider_authority = _provider_authority()

    web_spec = {**WEB_SPEC, **web_candidate}
    api_spec = {**API_SPEC, **api_candidate}
    web_receipt_ok, web_errors = _validate_receipt(
        web_receipt,
        spec=web_spec,
        provider_authority=provider_authority,
        accepted_sha=accepted_sha,
        now=evaluated_at,
    )
    api_receipt_ok, api_errors = _validate_receipt(
        api_receipt,
        spec=api_spec,
        provider_authority=provider_authority,
        accepted_sha=accepted_sha,
        now=evaluated_at,
    )

    web_route_reachable = 200 <= web_status < 400
    web_legacy_server_signal = "github" in (web_server or "").lower()
    api_health_reachable = api_status == 200

    web_origin_verified = (
        web_route_reachable and not web_legacy_server_signal and web_receipt_ok
    )
    api_origin_verified = api_health_reachable and api_receipt_ok
    production_green = web_origin_verified and api_origin_verified

    if production_green:
        verdict = "PASS"
    elif not web_route_reachable or web_legacy_server_signal or not api_health_reachable:
        verdict = "FAIL"
    else:
        verdict = "HOLD"

    evidence_errors = [
        *[f"web: {item}" for item in (web_receipt_load_errors or [])],
        *[f"web: {item}" for item in web_errors],
        *[f"api: {item}" for item in (api_receipt_load_errors or [])],
        *[f"api: {item}" for item in api_errors],
    ]

    return {
        "accepted_release_sha": accepted_sha,
        "same_release_sha_required": True,
        "provider_authority": {
            "provider": provider_authority["provider"],
            "project_id": provider_authority["project_id"],
            "environment_id": provider_authority["environment_id"],
            "environment_name": provider_authority["environment_name"],
        },
        "receipt_max_age_seconds": int(RECEIPT_MAX_AGE.total_seconds()),
        "web": {
            "status": web_status,
            "server": web_server,
            "route_reachable": web_route_reachable,
            "legacy_server_signal": web_legacy_server_signal,
            "provider_receipt_valid": web_receipt_ok,
            "canonical_origin_verified": web_origin_verified,
            "candidate": web_candidate,
        },
        "api": {
            "status": api_status,
            "health_reachable": api_health_reachable,
            "provider_receipt_valid": api_receipt_ok,
            "canonical_origin_verified": api_origin_verified,
            "candidate": api_candidate,
        },
        "production_green": production_green,
        "verdict": verdict,
        "evidence_errors": sorted(set(evidence_errors)),
        "next_actions": []
        if production_green
        else [
            "READ-ONLY: capture fresh Railway provider receipts for canonical web and API",
            "READ-ONLY: bind both receipts to the canonical project + production environment",
            "READ-ONLY: bind web receipt to provider Config File /apps/web/railway.toml",
            "READ-ONLY: bind both deployment SHAs to the same accepted release SHA",
            "READ-ONLY: verify generated/custom-domain routing, ownership, TLS, and API /healthz",
            "HOLD: no deploy/redeploy/domain/DNS/DB/secret mutation from this gate",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--frontend-base", default="https://dealix.me")
    parser.add_argument("--api-health-url", default="https://api.dealix.me/healthz")
    parser.add_argument("--web-provider-receipt", type=Path)
    parser.add_argument("--api-provider-receipt", type=Path)
    parser.add_argument("--accepted-sha")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        provider_authority = _provider_authority()
        web_candidate, api_candidate = _canonical_candidates()
    except (OSError, json.JSONDecodeError, RuntimeError) as exc:
        print("RAILWAY_PRODUCTION_IDENTITY_GATE=FAIL")
        print(f"  source_contract_error={exc}")
        print("RAILWAY_PRODUCTION_IDENTITY_GATE_VERDICT=FAIL")
        return 1

    web_status, web_server = _probe(
        f"{args.frontend_base.rstrip('/')}/ar", method="HEAD"
    )
    api_status, _ = _probe(args.api_health_url, method="GET")
    web_receipt, web_load_errors = _load_receipt(args.web_provider_receipt)
    api_receipt, api_load_errors = _load_receipt(args.api_provider_receipt)

    out = evaluate_production_identity(
        web_status=web_status,
        web_server=web_server,
        api_status=api_status,
        web_receipt=web_receipt,
        api_receipt=api_receipt,
        accepted_sha=args.accepted_sha,
        web_receipt_load_errors=web_load_errors,
        api_receipt_load_errors=api_load_errors,
        web_candidate=web_candidate,
        api_candidate=api_candidate,
        provider_authority=provider_authority,
    )

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(
            "WEB_CANONICAL_ORIGIN_VERIFIED="
            f"{str(out['web']['canonical_origin_verified']).upper()}"
        )
        print(
            "API_CANONICAL_ORIGIN_VERIFIED="
            f"{str(out['api']['canonical_origin_verified']).upper()}"
        )
        print(f"PRODUCTION_GREEN={str(out['production_green']).upper()}")
        for error in out["evidence_errors"]:
            print(f"  evidence_error={error}")
        for action in out["next_actions"]:
            print(f"  -> {action}")

    print(f"RAILWAY_PRODUCTION_IDENTITY_GATE_VERDICT={out['verdict']}")
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
