#!/usr/bin/env python3
"""Composite post-#1712 Dealix commercial launch gate.

This gate is read-only with respect to external systems. It composes existing
commercial truth verifiers and distinguishes source readiness from deployed
production readiness. A merged commit is never treated as proof of deployment.

Omega V3 note: the historical five executor names are compatibility aliases,
not architecture authority. Current execution authority is registry-derived.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
REPORT = ROOT / "reports/commercial/post_1712_launch_gate.json"
LEGACY_EXECUTOR_ALIASES = ["dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"]
LEGACY_ALIAS_SEMANTICS = "LEGACY_EXECUTOR_ALIASES_ONLY_NOT_ARCHITECTURE_AUTHORITY"
CURRENT_ARCHITECTURE = "agentic_holding_sector_company_mesh"
RETIRED_PUBLIC_SURFACES = {
    "/trust.html": "/trust-center.html",
    "/security.html": "/trust-center.html",
    "/why-saudi-ai.html": "/trust-center.html",
    "/roi.html": "/proof.html",
    "/case-study.html": "/proof.html",
}
BANNED_STALE_PUBLIC_CLAIMS = ("PDPL Compliant", "Saudi data residency", "ZATCA Phase 2 Ready")
REQUIRED_FILES = [
    "skills/dealix-commercial-execution/SKILL.md",
    "dealix/commercial/universal_diagnostic_factory.py",
    "dealix/commercial/sector_commercial_factory.py",
    "dealix/commercial/sector_company_factory.py",
    "scripts/ops/session_factory.py",
    "scripts/commercial/commercial_readiness_check.py",
    "scripts/commercial/verify_op2_sector_diagnostic_router.py",
    "data/commercial/op2_sector_diagnostic_routes_v1.json",
    "docs/commercial/POST_1712_COMMERCIAL_LAUNCH_ACCEPTANCE_2026-09-12.md",
]
SUBCHECKS = [
    [sys.executable, "scripts/commercial/commercial_readiness_check.py"],
    [sys.executable, "scripts/commercial/verify_op2_sector_diagnostic_router.py"],
]


def run_check(argv: list[str]) -> dict[str, Any]:
    proc = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True, timeout=120, check=False)
    return {"argv": argv, "returncode": proc.returncode, "stdout": proc.stdout[-4000:], "stderr": proc.stderr[-2000:]}


def load_routes(errors: list[str]) -> dict[str, Any]:
    path = ROOT / "data/commercial/op2_sector_diagnostic_routes_v1.json"
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"diagnostic routes unreadable: {exc}")
        return {}


def validate_routes(payload: dict[str, Any], errors: list[str]) -> None:
    routes = payload.get("routes") or []
    if not routes:
        errors.append("no sector diagnostic routes")
    if payload.get("counts_as_pipeline") is not False or payload.get("counts_as_revenue") is not False:
        errors.append("research diagnostic routes must never count as pipeline/revenue")

    holding = payload.get("agentic_holding")
    if holding is not None:
        if holding.get("architecture") != CURRENT_ARCHITECTURE:
            errors.append("agentic_holding architecture drift")
        if holding.get("fixed_five_authority") is not False:
            errors.append("fixed-five architecture authority is forbidden")
        if holding.get("orphan_failures"):
            errors.append("agentic_holding has orphan failures")
        expected_sector_routes = holding.get("sector_companies")
        if not isinstance(expected_sector_routes, int) or expected_sector_routes < 1:
            errors.append("agentic_holding sector-company count missing or invalid")
        elif len(routes) != expected_sector_routes:
            errors.append(
                f"sector route count must match current Agentic Holding registry: "
                f"expected {expected_sector_routes}, got {len(routes)}"
            )

    for route in routes:
        sector = route.get("sector_id", "UNKNOWN")
        entry = route.get("diagnostic_entry") or {}
        if entry.get("route") != "/book":
            errors.append(f"{sector}: canonical diagnostic route must be /book")
        if entry.get("card_required") is not False:
            errors.append(f"{sector}: diagnostic must be card-free")
        if entry.get("roi_promised") is not False:
            errors.append(f"{sector}: diagnostic must not promise ROI")

        handoff = route.get("crm_handoff") or {}
        if handoff.get("canonical_agents") != LEGACY_EXECUTOR_ALIASES:
            errors.append(f"{sector}: legacy executor alias compatibility drift")
        if handoff.get("fixed_five_authority") is True:
            errors.append(f"{sector}: fixed-five architecture authority is forbidden")
        semantics = handoff.get("canonical_agents_field_semantics")
        if semantics is not None and semantics != LEGACY_ALIAS_SEMANTICS:
            errors.append(f"{sector}: legacy alias semantics drift")
        architecture = handoff.get("architecture")
        if architecture is not None and architecture != CURRENT_ARCHITECTURE:
            errors.append(f"{sector}: Agentic Holding architecture drift")


def fetch_status(url: str, timeout: float = 8.0) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "Dealix-Commercial-Launch-Gate/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(16384).decode("utf-8", errors="replace")
            return {"url": url, "final_url": response.geturl(), "ok": 200 <= response.status < 400, "status": response.status, "body_sample": body[:12000]}
    except urllib.error.HTTPError as exc:
        body = exc.read(4096).decode("utf-8", errors="replace")
        return {"url": url, "final_url": exc.geturl(), "ok": False, "status": exc.code, "body_sample": body[:4000], "error": str(exc)}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"url": url, "final_url": url, "ok": False, "error": str(exc)}


def required_http_failures(checks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in checks if not item.get("surface") and not item.get("ok")]


def validate_retired_surface(check: dict[str, Any], path: str, target: str, errors: list[str]) -> None:
    if not check.get("ok"):
        return
    body = str(check.get("body_sample", ""))
    lowered = body.lower()
    for claim in BANNED_STALE_PUBLIC_CLAIMS:
        if claim.lower() in lowered:
            errors.append(f"stale public claim on retired surface {path}: {claim}")
    final_url = str(check.get("final_url", "")).rstrip("/")
    target_ok = final_url.endswith(target.rstrip("/")) or "DEALIX_RETIRED_PUBLIC_SURFACE" in body
    if not target_ok:
        errors.append(f"retired public surface not converged: {path} -> {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--public-base-url", default="")
    parser.add_argument("--api-health-url", default="")
    parser.add_argument("--expected-release", default="")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).exists():
            errors.append(f"missing required canonical asset: {rel}")

    routes = load_routes(errors)
    if routes:
        validate_routes(routes, errors)

    skill_path = ROOT / "skills/dealix-commercial-execution/SKILL.md"
    if skill_path.exists():
        skill = skill_path.read_text(encoding="utf-8")
        for invariant in ("research != relationship", "draft != sent", "quote != invoice", "invoice != payment"):
            if invariant not in skill:
                errors.append(f"commercial skill missing invariant: {invariant}")

    acceptance_path = ROOT / "docs/commercial/POST_1712_COMMERCIAL_LAUNCH_ACCEPTANCE_2026-09-12.md"
    if acceptance_path.exists():
        acceptance = acceptance_path.read_text(encoding="utf-8")
        if "payment != revenue" not in acceptance:
            errors.append("post-1712 acceptance contract missing payment != revenue invariant")

    subchecks = [run_check(command) for command in SUBCHECKS if (ROOT / command[1]).exists()]
    for check in subchecks:
        if check["returncode"] != 0:
            errors.append(f"subcheck failed: {' '.join(check['argv'])}")

    production_checks: list[dict[str, Any]] = []
    if args.public_base_url:
        base = args.public_base_url.rstrip("/")
        production_checks.extend([fetch_status(base + "/"), fetch_status(base + "/book")])
        for path, target in RETIRED_PUBLIC_SURFACES.items():
            check = fetch_status(base + path)
            check["surface"] = path
            check["expected_target"] = target
            production_checks.append(check)
            validate_retired_surface(check, path, target, errors)
            if not check.get("ok"):
                warnings.append(f"retired public surface unavailable instead of redirect: {path}")
    if args.api_health_url:
        health = fetch_status(args.api_health_url)
        production_checks.append(health)
        if args.expected_release and health.get("ok"):
            sample = health.get("body_sample", "")
            if args.expected_release not in sample:
                errors.append("deployed API release does not match expected release")
    if required_http_failures(production_checks):
        errors.append("one or more required production HTTP checks failed")

    deployment_verified = bool(args.public_base_url and args.api_health_url and args.expected_release and not errors)
    if errors:
        status = "BLOCKED"
    elif deployment_verified:
        status = "COMMERCIAL_LAUNCH_GREEN"
    else:
        status = "SOURCE_READY_DEPLOYMENT_UNVERIFIED"
        warnings.append("source readiness does not prove deployed production identity")

    holding = routes.get("agentic_holding") if routes else None
    report = {
        "schema": "dealix.post-1712-commercial-launch-gate.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "sector_routes": len(routes.get("routes") or []) if routes else 0,
        # Backward-compatible field only; not architecture authority.
        "canonical_agents": LEGACY_EXECUTOR_ALIASES,
        "canonical_agents_field_semantics": LEGACY_ALIAS_SEMANTICS,
        "fixed_five_authority": False,
        "agentic_holding": holding,
        "subchecks": subchecks,
        "production_checks": production_checks,
        "retired_404_count": sum(1 for item in production_checks if item.get("surface") and item.get("status") == 404),
        "deployment_verified": deployment_verified,
        "external_effects_executed": False,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"DEALIX_POST_1712_COMMERCIAL_LAUNCH={status}")
    print(f"REPORT={REPORT.relative_to(ROOT)}")
    for item in errors:
        print(f"FAIL: {item}")
    for item in warnings:
        print(f"WARN: {item}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())