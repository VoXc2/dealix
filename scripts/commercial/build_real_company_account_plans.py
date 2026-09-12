#!/usr/bin/env python3
"""Build truth-safe internal account plans from the Dealix company-radar seed."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial.real_company_target_radar import (
    RealCompanyRecord,
    RealCompanyTargetRadar,
)

DEFAULT_INPUT = REPO_ROOT / "data/commercial/real_company_target_radar_seed_v1.json"
DEFAULT_OUTPUT = REPO_ROOT / "data/commercial/real_company_account_plans_v1.json"


def build(input_path: Path, output_path: Path) -> dict[str, object]:
    raw = json.loads(input_path.read_text(encoding="utf-8"))
    records = [RealCompanyRecord(**item) for item in raw.get("records", [])]
    radar = RealCompanyTargetRadar(records)
    plans = [radar.build_account_plan(item.company_id).model_dump() for item in radar.records()]
    payload: dict[str, object] = {
        "schema": "dealix.real-company-account-plans.v1",
        "source": str(input_path.relative_to(REPO_ROOT) if input_path.is_relative_to(REPO_ROOT) else input_path),
        "truth_policy": "INTERNAL_HYPOTHESIS_ONLY_NO_EXTERNAL_SEND",
        "count": len(plans),
        "plans": plans,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = build(args.input.resolve(), args.output.resolve())
    print("REAL_COMPANY_ACCOUNT_PLANS=PASS")
    print(f"ACCOUNT_PLANS={payload['count']}")
    print("EXTERNAL_SEND=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
