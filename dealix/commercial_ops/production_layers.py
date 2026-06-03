"""Production layer map — live probes + env matrix (no secrets printed)."""

from __future__ import annotations

import json
import os
import socket
import urllib.error
import urllib.request
from typing import Any

from dealix.commercial_ops.railway_launch import (
    check_railway_api_env,
    check_railway_frontend_env,
)
from dealix.commercial_ops.railway_production import (
    DEFAULT_API_BASE,
    analyze_railway_production,
    probe_get,
    probe_trust_layer,
)

DEFAULT_FRONTEND_BASE = "https://dealix.me"
GITHUB_PAGES_SERVER = "github.com"


def _set(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def _integration_env() -> dict[str, bool]:
    keys = (
        "MOYASAR_SECRET_KEY",
        "MOYASAR_WEBHOOK_SECRET",
        "HUBSPOT_ACCESS_TOKEN",
        "CALENDLY_WEBHOOK_SECRET",
        "CALENDLY_WEBHOOK_SIGNING_KEY",
        "CALENDLY_URL",
        "POSTHOG_API_KEY",
    )
    return {k: _set(k) for k in keys}


def _calendly_ok(env: dict[str, bool]) -> bool:
    return env["CALENDLY_WEBHOOK_SECRET"] or env["CALENDLY_WEBHOOK_SIGNING_KEY"]


def _probe_head(url: str, *, timeout_sec: float = 12.0) -> dict[str, Any]:
    try:
        req = urllib.request.Request(url, method="HEAD")
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            headers = {k.lower(): v for k, v in resp.headers.items()}
            return {
                "probed": True,
                "url": url,
                "status": resp.getcode(),
                "ok": resp.getcode() == 200,
                "server": headers.get("server", ""),
                "location": headers.get("location", ""),
            }
    except urllib.error.HTTPError as exc:
        headers = {k.lower(): v for k, v in (exc.headers.items() if exc.headers else [])}
        return {
            "probed": True,
            "url": url,
            "status": exc.code,
            "ok": False,
            "server": headers.get("server", ""),
            "location": headers.get("location", ""),
        }
    except Exception as exc:
        return {"probed": True, "url": url, "ok": False, "error": str(exc)}


def _dns_resolves(host: str) -> bool:
    try:
        socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        return True
    except OSError:
        return False


def _pct(score: float) -> int:
    return max(0, min(100, int(round(score * 100))))


def layer_0_dns_healthz(api_base: str) -> dict[str, Any]:
    host = api_base.replace("https://", "").replace("http://", "").split("/")[0]
    healthz = probe_get(api_base, "/healthz")
    health = probe_get(api_base, "/health")
    snippet = (healthz.get("snippet") or "").lower()
    healthz_rich = "version" in snippet or "git_sha" in snippet
    checks = [
        _dns_resolves(host),
        healthz.get("ok"),
        health.get("ok"),
        healthz_rich or (health.get("ok") and "version" in (health.get("snippet") or "").lower()),
    ]
    score = sum(1 for c in checks if c) / len(checks)
    return {
        "id": 0,
        "name": "DNS + healthz",
        "pct": _pct(score),
        "dns_ok": checks[0],
        "healthz": healthz,
        "health": health,
        "healthz_has_version": healthz_rich,
        "blocker_ar": (
            ""
            if score >= 0.75
            else "تحقق DNS لـ api.dealix.me ونشر API الأحدث (healthz يجب أن يعيد version)"
        ),
    }


def layer_1_railway_p0(*, check_env: bool) -> dict[str, Any]:
    repo = analyze_railway_production(api_base=False)
    api_env = check_railway_api_env() if check_env else {"ready_for_api_deploy": None}
    ready_repo = repo["repo"]["ok"]
    ready_env = api_env.get("ready_for_api_deploy") if check_env else True
    if check_env and ready_env is False:
        ready_env = False
    elif not check_env:
        ready_env = True
    score = (0.5 if ready_repo else 0.0) + (0.5 if ready_env else 0.0)
    missing = api_env.get("missing_required") or [] if check_env else []
    return {
        "id": 1,
        "name": "Railway P0 secrets",
        "pct": _pct(score),
        "repo_ok": ready_repo,
        "api_env_ready": ready_env,
        "missing_required": missing,
        "blocker_ar": (
            ""
            if score >= 1.0
            else (
                f"أكمل متغيرات API: {', '.join(missing)}"
                if missing
                else "أصلح railway.toml / Dockerfile في المستودع"
            )
        ),
    }


def layer_2_webhooks(*, check_env: bool) -> dict[str, Any]:
    env = _integration_env()
    moyasar = env["MOYASAR_WEBHOOK_SECRET"]
    hubspot = env["HUBSPOT_ACCESS_TOKEN"]
    calendly = _calendly_ok(env)
    live_moyasar = probe_get(DEFAULT_API_BASE, "/api/v1/webhooks/moyasar", timeout_sec=8.0)
    # POST without body may 405/422 — route exists if not 404
    route_exists = live_moyasar.get("status") not in (404, None)
    if check_env:
        score = (moyasar + hubspot + calendly + route_exists) / 4.0
    else:
        score = (route_exists + (1 if moyasar else 0) + (1 if hubspot else 0) + (1 if calendly else 0)) / 4.0
    return {
        "id": 2,
        "name": "Webhooks",
        "pct": _pct(score),
        "moyasar_secret": moyasar if check_env else None,
        "hubspot": hubspot if check_env else None,
        "calendly": calendly if check_env else None,
        "webhook_routes_live": route_exists,
        "blocker_ar": (
            ""
            if score >= 0.75
            else "MOYASAR_WEBHOOK_SECRET + Calendly signing key + HubSpot على Railway API"
        ),
    }


def layer_3_paid_launch(*, check_env: bool) -> dict[str, Any]:
    env = _integration_env()
    posthog = env["POSTHOG_API_KEY"]
    moyasar_pay = env["MOYASAR_SECRET_KEY"]
    trust = probe_trust_layer(DEFAULT_API_BASE)
    meta_ok = (trust.get("probes") or {}).get("api_v1_meta", {}).get("ok")
    if check_env:
        score = (posthog + moyasar_pay + bool(meta_ok)) / 3.0
    else:
        score = (bool(meta_ok) + (1 if posthog else 0) + (1 if moyasar_pay else 0)) / 3.0
    return {
        "id": 3,
        "name": "Paid launch",
        "pct": _pct(score),
        "posthog": posthog if check_env else None,
        "moyasar_key": moyasar_pay if check_env else None,
        "meta_live": meta_ok,
        "blocker_ar": (
            ""
            if score >= 0.66
            else "POSTHOG_API_KEY + MOYASAR_SECRET_KEY + نشر /api/v1/meta"
        ),
    }


def layer_4_frontend(frontend_base: str, *, check_env: bool) -> dict[str, Any]:
    fe_env = check_railway_frontend_env() if check_env else {"ready_for_fe_deploy": None}
    ar = _probe_head(f"{frontend_base.rstrip('/')}/ar")
    root = _probe_head(frontend_base.rstrip("/") or frontend_base)
    server = (ar.get("server") or root.get("server") or "").lower()
    on_github_pages = GITHUB_PAGES_SERVER in server
    ar_ok = ar.get("ok") is True
    if check_env:
        env_ok = fe_env.get("ready_for_fe_deploy") is True
        score = (
            (1.0 if ar_ok and not on_github_pages else 0.0) * 0.6
            + (0.4 if env_ok else 0.0)
        )
    else:
        score = 1.0 if ar_ok and not on_github_pages else (0.3 if ar_ok else 0.0)
    return {
        "id": 4,
        "name": "Frontend /ar",
        "pct": _pct(score),
        "ar": ar,
        "root": root,
        "github_pages": on_github_pages,
        "fe_env_ready": fe_env.get("ready_for_fe_deploy") if check_env else None,
        "missing_fe": fe_env.get("missing") or [] if check_env else [],
        "blocker_ar": (
            ""
            if ar_ok and not on_github_pages
            else (
                "dealix.me يشير إلى GitHub Pages — انقل DNS إلى Railway Frontend "
                "(docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md)"
                if on_github_pages
                else "Frontend vars + Redeploy — هدف dealix.me/ar = 200"
            )
        ),
    }


def layer_5_revenue() -> dict[str, Any]:
    try:
        from scripts.verify_first_paid_diagnostic_tracker import analyze

        pipe = analyze()
        paid = int(pipe.get("payment_received_real") or 0)
        proof = int(pipe.get("proof_pack_delivered_real") or 0)
        closed = bool(pipe.get("first_close_ready"))
        score = 1.0 if closed else (0.5 if paid or proof else 0.0)
        return {
            "id": 5,
            "name": "First revenue",
            "pct": _pct(score),
            "paid": paid,
            "proof": proof,
            "pipeline_open": not closed,
            "blocker_ar": "" if closed else "Phase 0–1: أول دفعة + Proof Pack (بعد Layer 0–4)",
        }
    except Exception as exc:
        return {
            "id": 5,
            "name": "First revenue",
            "pct": 0,
            "error": str(exc),
            "blocker_ar": "شغّل تتبع الإيراد بعد إغلاق Layer 4",
        }


def build_production_layers(
    *,
    api_base: str = DEFAULT_API_BASE,
    frontend_base: str = DEFAULT_FRONTEND_BASE,
    check_env: bool = False,
) -> dict[str, Any]:
    """Full layer map for founder go-live."""
    layers = [
        layer_0_dns_healthz(api_base),
        layer_1_railway_p0(check_env=check_env),
        layer_2_webhooks(check_env=check_env),
        layer_3_paid_launch(check_env=check_env),
        layer_4_frontend(frontend_base, check_env=check_env),
        layer_5_revenue(),
    ]
    trust = probe_trust_layer(api_base)
    avg_pct = sum(layer["pct"] for layer in layers) / len(layers)
    blockers = [layer["blocker_ar"] for layer in layers if layer.get("blocker_ar")]
    critical = [layer for layer in layers[:5] if layer["pct"] < 70]
    verdict = "PASS" if not critical and trust.get("ok") else ("WARN" if avg_pct >= 60 else "FAIL")
    return {
        "verdict": verdict,
        "overall_pct": int(round(avg_pct)),
        "api_base": api_base,
        "frontend_base": frontend_base,
        "trust_layer": trust,
        "layers": layers,
        "blockers_ar": blockers,
        "founder_next_ar": blockers[:3],
    }


def format_layers_report(blob: dict[str, Any]) -> str:
    lines = [
        "== Dealix production layers ==",
        f"  verdict: {blob['verdict']}",
        f"  overall: {blob['overall_pct']}%",
        f"  api: {blob['api_base']}",
        f"  web: {blob['frontend_base']}",
        "",
    ]
    for layer in blob["layers"]:
        bar = "█" * (layer["pct"] // 10) + "░" * (10 - layer["pct"] // 10)
        lines.append(f"Layer {layer['id']} {layer['name']}: {bar} {layer['pct']}%")
        if layer.get("blocker_ar"):
            lines.append(f"  → {layer['blocker_ar']}")
    trust = blob.get("trust_layer") or {}
    for path, row in (trust.get("probes") or {}).items():
        if row.get("probed"):
            lines.append(f"  probe {path}: {row.get('status', row.get('error'))}")
    return "\n".join(lines)


def write_layers_cache(blob: dict[str, Any], path: str | None = None) -> str:
    from dealix.commercial_ops.paths import REPO_ROOT

    out = REPO_ROOT / (path or "dealix/transformation/production_layers_cache.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(blob, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(out.relative_to(REPO_ROOT)).replace("\\", "/")
