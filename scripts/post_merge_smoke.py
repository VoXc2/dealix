#!/usr/bin/env python3
"""Post-Merge Smoke — Wave 19+ Operational Closure.

After PR #235 merges and Railway auto-deploys, the founder runs ONE
command to verify every public surface responds correctly. JSON output;
exit 0 = all green, exit 1 = at least one endpoint failed.

Replaces curl-by-hand for the 8 public + 4 admin-gated endpoints.

Usage:
    python scripts/post_merge_smoke.py https://api.dealix.me
    python scripts/post_merge_smoke.py https://api.dealix.me --admin $ADMIN_KEY
    python scripts/post_merge_smoke.py --local           # in-process via TestClient
    python scripts/post_merge_smoke.py --json https://api.dealix.me

NEVER POSTs. NEVER charges. NEVER sends. Read-only.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


# ── Endpoints to smoke ───────────────────────────────────────────────

# (path, expected_status, public, shape_assertion_fn_name)
PUBLIC_ENDPOINTS: tuple[tuple[str, int, str], ...] = (
    ("/healthz", 200, "health"),
    ("/api/v1/dealix-promise", 200, "promise"),
    ("/api/v1/dealix-promise/markdown", 200, "markdown"),
    ("/api/v1/doctrine", 200, "doctrine"),
    ("/api/v1/doctrine/controls", 200, "doctrine_controls"),
    ("/api/v1/doctrine/markdown", 200, "markdown"),
    ("/api/v1/commercial-map", 200, "commercial_map"),
    ("/api/v1/commercial-map/markdown", 200, "markdown"),
    ("/api/v1/gcc-markets", 200, "gcc_markets"),
    ("/api/v1/gcc-markets/markdown", 200, "markdown"),
    ("/api/v1/capital-assets/public", 200, "public_assets"),
    ("/api/v1/capital-assets/public/markdown", 200, "markdown"),
    ("/api/v1/founder/launch-status/public", 200, "launch_status"),
    ("/api/v1/founder/command-center/public", 200, "command_center_public"),
)

ADMIN_ENDPOINTS: tuple[tuple[str, int], ...] = (
    ("/api/v1/founder/command-center", 200),
    ("/api/v1/founder/post-deploy-check", 200),
    ("/api/v1/founder/launch-status", 200),
    ("/api/v1/capital-assets", 200),
)


def _shape_check(name: str, body: Any) -> str | None:
    """Return error message if shape doesn't match expectation, else None."""
    if name == "health":
        if not isinstance(body, dict) or body.get("status") != "ok":
            return f"expected {{'status':'ok',...}}, got {body!r}"
        return None
    if name == "promise":
        if body.get("commitments_count") != 11:
            return f"commitments_count != 11 (got {body.get('commitments_count')})"
        return None
    if name == "doctrine":
        if body.get("non_negotiables_count") != 11:
            return f"non_negotiables_count != 11"
        if not body.get("public_framework"):
            return "public_framework not True"
        return None
    if name == "doctrine_controls":
        if body.get("controls_count") != 11:
            return f"controls_count != 11"
        return None
    if name == "commercial_map":
        if body.get("registry_count") != 3:
            return f"registry_count != 3 (got {body.get('registry_count')})"
        return None
    if name == "gcc_markets":
        if body.get("market_count") != 4:
            return f"market_count != 4 (got {body.get('market_count')})"
        if body.get("active_count") != 1:
            return f"active_count != 1 (Saudi-only beachhead)"
        return None
    if name == "public_assets":
        if not isinstance(body.get("assets"), list):
            return "assets is not a list"
        # public-safe view MUST NOT leak file_paths or commercial_use
        for a in body["assets"]:
            if "file_paths" in a:
                return f"asset {a.get('asset_id')} leaks file_paths in public view"
            if "commercial_use" in a:
                return f"asset {a.get('asset_id')} leaks commercial_use in public view"
        return None
    if name == "launch_status":
        if "governance_decision" not in body:
            return "missing governance_decision"
        return None
    if name == "command_center_public":
        # Public view MUST NOT include commercial-sensitive aggregates
        if "arr_pacing" in body:
            return "public view leaks arr_pacing"
        if "anchor_partners" in body:
            return "public view leaks anchor_partners"
        return None
    if name == "markdown":
        if not isinstance(body, str):
            return "markdown response is not str"
        if "النتائج التقديرية" not in body:
            return "missing bilingual disclaimer"
        return None
    return None


# ── HTTP clients ─────────────────────────────────────────────────────


def _make_local_client():
    from fastapi.testclient import TestClient
    from api.main import app
    return TestClient(app)


