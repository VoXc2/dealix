"""Check required env vars for a given mode.

Usage:
    python3 scripts/check_required_env.py --mode demo
    python3 scripts/check_required_env.py --mode production
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


REQUIRED_PRODUCTION = [
    "APP_SECRET_KEY",
    "DATABASE_URL",
]

REQUIRED_OPTIONAL_CONNECTORS = [
    "GOOGLE_PLACES_API_KEY",
    "HUBSPOT_PRIVATE_APP_TOKEN",
    "WHATSAPP_BUSINESS_TOKEN",
    "EMAIL_PROVIDER_API_KEY",
]

REQUIRED_ADMIN = [
    "DEALIX_ADMIN_TOKEN",
    "DEALIX_ADMIN_PASSWORD",
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["demo", "production"], default="demo")
    args = parser.parse_args()

    if args.mode == "demo":
        print("Demo mode: no production env vars required.")
        return 0

    missing = []
    for var in REQUIRED_PRODUCTION + REQUIRED_ADMIN:
        if not os.environ.get(var):
            missing.append(var)
    if missing:
        print("Missing required env vars for production:")
        for m in missing:
            print(f"  - {m}")
        return 1
    print("Production env OK.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
