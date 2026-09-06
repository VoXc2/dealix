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
import re
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
INSPECTION_STAGES = {
    "source_read",
    "domain_import",
    "domain_routes",
    "application_import",
    "application_routes",
}
INSPECTION_CODES = {
    "route_graph_limit",
    "opaque_route_node",
    "empty_route_inventory",
    "module_source_mismatch",
}
_SAFE_DETAIL_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,160}$")
_SAFE_EDGES = {"root", "routes", "original_router", "app"}


class InspectionError(ValueError):
    """A verifier-owned, non-secret structural inspection failure."""

    def __init__(
        self,
        code: str,
        detail: str | None = None,
        parent: str | None = None,
        edge: str | None = None,
    ):
        if code not in INSPECTION_CODES:
            raise ValueError("invalid_inspection_code")
        self.code = code
        self.detail = detail if detail and _SAFE_DETAIL_RE.fullmatch(detail) else None
        self.parent = parent if parent and _SAFE_DETAIL_RE.fullmatch(parent) else None
        self.edge = edge if edge in _SAFE_EDGES else None
        super().__init__(code)


def _inspection_error(
    code: str,
    detail: str | None = None,
    parent: str | None = None,
    edge: str | None = None,
) -> None:
    raise InspectionError(code, detail, parent, edge)


def _type_fingerprint(item: object) -> str:
    """Return only a bounded module/class identifier; never repr/str/object state."""
    cls = type(item)
    return f"{getattr(cls, '__module__', 'unknown')}.{getattr(cls, '__qualname__', cls.__name__)}"


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
    """Traverse eager/lazy/mounted routes and fail closed on opaque nodes.

    Traversal provenance is retained only as bounded type fingerprints plus an
    allowlisted edge name. This exists strictly to diagnose fail-closed HOLDs;
    it must never serialize object state, repr/str values, paths, or exceptions.
    """
    pending: list[tuple[object, str | None, str]] = [
        (root, None, "root") for root in roots
    ]
    visited: set[int] = set()
    findings: set[str] = set()
    endpoints = 0
    while pending:
        item, parent_type, ingress_edge = pending.pop()
        if id(item) in visited:
            continue
        visited.add(id(item))
        if len(visited) > 100000:
            _inspection_error("route_graph_limit")
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

        parent_for_children = _type_fingerprint(item)
        children: list[tuple[object, str]] = []
        routes = getattr(item, "routes", None)
        if routes is not None:
            children.extend((child, "routes") for child in list(routes))
        original = getattr(item, "original_router", None)
        if original is not None:
            children.append((original, "original_router"))
        # Mount.app can be the only access path for a mounted ASGI application.
        # Do not treat generic framework callables such as APIRouter.app as
        # structural children: the app edge is a Mount-specific traversal edge.
        app = getattr(item, "app", None)
        if is_mount and not children and app is not None and app is not item:
            children.append((app, "app"))
        if endpoint is None and not children and routes is None:
            _inspection_error(
                "opaque_route_node",
                _type_fingerprint(item),
                parent_type,
                ingress_edge,
            )
        pending.extend(
            (child, parent_for_children, child_edge)
            for child, child_edge in children
        )
    if endpoints == 0:
        _inspection_error("empty_route_inventory")
    return endpoints, sorted(findings)


def _checked_import(name: str, path: Path) -> object:
    module = importlib.import_module(name)
    origin = getattr(module, "__file__", None)
    if not origin or Path(origin).resolve() != path.resolve():
        _inspection_error("module_source_mismatch")
    return module


def main() -> int:
    if os.environ.get("APP_ENV") != "test" or any(
        os.environ.get(flag) != "0" for flag in SAFE_FLAGS
    ):
        print("AUTONOMOUS_QUARANTINE=HOLD")
        print("reason=test_environment_and_fail_closed_flags_required")
        return 4
    stage = "source_read"
    try:
        source = DOMAIN_INIT.read_text(encoding="utf-8")
        paths = _route_paths(LEGACY_ROUTER.read_text(encoding="utf-8"))
        if _registration_findings(source):
            print("AUTONOMOUS_QUARANTINE=FAIL")
            print("reason=legacy_domain_import_detected")
            return 2
        # Executing this script by pathname otherwise prioritizes scripts/ops.
        sys.path.insert(0, str(ROOT))
        stage = "domain_import"
        domain = _checked_import("api.routers.domains.agents", DOMAIN_INIT)
        stage = "domain_routes"
        domain_count, domain_bad = _inspect_routes(domain.get_routers())
        stage = "application_import"
        application = _checked_import("api.main", ROOT / "api/main.py")
        stage = "application_routes"
        app_count, app_bad = _inspect_routes([application.app])
        if domain_bad or app_bad:
            print("AUTONOMOUS_QUARANTINE=FAIL")
            print("reason=" + ",".join(sorted(set(domain_bad + app_bad))))
            return 3
    except InspectionError as exc:
        print("AUTONOMOUS_QUARANTINE=HOLD")
        print("reason=inspection_incomplete")
        print("inspection_stage=" + (stage if stage in INSPECTION_STAGES else "unknown"))
        print("inspection_code=" + exc.code)
        if exc.detail:
            print("inspection_detail=" + exc.detail)
        if exc.parent:
            print("inspection_parent=" + exc.parent)
        if exc.edge:
            print("inspection_edge=" + exc.edge)
        print("error_type=InspectionError")
        return 4
    except Exception as exc:
        # Exception messages can contain DSNs or credentials. Emit only type +
        # verifier-owned stage, never repr(exc), str(exc), env values, or paths.
        print("AUTONOMOUS_QUARANTINE=HOLD")
        print("reason=inspection_incomplete")
        print("inspection_stage=" + (stage if stage in INSPECTION_STAGES else "unknown"))
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