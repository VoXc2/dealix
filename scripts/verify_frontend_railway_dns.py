#!/usr/bin/env python3
"""Verify dealix.me frontend Railway readiness (Layer 4) — DNS must not be GitHub Pages."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.production_layers import layer_4_frontend  # noqa: E402
from dealix.commercial_ops.railway_launch import check_railway_frontend_env  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--frontend-base", default=os.getenv("DEALIX_FRONTEND_BASE", "https://dealix.me"))
    p.add_argument("--check-env", action="store_true")
    p.add_argument("--strict", action="store_true")
    args = p.parse_args()

    layer = layer_4_frontend(args.frontend_base.rstrip("/"), check_env=args.check_env)
    fe_env = check_railway_frontend_env() if args.check_env else {}

    print("== Frontend Railway / DNS verify ==")
    print(f"  Layer 4 pct: {layer['pct']}%")
    print(f"  /ar status: {(layer.get('ar') or {}).get('status')}")
    print(f"  github_pages: {layer.get('github_pages')}")
    if layer.get("blocker_ar"):
        print(f"  blocker: {layer['blocker_ar']}")
    if fe_env:
        print(f"  fe_env_ready: {fe_env.get('ready_for_fe_deploy')}")
        if fe_env.get("missing"):
            print(f"  missing: {fe_env['missing']}")
        if fe_env.get("hint_ar"):
            print(f"  hint: {fe_env['hint_ar']}")

    ok = layer["pct"] >= 70 and not layer.get("github_pages")
    print(f"FRONTEND_RAILWAY_DNS_VERDICT={'PASS' if ok else 'FAIL'}")
    if args.strict and not ok:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
