#!/usr/bin/env python3
"""Verify GTM public surfaces registry + API trust endpoints (repo + optional live)."""

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

from dealix.commercial_ops.gtm_public_surfaces import (  # noqa: E402
    build_gtm_public_surfaces_snapshot,
    verify_gtm_public_surfaces_repo,
)


def _probe_json(url: str, timeout: float = 12.0) -> dict[str, object]:
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read(4096).decode("utf-8", errors="replace")
            return {"ok": resp.getcode() == 200, "status": resp.getcode(), "url": url, "body": body[:200]}
    except urllib.error.HTTPError as exc:
        return {"ok": False, "status": exc.code, "url": url, "error": str(exc)}
    except Exception as exc:
        return {"ok": False, "url": url, "error": str(exc)}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    repo = verify_gtm_public_surfaces_repo()
    snap = build_gtm_public_surfaces_snapshot()
    live: dict[str, object] = {"probed": False}
    verdict = "PASS" if repo["ok"] else "FAIL"

    if not args.skip_live and args.api_base:
        base = args.api_base.rstrip("/")
        hz = _probe_json(f"{base}/healthz")
        ver = _probe_json(f"{base}/version")
        meta = _probe_json(f"{base}/api/v1/meta")
        live = {"probed": True, "healthz": hz, "version": ver, "meta": meta}
        if repo["ok"] and not all(x.get("ok") for x in (hz, ver, meta)):
            verdict = "WARN"

    blob = {"verdict": verdict, "repo": repo, "snapshot": snap, "live": live}
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== verify_gtm_public_surfaces ==")
        for issue in repo.get("issues", []):
            print(f"  FAIL: {issue}")
        if repo.get("ok"):
            print(f"  ok: {len(snap.get('frontend_public_routes', []))} public frontend routes")
        if live.get("probed"):
            for key in ("healthz", "version", "meta"):
                row = live.get(key) or {}
                print(f"  live {key}: {row.get('url')} -> {row.get('status', row.get('error'))}")

    print(f"DEALIX_GTM_PUBLIC_SURFACES_VERDICT={verdict}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
