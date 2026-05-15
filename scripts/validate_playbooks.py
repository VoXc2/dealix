#!/usr/bin/env python3
"""Validate playbook coverage for all sellable services."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_playbook_catalog, load_pricing_model


def main() -> int:
    playbooks = load_playbook_catalog()
    pricing = load_pricing_model()
    acceptance_path = Path("delivery/acceptance/acceptance_criteria.json")
    rollback_path = Path("delivery/rollback/rollback_policy.json")
    escalation_path = Path("delivery/escalation/escalation_policy.json")
    errors: list[str] = []

    required_fields = {
        "owner",
        "decision_gate",
        "delivery_window_days",
        "implementation_steps",
        "out_of_scope",
        "acceptance_criteria",
        "rollout_plan",
        "rollback_plan",
        "stopping_conditions",
        "next_step",
        "security_review",
    }

    for engine in pricing["service_matrix"].keys():
        engine_cfg = playbooks.get(engine)
        if not engine_cfg:
            errors.append(f"missing playbook engine: {engine}")
            continue
        tiers = engine_cfg.get("tiers", {})
        for tier in ("bronze", "silver", "gold"):
            tier_cfg = tiers.get(tier)
            if not tier_cfg:
                errors.append(f"{engine}: missing playbook tier {tier}")
                continue
            missing = sorted(required_fields - set(tier_cfg.keys()))
            if missing:
                errors.append(f"{engine}_{tier}: missing fields {', '.join(missing)}")

    if not acceptance_path.exists():
        errors.append("missing delivery acceptance criteria file")
    if not rollback_path.exists():
        errors.append("missing delivery rollback policy file")
    if not escalation_path.exists():
        errors.append("missing delivery escalation policy file")

    if errors:
        print("PLAYBOOK_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("PLAYBOOK_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
