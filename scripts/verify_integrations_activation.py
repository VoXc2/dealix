#!/usr/bin/env python3
"""Verify external integration env + suggest founder_integration_truth.yaml updates."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
TRUTH = ROOT / "dealix/transformation/founder_integration_truth.yaml"


def _has(*keys: str) -> bool:
    return all(os.getenv(k, "").strip() for k in keys)


def _status_for_integration(integration_id: str) -> str:
    checks: dict[str, tuple[tuple[str, ...], str]] = {
        "moyasar_live": (("MOYASAR_SECRET_KEY",), "sk_live"),
        "moyasar_sandbox": (("MOYASAR_SECRET_KEY",), "sk_test"),
        "hubspot_crm": (("HUBSPOT_ACCESS_TOKEN",), ""),
        "gmail_oauth": (("GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET"), ""),
        "whatsapp_business": (("WHATSAPP_ACCESS_TOKEN", "WHATSAPP_PHONE_NUMBER_ID"), ""),
        "posthog": (("POSTHOG_API_KEY",), ""),
    }
    spec = checks.get(integration_id)
    if not spec:
        return "unknown"
    keys, prefix = spec
    if not _has(*keys):
        return "red"
    val = os.getenv(keys[0], "")
    if prefix and not val.startswith(prefix):
        return "yellow"
    return "green"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--from-railway-env", action="store_true")
    p.add_argument("--write-truth-hints", action="store_true")
    args = p.parse_args()

    if args.from_railway_env:
        env_path = ROOT / ".env.railway.api.generated"
        if env_path.is_file():
            for raw in env_path.read_text(encoding="utf-8").splitlines():
                line = raw.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v

    truth = yaml.safe_load(TRUTH.read_text(encoding="utf-8")) if TRUTH.is_file() else {}
    integrations = truth.get("integrations") or []
    rows: list[dict] = []
    blockers: list[str] = []

    id_map = {
        "moyasar": "moyasar_live",
        "moyasar_sandbox": "moyasar_sandbox",
        "hubspot": "hubspot_crm",
        "gmail": "gmail_oauth",
        "whatsapp": "whatsapp_business",
        "posthog": "posthog",
    }

    for item in integrations:
        iid = item.get("id", "")
        mapped = id_map.get(iid, iid)
        live = _status_for_integration(mapped) if mapped in {
            "moyasar_live",
            "moyasar_sandbox",
            "hubspot_crm",
            "gmail_oauth",
            "whatsapp_business",
            "posthog",
        } else item.get("status", "unknown")
        yaml_status = item.get("status", "unknown")
        rows.append({"id": iid, "yaml_status": yaml_status, "env_probe": live, "match": yaml_status == live})
        if live == "red" and yaml_status != "red":
            blockers.append(f"{iid}: yaml={yaml_status} but env=red — update truth or set env")

    print("INTEGRATIONS_ACTIVATION_REPORT")
    for row in rows:
        match = "OK" if row["match"] else "DRIFT"
        print(f"  {row['id']}: yaml={row['yaml_status']} env={row['env_probe']} [{match}]")
    for b in blockers:
        print(f"  blocker: {b}")

    if args.write_truth_hints and blockers:
        print("  hint: edit dealix/transformation/founder_integration_truth.yaml after manual verify")

    verdict = "PASS" if not blockers else "NEEDS_ENV"
    print(f"INTEGRATIONS_ACTIVATION_VERDICT={verdict}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
