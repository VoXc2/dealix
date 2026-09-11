"""Railway production config-as-code checks (repo + optional live API)."""

from __future__ import annotations

import json
import re
import tomllib
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Literal

from dealix.commercial_ops.paths import REPO_ROOT

RAILWAY_TOML = REPO_ROOT / "railway.toml"
RAILWAY_JSON = REPO_ROOT / "railway.json"
DOCKERFILE = REPO_ROOT / "Dockerfile"
PREDEPLOY_SH = REPO_ROOT / "scripts" / "railway_predeploy.sh"
SETTINGS_DOC = REPO_ROOT / "docs" / "ops" / "RAILWAY_PRODUCTION_SETTINGS_AR.md"
DEFAULT_API_BASE = "https://api.dealix.me"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


CANONICAL_PREDEPLOY = "bash /app/scripts/railway_predeploy.sh"
CANONICAL_PREDEPLOY_MARKER = "/app/scripts/railway_predeploy.sh"
CANONICAL_PREDEPLOY_COMMAND = (
    "if [ -f /app/scripts/railway_predeploy.sh ]; then "
    "bash /app/scripts/railway_predeploy.sh; else echo "
    "'RAILWAY_PREDEPLOY: no predeploy script'; fi"
)
CANONICAL_START = "/app/start.sh"
CANONICAL_RESTART_MAX_RETRIES = 3
BAD_UI_PREDEPLOY_SNIPPETS = (
    "no migration needed",
    'echo "no migration needed"',
)


def _extract_predeploy_commands(text: str) -> tuple[str, ...] | None:
    """Parse a Railway config and return deploy.preDeployCommand structurally."""
    raw = (text or "").strip()
    if not raw:
        return None
    try:
        if raw.startswith("{"):
            config = json.loads(raw)
        else:
            config = tomllib.loads(raw)
    except (json.JSONDecodeError, tomllib.TOMLDecodeError):
        return None
    if not isinstance(config, dict):
        return None
    deploy = config.get("deploy")
    if not isinstance(deploy, dict):
        return None
    commands = deploy.get("preDeployCommand")
    if not isinstance(commands, list) or not commands:
        return None
    if not all(isinstance(command, str) for command in commands):
        return None
    normalized = tuple(command.strip() for command in commands)
    return normalized if all(normalized) else None


def _has_canonical_predeploy(text: str) -> bool:
    """Require one exact canonical Bash command in the documented array schema."""
    return _extract_predeploy_commands(text) == (CANONICAL_PREDEPLOY_COMMAND,)


def _evidence_value(value: str | None) -> str | None:
    text = (value or "").strip()
    return text or None


def classify_release_evidence(
    *,
    github_context_state: str | None,
    railway_deployment_status: str | None,
    expected_deployment_id: str | None = None,
    observed_deployment_id: str | None = None,
    expected_project_id: str | None = None,
    observed_project_id: str | None = None,
    expected_service_id: str | None = None,
    observed_service_id: str | None = None,
    expected_environment_id: str | None = None,
    observed_environment_id: str | None = None,
    expected_sha: str | None = None,
    deployed_sha: str | None = None,
    live_sha: str | None = None,
) -> dict[str, Any]:
    """Classify release evidence only when provider success is identity-bound."""
    github_state = (github_context_state or "").strip().lower() or None
    railway_status = (railway_deployment_status or "").strip().upper() or None
    provider_success = railway_status == "SUCCESS"

    identity_values = {
        "expected_deployment_id": _evidence_value(expected_deployment_id),
        "observed_deployment_id": _evidence_value(observed_deployment_id),
        "expected_project_id": _evidence_value(expected_project_id),
        "observed_project_id": _evidence_value(observed_project_id),
        "expected_service_id": _evidence_value(expected_service_id),
        "observed_service_id": _evidence_value(observed_service_id),
        "expected_environment_id": _evidence_value(expected_environment_id),
        "observed_environment_id": _evidence_value(observed_environment_id),
        "expected_sha": _evidence_value(expected_sha),
        "deployed_sha": _evidence_value(deployed_sha),
        "live_sha": _evidence_value(live_sha),
    }
    identity_complete = all(identity_values.values())
    identity_bound = bool(
        identity_complete
        and identity_values["expected_deployment_id"] == identity_values["observed_deployment_id"]
        and identity_values["expected_project_id"] == identity_values["observed_project_id"]
        and identity_values["expected_service_id"] == identity_values["observed_service_id"]
        and identity_values["expected_environment_id"] == identity_values["observed_environment_id"]
        and identity_values["expected_sha"] == identity_values["deployed_sha"]
        and identity_values["expected_sha"] == identity_values["live_sha"]
    )
    sha_values = (identity_values["expected_sha"], identity_values["deployed_sha"], identity_values["live_sha"])
    sha_format_valid = all(isinstance(v, str) and re.fullmatch(r"[0-9a-f]{40}", v) for v in sha_values)
    identity_bound = identity_bound and sha_format_valid
    release_valid = provider_success and identity_bound

    if provider_success and not identity_complete:
        reason = "RAILWAY_SUCCESS_IDENTITY_BINDING_INCOMPLETE"
    elif provider_success and not identity_bound:
        reason = "RAILWAY_SUCCESS_IDENTITY_MISMATCH"
    elif release_valid:
        reason = "RAILWAY_DEPLOYMENT_SUCCESS"
    elif railway_status == "SKIPPED":
        reason = "RAILWAY_DEPLOYMENT_SKIPPED_NOT_RELEASE_EVIDENCE"
    elif railway_status is None:
        reason = "RAILWAY_DEPLOYMENT_STATUS_MISSING"
    else:
        reason = f"RAILWAY_DEPLOYMENT_NOT_SUCCESS:{railway_status}"

    return {
        "github_context_state": github_state,
        "railway_deployment_status": railway_status,
        "github_context_is_release_authority": False,
        "provider_deployment_success": provider_success,
        "identity_binding_complete": identity_complete,
        "identity_binding_valid": identity_bound,
        "release_evidence_valid": release_valid,
        "reason": reason,
    }

