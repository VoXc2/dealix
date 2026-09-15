#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "data" / "commercial" / "public_pricing_authority_v1.json"
PRICING = ROOT / "api" / "routers" / "pricing.py"
AGENTS = ROOT / "AGENTS.md"


def fail(reason: str) -> None:
    raise SystemExit(f"DEALIX_PUBLIC_PRICING_AUTHORITY=FAIL reason={reason}")


def main() -> None:
    if not CONTRACT.exists():
        fail("contract_missing")
    data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    if data.get("schema") != "dealix.public_pricing_authority.v1":
        fail("schema_drift")
    if data.get("public_fixed_pricing") is not False:
        fail("public_fixed_pricing_reenabled")
    if data.get("public_checkout_authority") is not False:
        fail("public_checkout_authority_reenabled")
    if data.get("public_fixed_duration") is not False:
        fail("public_fixed_duration_reenabled")
    if data.get("environment_flags_may_create_public_price_authority") is not False:
        fail("env_flag_price_authority_reenabled")
    if data.get("customer_specific_quote_required") is not True:
        fail("customer_specific_quote_not_required")
    if data.get("payment_execution_requires_separate_authority") is not True:
        fail("payment_execution_not_separate")

    pricing = PRICING.read_text(encoding="utf-8")
    required_pricing_markers = [
        "TEST_ONLY_PLANS",
        "checkout_not_founder_approved",
        "pricing_catalog_unavailable",
    ]
    for marker in required_pricing_markers:
        if marker not in pricing:
            fail(f"pricing_guard_missing:{marker}")

    for marker in ("public_fixed_price = True", "PUBLIC_FIXED_PRICE = True"):
        if marker in pricing:
            fail(f"runtime_public_price_authority:{marker}")

    rules = "\n".join(data.get("agent_rules", [])).lower()
    for marker in (
        "never infer a current customer price",
        "customer-specific quote reference",
        "499 sar",
        "quote does not authorize payment execution",
        "payment truth requires verified payment evidence",
    ):
        if marker not in rules:
            fail(f"agent_rule_missing:{marker.replace(' ', '_')}")

    agents = AGENTS.read_text(encoding="utf-8").lower()
    for forbidden in ("always 499 sar", "canonical 499 sar", "current 7-day pilot"):
        if forbidden in agents:
            fail(f"agents_current_legacy_authority:{forbidden.replace(' ', '_')}")

    print("DEALIX_PUBLIC_PRICING_AUTHORITY=PASS")
    print("PUBLIC_FIXED_PRICING=BLOCKED")
    print("PUBLIC_FIXED_DURATION=BLOCKED")
    print("CUSTOMER_SPECIFIC_QUOTE=REQUIRED")
    print("ENV_FLAGS=NON_AUTHORITY")
    print("INVOICE_NE_PAYMENT=PASS")


if __name__ == "__main__":
    main()
