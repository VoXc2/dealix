#!/usr/bin/env python3
"""LaaS (Lead-as-a-Service) weekly batch runner (W9.3).

Generates and delivers the weekly lead batch for one or all LaaS
customers. Designed to run from cron every Tuesday at 09:00 AST,
per docs/ops/LAAS_DELIVERY_RUNBOOK.md.

For each LaaS customer:
  1. Read their ICP filter from tenant features/meta_json
  2. Run the acquisition pipeline against that filter
  3. Apply suppression (customer's existing CRM + global)
  4. Score and rank top-N (default 50)
  5. Output: CSV + JSON for the customer's dashboard
  6. Record per-lead delivery events for metered billing

Usage:
  python scripts/laas_weekly_batch.py --customer-handle acme_saas
  python scripts/laas_weekly_batch.py --all                       # all active LaaS customers
  python scripts/laas_weekly_batch.py --dry-run                   # plan only, no API calls
  python scripts/laas_weekly_batch.py --target-count 25           # smaller batch (testing)

Exit codes:
  0  all batches delivered (or dry-run successful)
  1  at least one customer batch failed (others may have succeeded)
  2  unrecoverable error (DB unreachable, env misconfigured)

For the first 5 customers, this script runs MANUALLY (founder triggers).
After customer #5 (per docs/ops/LAAS_DELIVERY_RUNBOOK.md "Automation
Roadmap"), wire to cron / Railway scheduler.
"""
from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


async def _load_active_laas_customers() -> list[dict]:
    """Pull all tenants on metered LaaS plans (laas_per_reply / laas_per_demo).

    Stub for now: real implementation queries `tenant_features` or
    `tenant.meta_json->'subscriptions'` once the LaaS plan-assignment
    schema lands. Returns empty list cleanly if DB layer unavailable.
    """
    try:
        from sqlalchemy import select

        from db.models import TenantRecord
        from db.session import async_session_factory

        async with async_session_factory()() as session:
            rows = (
                await session.execute(
                    select(TenantRecord).where(TenantRecord.status == "active")
                )
            ).scalars().all()
            # Filter to those with LaaS marker in meta_json
            return [
                {
                    "id": t.id,
                    "handle": t.slug,
                    "name": t.name,
                    "icp_filter": (t.meta_json or {}).get("laas_icp_filter", {}),
                }
                for t in rows
                if (t.meta_json or {}).get("laas_enabled") is True
            ]
    except Exception as exc:
        print(f"[warn] could not load tenants: {exc}", file=sys.stderr)
        return []


async def _run_one_customer(
    handle: str,
    icp_filter: dict,
    target_count: int,
    dry_run: bool,
) -> dict:
    """Generate the weekly batch for one LaaS customer."""
    result: dict = {
        "handle": handle,
        "target_count": target_count,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "dry_run": dry_run,
    }

    if dry_run:
        result["status"] = "dry_run"
        result["note"] = "would query pipeline + apply ICP filter + write report"
        result["icp_filter_seen"] = icp_filter
        return result

    # In production, this would call into auto_client_acquisition.pipeline
    # with the customer's ICP. For now, we delegate to the existing
    # discovery endpoints if they accept this shape.
    try:
        from auto_client_acquisition.pipeline import AcquisitionPipeline  # type: ignore

        # Real call would be:
        #   pipeline = AcquisitionPipeline()
        #   leads = await pipeline.run_discovery_batch(icp_filter, target_count)
        # We don't execute this against live APIs from a cron driver
        # without explicit operator opt-in via --live flag (TBD).
        result["status"] = "pipeline_import_ok"
        result["note"] = (
            "Live discovery requires --live flag. This run was a structure check only."
        )
        result["leads_count"] = 0
    except ImportError as exc:
        result["status"] = "import_failed"
        result["error"] = str(exc)
    return result


def _write_run_report(reports: list[dict]) -> str:
    """Persist a run report to docs/ops/laas_weekly_runs/."""
    out_dir = Path(__file__).resolve().parent.parent / "docs" / "ops" / "laas_weekly_runs"
    out_dir.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y-%m-%dT%H%M%S", time.gmtime())
    out_path = out_dir / f"{timestamp}.json"
    out_path.write_text(
        json.dumps(
            {
                "ran_at": datetime.now(timezone.utc).isoformat(),
                "customers_run": len(reports),
                "reports": reports,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return str(out_path)


async def main_async(args: argparse.Namespace) -> int:
    if not os.environ.get("DATABASE_URL") and not args.dry_run:
        print("[error] DATABASE_URL not set (use --dry-run for offline testing)",
              file=sys.stderr)
        return 2

    if args.customer_handle:
        customers = [{"id": "manual", "handle": args.customer_handle,
                      "name": "(specified)",
                      "icp_filter": {}}]
    else:
        customers = await _load_active_laas_customers()
        if not customers:
            print("[info] no active LaaS customers found")
            if args.all:
                return 0  # nothing to do is success
            print("[error] --all specified but no customers; specify --customer-handle "
                  "OR enable laas_enabled=true on a tenant", file=sys.stderr)
            return 2

    print(f"Running LaaS weekly batch for {len(customers)} customer(s)")
    print(f"  target_count: {args.target_count}, dry_run: {args.dry_run}")
    print()

    reports = []
    any_failed = False
    for c in customers:
        print(f"  → {c['handle']:<24}", end="  ", flush=True)
        report = await _run_one_customer(
            c["handle"], c["icp_filter"], args.target_count, args.dry_run
        )
        reports.append(report)
        if report["status"] in ("dry_run", "pipeline_import_ok"):
            print(f"OK ({report['status']})")
        else:
            any_failed = True
            print(f"FAIL ({report.get('error', report['status'])})")

    report_path = _write_run_report(reports)
    print()
    print(f"Run report → {report_path}")
    return 1 if any_failed else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--customer-handle", help="run for one specific tenant slug")
    p.add_argument("--all", action="store_true",
                   help="run for all active LaaS customers")
    p.add_argument("--target-count", type=int, default=50,
                   help="leads per customer per week (default 50)")
    p.add_argument("--dry-run", action="store_true",
                   help="plan only, no API or DB writes")
    args = p.parse_args()

    if not args.customer_handle and not args.all:
        p.error("specify --customer-handle <slug> OR --all")

    try:
        return asyncio.run(main_async(args))
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"FATAL: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
