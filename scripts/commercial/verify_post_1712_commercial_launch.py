#!/usr/bin/env python3
"""Composite post-#1712 Dealix commercial launch gate.

This gate is read-only with respect to external systems. It composes existing
commercial truth verifiers and distinguishes source readiness from deployed
production readiness. A merged commit is never treated as proof of deployment.
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
CANONICAL_AGENTS = ["dealix-pm", "dealix-sales", "dealix-delivery", "dealix-engineer", "dealix-content"]
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
    if len(routes) != 20:
        errors.append(f"expected 20 canonical sector routes, got {len(routes)}")
    if payload.get("counts_as_pipeline") is not False or payload.get("counts_as_revenue") is not False:
        errors.append("research diagnostic routes must never count as pipeline/revenue")
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
        if handoff.get("canonical_agents") != CANONICAL_AGENTS:
            errors.append(f"{sector}: handoff must use exactly five canonical agents")


def fetch_status(url: str, timeout: float = 8.0) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "Dealix-Commercial-Launch-Gate/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read(8192).decode("utf-8", errors="replace")
            return {"url": url, "ok": 200 <= response.status < 400, "status": response.status, "body_sample": body[:1000]}
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        return {"url": url, "ok": False, "error": str(exc)}


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
    if args.api_health_url:
        health = fetch_status(args.api_health_url)
        production_checks.append(health)
        if args.expected_release and health.get("ok"):
            sample = health.get("body_sample", "")
            if args.expected_release not in sample:
                errors.append("deployed API release does not match expected release")
    if production_checks and not all(item.get("ok") for item in production_checks):
        errors.append("one or more production HTTP checks failed")

    deployment_verified = bool(args.public_base_url and args.api_health_url and args.expected_release and not errors)
    if errors:
        status = "BLOCKED"
    elif deployment_verified:
        status = "COMMERCIAL_LAUNCH_GREEN"
    else:
        status = "SOURCE_READY_DEPLOYMENT_UNVERIFIED"
        warnings.append("source readiness does not prove deployed production identity")

    report = {
        "schema": "dealix.post-1712-commercial-launch-gate.v1",
        "generated_at": datetime.now(UTC).isoformat(),
        "status": status,
        "errors": errors,
        "warnings": warnings,
        "sector_routes": len(routes.get("routes") or []) if routes else 0,
        "canonical_agents": CANONICAL_AGENTS,
        "subchecks": subchecks,
        "production_checks": production_checks,
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
