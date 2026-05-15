#!/usr/bin/env python3
"""Validate Saudi AI service catalog completeness and governance."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

CATALOG_PATH = Path("dealix/catalogs/saudi_ai_service_catalog_v2.json")

REQUIRED_LINES = {
    "market_radar": "MARKET_RADAR",
    "lead_intelligence": "LEAD_INTELLIGENCE",
    "company_brain": "COMPANY_BRAIN",
    "decision_passport": "DECISION_PASSPORT",
    "whatsapp_decision_layer": "WHATSAPP_DECISION_LAYER",
    "action_approval_engine": "ACTION_APPROVAL_ENGINE",
    "delivery_os": "DELIVERY_OS",
    "support_cs_os": "SUPPORT_OS",
    "payment_revenue_truth": "PAYMENT_TRUTH",
    "proof_expansion_engine": "PROOF_ENGINE",
    "learning_flywheel": "LEARNING_FLYWHEEL",
    "trust_security_compliance": "TRUST_LAYER",
}

REQUIRED_SERVICE_FIELDS = {
    "id",
    "tier",
    "name_ar",
    "problem_ar",
    "decision_ar",
    "execution_ar",
    "proof_ar",
    "expansion_next_ar",
    "action_mode",
    "delivery_window_days",
    "kpis",
}

ALLOWED_ACTION_MODES = {
    "suggest_only",
    "draft_only",
    "approval_required",
    "approved_manual",
    "blocked",
}

REQUIRED_HARD_RULES = {
    "no_cold_whatsapp",
    "no_linkedin_automation",
    "no_scraping",
    "no_live_send_without_approval",
    "no_live_charge_without_approval",
    "no_fake_proof",
    "no_fake_revenue",
}

FORBIDDEN_TERMS = [
    "guaranteed",
    "مضمون",
    "100% guaranteed",
    "live auto-send",
]


def _is_non_empty(value: Any) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return len(value) > 0
    return value is not None


def _validate_service(service: dict[str, Any], blockers: list[str], ctx: str) -> None:
    missing = sorted(field for field in REQUIRED_SERVICE_FIELDS if field not in service)
    if missing:
        blockers.append(f"{ctx} missing fields: {', '.join(missing)}")
        return

    for field in REQUIRED_SERVICE_FIELDS:
        if not _is_non_empty(service[field]):
            blockers.append(f"{ctx} has empty field: {field}")

    mode = service.get("action_mode")
    if mode not in ALLOWED_ACTION_MODES:
        blockers.append(f"{ctx} has invalid action_mode: {mode}")


def main() -> int:
    blockers: list[str] = []
    verdicts: dict[str, str] = {}

    if not CATALOG_PATH.exists():
        print("DEALIX_SAUDI_REVENUE_COMMAND_CENTER=FAIL")
        print("BLOCKERS=catalog file missing")
        print("NEXT_FOUNDER_ACTION=Create the service catalog file before running verifier.")
        return 1

    catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    line_map = {line.get("line_id"): line for line in catalog.get("service_lines", [])}

    for line_id, marker in REQUIRED_LINES.items():
        line = line_map.get(line_id)
        if not line:
            verdicts[marker] = "fail"
            blockers.append(f"Missing service line: {line_id}")
            continue

        services = line.get("services", [])
        if len(services) < 3:
            verdicts[marker] = "fail"
            blockers.append(f"{line_id} has less than 3 services")
            continue

        local_before = len(blockers)
        for idx, service in enumerate(services, start=1):
            _validate_service(service, blockers, f"{line_id}#{idx}")

        verdicts[marker] = "pass" if len(blockers) == local_before else "fail"

    hard_rules = set(catalog.get("hard_rules", []))
    missing_rules = sorted(REQUIRED_HARD_RULES - hard_rules)
    if missing_rules:
        blockers.append(f"Missing hard rules: {', '.join(missing_rules)}")

    research_context = catalog.get("research_context", [])
    if len(research_context) < 3:
        blockers.append("research_context must include at least 3 references")

    rendered = json.dumps(catalog, ensure_ascii=False).lower()
    for term in FORBIDDEN_TERMS:
        if term in rendered:
            blockers.append(f"Forbidden term detected: {term}")

    # Derived checks to align with operating model markers.
    verdicts["CUSTOMER_PORTAL"] = (
        "pass"
        if (
            "delivery_os" in line_map
            and "support_cs_os" in line_map
            and "proof_expansion_engine" in line_map
            and "arabic_first_customer_experience" in catalog.get("strategy_principles", [])
        )
        else "fail"
    )
    if verdicts["CUSTOMER_PORTAL"] == "fail":
        blockers.append("Customer portal readiness dependencies are incomplete")

    verdicts["EXPANSION_ENGINE"] = (
        "pass" if verdicts.get("PROOF_ENGINE") == "pass" else "fail"
    )
    verdicts["SECURITY"] = (
        "pass"
        if verdicts.get("TRUST_LAYER") == "pass" and not missing_rules
        else "fail"
    )
    verdicts["OBSERVABILITY"] = (
        "pass"
        if (
            all(verdicts.get(marker) == "pass" for marker in REQUIRED_LINES.values())
            and all(
                all(service.get("kpis") for service in line.get("services", []))
                for line in catalog.get("service_lines", [])
            )
        )
        else "fail"
    )

    if verdicts["EXPANSION_ENGINE"] == "fail":
        blockers.append("Expansion readiness depends on proof engine completeness")
    if verdicts["SECURITY"] == "fail":
        blockers.append("Security readiness depends on trust layer and hard rules")
    if verdicts["OBSERVABILITY"] == "fail":
        blockers.append("Observability readiness requires KPI coverage on all services")

    required_markers = [
        "MARKET_RADAR",
        "LEAD_INTELLIGENCE",
        "COMPANY_BRAIN",
        "WHATSAPP_DECISION_LAYER",
        "DECISION_PASSPORT",
        "ACTION_APPROVAL_ENGINE",
        "DELIVERY_OS",
        "CUSTOMER_PORTAL",
        "SUPPORT_OS",
        "PAYMENT_TRUTH",
        "PROOF_ENGINE",
        "EXPANSION_ENGINE",
        "LEARNING_FLYWHEEL",
        "TRUST_LAYER",
        "SECURITY",
        "OBSERVABILITY",
    ]

    overall_pass = all(verdicts.get(marker) == "pass" for marker in required_markers) and not blockers

    print(f"DEALIX_SAUDI_REVENUE_COMMAND_CENTER={'PASS' if overall_pass else 'FAIL'}")
    for marker in required_markers:
        print(f"{marker}={verdicts.get(marker, 'fail')}")
    print(f"FIRST_3_PAID_PILOTS_READY={'yes' if overall_pass else 'no'}")
    print(f"SELLABLE_NOW={'yes' if overall_pass else 'no'}")
    print(f"BLOCKERS={'none' if not blockers else '; '.join(blockers)}")
    if overall_pass:
        print("NEXT_FOUNDER_ACTION=Execute 30 warm intros using the Foundation offers this week.")
    else:
        print("NEXT_FOUNDER_ACTION=Close listed blockers and rerun verifier before outbound launch.")

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
