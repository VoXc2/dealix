#!/usr/bin/env python3
"""Verify canonical Railway deploy surfaces and production authority.

`apps/web` is the only canonical public frontend. The historical `frontend/`
surface may remain in the repository for compatibility, but it must never gain
production authority and must never be required for canonical launch acceptance.

The canonical web service must use its dedicated `/apps/web/railway.toml` at the
provider. This prevents the frontend from inheriting repo-root API pre-deploy
commands. Provider config selection is part of production identity, not an
operator convenience.
"""

from __future__ import annotations

import json
import tomllib
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SERVICE_MATRIX = ROOT / "dealix/config/railway_services.json"
CANONICAL_SOURCE_REPOSITORY = "Dealix-sa/dealix"
CANONICAL_WEB_CONFIG = "apps/web/railway.toml"
CANONICAL_WEB_PROVIDER_CONFIG = "/apps/web/railway.toml"

REQUIRED_FILES = [
    "Dockerfile",
    "railway.json",
    "api/routers/health.py",
    "dealix/config/railway_services.json",
    "apps/web/Dockerfile",
    CANONICAL_WEB_CONFIG,
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


def load_railway_config(path: str) -> dict[str, Any]:
    target = ROOT / path
    if not target.exists():
        fail(f"missing {path}")
    if target.suffix == ".json":
        return load_json(path)
    if target.suffix == ".toml":
        try:
            payload = tomllib.loads(target.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            fail(f"invalid TOML in {path}: {exc}")
        if not isinstance(payload, dict):
            fail(f"Railway config root must be an object: {path}")
        return payload
    fail(f"unsupported Railway config format: {path}")


def service_path(root_dir: str, path: str) -> str:
    prefix = root_dir.rstrip("/")
    return f"{prefix}/{path}" if prefix not in ("", ".") else path


def verify_railway_config(path: str, *, allow_predeploy: bool) -> None:
    cfg = load_railway_config(path)
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
        fail(
            "dealix/config/railway_services.json must list API, apps/web, "
            "and background services"
        )

    if any(not isinstance(svc, dict) for svc in services):
        fail("railway service entry must be an object")

    by_name = {str(svc.get("name", "")): svc for svc in services}
    required = {"dealix-api", "dealix-apps-web"}
    if not required.issubset(by_name):
        missing = sorted(required - set(by_name))
        fail(
            f"railway service names missing required services: {missing} "
            f"not in {sorted(by_name)}"
        )

    canonical_web = [
        svc for svc in services if svc.get("role") == "canonical_public_web"
    ]
    if len(canonical_web) != 1:
        fail(
            "exactly one canonical_public_web service is required; "
            f"found {len(canonical_web)}"
        )

    web = canonical_web[0]
    if web.get("name") != "dealix-apps-web":
        fail("canonical_public_web authority must belong to dealix-apps-web")
    if web.get("rootDirectory") != "apps/web":
        fail("dealix-apps-web canonical rootDirectory must be apps/web")
    if web.get("expectedSourceRepository") != CANONICAL_SOURCE_REPOSITORY:
        fail("dealix-apps-web must be bound to Dealix-sa/dealix source authority")
    if web.get("productionAuthority") is not True:
        fail("dealix-apps-web must explicitly carry productionAuthority=true")
    if web.get("publicNetworking") is not True:
        fail("dealix-apps-web must explicitly carry publicNetworking=true")
    if web.get("requiredEnv") != ["NEXT_PUBLIC_API_URL", "NEXT_PUBLIC_SITE_URL"]:
        fail(
            "dealix-apps-web requiredEnv must contain only canonical "
            "browser-safe URL variables"
        )
    if web.get("railwayConfig") != CANONICAL_WEB_CONFIG:
        fail(
            "dealix-apps-web railwayConfig must be apps/web/railway.toml; "
            "repo-root config can carry API predeploy authority"
        )
    if web.get("providerConfigFile") != CANONICAL_WEB_PROVIDER_CONFIG:
        fail(
            "dealix-apps-web providerConfigFile must be "
            "/apps/web/railway.toml"
        )
    if web.get("runsPredeploy") is not False:
        fail("dealix-apps-web must explicitly run no predeploy command")

    api = by_name["dealix-api"]
    if api.get("role") != "canonical_api" or api.get("productionAuthority") is not True:
        fail("dealix-api must be canonical_api with productionAuthority=true")
    if api.get("expectedSourceRepository") != CANONICAL_SOURCE_REPOSITORY:
        fail("dealix-api must be bound to Dealix-sa/dealix source authority")

    legacy = by_name.get("dealix-frontend")
    if legacy is not None:
        if legacy.get("role") != "legacy_public_web":
            fail("dealix-frontend must be explicitly marked legacy_public_web")
        if legacy.get("productionAuthority") is not False:
            fail("dealix-frontend must never carry production authority")
        if legacy.get("rootDirectory") != "frontend":
            fail("dealix-frontend legacy rootDirectory must remain frontend")

    # Validate only canonical deploy surfaces as launch requirements. Legacy
    # compatibility entries are authority-checked above but are intentionally
    # not required to have buildable files/configs for canonical acceptance.
    for name in ("dealix-api", "dealix-apps-web"):
        svc = by_name[name]
        railway_config = str(svc.get("railwayConfig", ""))
        dockerfile = str(svc.get("dockerfilePath", ""))
        root_dir = str(svc.get("rootDirectory", ""))
        healthcheck = str(svc.get("healthcheckPath", ""))
        required_env = svc.get("requiredEnv")

        if not dockerfile:
            fail(f"{name}: missing dockerfilePath")
        if not railway_config:
            fail(f"{name}: missing railwayConfig")
        if healthcheck != "/healthz":
            fail(f"{name}: healthcheckPath must be /healthz")
        if not isinstance(required_env, list):
            fail(f"{name}: requiredEnv must be a list")

        read(railway_config)
        read(service_path(root_dir, dockerfile))


def verify_web_surface(*, next_config: str, dockerfile: str, healthz: str) -> None:
    content = read(next_config)
    if "output: 'standalone'" not in content and 'output: "standalone"' not in content:
        fail(f"{next_config} must enable standalone output")

    docker = read(dockerfile)
    if ".next/standalone" not in docker:
        fail(f"{dockerfile} must copy .next/standalone")
    for marker in FORBIDDEN_PUBLIC_SECRET_MARKERS:
        if marker in docker:
            fail(
                f"{dockerfile} must not expose secrets through public env marker {marker}"
            )

    health = read(healthz)
    if "status" not in health or "ok" not in health:
        fail(f"{healthz} must return a simple ok payload")


def verify_cutover_runbook() -> None:
    runbook = read("docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md")
    required_markers = [
        "dealix-apps-web",
        "apps/web",
        "Dealix-sa/dealix",
        "productionAuthority",
        "UNKNOWN_NOT_EVIDENCE_BACKED",
    ]
    for marker in required_markers:
        if marker not in runbook:
            fail(f"cutover runbook missing canonical marker: {marker}")

    forbidden_claims = [
        "Root directory | `frontend`",
        "Root Directory | `frontend`",
        "المالك الكنسي الحالي للواجهة العامة هو `frontend`",
    ]
    for marker in forbidden_claims:
        if marker in runbook:
            fail(f"cutover runbook reintroduced legacy frontend authority: {marker}")


def main() -> None:
    for path in REQUIRED_FILES:
        read(path)

    verify_service_matrix()
    verify_cutover_runbook()
    verify_railway_config("railway.json", allow_predeploy=True)
    verify_railway_config(CANONICAL_WEB_CONFIG, allow_predeploy=False)
    verify_web_surface(
        next_config="apps/web/next.config.js",
        dockerfile="apps/web/Dockerfile",
        healthz="apps/web/app/healthz/route.ts",
    )

    print("RAILWAY_SURFACES_OK")


if __name__ == "__main__":
    main()
