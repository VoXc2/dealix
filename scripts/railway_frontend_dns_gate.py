#!/usr/bin/env python3
"""Frontend DNS gate — verify dealix.me /ar is on Railway (Layer 4)."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs/ops/DEALIX_ME_FRONTEND_DNS_RAILWAY_AR.md"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8

    ensure_stdout_utf8()
except Exception:
    pass


def _head(url: str, timeout: float = 15.0) -> tuple[int, str]:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            server = resp.headers.get("Server", "")
            return resp.status, server
    except urllib.error.HTTPError as exc:
        return exc.code, exc.headers.get("Server", "") if exc.headers else ""


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frontend-base", default="https://dealix.me")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    base = args.frontend_base.rstrip("/")
    ar_url = f"{base}/ar"

    status, server = _head(ar_url)
    github_pages = "github.com" in (server or "").lower()
    ok = status == 200 and not github_pages

    out = {
        "frontend_base": base,
        "ar_url": ar_url,
        "status": status,
        "server": server,
        "github_pages": github_pages,
        "layer_4_ok": ok,
        "doc": str(DOC.relative_to(ROOT)).replace("\\", "/"),
        "next_ar": [] if ok else [
            "أنشئ خدمة Frontend على Railway (Root Directory = frontend)",
            "Custom domain: dealix.me + www",
            "DNS: CNAME dealix.me → Railway (أزل GitHub Pages A/CNAME)",
            f"راجع {DOC.name}",
            "powershell -File scripts/founder_complete_layers_now.ps1 -SkipPush",
        ],
    }
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print(f"FRONTEND_DNS_GATE={'PASS' if ok else 'FAIL'}")
        print(f"  {ar_url} -> {status} server={server or 'unknown'}")
        if not ok:
            for line in out["next_ar"]:
                print(f"  → {line}")
    print(f"FRONTEND_DNS_GATE_VERDICT={'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
