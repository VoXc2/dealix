#!/usr/bin/env python3
"""Read-only public exact-SHA release identity check for Dealix self-host authority."""
from __future__ import annotations
import argparse, json, re, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
HEADERS={"User-Agent":"Dealix-Selfhost-Release-Identity/1.0","Accept":"application/json"}

def fetch(url: str) -> dict:
    req=urllib.request.Request(url,headers=HEADERS,method="GET")
    with urllib.request.urlopen(req,timeout=15) as r:
        return json.loads(r.read(4096).decode("utf-8"))

def main() -> int:
    ap=argparse.ArgumentParser(); ap.add_argument("--accepted-sha", required=True); ap.add_argument("--frontend-base", default="https://dealix.me"); ap.add_argument("--api-base", default="https://api.dealix.me"); a=ap.parse_args()
    if not re.fullmatch(r"[0-9a-f]{40}", a.accepted_sha):
        print("SELFHOST_PUBLIC_RELEASE_IDENTITY=HOLD reason=accepted_sha_not_exact"); return 2
    try:
        web=fetch(a.frontend_base.rstrip("/")+"/healthz"); api=fetch(a.api_base.rstrip("/")+"/version")
    except Exception as exc:
        print(f"SELFHOST_PUBLIC_RELEASE_IDENTITY=HOLD reason=probe_failed type={type(exc).__name__}"); print("PRODUCTION_GREEN=false"); return 1
    web_sha=web.get("git_sha"); api_sha=api.get("git_sha")
    ok=web.get("status")=="ok" and api.get("status")=="ok" and web_sha==a.accepted_sha and api_sha==a.accepted_sha
    print(f"WEB_SHA={web_sha or 'unknown'}"); print(f"API_SHA={api_sha or 'unknown'}")
    print(f"SELFHOST_PUBLIC_RELEASE_IDENTITY={'PASS' if ok else 'HOLD'}"); print(f"PRODUCTION_GREEN={'true' if ok else 'false'}")
    return 0 if ok else 1
if __name__ == "__main__": raise SystemExit(main())
