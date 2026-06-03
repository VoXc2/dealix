#!/usr/bin/env python3
"""Paid launch readiness — env + integration matrix (no Moyasar claim until configured)."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_launch import (  # noqa: E402
    check_railway_api_env,
    check_railway_frontend_env,
)

RAILWAY_ENV = ROOT / ".env.railway.generated"
RAILWAY_FE_ENV = ROOT / ".env.railway.frontend.generated"

FAILURES: list[str] = []
WARNINGS: list[str] = []
# Infra go-live strict: drafts-only integrations do not block production layers gate
OPTIONAL_STRICT_INTEGRATIONS = frozenset({"GMAIL_CLIENT_ID"})


def _set(name: str) -> bool:
    return bool((os.getenv(name) or "").strip())


def check_integration_env() -> None:
    integrations = {
        "MOYASAR_SECRET_KEY": "Moyasar live/test",
        "MOYASAR_WEBHOOK_SECRET": "Moyasar webhook",
        "HUBSPOT_ACCESS_TOKEN": "HubSpot sync",
        "CALENDLY_WEBHOOK_SIGNING_KEY": "Calendly webhooks",
        "CALENDLY_URL": "Calendly booking link",
        "POSTHOG_API_KEY": "PostHog analytics",
        "GMAIL_CLIENT_ID": "Gmail OAuth (drafts)",
    }
    for key, label in integrations.items():
        ok = _set(key)
        if key == "CALENDLY_WEBHOOK_SIGNING_KEY" and not ok:
            ok = _set("CALENDLY_WEBHOOK_SECRET")
        if ok:
            print(f"  ok: {label} ({key})")
        elif key in OPTIONAL_STRICT_INTEGRATIONS:
            print(f"  optional: {label} — {key} (drafts; not blocking infra strict)")
        else:
            WARNINGS.append(f"{label}: set {key}")
            print(f"  FOUNDER_ACTION: {label} — {key}")


def check_docs() -> None:
    required = [
        "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md",
        "docs/ops/MANUAL_PAYMENT_SOP.md",
        "docs/commercial/PAID_LAUNCH_TRACKER_AR.md",
        "docs/LAUNCH_GATES.md",
    ]
    for rel in required:
        if (ROOT / rel).is_file():
            print(f"  ok: {rel}")
        else:
            FAILURES.append(f"missing {rel}")


def _load_dotenv_file(path: Path) -> int:
    if not path.is_file():
        return 0
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        if key and key not in os.environ:
            os.environ[key] = val.strip().strip('"').strip("'")
            n += 1
    return n


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--strict",
        action="store_true",
        help="Fail if any integration env or payment keys missing",
    )
    p.add_argument(
        "--from-railway-env",
        action="store_true",
        help="Load .env.railway.generated and .env.railway.frontend.generated (no overwrite)",
    )
    args = p.parse_args()

    if args.from_railway_env:
        loaded = _load_dotenv_file(RAILWAY_ENV) + _load_dotenv_file(RAILWAY_FE_ENV)
        if loaded:
            print(f"  loaded {loaded} env keys from railway generated files (not printed)")

    print("== verify_paid_launch_readiness ==")
    print("\n== Docs ==")
    check_docs()
    print("\n== Integrations (FOUNDER_ACTION until set) ==")
    check_integration_env()
    print("\n== Railway / deploy env ==")
    api = check_railway_api_env()
    fe = check_railway_frontend_env()
    if api["ready_for_api_deploy"]:
        print("  ok: API deploy env snapshot")
    else:
        WARNINGS.append(f"API env missing: {api['missing_required']}")
    if fe["ready_for_fe_deploy"]:
        print("  ok: Frontend deploy env snapshot")
    else:
        WARNINGS.append(f"Frontend env missing: {fe['missing']}")
    if not api["ready_for_payments"]:
        WARNINGS.append(f"Payments: {api['missing_payments']}")

    print("\n== First paid Diagnostic pipeline ==")
    try:
        from scripts.verify_first_paid_diagnostic_tracker import analyze

        pipe = analyze()
        print(
            f"  pipeline: {pipe['payment_received_real']} paid · "
            f"{pipe['proof_pack_delivered_real']} proof (real companies)"
        )
        print(f"  verdict: {'CLOSED' if pipe['first_close_ready'] else 'PIPELINE_OPEN'}")
        if pipe["crm_kpi_pending"]:
            print("  FOUNDER_ACTION: sync kpi_founder_commercial_import.yaml from CRM export")
            # CRM import is founder ops — not infra deploy gate
    except Exception as exc:
        WARNINGS.append(f"first_paid tracker: {exc}")

    if FAILURES:
        print("\nPAID_LAUNCH_READINESS=FAIL")
        for f in FAILURES:
            print(f"  - {f}")
        return 1

    if args.strict and WARNINGS:
        print("\nPAID_LAUNCH_READINESS=FAIL (strict)")
        for w in WARNINGS:
            print(f"  - {w}")
        return 1

    for w in WARNINGS:
        print(f"  (pending) {w}")
    print("\nPAID_LAUNCH_READINESS=ROADMAP_OK (soft — complete FOUNDER_ACTION for paid)")
    print("Next: docs/commercial/PAID_LAUNCH_TRACKER_AR.md · bash scripts/official_launch_verify.sh")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
