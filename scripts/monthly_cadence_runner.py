#!/usr/bin/env python3
"""Monthly cadence runner — for every active retainer customer:

1. Generate Monthly Value Report via value_os.monthly_report.generate
2. Generate Adoption Score (estimate; needs signal inputs to be precise)
3. Generate Retainer Readiness gate
4. Write a markdown + JSON sidecar to data/monthly_reports/{customer_id}/{YYYY-MM}.{md,json}
5. Queue a renewal schedule if not already scheduled
6. NO external sends — founder reviews + approves manually

Usage:
    python scripts/monthly_cadence_runner.py --customers acme
    python scripts/monthly_cadence_runner.py --all-active
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _all_active() -> list[str]:
    from scripts.weekly_brief_runner import _active_customers  # type: ignore
    return _active_customers()


def _generate_for(customer_id: str) -> dict:
    from auto_client_acquisition.adoption_os.adoption_score import compute as compute_adoption
    from auto_client_acquisition.adoption_os.retainer_readiness import (
        evaluate as evaluate_retainer,
    )
    from auto_client_acquisition.value_os.monthly_report import generate as generate_monthly

    report = generate_monthly(customer_id=customer_id)
    adoption = compute_adoption(customer_id=customer_id)
    retainer = evaluate_retainer(
        customer_id=customer_id,
        adoption_score=adoption.score,
        proof_score=80.0,  # default; real value requires latest proof_pack lookup
        workflow_owner_present=True,
        governance_risk_controlled=True,
    )
    return {
        "customer_id": customer_id,
        "month": report.month,
        "monthly_value_report": report.to_dict(),
        "monthly_value_markdown": report.to_markdown(),
        "adoption_score": adoption.to_dict(),
        "retainer_readiness": retainer.to_dict(),
        "is_estimate": True,
        "governance_decision": "allow_with_review",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--customers", default="")
    parser.add_argument("--all-active", action="store_true")
    parser.add_argument("--out-dir", default="data/monthly_reports")
    parser.add_argument("--schedule-renewals", action="store_true")
    args = parser.parse_args()

    if args.all_active:
        customers = _all_active()
    elif args.customers:
        customers = [c.strip() for c in args.customers.split(",") if c.strip()]
    else:
        print("No customers selected. Use --customers or --all-active.")
        return 1

    out_dir = REPO_ROOT / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    for cid in customers:
        bundle = _generate_for(cid)
        cust_dir = out_dir / cid
        cust_dir.mkdir(parents=True, exist_ok=True)
        month = bundle["month"]
        (cust_dir / f"{month}.json").write_text(
            json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        (cust_dir / f"{month}.md").write_text(
            bundle["monthly_value_markdown"], encoding="utf-8"
        )
        summary.append({
            "customer_id": cid,
            "month": month,
            "adoption_tier": bundle["adoption_score"]["tier"],
            "retainer_eligible": bundle["retainer_readiness"]["eligible"],
        })

        if args.schedule_renewals:
            from auto_client_acquisition.payment_ops.renewal_scheduler import (
                schedule_renewal,
            )
            schedule_renewal(
                customer_id=cid,
                plan="managed_revenue_ops_starter",
                amount_sar=2999,
                cadence_days=30,
            )

    print(json.dumps({"customers_processed": len(customers), "summary": summary}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
