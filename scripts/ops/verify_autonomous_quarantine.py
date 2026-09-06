#!/usr/bin/env python3
"""Verify legacy-router quarantine in a test-environment application composition.

This is source/runtime-import evidence, NOT deployed-production or tenant-safety
proof. Never import the quarantined module, serve requests, or authorize release.
"""
from __future__ import annotations

import ast
import importlib
import importlib.util
import os
import sys
from collections.abc import Iterable
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOMAIN_INIT = ROOT / "api/routers/domains/agents/__init__.py"
LEGACY_ROUTER = ROOT / "api/routers/autonomous.py"
LEGACY_MODULE = "api.routers.autonomous"
HIGH_RISK_LEGACY_PATHS = (
    "/companies/intake", "/outreach/queue", "/payments/mark-paid",
    "/customers/onboard", "/partners/intake",
)
SAFE_FLAGS = (
    "DEALIX_EXTERNAL_SEND", "DEALIX_EMAIL_LIVE_SEND", "DEALIX_WHATSAPP_OUTBOUND",
    "DEALIX_PUBLIC_PUBLISH", "DEALIX_PAID_SPEND", "DEALIX_PAYMENT_EXECUTION",
    "DEALIX_PRODUCTION_MUTATION", "DEALIX_DNS_MUTATION", "DEALIX_DB_MUTATION",
    "DEALIX_SECRET_MUTATION", "DEALIX_IDENTITY_MUTATION", "DEALIX_AGENT_SELF_AUTHORITY",
)


def _legacy(name: str) -> bool:
    return name == LEGACY_MODULE or name.startswith(LEGACY_MODULE + ".")


def _registration_findings(source: str) -> list[str]:
    """Inspect syntax, not comments/docstrings; runtime inspection is also required."""
    findings: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            findings.update(a.name for a in node.names if _legacy(a.name))
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if node.level:
                module = importlib.util.resolve_name(
                    "." * node.level + module, "api.routers.domains.agents"
                )
            if _legacy(module):
                findings.add(module)
            if module == "api.routers":
                findings.update(LEGACY_MODULE for a in node.names if a.name == "autonomous")
        elif isinstance(node, ast.Call):
            name = getattr(node.func, "id", getattr(node.func, "attr", ""))
            if name in {"import_module", "__import__"} and node.args:
                arg = node.args[0]
                if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
                    if _legacy(arg.value):
                        findings.add(arg.value)
    return sorted(findings)


def _route_paths(source: str) -> set[str]:
    paths: set[str] = set()
    for node in ast.walk(ast.parse(source)):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        for dec in node.decorator_list:
            if not isinstance(dec, ast.Call) or not isinstance(dec.func, ast.Attribute):
                continue
            if not isinstance(dec.func.value, ast.Name) or dec.func.value.id != "router":
                continue
            value = dec.args[0] if dec.args else next(
                (k.value for k in dec.keywords if k.arg == "path"), None
            )
            if isinstance(value, ast.Constant) and isinstance(value.value, str):
                paths.add(value.value)
    return paths


def _endpoint_is_legacy(endpoint: object) -> bool:
    pending = [endpoint]
    visited: set[int] = set()
    while pending:
        item = pending.pop()
        if item is None or id(item) in visited:
            continue
        visited.add(id(item))
        if _legacy(getattr(item, "__module__", "") or ""):
            return True
        for attr in ("__wrapped__", "func", "__func__"):
            child = getattr(item, attr, None)
            if child is not None:
                pending.append(child)
    return False


def _inspect_routes(roots: Iterable[object]) -> tuple[int, list[str]]:
    """Traverse eager routers, lazy inclusions and mounted route trees; reject opaque nodes."""
    pending = list(roots)
    visited: set[int] = set()
    findings: set[str] = set()
    endpoints = 0
    while pending:
        item = pending.pop()
        if id(item) in visited:
            continue
        visited.add(id(item))
        if len(visited) > 100000:
            raise ValueError("route_graph_limit")
        context = getattr(item, "include_context", None)
        for obj in (item, context):
            if obj is not None and "autonomous" in (getattr(obj, "tags", None) or []):
                findings.add("legacy_tag")
        is_mount = any(cls.__name__ == "Mount" for cls in type(item).__mro__)
        endpoint = getattr(item, "endpoint", None)
        if endpoint is not None:
            endpoints += 1
            if _endpoint_is_legacy(endpoint):
                findings.add("legacy_endpoint_module")
        children: list[object] = []
        routes = getattr(item, "routes", None)
        if routes is not None:
            children.extend(list(routes))
        original = getattr(item, "original_router", None)
        if original is not None:
            children.append(original)
        # Mount.app can be the only access path for a mounted ASGI application.
        app = getattr(item, "app", None)
        if (endpoint is None or is_mount) and not children and app is not None and app is not item:
            children.append(app)
        if endpoint is None and not children and routes is None:
            raise ValueError("opaque_route_node")
        pending.extend(children)
    if endpoints == 0:
        raise ValueError("empty_route_inventory")
    return endpoints, sorted(findings)


def _checked_import(name: str, path: Path) -> object:
    module = importlib.import_module(name)
    origin = getattr(module, "__file__", None)
    if not origin or Path(origin).resolve() != path.resolve():
        raise ValueError("module_source_mismatch")
    return module


def main() -> int:
    if os.environ.get("APP_ENV") != "test" or any(
        os.environ.get(flag) != "0" for flag in SAFE_FLAGS
    ):
        print("AUTONOMOUS_QUARANTINE=HOLD")
        print("reason=test_environment_and_fail_closed_flags_required")
        return 4
    try:
        source = DOMAIN_INIT.read_text(encoding="utf-8")
        paths = _route_paths(LEGACY_ROUTER.read_text(encoding="utf-8"))
        if _registration_findings(source):
            print("AUTONOMOUS_QUARANTINE=FAIL")
            print("reason=legacy_domain_import_detected")
            return 2
        # Executing this script by pathname otherwise prioritizes scripts/ops.
        sys.path.insert(0, str(ROOT))
        domain = _checked_import("api.routers.domains.agents", DOMAIN_INIT)
        domain_count, domain_bad = _inspect_routes(domain.get_routers())
        application = _checked_import("api.main", ROOT / "api/main.py")
        app_count, app_bad = _inspect_routes([application.app])
        if domain_bad or app_bad:
            print("AUTONOMOUS_QUARANTINE=FAIL")
            print("reason=" + ",".join(sorted(set(domain_bad + app_bad))))
            return 3
    except Exception as exc:
        # Exception messages can contain DSNs or credentials. Emit type only.
        print("AUTONOMOUS_QUARANTINE=HOLD")
        print("reason=inspection_incomplete")
        print("error_type=" + type(exc).__name__)
        return 4
    print("AUTONOMOUS_QUARANTINE=PASS")
    print("scope=test_environment_imported_application_only")
    print("deployed_production_verified=false")
    print("tenant_isolation_verified=false")
    print(f"agents_domain_endpoints={domain_count}")
    print(f"application_endpoints={app_count}")
    print(f"legacy_high_risk_paths_present={len(set(HIGH_RISK_LEGACY_PATHS) & paths)}")
    print("re_registration_authorized=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