def _hit(client_kind: str, base_url: str | None, path: str,
         headers: dict[str, str] | None = None,
         test_client=None) -> tuple[int, Any, float]:
    """Returns (status_code, body, duration_seconds)."""
    started = time.monotonic()
    if client_kind == "local":
        resp = test_client.get(path, headers=headers or {})
        status = resp.status_code
        try:
            body = resp.json()
        except Exception:
            body = resp.text
    else:
        # Use urllib (stdlib) — avoids forcing a 'requests' install on prod.
        from urllib import request, error
        full = (base_url or "").rstrip("/") + path
        req = request.Request(full, headers=headers or {})
        try:
            with request.urlopen(req, timeout=30) as r:
                status = r.status
                raw = r.read()
                try:
                    body = json.loads(raw)
                except Exception:
                    body = raw.decode("utf-8", errors="ignore")
        except error.HTTPError as e:
            status = e.code
            try:
                body = json.loads(e.read())
            except Exception:
                body = str(e)
        except Exception as e:
            status = -1
            body = f"ERROR: {type(e).__name__}: {e}"
    duration = time.monotonic() - started
    return status, body, duration


# ── Aggregator ───────────────────────────────────────────────────────


def smoke(base_url: str | None, admin_key: str | None, local: bool) -> dict[str, Any]:
    client_kind = "local" if local else "http"
    test_client = _make_local_client() if local else None

    results: list[dict[str, Any]] = []

    # Public endpoints
    for path, expected, shape_name in PUBLIC_ENDPOINTS:
        status, body, dur = _hit(client_kind, base_url, path, test_client=test_client)
        ok = status == expected
        shape_err = _shape_check(shape_name, body) if ok else None
        if shape_err:
            ok = False
        results.append({
            "path": path,
            "type": "public",
            "expected_status": expected,
            "got_status": status,
            "duration_ms": round(dur * 1000, 1),
            "ok": ok,
            "shape_error": shape_err,
        })

    # Admin endpoints (only if key provided OR local mode)
    if admin_key or local:
        if local:
            import os
            # In local mode, accept an existing ADMIN_API_KEYS env var
            # (tests set it explicitly) and fall back to a deterministic
            # test value otherwise. The header MUST match whatever the
            # env actually contains so require_admin_key accepts it.
            existing = os.environ.get("ADMIN_API_KEYS", "").strip()
            if existing:
                # Use the first key from the comma-separated env var
                key_value = existing.split(",")[0].strip()
            else:
                key_value = "test_post_merge_smoke_local"
                os.environ["ADMIN_API_KEYS"] = key_value
            headers = {"X-Admin-API-Key": key_value}
        else:
            headers = {"X-Admin-API-Key": admin_key or ""}
        for path, expected in ADMIN_ENDPOINTS:
            status, body, dur = _hit(client_kind, base_url, path, headers=headers, test_client=test_client)
            ok = status == expected
            results.append({
                "path": path,
                "type": "admin",
                "expected_status": expected,
                "got_status": status,
                "duration_ms": round(dur * 1000, 1),
                "ok": ok,
                "shape_error": None,
            })

    passed = sum(1 for r in results if r["ok"])
    failed = len(results) - passed
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": base_url if not local else "(local TestClient)",
        "client_kind": client_kind,
        "summary": {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "all_green": failed == 0,
        },
        "results": results,
        "is_estimate": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", nargs="?", help="https://api.dealix.me (omit for --local)")
    parser.add_argument("--local", action="store_true",
                        help="Use in-process TestClient instead of HTTP")
    parser.add_argument("--admin", default=None,
                        help="Admin API key (X-Admin-API-Key) to hit admin endpoints")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.local and not args.base_url:
        parser.error("either --local or a base_url argument is required")

    # In --json mode the only thing on stdout should be the JSON payload.
    # The FastAPI/structlog request logs are routed to stdout by default,
    # so we redirect them to /dev/null during the smoke run.
    if args.json:
        import contextlib
        import io
        import logging
        logging.disable(logging.CRITICAL)
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured), contextlib.redirect_stderr(captured):
            report = smoke(
                base_url=args.base_url,
                admin_key=args.admin,
                local=args.local,
            )
    else:
        report = smoke(
            base_url=args.base_url,
            admin_key=args.admin,
            local=args.local,
        )

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"━━ Post-Merge Smoke · {report['base_url']} ━━")
        print()
        for r in report["results"]:
            mark = "✅" if r["ok"] else "❌"
            print(f"  {mark} [{r['type']:5}] {r['got_status']} {r['path']}  ({r['duration_ms']} ms)")
            if r.get("shape_error"):
                print(f"       shape error: {r['shape_error']}")
        s = report["summary"]
        print()
        print(f"Total: {s['total']}  ·  Passed: {s['passed']}  ·  Failed: {s['failed']}")
        if s["all_green"]:
            print("✅ All public surfaces healthy. Production is live.")
        else:
            print("❌ At least one surface failed. Check docs/ops/POST_MERGE_SMOKE.md.")

    return 0 if report["summary"]["all_green"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
