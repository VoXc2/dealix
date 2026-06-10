#!/usr/bin/env python3
"""Post-redeploy verification — API trust layer, webhooks, frontend, layers."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.production_layers import (  # noqa: E402
    build_production_layers,
    format_layers_report,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def probe(url: str, *, method: str = "GET", timeout: float = 12.0) -> dict[str, object]:
    try:
        req = urllib.request.Request(url, method=method)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(8192).decode("utf-8", errors="replace")
            return {"ok": resp.getcode() == 200, "status": resp.getcode(), "body": body[:500]}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "body": ""}
    except Exception as exc:
        return {"ok": False, "status": None, "error": str(exc)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--frontend-base", default=os.getenv("DEALIX_FRONTEND_BASE", "https://dealix.me"))
    p.add_argument("--admin-key", default=os.getenv("DEALIX_ADMIN_API_KEY", ""))
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    api = args.api_base.rstrip("/")
    fe = args.frontend_base.rstrip("/")
    failures: list[str] = []

    checks: dict[str, object] = {}

    for path in ("/healthz", "/health", "/version", "/api/v1/meta", "/openapi.json"):
        row = probe(f"{api}{path}")
        checks[path] = row
        if path in ("/healthz", "/health", "/version", "/api/v1/meta") and not row.get("ok"):
            failures.append(f"{path} -> {row.get('status', row.get('error'))}")

    hz = checks.get("/healthz") or {}
    if hz.get("ok") and "version" not in str(hz.get("body", "")).lower():
        failures.append("/healthz missing version in body (stale deploy)")

    for path in ("/api/v1/webhooks/moyasar", "/api/v1/webhooks/calendly", "/api/v1/webhooks/hubspot"):
        row = probe(f"{api}{path}", method="GET")
        # GET may return 405/422 when route is mounted — only 404 means missing
        if row.get("status") in (405, 422):
            row = {**row, "ok": True, "route_mounted": True}
        checks[path] = row
        if row.get("status") == 404:
            failures.append(f"{path} not mounted")

    ar = probe(f"{fe}/ar", method="HEAD")
    checks["/ar"] = ar
    if not ar.get("ok"):
        failures.append(f"{fe}/ar -> {ar.get('status', ar.get('error'))}")

    layers = build_production_layers(api_base=api, frontend_base=fe, check_env=False)

    founder_layers: dict[str, object] | None = None
    if args.admin_key:
        try:
            req = urllib.request.Request(
                f"{api}/api/v1/founder/production-layers",
                headers={"X-Admin-API-Key": args.admin_key},
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                founder_layers = json.loads(resp.read().decode("utf-8"))
                routes = founder_layers.get("trust_routes_registered") or {}
                if not routes.get("version"):
                    failures.append("running container missing /version route")
        except Exception as exc:
            checks["founder_production_layers"] = {"ok": False, "error": str(exc)}
    else:
        checks["founder_production_layers"] = {"skipped": True, "reason": "no DEALIX_ADMIN_API_KEY"}

    verdict = "PASS" if not failures else "FAIL"
    out = {
        "verdict": verdict,
        "api_base": api,
        "frontend_base": fe,
        "checks": checks,
        "layers": layers,
        "founder_production_layers": founder_layers,
        "failures": failures,
    }

    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("== post_redeploy_verify_dealix ==")
        for path, row in checks.items():
            if isinstance(row, dict) and "status" in row:
                print(f"  {path}: {row.get('status')} {'OK' if row.get('ok') else 'FAIL'}")
        print()
        print(format_layers_report(layers))
        if failures:
            print("\nFailures:")
            for f in failures:
                print(f"  - {f}")

    print(f"\nDEALIX_POST_REDEPLOY_VERDICT={verdict}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
