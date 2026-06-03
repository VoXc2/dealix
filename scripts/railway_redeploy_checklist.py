#!/usr/bin/env python3
"""Pre-redeploy checklist — trust layer (/version, /api/v1/meta) must exist after deploy."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_production import (  # noqa: E402
    DEFAULT_API_BASE,
    probe_trust_layer,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", DEFAULT_API_BASE))
    args = p.parse_args()
    base = args.api_base.rstrip("/")

    trust = probe_trust_layer(base)
    print(f"== Railway redeploy trust probe: {base} ==")
    for path, row in (trust.get("probes") or {}).items():
        status = row.get("status", row.get("error", "?"))
        ok = row.get("ok")
        mark = "OK" if ok else "FAIL"
        print(f"  [{mark}] {path}: {status}")

    if trust.get("ok"):
        print("RAILWAY_REDEPLOY_TRUST=PASS")
        return 0

    print("RAILWAY_REDEPLOY_TRUST=FAIL")
    print("  → Redeploy API from latest main; platform_meta registered once in api/main.py")
    print("  → Local: APP_ENV=test pytest tests/test_platform_meta.py -q")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
