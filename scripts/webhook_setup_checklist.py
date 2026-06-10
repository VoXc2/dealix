#!/usr/bin/env python3
"""Webhook setup checklist — env names + live route probes (no secrets)."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_production import DEFAULT_API_BASE, probe_get  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

WEBHOOKS = (
    ("moyasar", "/api/v1/webhooks/moyasar", "MOYASAR_WEBHOOK_SECRET"),
    ("calendly", "/api/v1/webhooks/calendly", "CALENDLY_WEBHOOK_SECRET"),
    ("hubspot", "/api/v1/webhooks/hubspot", "HUBSPOT_ACCESS_TOKEN"),
)


def _set(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def _load_railway_env() -> None:
    for name in (".env.railway.generated", ".env.railway.frontend.generated"):
        path = ROOT / name
        if not path.is_file():
            continue
        for raw in path.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            if key and key not in os.environ:
                os.environ[key] = val.strip().strip('"').strip("'")


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--from-railway-env", action="store_true")
    args = ap.parse_args()
    if args.from_railway_env:
        _load_railway_env()
    base = DEFAULT_API_BASE
    print("== webhook_setup_checklist ==")
    print(f"  api: {base}\n")

    ok_all = True
    for label, path, env_key in WEBHOOKS:
        probe = probe_get(base, path, timeout_sec=10.0)
        route_ok = probe.get("status") not in (404, None)
        secret_ok = _set(env_key) or (
            label == "calendly"
            and (_set("CALENDLY_WEBHOOK_SIGNING_KEY") or _set("CALENDLY_WEBHOOK_SECRET"))
        )
        status = probe.get("status", probe.get("error", "?"))
        print(f"  {label}: route HTTP {status} | env {env_key}={'ok' if secret_ok else 'MISSING'}")
        if not route_ok or not secret_ok:
            ok_all = False

    print("\n  Dashboard URLs:")
    print("    Moyasar:  https://dashboard.moyasar.com/webhooks")
    print("    Calendly: https://calendly.com/integrations/api_webhooks")
    print("    HubSpot:  app hubspot → webhooks")

    print(f"\nWEBHOOK_SETUP_VERDICT={'PASS' if ok_all else 'ACTION'}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    raise SystemExit(main())
