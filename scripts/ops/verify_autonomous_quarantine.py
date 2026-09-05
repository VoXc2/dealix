#!/usr/bin/env python3
"""Fail-closed verifier for legacy autonomous router quarantine (#1070).

The legacy ``api.routers.autonomous`` module may remain in the repository as
migration/history material, but it MUST NOT be production-registered while its
mixed-generation public/global endpoints remain unresolved.

This verifier does not authorize re-registration. It proves the opposite:
Dealix can operate canonical tenant-safe surfaces while the legacy router stays
unavailable to production callers.
"""

from __future__ import annotations

import ast
import importlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_INIT = ROOT / "api" / "routers" / "domains" / "agents" / "__init__.py"
LEGACY_ROUTER = ROOT / "api" / "routers" / "autonomous.py"

FORBIDDEN_REGISTRATION_TOKENS = (
    "autonomous.router",
    "api.routers.autonomous",
)

HIGH_RISK_LEGACY_PATHS = (
    "/companies/intake",
    "/outreach/queue",
    "/payments/mark-paid",
    "/customers/onboard",
    "/partners/intake",
)


def _route_paths(source: str) -> set[str]:
    tree = ast.parse(source)
    paths: set[str] = set()
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call):
                continue
            func = decorator.func
            if not isinstance(func, ast.Attribute):
                continue
            if not isinstance(func.value, ast.Name) or func.value.id != "router":
                continue
            if not decorator.args:
                continue
            value = decorator.args[0]
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                paths.add(value.value)
    return paths


def main() -> int:
    domain_source = DOMAIN_INIT.read_text(encoding="utf-8")
    legacy_source = LEGACY_ROUTER.read_text(encoding="utf-8")

    bad_registration = [
        token for token in FORBIDDEN_REGISTRATION_TOKENS if token in domain_source
    ]
    if bad_registration:
        print("AUTONOMOUS_QUARANTINE=FAIL")
        print("reason=legacy_router_registration_detected")
        print("tokens=" + ",".join(bad_registration))
        return 2

    paths = _route_paths(legacy_source)
    present_high_risk = sorted(set(HIGH_RISK_LEGACY_PATHS) & paths)

    domain = importlib.import_module("api.routers.domains.agents")
    routers = domain.get_routers()
    router_tags = {
        tag
        for router in routers
        for route in getattr(router, "routes", [])
        for tag in getattr(route, "tags", []) or []
    }
    if "autonomous" in router_tags:
        print("AUTONOMOUS_QUARANTINE=FAIL")
        print("reason=autonomous_tag_present_in_production_domain")
        return 3

    print("AUTONOMOUS_QUARANTINE=PASS")
    print("production_registered=false")
    print(f"legacy_high_risk_paths_present={len(present_high_risk)}")
    for path in present_high_risk:
        print(f"legacy_path={path}")
    print("re_registration_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
