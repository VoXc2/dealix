#!/usr/bin/env python3
"""Fail-closed source verifier for Dealix Partner Network V2."""
from __future__ import annotations

import json
import sys
from decimal import Decimal
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from dealix.commercial.partner_program_v2 import (
    ATTRIBUTION_PROTECTION_DAYS,
    DEFAULT_CLEARING_DAYS,
    DEFAULT_SAAS_COMMISSION_MONTHS,
    SAAS_RATES,
    SERVICE_RATES,
)

PARTNER_RULES = ROOT / "dealix/config/partner_rules.yaml"
AFFILIATE_RULES = ROOT / "dealix/config/affiliate_rules.yaml"
SCHEMA = ROOT / "schemas/partner_deal_registration_v2.schema.json"
POLICY = ROOT / "docs/partners/PARTNER_NETWORK_V2.md"
ENABLEMENT = ROOT / "docs/partners/PARTNER_MARKETER_ENABLEMENT_V2_AR_EN.md"
TERMS = ROOT / "docs/partners/PARTNER_TERMS_V2_DRAFT.md"
PACKAGES = ROOT / "docs/partners/PARTNER_PACKAGES.md"
ONBOARDING = ROOT / "docs/partners/PARTNER_ONBOARDING.md"
LAUNCH_COPY = ROOT / "docs/partners/PARTNER_LAUNCH_COPY_V2_AR_EN.md"
SECTOR_ROUTING = ROOT / "docs/partners/PARTNER_SECTOR_ROUTING_V2.md"


def fail(message: str) -> None:
    raise SystemExit(f"PARTNER_NETWORK_V2=FAIL reason={message}")


def main() -> None:
    for path in (PARTNER_RULES, AFFILIATE_RULES, SCHEMA, POLICY, ENABLEMENT, TERMS, PACKAGES, ONBOARDING, LAUNCH_COPY, SECTOR_ROUTING):
        if not path.is_file():
            fail(f"missing:{path.relative_to(ROOT)}")

    partner_rules = yaml.safe_load(PARTNER_RULES.read_text(encoding="utf-8")) or {}
    v2 = partner_rules.get("partner_network_v2") or {}
    if v2.get("authority") != "dealix.commercial.partner_program_v2":
        fail("wrong_authority")
    if v2.get("protection_days") != ATTRIBUTION_PROTECTION_DAYS:
        fail("protection_window_drift")
    if v2.get("clearing_days") != DEFAULT_CLEARING_DAYS:
        fail("clearing_days_drift")
    if v2.get("saas_commission_months") != DEFAULT_SAAS_COMMISSION_MONTHS:
        fail("saas_window_drift")

    config_service = {k: Decimal(str(v)) for k, v in (v2.get("service_rates") or {}).items()}
    code_service = dict(SERVICE_RATES)
    config_saas = {k: Decimal(str(v)) for k, v in (v2.get("saas_rates") or {}).items()}
    code_saas = dict(SAAS_RATES)
    if config_service != code_service:
        fail("service_rate_drift")
    if config_saas != code_saas:
        fail("saas_rate_drift")

    affiliate_rules = yaml.safe_load(AFFILIATE_RULES.read_text(encoding="utf-8")) or {}
    compliance = affiliate_rules.get("partner_network_v2_compliance") or {}
    required_true = (
        "marketing_consent_required",
        "consent_evidence_required",
        "sender_identity_required",
        "opt_out_required",
        "cold_whatsapp_prohibited",
        "government_or_tender_requires_review",
        "government_official_or_employee_hold",
        "influence_based_compensation_prohibited",
        "public_claims_require_evidence",
    )
    missing = [key for key in required_true if compliance.get(key) is not True]
    if missing:
        fail(f"compliance_gate_missing:{','.join(missing)}")
    if compliance.get("pricing_authority") != "dealix_only":
        fail("pricing_authority_not_dealix_only")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    required = set(schema.get("required") or [])
    for key in ("partner_id", "partner_motion", "relationship_evidence", "consent_status", "government_or_tender"):
        if key not in required:
            fail(f"schema_required_missing:{key}")

    joined = "\n".join(
        path.read_text(encoding="utf-8") for path in (POLICY, ENABLEMENT, TERMS, PACKAGES, ONBOARDING, LAUNCH_COPY, SECTOR_ROUTING)
    ).lower()
    required_terms = (
        "nccr",
        "verified collected",
        "120 days",
        "180 days",
        "cold whatsapp",
        "government",
        "customer-specific quote",
        "staged_not_paid",
    )
    for term in required_terms:
        if term not in joined:
            fail(f"documentation_missing:{term}")

    packages_text = PACKAGES.read_text(encoding="utf-8")
    for retired_price in ("3,000 SAR setup", "8,000 SAR setup", "25,000 SAR setup"):
        if retired_price in packages_text:
            fail(f"retired_fixed_partner_price_present:{retired_price}")
    if "No public fixed customer pricing authority" not in packages_text:
        fail("customer_specific_quote_authority_missing")

    print("PARTNER_NETWORK_V2=PASS")
    print("AUTHORITY=dealix.commercial.partner_program_v2")
    print("SERVICES=7.5%-20%_MARGIN_GOVERNED")
    print("SAAS=20%-30%_MAX_12_MONTHS")
    print("ATTRIBUTION=120_DAYS_EXTENDABLE_TO_180")
    print("PAYOUT_TRUTH=STAGED_NOT_PAID_UNTIL_EXTERNAL_RECEIPT")
    print("COMPLIANCE=PDPL_CONSENT_B2G_HOLD_NO_COLD_WHATSAPP")


if __name__ == "__main__":
    main()
