#!/usr/bin/env python3
"""Wave 13 Phase 5 — Weekly Executive Pack CLI generator.

Runs Friday 4PM KSA cron-able. Writes one MD per customer to:
  data/wave13/exec_packs/{customer_handle}_{YYYY-WW}.md

Article 4 NO_LIVE_SEND: NEVER auto-emails; founder copies manually.
Article 8: every numeric `is_estimate=True`; commitment language only.

Usage:
  python3 scripts/dealix_weekly_executive_pack.py --customer-handle acme
  python3 scripts/dealix_weekly_executive_pack.py --customer-handle acme --audience founder
  python3 scripts/dealix_weekly_executive_pack.py --all-customers (reads data/customers/*)
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

# Repo root for direct imports without api/* cascade
_REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_REPO_ROOT))


def _output_dir() -> Path:
    out = _REPO_ROOT / "data" / "wave13" / "exec_packs"
    out.mkdir(parents=True, exist_ok=True)
    return out


def _week_label(now: datetime | None = None) -> str:
    now = now or datetime.now(timezone.utc)
    week_num = now.isocalendar().week
    return f"{now.year}-W{week_num:02d}"


def _generate_for_customer(customer_handle: str, audience: str = "customer") -> Path:
    """Build pack + render + write MD. Returns the file path."""
    # Lazy imports — keep CLI fast and avoid api/* cascade
    from auto_client_acquisition.executive_pack_v2.composer import build_weekly_pack
    from auto_client_acquisition.executive_pack_v2.renderers import render_pack

    pack = build_weekly_pack(customer_handle=customer_handle)
    md = render_pack(pack, audience=audience)

    label = pack.week_label or _week_label()
    suffix = "" if audience == "customer" else f"_{audience}"
    out_path = _output_dir() / f"{customer_handle}_{label}{suffix}.md"
    out_path.write_text(md, encoding="utf-8")

    # Sidecar JSON for portability
    json_path = out_path.with_suffix(".json")
    json_path.write_text(pack.model_dump_json(indent=2), encoding="utf-8")

    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dealix Weekly Executive Pack — Friday cron generator (NEVER auto-sends)"
    )
    parser.add_argument(
        "--customer-handle",
        type=str,
        help="One customer to render. Either this OR --all-customers is required.",
    )
    parser.add_argument(
        "--audience",
        choices=["customer", "founder"],
        default="customer",
        help="Render style (customer = Arabic-first / founder = full detail)",
    )
    parser.add_argument(
        "--all-customers",
        action="store_true",
        help="Render packs for every handle under data/customers/",
    )
    args = parser.parse_args()

    if not args.customer_handle and not args.all_customers:
        parser.error("--customer-handle or --all-customers required")

    handles: list[str] = []
    if args.all_customers:
        customers_dir = _REPO_ROOT / "data" / "customers"
        if customers_dir.is_dir():
            handles = sorted(d.name for d in customers_dir.iterdir() if d.is_dir())
        if not handles:
            print("No customers found under data/customers/. Use --customer-handle <h>.")
            return 0
    else:
        handles = [args.customer_handle]

    print(f"=== Dealix Weekly Executive Pack — {_week_label()} ({args.audience} view) ===")
    written: list[Path] = []
    for h in handles:
        try:
            path = _generate_for_customer(h, audience=args.audience)
            written.append(path)
            print(f"  ✓ {h}: {path.relative_to(_REPO_ROOT)}")
        except Exception as exc:  # pragma: no cover — defensive
            print(f"  ✗ {h}: {exc}")

    print(f"\n{len(written)} pack(s) written.")
    print("Article 4 NO_LIVE_SEND: founder copies + sends manually.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
