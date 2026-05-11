#!/usr/bin/env python3
"""Verify final launch stack readiness for commercial execution."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_final_service_stack
from saudi_ai_provider.verifier import verify_sellable


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    stack = load_final_service_stack()
    services = stack.get("services", [])
    if len(services) < 10:
        errors.append("final_service_stack requires at least 10 high-value services")

    required_fields = [
        "service_id",
        "layer",
        "target_segments",
        "buyers",
        "core_outcome",
        "setup_fee_sar_range",
        "monthly_retainer_sar_range",
        "kpi_targets",
        "differentiators",
        "deployment_window_days",
    ]

    for service in services:
        for field in required_fields:
            if field not in service:
                errors.append(f"{service.get('service_id', 'UNKNOWN')}: missing {field}")
        setup_range = service.get("setup_fee_sar_range", [0, 0])
        monthly_range = service.get("monthly_retainer_sar_range", [0, 0])
        if len(setup_range) != 2 or setup_range[0] <= 0 or setup_range[1] <= 0:
            errors.append(f"{service['service_id']}: invalid setup_fee_sar_range")
        if len(monthly_range) != 2 or monthly_range[0] <= 0 or monthly_range[1] <= 0:
            errors.append(f"{service['service_id']}: invalid monthly_retainer_sar_range")
        if setup_range[1] < setup_range[0]:
            errors.append(f"{service['service_id']}: setup max below min")
        if monthly_range[1] < monthly_range[0]:
            errors.append(f"{service['service_id']}: monthly max below min")
        if len(service.get("kpi_targets", [])) < 3:
            warnings.append(f"{service['service_id']}: fewer than 3 KPI targets")

    verification = verify_sellable()
    launch_ready = (
        verification.sellable_now
        and verification.deliverable_now
        and verification.operable_now
        and verification.compliance_now
    )

    if errors:
        print("DEALIX_FINAL_LAUNCH_VERDICT=FAIL")
        for err in errors:
            print(f"- ERROR: {err}")
        return 1

    print("DEALIX_FINAL_LAUNCH_VERDICT=PASS" if launch_ready else "DEALIX_FINAL_LAUNCH_VERDICT=CONDITIONAL")
    print(f"SELLABLE_NOW={'true' if verification.sellable_now else 'false'}")
    print(f"DELIVERABLE_NOW={'true' if verification.deliverable_now else 'false'}")
    print(f"OPERABLE_NOW={'true' if verification.operable_now else 'false'}")
    print(f"COMPLIANCE_NOW={'true' if verification.compliance_now else 'false'}")
    print(f"NEXT_FOUNDER_ACTION={verification.next_founder_action}")
    if warnings:
        print("WARNINGS:")
        for warning in warnings:
            print(f"- {warning}")
    return 0 if launch_ready else 1


if __name__ == "__main__":
    raise SystemExit(main())
