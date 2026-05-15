#!/usr/bin/env python3
"""Validate monetization automation strategy and customer-state schemas."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_monetization_strategy


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    errors: list[str] = []
    strategy = load_monetization_strategy()

    if "scorecard" not in strategy:
        errors.append("monetization_strategy: missing scorecard")
    else:
        scorecard = strategy["scorecard"]
        if "weights" not in scorecard:
            errors.append("monetization_strategy: missing scorecard.weights")
        if "thresholds" not in scorecard:
            errors.append("monetization_strategy: missing scorecard.thresholds")

    if not strategy.get("priority_service_families"):
        errors.append("monetization_strategy: priority_service_families missing")
    if "renewal" not in strategy:
        errors.append("monetization_strategy: renewal section missing")
    if "expansion" not in strategy:
        errors.append("monetization_strategy: expansion section missing")

    state_schema_path = Path("revenue/customer_state_schema.json")
    if not state_schema_path.exists():
        errors.append("missing revenue/customer_state_schema.json")
    else:
        schema = _load(state_schema_path)
        required = schema.get("required_fields", [])
        for key in (
            "customer_id",
            "service_id",
            "health_score",
            "sla_compliance",
            "payment_delay_days",
            "proof_events_count",
            "expansion_readiness",
            "usage_growth_rate",
        ):
            if key not in required:
                errors.append(f"customer_state_schema missing required field: {key}")

    demo_state_path = Path("revenue/demo_customer_state.json")
    if not demo_state_path.exists():
        errors.append("missing revenue/demo_customer_state.json")
    else:
        demo = _load(demo_state_path)
        for key in ("customer_id", "service_id", "health_score"):
            if key not in demo:
                errors.append(f"demo_customer_state missing field: {key}")

    if errors:
        print("MONETIZATION_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("MONETIZATION_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