def check_repo_railway_config() -> dict[str, Any]:
    """Validate railway.toml, Dockerfile CMD, and predeploy script."""
    issues: list[str] = []
    warnings: list[str] = []

    toml = _read(RAILWAY_TOML)
    if not toml.strip():
        issues.append("missing railway.toml")
    elif 'healthcheckPath = "/healthz"' not in toml:
        issues.append('railway.toml must set healthcheckPath = "/healthz"')
    if not _has_canonical_predeploy(toml):
        issues.append(
            "railway.toml preDeployCommand must be one canonical Bash command array"
        )
    if "startCommand" in toml and "NO startCommand" not in toml:
        warnings.append("railway.toml should not set startCommand (use Dockerfile CMD)")

    jsn = _read(RAILWAY_JSON)
    if jsn and "/healthz" not in jsn:
        issues.append("railway.json healthcheckPath should be /healthz")
    if jsn and not _has_canonical_predeploy(jsn):
        issues.append(
            "railway.json preDeployCommand must be one canonical Bash command array"
        )

    docker = _read(DOCKERFILE)
    if "/app/start.sh" not in docker:
        issues.append("Dockerfile must CMD /app/start.sh")
    if "healthz" not in docker and "/health" in docker:
        warnings.append("Dockerfile HEALTHCHECK should prefer /healthz")

    if not PREDEPLOY_SH.is_file():
        issues.append("missing scripts/railway_predeploy.sh")
    elif "RUN_RAILWAY_PRE_DEPLOY_MIGRATE" not in _read(PREDEPLOY_SH):
        warnings.append(
            "railway_predeploy.sh should gate migrations on "
            "RUN_RAILWAY_PRE_DEPLOY_MIGRATE"
        )

    for cfg_name, cfg_text in (("railway.toml", toml), ("railway.json", jsn)):
        if not cfg_text:
            continue
        if "railway_predeploy" not in cfg_text:
            issues.append(
                f"{cfg_name} must set preDeployCommand to railway_predeploy.sh"
            )
        lowered = cfg_text.lower()
        for bad in BAD_UI_PREDEPLOY_SNIPPETS:
            if bad in lowered:
                issues.append(
                    f"{cfg_name} must not use echo no-migration stub — "
                    f"use {CANONICAL_PREDEPLOY}"
                )
                break

    if not SETTINGS_DOC.is_file():
        issues.append("missing docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md")

    return {
        "issues": issues,
        "warnings": warnings,
        "ok": len(issues) == 0,
    }


def probe_get(
    api_base: str,
    path: str,
    *,
    timeout_sec: float = 12.0,
    max_bytes: int = 4096,
) -> dict[str, Any]:
    """GET {api_base}{path} — returns status without raising."""
    base = (api_base or "").strip().rstrip("/")
    if not base:
        return {"probed": False, "reason": "no_api_base"}
    url = f"{base}{path}"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            code = resp.getcode()
            body = resp.read(max_bytes).decode("utf-8", errors="replace")
            return {
                "probed": True,
                "url": url,
                "status": code,
                "ok": code == 200,
                "snippet": body[:200],
            }
    except urllib.error.HTTPError as exc:
        return {
            "probed": True,
            "url": url,
            "status": exc.code,
            "ok": False,
            "error": str(exc),
        }
    except Exception as exc:
        return {"probed": True, "url": url, "ok": False, "error": str(exc)}


