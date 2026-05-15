#!/usr/bin/env python3
"""Validate go-live sales runbook structure and service mappings."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from saudi_ai_provider.catalog import load_final_service_stack, load_go_live_sales_runbook
from saudi_ai_provider.go_live_sales import build_go_live_sales_plan, evaluate_signature_readiness


def main() -> int:
    errors: list[str] = []
    runbook = load_go_live_sales_runbook()
    stack = load_final_service_stack()
    service_ids = {service["service_id"] for service in stack.get("services", [])}

    for key in (
        "daily_execution_blocks",
        "segment_priorities",
        "target_plays",
        "signature_policy",
        "weekly_exec_review",
        "monthly_board_pack",
    ):
        if key not in runbook:
            errors.append(f"runbook missing key: {key}")

    for segment in ("smb", "mid_market", "enterprise"):
        priorities = runbook.get("segment_priorities", {}).get(segment, [])
        if not priorities:
            errors.append(f"{segment}: missing priority services")
        for service_id in priorities:
            if service_id not in service_ids:
                errors.append(f"{segment}: unknown priority service {service_id}")

    for play in runbook.get("target_plays", []):
        for field in (
            "play_id",
            "segments",
            "industry",
            "buyer",
            "pain",
            "primary_service",
            "kpi_promise",
            "sku_offer",
            "signature_trigger",
        ):
            if field not in play:
                errors.append(f"play missing field {field}: {play}")
        if play.get("primary_service") not in service_ids:
            errors.append(f"unknown primary_service in play {play.get('play_id')}")
        for support_service in play.get("supporting_services", []):
            if support_service not in service_ids:
                errors.append(
                    f"unknown supporting_service {support_service} in play {play.get('play_id')}"
                )

    try:
        build_go_live_sales_plan("enterprise")
        evaluate_signature_readiness(
            stage="executive_alignment",
            buyer_commitment="high",
            proof_level="L3",
            risk_status="low",
            governance_contract_accepted=True,
        )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"go-live planner runtime check failed: {type(exc).__name__}: {exc}")

    if errors:
        print("GO_LIVE_SALES_VALIDATION=FAIL")
        for err in errors:
            print(f"- {err}")
        return 1

    print("GO_LIVE_SALES_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
