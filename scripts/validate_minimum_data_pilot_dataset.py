#!/usr/bin/env python3
"""Validate a proposed first-Pilot dataset without importing or persisting it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from pydantic import ValidationError

from dealix.privacy.minimum_data import MinimumDataPilotDataset


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("dataset", type=Path, help="JSON dataset to validate; no import occurs")
    args = parser.parse_args()

    raw = json.loads(args.dataset.read_text(encoding="utf-8"))
    try:
        dataset = MinimumDataPilotDataset.model_validate(raw)
    except ValidationError as exc:
        print("MINIMUM_DATASET=REJECT")
        print(exc)
        return 1

    print(
        "MINIMUM_DATASET=PASS "
        f"tenant={dataset.tenant_id} company={dataset.company_id} "
        f"metrics={len(dataset.baseline_metrics)} opportunities={len(dataset.opportunities)} "
        "personal_data=not_authorized persistence=none external_effect=none"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