def probe_healthz(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    """GET {api_base}/healthz — returns status without raising."""
    return probe_get(api_base, "/healthz", timeout_sec=timeout_sec)


def probe_trust_layer(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    """Probe GTM trust endpoints on production API."""
    paths = ("/healthz", "/version", "/api/v1/meta", "/health")
    probes = {
        p.strip("/").replace("/", "_") or "root": probe_get(
            api_base, p, timeout_sec=timeout_sec
        )
        for p in paths
    }
    healthz = probes.get("healthz") or {}
    snippet = (healthz.get("snippet") or "").lower()
    deploy_stale = healthz.get("ok") and "version" not in snippet
    version_missing = (probes.get("version") or {}).get("status") == 404
    meta_missing = (probes.get("api_v1_meta") or {}).get("status") == 404
    ok = all(p.get("ok") for p in probes.values() if p.get("probed"))
    return {
        "probes": probes,
        "deploy_stale_hint_ar": (
            "النشر الحي قديم — /healthz بلا version أو /version غير منشور. "
            "انتظر CI + Railway deploy."
            if deploy_stale or version_missing or meta_missing
            else ""
        ),
        "ok": ok and not deploy_stale and not version_missing,
    }


def analyze_railway_production(
    *, api_base: str | Literal[False] | None = None
) -> dict[str, Any]:
    repo = check_repo_railway_config()
    base = "" if api_base is False else (api_base or DEFAULT_API_BASE)
    live = probe_healthz(base) if base else {"probed": False}
    trust = probe_trust_layer(base) if base else {"probed": False}
    verdict = "PASS" if repo["ok"] else "FAIL"
    if repo["ok"] and live.get("probed") and not live.get("ok"):
        verdict = "WARN"
    if repo["ok"] and trust.get("deploy_stale_hint_ar"):
        verdict = "WARN"
    return {
        "repo": repo,
        "live_healthz": live,
        "live_trust_layer": trust,
        "canonical_start_command": CANONICAL_START,
        "canonical_predeploy": CANONICAL_PREDEPLOY,
        "canonical_restart_max_retries": CANONICAL_RESTART_MAX_RETRIES,
        "verdict": verdict,
        "settings_doc": str(SETTINGS_DOC.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def parse_railway_ui_predeploy_drift(predeploy: str) -> str | None:
    """Return Arabic hint if Railway UI pre-deploy drifts from repo authority."""
    cmd = (predeploy or "").strip()
    if not cmd:
        return None
    lower = cmd.lower()
    if cmd in (CANONICAL_PREDEPLOY, CANONICAL_PREDEPLOY_COMMAND):
        return None
    for bad in BAD_UI_PREDEPLOY_SNIPPETS:
        if bad in lower:
            return (
                f"استبدل Pre-deploy في Railway UI بـ {CANONICAL_PREDEPLOY} "
                "(أو اتركه فارغاً ليأخذ railway.toml). "
                "للترحيل التلقائي: RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1"
            )
    if "railway_predeploy" in lower:
        return f"Pre-deploy must invoke Bash exactly: {CANONICAL_PREDEPLOY}"
    return f"Pre-deploy يجب أن يطابق railway.toml: {CANONICAL_PREDEPLOY}"


def parse_railway_ui_drift_hint(start_command: str) -> str | None:
    """Return Arabic hint if UI start command likely breaks PORT expansion."""
    cmd = (start_command or "").strip()
    if not cmd:
        return None
    if cmd in ("/app/start.sh", "bash /app/start.sh", "sh /app/start.sh"):
        return None
    if re.match(r"^\./start\.sh$", cmd):
        return "امسح Start Command أو استبدل ./start.sh بـ /app/start.sh"
    if "uvicorn" in cmd and "$PORT" not in cmd and "${PORT" not in cmd:
        return "لا تضع uvicorn مباشرة في Start Command — استخدم /app/start.sh"
    return "امسح Start Command في Railway UI لاستخدام Dockerfile CMD"


def parse_railway_ui_restart_retries_drift(value: str | int | None) -> str | None:
    """Return Arabic hint when Railway UI restart retries drift from config-as-code."""
    raw = "" if value is None else str(value).strip()
    if not raw:
        return None
    try:
        retries = int(raw)
    except ValueError:
        return (
            "قيمة Max restart retries غير صالحة؛ "
            f"اضبطها على {CANONICAL_RESTART_MAX_RETRIES} لتطابق railway.toml"
        )
    if retries == CANONICAL_RESTART_MAX_RETRIES:
        return None
    return (
        f"اضبط Max restart retries في Railway UI من {retries} "
        f"إلى {CANONICAL_RESTART_MAX_RETRIES} لتطابق railway.toml"
    )
