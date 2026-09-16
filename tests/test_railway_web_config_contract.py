from __future__ import annotations

import json
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "dealix/config/railway_services.json"
WEB_CONFIG = ROOT / "apps/web/railway.toml"
ROOT_CONFIG = ROOT / "railway.toml"
NEXT_CONFIG = ROOT / "apps/web/next.config.js"
DOCKERFILE = ROOT / "apps/web/Dockerfile"


def _matrix_web() -> dict:
    payload = json.loads(MATRIX.read_text(encoding="utf-8"))
    matches = [
        service
        for service in payload["services"]
        if service.get("role") == "canonical_public_web"
        and service.get("productionAuthority") is True
    ]
    assert len(matches) == 1
    return matches[0]


def test_canonical_web_uses_dedicated_provider_config_file() -> None:
    web = _matrix_web()
    assert web["name"] == "dealix-apps-web"
    assert web["expectedSourceRepository"] == "Dealix-sa/dealix"
    assert web["rootDirectory"] == "apps/web"
    assert web["railwayConfig"] == "apps/web/railway.toml"
    assert web["providerConfigFile"] == "/apps/web/railway.toml"
    assert web["runsPredeploy"] is False


def test_apps_web_config_has_no_api_predeploy_command() -> None:
    config = tomllib.loads(WEB_CONFIG.read_text(encoding="utf-8"))
    assert config["build"]["builder"] == "DOCKERFILE"
    assert config["build"]["dockerfilePath"] == "Dockerfile"
    assert config["deploy"]["healthcheckPath"] == "/healthz"
    assert "preDeployCommand" not in config["deploy"]


def test_repo_root_config_is_not_the_canonical_web_config() -> None:
    root_config = tomllib.loads(ROOT_CONFIG.read_text(encoding="utf-8"))
    web_config = tomllib.loads(WEB_CONFIG.read_text(encoding="utf-8"))
    assert "preDeployCommand" not in root_config["deploy"]
    assert "preDeployCommand" not in web_config["deploy"]
    assert _matrix_web()["providerConfigFile"] != "/railway.toml"


def test_railway_app_root_build_keeps_next_standalone_entrypoint_at_root() -> None:
    next_config = NEXT_CONFIG.read_text(encoding="utf-8")
    dockerfile = DOCKERFILE.read_text(encoding="utf-8")

    # The repository intentionally has lockfiles at both repo root and apps/web.
    # Pin tracing to the Next application so direct VPS builds and Railway's
    # apps/web Docker context resolve the same standalone entrypoint contract.
    assert "output: \"standalone\"" in next_config
    assert "outputFileTracingRoot: __dirname" in next_config
    assert "path.join(__dirname, \"../../\")" not in next_config
    assert 'COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./' in dockerfile
    assert 'CMD ["node", "server.js"]' in dockerfile
