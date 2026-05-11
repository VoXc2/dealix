#!/usr/bin/env python3
"""Generate offer/SOW/risk files for a service SKU."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.offers import generate_offer


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate offer artifacts")
    parser.add_argument("--service", required=True, help="Service SKU, e.g. CUSTOMER_PORTAL_GOLD")
    parser.add_argument(
        "--segment",
        required=True,
        choices=["smb", "mid_market", "enterprise"],
    )
    parser.add_argument("--industry", default="general")
    parser.add_argument("--lang", choices=["ar", "en"], default="ar")
    args = parser.parse_args()

    outputs = generate_offer(args.service, args.segment, args.lang)
    for key, path in outputs.items():
        print(f"{key}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
