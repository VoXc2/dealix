#!/usr/bin/env python3
"""Dealix-on-Dealix Proof Pack v1 — Wave 15 (A3).

Runs the 10-step Sprint orchestrator on the bundled synthetic Saudi B2B
demo CSV (data/demo/saudi_b2b_demo.csv) and produces:

1. `data/proofs/dealix_internal_v1_proof_pack.json` — full SprintRun
   serialized
2. Updates `docs/case-studies/case_003_dealix_internal.md` placeholders
   with actual proof_score / proof_tier / capital_assets count
3. Prints a summary the founder can paste into LinkedIn post 004

NEVER touches real customer data. The CSV is synthetic. No external
sends. Idempotent — running twice overwrites the artifact and re-fills
the case-study placeholders.

Usage:
    python scripts/dealix_on_dealix_proof.py
    python scripts/dealix_on_dealix_proof.py --engagement-id custom_v2
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))


def _read_demo_csv() -> tuple[str, list[dict[str, str]]]:
    csv_path = REPO_ROOT / "data" / "demo" / "saudi_b2b_demo.csv"
    raw = csv_path.read_text(encoding="utf-8")
    reader = csv.DictReader(raw.splitlines())
    accounts = list(reader)
    return raw, accounts


def _demo_passport() -> dict:
    return {
        "source_id": "DEALIX-ON-DEALIX-DEMO-V1",
        "source_type": "client_upload",
        "owner": "dealix",
        "allowed_use": ("internal_analysis", "scoring"),
        "contains_pii": False,
        "sensitivity": "low",
        "ai_access_allowed": True,
        "external_use_allowed": False,
        "retention_policy": "project_duration",
    }


def _update_case_study(
    *,
    case_path: Path,
    dq_score: float,
    proof_score: float,
    proof_tier: str,
    capital_assets_count: int,
    retainer_eligible: bool,
    engagement_id: str,
) -> None:
    if not case_path.exists():
        print(f"⚠ case-study not found at {case_path} — skip placeholder fill")
        return
    text = case_path.read_text(encoding="utf-8")
    substitutions = {
        "<DQ>": f"{dq_score:.1f}",
        "<SCORE>": f"{proof_score:.1f}",
        "<TIER>": proof_tier,
        "<ELIGIBLE>": "yes" if retainer_eligible else "no",
        "<ENGAGEMENT_ID>": engagement_id,
        "<CAPITAL_COUNT>": str(capital_assets_count),
        "<GENERATED_AT>": datetime.now(timezone.utc).isoformat(),
    }
    for placeholder, value in substitutions.items():
        text = text.replace(placeholder, value)
    case_path.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--engagement-id", default="dealix_internal_v1")
    parser.add_argument(
        "--out",
        default="data/proofs/dealix_internal_v1_proof_pack.json",
    )
    args = parser.parse_args()

    raw_csv, accounts = _read_demo_csv()
    print(f"✓ Loaded {len(accounts)} synthetic accounts from demo CSV")

    from auto_client_acquisition.delivery_factory.delivery_sprint import run_sprint

    run = run_sprint(
        engagement_id=args.engagement_id,
        customer_id="dealix_internal_demo",
        source_passport=_demo_passport(),
        raw_csv=raw_csv,
        accounts=accounts,
        problem_summary=(
            "Demonstrate Dealix methodology on a synthetic Saudi B2B pipeline. "
            "Rank accounts by relationship + sector + recency. Surface ≥1 "
            "reusable capital asset. Generate a 14-section Proof Pack. NO real "
            "customer data; methodology is the artifact."
        ),
        workflow_owner_present=True,
    )

    out_path = REPO_ROOT / args.out
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(run.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    dq_score = 0.0
    for step in run.steps:
        if step.name == "data_quality":
            dq_score = float(step.output.get("dq_overall", 0.0))

    capital_count = len(run.capital_assets_registered)

    print()
    print(f"━━ Proof artifact written → {out_path.relative_to(REPO_ROOT)} ━━")
    print(f"  engagement_id:            {run.engagement_id}")
    print(f"  customer_id:              {run.customer_id}")
    print(f"  steps_run:                {len(run.steps)} / 8")
    print(f"  DQ score:                 {dq_score:.1f} / 100")
    print(f"  Proof score:              {run.proof_score:.1f} / 100")
    print(f"  Proof tier:               {run.proof_tier}")
    print(f"  Capital assets:           {capital_count}")
    print(f"  Retainer eligible:        {run.retainer_eligible}")
    print(f"  Governance envelope:      {run.governance_decision}")

    # Update the case-study placeholders.
    case_path = REPO_ROOT / "docs" / "case-studies" / "case_003_dealix_internal.md"
    _update_case_study(
        case_path=case_path,
        dq_score=dq_score,
        proof_score=run.proof_score,
        proof_tier=run.proof_tier,
        capital_assets_count=capital_count,
        retainer_eligible=run.retainer_eligible,
        engagement_id=run.engagement_id,
    )
    print(f"  Case study updated:       {case_path.relative_to(REPO_ROOT)}")

    print()
    print("LinkedIn post 004 placeholders to fill:")
    print(f"  Proof Score: {run.proof_score:.0f}/100")
    print(f"  Tier:        {run.proof_tier}")
    print(f"  Capital:     {capital_count}")
    print()
    print("_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
