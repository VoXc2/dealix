"""Strict sellability verifier for Saudi AI provider operating system."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .catalog import (
    load_kpi_tree,
    load_playbook_catalog,
    load_pricing_model,
    load_risk_register,
    load_sellable_rules,
)


@dataclass(frozen=True)
class VerificationResult:
    sellable_now: bool
    blockers: list[str]
    marker_results: dict[str, str]
    next_founder_action: str


def _all_service_ids(pricing_model: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for engine in sorted(pricing_model["service_matrix"].keys()):
        for tier in ("BRONZE", "SILVER", "GOLD"):
            ids.append(f"{engine}_{tier}")
    return ids


def verify_sellable() -> VerificationResult:
    rules = load_sellable_rules()
    pricing = load_pricing_model()
    kpis = load_kpi_tree()
    playbooks = load_playbook_catalog()
    risks = load_risk_register()

    blockers: list[str] = []
    markers: dict[str, str] = {}
    service_ids = _all_service_ids(pricing)

    required_fields = set(rules["required_fields"])
    blocking_conditions = set(rules["blocking_conditions"])
    data_sensitive_engines = {
        "LEAD_INTELLIGENCE",
        "WHATSAPP_DECISION_LAYER",
        "CUSTOMER_PORTAL",
        "SUPPORT_OS",
        "PAYMENT_TRUTH",
        "TRUST_LAYER",
        "SECURITY",
        "OBSERVABILITY",
        "PROOF_ENGINE",
    }

    for service_id in service_ids:
        engine, tier = service_id.rsplit("_", 1)
        tier_l = tier.lower()

        engine_pricing = pricing["service_matrix"].get(engine)
        if not engine_pricing:
            blockers.append(f"{service_id}: missing_price")
            continue
        tier_pricing = engine_pricing["tiers"].get(tier_l)
        if not tier_pricing:
            blockers.append(f"{service_id}: missing_price")
            continue

        if "buyer" in required_fields and not engine_pricing.get("requires"):
            blockers.append(f"{service_id}: missing_buyer")

        if "pricing" in required_fields:
            for field in (
                "setup_fee_sar",
                "monthly_retainer_sar",
                "gross_margin_target",
                "delivery_hours_estimate",
                "minimum_contract_months",
                "discount_floor",
            ):
                if field not in tier_pricing:
                    blockers.append(f"{service_id}: missing_price ({field})")

        engine_kpis = kpis.get(engine)
        if not engine_kpis:
            blockers.append(f"{service_id}: missing_kpis")
        else:
            for key in ("north_star", "business_kpis", "operational_kpis", "guardrail_kpis"):
                if key not in engine_kpis:
                    blockers.append(f"{service_id}: missing_kpis ({key})")

        engine_playbook = playbooks.get(engine, {})
        tier_playbook = engine_playbook.get("tiers", {}).get(tier_l)
        if not tier_playbook:
            blockers.append(f"{service_id}: missing_delivery_playbook")
        else:
            if "decision" in required_fields and not tier_playbook.get("decision_gate"):
                blockers.append(f"{service_id}: missing_decision")
            if "implementation_steps" in required_fields and not tier_playbook.get(
                "implementation_steps"
            ):
                blockers.append(f"{service_id}: missing_implementation_steps")
            if "acceptance_criteria" in required_fields and not tier_playbook.get(
                "acceptance_criteria"
            ):
                blockers.append(f"{service_id}: missing_acceptance_criteria")
            if "security_review" in required_fields and not tier_playbook.get("security_review"):
                blockers.append(f"{service_id}: missing_security_review")
            for req in (
                "decision_gate",
                "implementation_steps",
                "acceptance_criteria",
                "rollout_plan",
                "rollback_plan",
                "owner",
                "security_review",
            ):
                if req not in tier_playbook:
                    blockers.append(f"{service_id}: missing playbook field {req}")
            if "owner" not in tier_playbook:
                blockers.append(f"{service_id}: missing_owner")
            if "rollout_plan" not in tier_playbook:
                blockers.append(f"{service_id}: no_rollout_plan")

        engine_risks = risks.get(engine, [])
        if "risks" in required_fields and not engine_risks:
            blockers.append(f"{service_id}: missing risk register")
        else:
            for risk in engine_risks:
                if risk.get("blocker") and not str(risk.get("mitigation", "")).strip():
                    blockers.append(f"{service_id}: risk blocker without mitigation")

        if "evidence" in required_fields:
            if not engine_kpis or not engine_kpis.get("target_benchmarks"):
                blockers.append(f"{service_id}: missing_evidence")

        requires_text = " ".join(engine_pricing.get("requires", []))
        not_sellable_flags = " ".join(engine_pricing.get("not_sellable_if", []))
        if "missing_data_policy" in blocking_conditions and engine in data_sensitive_engines:
            has_data_policy_signal = (
                "DATA" in requires_text
                or "POLICY" in requires_text
                or "CONSENT" in requires_text
                or "CONSENT" in not_sellable_flags
                or "NO_DATA_POLICY" in not_sellable_flags
                or "NO_SECURITY_APPROVAL" in not_sellable_flags
            )
            if not has_data_policy_signal:
                blockers.append(f"{service_id}: missing_data_policy")

    # Basic check that test coverage exists for the operating system package.
    if "no_test_coverage" in blocking_conditions:
        expected_tests = [
            Path("tests/test_saudi_ai_provider_cli.py"),
            Path("tests/test_saudi_ai_provider_pricing.py"),
            Path("tests/test_saudi_ai_provider_kpis.py"),
            Path("tests/test_offer_generation.py"),
        ]
        if not all(path.exists() for path in expected_tests):
            blockers.append("global: no_test_coverage")

    # marker outputs aligned with command-center verifier style
    markers["PRICING"] = "pass" if not any("missing_price" in b for b in blockers) else "fail"
    markers["DELIVERY_PLAYBOOKS"] = (
        "pass" if not any("missing_delivery_playbook" in b for b in blockers) else "fail"
    )
    markers["KPI_TREE"] = "pass" if not any("missing_kpis" in b for b in blockers) else "fail"
    markers["RISK_REGISTER"] = (
        "pass" if not any("risk register" in b for b in blockers) else "fail"
    )
    markers["SECURITY_REVIEW"] = (
        "pass" if not any("security_review" in b for b in blockers) else "fail"
    )

    # Explicitly include configured blocking conditions for transparency.
    for condition in sorted(blocking_conditions):
        condition_hit = any(condition in blocker for blocker in blockers)
        markers[condition.upper()] = "fail" if condition_hit else "pass"

    sellable_now = len(blockers) == 0
    next_action = (
        "Run package and quote flows, then start demos for top 3 target segments."
        if sellable_now
        else f"Close first blocker: {blockers[0]}"
    )
    return VerificationResult(
        sellable_now=sellable_now,
        blockers=blockers,
        marker_results=markers,
        next_founder_action=next_action,
    )


def print_verification_report(result: VerificationResult) -> None:
    print(f"SELLABLE_NOW={'true' if result.sellable_now else 'false'}")
    print(f"DELIVERABLE_NOW={'true' if result.sellable_now else 'false'}")
    for key in sorted(result.marker_results.keys()):
        print(f"{key}={result.marker_results[key]}")
    if result.blockers:
        print("WHY_NOT_SELLABLE:")
        for blocker in result.blockers:
            print(f"- {blocker}")
    else:
        print("WHY_NOT_SELLABLE: none")
    print(f"NEXT_FOUNDER_ACTION: {result.next_founder_action}")
