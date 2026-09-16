"""Self-host production source contract and public trust probes."""
from __future__ import annotations

import urllib.error
import urllib.request
from typing import Any, Literal

from dealix.commercial_ops.paths import REPO_ROOT

DEFAULT_API_BASE = "https://api.dealix.me"
PRODUCTION_PROBE_USER_AGENT = "Dealix-Production-Trust/1.0"
PRODUCTION_PROBE_ACCEPT = "application/json"

def production_probe_headers() -> dict[str, str]:
    return {"User-Agent": PRODUCTION_PROBE_USER_AGENT, "Accept": PRODUCTION_PROBE_ACCEPT}

def probe_get(api_base: str, path: str, *, timeout_sec: float = 12.0, max_bytes: int = 4096) -> dict[str, Any]:
    base = (api_base or "").strip().rstrip("/")
    if not base:
        return {"probed": False, "reason": "no_api_base"}
    url = f"{base}{path}"
    try:
        req = urllib.request.Request(url, method="GET", headers=production_probe_headers())
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            code = resp.getcode(); body = resp.read(max_bytes).decode("utf-8", errors="replace")
            return {"probed": True, "url": url, "status": code, "ok": code == 200, "snippet": body[:200]}
    except urllib.error.HTTPError as exc:
        return {"probed": True, "url": url, "status": exc.code, "ok": False, "error": str(exc)}
    except Exception as exc:
        return {"probed": True, "url": url, "ok": False, "error": str(exc)}

def probe_trust_layer(api_base: str, timeout_sec: float = 12.0) -> dict[str, Any]:
    paths = ("/healthz", "/version", "/api/v1/meta", "/health")
    probes = {x.strip("/").replace("/", "_") or "root": probe_get(api_base, x, timeout_sec=timeout_sec) for x in paths}
    healthz=probes.get("healthz") or {}; version=probes.get("version") or {}; meta=probes.get("api_v1_meta") or {}
    snippet=(healthz.get("snippet") or "").lower()
    identity = "version" in snippet or "git_sha" in snippet or bool(version.get("ok"))
    stale = bool(healthz.get("ok") and not identity)
    version_missing = version.get("status") == 404; meta_missing = meta.get("status") == 404
    ok = all(row.get("ok") for row in probes.values() if row.get("probed"))
    return {"probes": probes, "deploy_stale_hint_ar": ("هوية النشر الحي غير مثبتة على self-host — راجع /version و exact SHA parity." if stale or version_missing or meta_missing else ""), "ok": ok and not stale and not version_missing and not meta_missing}

def check_repo_selfhost_config() -> dict[str, Any]:
    required = [REPO_ROOT/'deploy/selfhost/compose.yml', REPO_ROOT/'ops/caddy/Caddyfile', REPO_ROOT/'dealix/config/production_release_authority.json', REPO_ROOT/'scripts/ops/selfhost_release.sh']
    missing=[str(x.relative_to(REPO_ROOT)) for x in required if not x.is_file()]
    forbidden=[x for x in ('railway.json','railway.toml','vercel.json') if (REPO_ROOT/x).exists()]
    compose=(REPO_ROOT/'deploy/selfhost/compose.yml').read_text(encoding='utf-8') if (REPO_ROOT/'deploy/selfhost/compose.yml').is_file() else ''
    tokens=('public-cutover','production-db','dealix-api:${DEALIX_IMAGE_TAG','dealix-web:${DEALIX_IMAGE_TAG')
    absent=[x for x in tokens if x not in compose]
    issues=[f"missing {x}" for x in missing]+[f"forbidden active provider config {x}" for x in forbidden]+[f"compose missing {x}" for x in absent]
    return {"ok": not issues, "issues": issues, "missing": missing, "forbidden": forbidden}

def analyze_selfhost_production(*, api_base: str | Literal[False] | None = None) -> dict[str, Any]:
    repo=check_repo_selfhost_config(); base='' if api_base is False else (api_base or DEFAULT_API_BASE)
    trust=probe_trust_layer(base) if base else {"probed": False}
    verdict='PASS' if repo['ok'] else 'FAIL'
    if repo['ok'] and trust.get('deploy_stale_hint_ar'): verdict='WARN'
    return {"repo": repo, "live_trust_layer": trust, "verdict": verdict, "release_mode": "manual_exact_sha", "runtime_authority": "selfhost_exact_git_sha"}
