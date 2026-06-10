#!/usr/bin/env python3
"""Verify Railway deploy surfaces for API and web services.

This is intentionally dependency-free so it can run in CI before Docker builds.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SERVICE_MATRIX = ROOT / "dealix/config/railway_services.json"

REQUIRED_FILES = [
    "Dockerfile",
    "railway.json",
    "api/routers/health.py",
    "dealix/config/railway_services.json",
    "frontend/Dockerfile",
    "frontend/railway.json",
    "frontend/next.config.ts",
    "frontend/src/app/healthz/route.ts",
    "apps/web/Dockerfile",
    "apps/web/railway.json",
    "apps/web/next.config.js",
    "apps/web/app/healthz/route.ts",
]

FORBIDDEN_PUBLIC_SECRET_MARKERS = [
    "NEXT_PUBLIC_DEALIX_ADMIN_API_KEY",
    "NEXT_PUBLIC_ADMIN_API_KEY",
    "NEXT_PUBLIC_API_KEY=",
]


def fail(message: str) -> None:
    raise SystemExit(f"RAILWAY_SURFACES_FAIL: {message}")


def read(path: str) -> str:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    return target.read_text(encoding="utf-8")


def load_json(path: str) -> dict[str, Any]:
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path}: {exc}")


def verify_railway_json(path: str, *, allow_predeploy: bool) -> None:
    cfg = load_json(path)
    build = cfg.get("build")
    deploy = cfg.get("deploy")
    if not isinstance(build, dict) or build.get("builder") != "DOCKERFILE":
        fail(f"{path} must use build.builder=DOCKERFILE")
    if build.get("dockerfilePath") != "Dockerfile":
        fail(f"{path} must use Dockerfile relative to service root")
    if not isinstance(deploy, dict) or deploy.get("healthcheckPath") != "/healthz":
        fail(f"{path} must healthcheck /healthz")
    if not allow_predeploy and "preDeployCommand" in deploy:
        fail(f"{path} must not run API predeploy commands for web images")


def verify_service_matrix() -> None:
    matrix = load_json("dealix/config/railway_services.json")
    services = matrix.get("services")
    if not isinstance(services, list) or len(services) < 3:
        fail("dealix/config/railway_services.json must list API, frontend, and apps/web services")

    names = {svc.get("name") for svc in services if isinstance(svc, dict)}
    required = {"dealix-api", "dealix-frontend", "dealix-apps-web"}
    if not required.issubset(names):
        missing = sorted(required - names)
        fail(f"railway service names missing core services: {missing} not in {sorted(names)}")

    # Core public-facing services require full validation.
    # Background workers/watchdogs only need a name + dockerfile.
    core_services = {"dealix-api", "dealix-frontend", "dealix-apps-web"}

    for svc in services:
        if not isinstance(svc, dict):
            fail("railway service entry must be an object")
        name = str(svc.get("name", ""))
        railway_config = str(svc.get("railwayConfig", ""))
        dockerfile = str(svc.get("dockerfilePath", ""))
        root_dir = str(svc.get("rootDirectory", ""))
        healthcheck = str(svc.get("healthcheckPath", ""))
        required_env = svc.get("requiredEnv")

        if not name or not dockerfile:
            fail(f"{name or '<unnamed>'}: missing name or dockerfilePath")

        if name in core_services:
            if not railway_config:
                fail(f"{name}: missing railwayConfig")
            if healthcheck != "/healthz":
                fail(f"{name}: healthcheckPath must be /healthz")
            if not isinstance(required_env, list) or not required_env:
                fail(f"{name}: requiredEnv must be a non-empty list")
            read(railway_config)
            read(f"{root_dir.rstrip('/') + '/' if root_dir not in ('', '.') else ''}{dockerfile}")


def main() -> None:
    for path in REQUIRED_FILES:
        read(path)

    verify_service_matrix()
    verify_railway_json("railway.json", allow_predeploy=True)
    verify_railway_json("frontend/railway.json", allow_predeploy=False)
    verify_railway_json("apps/web/railway.json", allow_predeploy=False)

    for path in ("frontend/next.config.ts", "apps/web/next.config.js"):
        content = read(path)
        if "output: 'standalone'" not in content and 'output: "standalone"' not in content:
            fail(f"{path} must enable standalone output")

    for path in ("frontend/Dockerfile", "apps/web/Dockerfile"):
        content = read(path)
        if ".next/standalone" not in content:
            fail(f"{path} must copy .next/standalone")
        for marker in FORBIDDEN_PUBLIC_SECRET_MARKERS:
            if marker in content:
                fail(f"{path} must not expose secrets through public env marker {marker}")

    for path in ("frontend/src/app/healthz/route.ts", "apps/web/app/healthz/route.ts"):
        content = read(path)
        if "status" not in content or "ok" not in content:
            fail(f"{path} must return a simple ok payload")

    print("RAILWAY_SURFACES_OK")


if __name__ == "__main__":
    main()
