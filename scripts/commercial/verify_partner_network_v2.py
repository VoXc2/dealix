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
LEGACY_DATA_ROOM_PROGRAM = ROOT / "business/data-room/PARTNER_PROGRAM.md"
LEGACY_DATA_ROOM_TERMS = ROOT / "business/data-room/STRATEGIC_PARTNERSHIP_TERMS.md"
LEGACY_MARKETING_QUARANTINE = ROOT / "data/commercial/legacy_marketing_quarantine.json"
COMMISSION_ENGINE = ROOT / "integrations/partner_portal/commission_engine.py"
PARTNER_API = ROOT / "integrations/partner_portal/api.py"


def fail(message: str) -> None:
    raise SystemExit(f"PARTNER_NETWORK_V2=FAIL reason={message}")


def main() -> None:
    for path in (PARTNER_RULES, AFFILIATE_RULES, SCHEMA, POLICY, ENABLEMENT, TERMS, PACKAGES, ONBOARDING, LAUNCH_COPY, SECTOR_ROUTING, COMMISSION_ENGINE, PARTNER_API):
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
    authority_rules = v2.get("authority_rules") or {}
    for key in ("one_company_machine", "no_parallel_partner_crm", "customer_specific_pricing_only", "portal_payment_execution_authority"):
        expected = key != "portal_payment_execution_authority"
        if authority_rules.get(key) is not expected:
            fail(f"authority_rule_drift:{key}")
    if not (v2.get("qualification") or {}).get("partner_application_required"):
        fail("partner_qualification_gate_missing")
    if not (v2.get("anti_fraud") or []):
        fail("anti_fraud_rules_missing")

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
    if affiliate_rules.get("legacy_reference_only") is not True:
        fail("legacy_affiliate_reference_not_marked")
    if (affiliate_rules.get("payout") or {}).get("only_after_event") != "verified_cash_collected":
        fail("legacy_payout_trigger_not_collection_based")

    engine_text = COMMISSION_ENGINE.read_text(encoding="utf-8")
    if 'commission.status = "paid"' in engine_text or 'reference=f"PAY-' in engine_text:
        fail("portal_fabricates_payment_truth")
    if "legacy_projection_not_payable" not in engine_text:
        fail("legacy_projection_payment_gate_missing")
    api_text = PARTNER_API.read_text(encoding="utf-8")
    for key in ("verified_collection_required_for_commission", "deal_value_is_not_commissionable_cash", "legacy_projection_is_not_payable"):
        if key not in api_text:
            fail(f"portal_hard_gate_missing:{key}")

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

    for legacy_path in (LEGACY_DATA_ROOM_PROGRAM, LEGACY_DATA_ROOM_TERMS, LEGACY_MARKETING_QUARANTINE):
        if not legacy_path.is_file():
            fail(f"missing_legacy_quarantine_surface:{legacy_path.relative_to(ROOT)}")

    legacy_program = LEGACY_DATA_ROOM_PROGRAM.read_text(encoding="utf-8")
    legacy_terms = LEGACY_DATA_ROOM_TERMS.read_text(encoding="utf-8")
    if "SUPERSEDED FOR COMMERCIAL AUTHORITY" not in legacy_program:
        fail("legacy_data_room_program_not_superseded")
    if "partners@dealix.local" in legacy_program:
        fail("invalid_local_partner_contact_present")
    if "SUPERSEDED FOR COMMERCIAL AUTHORITY" not in legacy_terms:
        fail("legacy_data_room_terms_not_superseded")
    for retired_term in ("Agency partner: 10%", "Consulting partner: 12%", "Training partner: revenue share 15%"):
        if retired_term in legacy_terms:
            fail(f"legacy_partner_rate_present:{retired_term}")

    quarantine = json.loads(LEGACY_MARKETING_QUARANTINE.read_text(encoding="utf-8"))
    authority = quarantine.get("authority") or {}
    if authority.get("current_entry_offer") != "Free Execution Diagnostic":
        fail("legacy_quarantine_entry_offer_drift")
    if authority.get("public_fixed_pilot_price_authorized") is not False:
        fail("legacy_quarantine_public_fixed_price_not_blocked")
    quarantined = set(quarantine.get("historical_surfaces_to_treat_as_non_authoritative_unless_reconciled") or [])
    for required_surface in (
        "business/data-room/PARTNER_PROGRAM.md",
        "business/data-room/STRATEGIC_PARTNERSHIP_TERMS.md",
        "docs/AGENCY_PARTNER_PITCH.md",
    ):
        if required_surface not in quarantined:
            fail(f"legacy_partner_surface_not_quarantined:{required_surface}")

    print("PARTNER_NETWORK_V2=PASS")
    print("AUTHORITY=dealix.commercial.partner_program_v2")
    print("SERVICES=7.5%-20%_MARGIN_GOVERNED")
    print("SAAS=20%-30%_MAX_12_MONTHS")
    print("ATTRIBUTION=120_DAYS_EXTENDABLE_TO_180")
    print("PAYOUT_TRUTH=STAGED_NOT_PAID_UNTIL_EXTERNAL_RECEIPT")
    print("COMPLIANCE=PDPL_CONSENT_B2G_HOLD_NO_COLD_WHATSAPP")


if __name__ == "__main__":
    main()
