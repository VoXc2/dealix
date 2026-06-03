"""Railway production config-as-code checks (repo + optional live API)."""

from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from dealix.commercial_ops.paths import REPO_ROOT

RAILWAY_TOML = REPO_ROOT / "railway.toml"
RAILWAY_JSON = REPO_ROOT / "railway.json"
DOCKERFILE = REPO_ROOT / "Dockerfile"
PREDEPLOY_SH = REPO_ROOT / "scripts" / "railway_predeploy.sh"
SETTINGS_DOC = REPO_ROOT / "docs" / "ops" / "RAILWAY_PRODUCTION_SETTINGS_AR.md"
DEFAULT_API_BASE = "https://api.dealix.me"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


CANONICAL_PREDEPLOY = "sh /app/scripts/railway_predeploy.sh"
CANONICAL_PREDEPLOY_MARKER = "/app/scripts/railway_predeploy.sh"
CANONICAL_START = "/app/start.sh"
BAD_UI_PREDEPLOY_SNIPPETS = (
    "no migration needed",
    'echo "no migration needed"',
)


def _has_canonical_predeploy(text: str) -> bool:
    return CANONICAL_PREDEPLOY_MARKER in text and "railway_predeploy" in text


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
        issues.append(f"railway.toml preDeployCommand must invoke {CANONICAL_PREDEPLOY_MARKER}")
    if "startCommand" in toml and "NO startCommand" not in toml:
        warnings.append("railway.toml should not set startCommand (use Dockerfile CMD)")

    jsn = _read(RAILWAY_JSON)
    if jsn and "/healthz" not in jsn:
        issues.append("railway.json healthcheckPath should be /healthz")
    if jsn and not _has_canonical_predeploy(jsn):
        issues.append(f"railway.json preDeployCommand must invoke {CANONICAL_PREDEPLOY_MARKER}")

    docker = _read(DOCKERFILE)
    if "/app/start.sh" not in docker:
        issues.append("Dockerfile must CMD /app/start.sh")
    if 'healthz' not in docker and '/health' in docker:
        warnings.append("Dockerfile HEALTHCHECK should prefer /healthz")

    if not PREDEPLOY_SH.is_file():
        issues.append("missing scripts/railway_predeploy.sh")
    elif "RUN_RAILWAY_PRE_DEPLOY_MIGRATE" not in _read(PREDEPLOY_SH):
        warnings.append("railway_predeploy.sh should gate migrations on RUN_RAILWAY_PRE_DEPLOY_MIGRATE")

    for cfg_name, cfg_text in (("railway.toml", toml), ("railway.json", jsn)):
        if not cfg_text:
            continue
        if "railway_predeploy" not in cfg_text:
            issues.append(f"{cfg_name} must set preDeployCommand to railway_predeploy.sh")
        lowered = cfg_text.lower()
        for bad in BAD_UI_PREDEPLOY_SNIPPETS:
            if bad in lowered:
                issues.append(
                    f"{cfg_name} must not use echo no-migration stub — use {CANONICAL_PREDEPLOY}"
                )
                break

    if not SETTINGS_DOC.is_file():
        issues.append("missing docs/ops/RAILWAY_PRODUCTION_SETTINGS_AR.md")

    return {
        "issues": issues,
        "warnings": warnings,
        "ok": len(issues) == 0,
    }


def probe_get(api_base: str, path: str, *, timeout_sec: float = 12.0, max_bytes: int = 4096) -> dict[str, Any]:
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
        return {"probed": True, "url": url, "status": exc.code, "ok": False, "error": str(exc)}
    except Exception as exc:
        return {"probed": True, "url": url, "ok": False, "error": str(exc)}


def probe_healthz(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    """GET {api_base}/healthz — returns status without raising."""
    return probe_get(api_base, "/healthz", timeout_sec=timeout_sec)


def probe_trust_layer(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    """Probe GTM trust endpoints on production API."""
    paths = ("/healthz", "/version", "/api/v1/meta", "/health")
    probes = {p.strip("/").replace("/", "_") or "root": probe_get(api_base, p, timeout_sec=timeout_sec) for p in paths}
    healthz = probes.get("healthz") or {}
    snippet = (healthz.get("snippet") or "").lower()
    deploy_stale = healthz.get("ok") and "version" not in snippet
    version_missing = (probes.get("version") or {}).get("status") == 404
    meta_missing = (probes.get("api_v1_meta") or {}).get("status") == 404
    ok = all(p.get("ok") for p in probes.values() if p.get("probed"))
    return {
        "probes": probes,
        "deploy_stale_hint_ar": (
            "النشر الحي قديم — /healthz بلا version أو /version غير منشور. انتظر CI + Railway deploy."
            if deploy_stale or version_missing or meta_missing
            else ""
        ),
        "ok": ok and not deploy_stale and not version_missing,
    }


def analyze_railway_production(*, api_base: str | None = None) -> dict[str, Any]:
    repo = check_repo_railway_config()
    base = (api_base or DEFAULT_API_BASE) if api_base is not False else ""
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
        "verdict": verdict,
        "settings_doc": str(SETTINGS_DOC.relative_to(REPO_ROOT)).replace("\\", "/"),
    }


def parse_railway_ui_predeploy_drift(predeploy: str) -> str | None:
    """Return Arabic hint if Railway UI pre-deploy drifts from railway.toml."""
    cmd = (predeploy or "").strip()
    if not cmd:
        return None
    lower = cmd.lower()
    if CANONICAL_PREDEPLOY in cmd or cmd == CANONICAL_PREDEPLOY:
        return None
    for bad in BAD_UI_PREDEPLOY_SNIPPETS:
        if bad in lower:
            return (
                f"استبدل Pre-deploy في Railway UI بـ {CANONICAL_PREDEPLOY} "
                "(أو اتركه فارغاً ليأخذ railway.toml). "
                "للترحيل التلقائي: RUN_RAILWAY_PRE_DEPLOY_MIGRATE=1"
            )
    if "railway_predeploy" in lower and "/app/scripts" not in lower:
        return f"استخدم مسار الحاوية: {CANONICAL_PREDEPLOY}"
    if "railway_predeploy" in lower:
        return None
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
