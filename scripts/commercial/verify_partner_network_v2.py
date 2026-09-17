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
    PARTNER_POLICY_VERSION,
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
V3_ROOT = ROOT / "docs/partners/v3"
V3_SCHEMA = V3_ROOT / "13_OPERATING_SCHEMA.json"
V3_RECEIPT = V3_ROOT / "EXECUTION_RECEIPT_2026-09-17.md"


def fail(message: str) -> None:
    raise SystemExit(f"PARTNER_NETWORK_V2=FAIL reason={message}")


def main() -> None:
    for path in (PARTNER_RULES, AFFILIATE_RULES, SCHEMA, POLICY, ENABLEMENT, TERMS, PACKAGES, ONBOARDING, LAUNCH_COPY, SECTOR_ROUTING, COMMISSION_ENGINE, PARTNER_API, V3_SCHEMA, V3_RECEIPT):
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

    hard_holds = set(v2.get("hard_holds") or [])
    for required_hold in (
        "non_saudi_independent_activity_without_authorization",
        "possible_employment_relationship",
        "mlm_or_downline_commission",
        "commercial_agency_or_regulated_brokerage_without_review",
    ):
        if required_hold not in hard_holds:
            fail(f"v3_hard_hold_missing:{required_hold}")
    if authority_rules.get("recruitment_only_commission") is not False:
        fail("v3_recruitment_only_commission_not_blocked")
    if authority_rules.get("downline_override_commission") is not False:
        fail("v3_downline_override_not_blocked")
    if authority_rules.get("policy_version_pinning_required") is not True:
        fail("v3_policy_version_pinning_missing")
    if authority_rules.get("material_state_change_receipts_required") is not True:
        fail("v3_material_receipts_missing")

    v3 = v2.get("v3_hardening") or {}
    if v3.get("authority") != "dealix.commercial.partner_program_v2":
        fail("v3_wrong_authority")
    if v3.get("policy_version") != PARTNER_POLICY_VERSION:
        fail("v3_policy_version_drift")
    if set(v3.get("activation_requires") or []) != {
        "legal_classification_clear", "tax_profile_recorded", "terms_accepted", "certification_passed"
    }:
        fail("v3_activation_gate_drift")
    no_mlm = v3.get("no_mlm") or {}
    if no_mlm.get("recruitment_only_commission") is not False or no_mlm.get("downline_override_commission") is not False:
        fail("v3_no_mlm_drift")
    if no_mlm.get("multi_partner_split_requires_same_opportunity_contribution") is not True:
        fail("v3_multi_partner_split_gate_missing")
    receipts = v3.get("receipts") or {}
    if receipts.get("policy_version_required") is not True or receipts.get("deterministic_content_hash_required") is not True:
        fail("v3_receipt_gate_missing")

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
        "partner_disclosure_required",
        "approved_asset_required",
        "guaranteed_income_claims_prohibited",
        "recruitment_only_commission_prohibited",
        "downline_override_commission_prohibited",
        "non_saudi_independent_activity_authorization_required",
        "possible_employment_relationship_hold",
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
    for key in (
        "verified_collection_required_for_commission",
        "deal_value_is_not_commissionable_cash",
        "legacy_projection_is_not_payable",
        "legal_classification_required_for_activation",
        "tier_upgrade_requires_verified_economic_quality",
        "referral_count_does_not_auto_upgrade_tier",
    ):
        if key not in api_text:
            fail(f"portal_hard_gate_missing:{key}")

    v3_schema = json.loads(V3_SCHEMA.read_text(encoding="utf-8"))
    if v3_schema.get("authority") != "canonical_company_machine_only":
        fail("v3_schema_parallel_authority")
    invariants = set(v3_schema.get("hard_invariants") or [])
    for invariant in (
        "public_contact_never_equals_consent",
        "no_mlm_or_downline_commission",
        "non_saudi_independent_activity_requires_authorization_proof",
        "payout_requires_external_receipt",
    ):
        if invariant not in invariants:
            fail(f"v3_schema_invariant_missing:{invariant}")
    receipt_text = V3_RECEIPT.read_text(encoding="utf-8")
    for receipt_term in ("No PR merge", "No production deploy", "No payout/bank transfer"):
        if receipt_term not in receipt_text:
            fail(f"v3_execution_receipt_gate_missing:{receipt_term}")

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
    print(f"V3_POLICY={PARTNER_POLICY_VERSION}")
    print("V3_HARDENING=LEGAL_CLASSIFICATION_NO_MLM_POLICY_RECEIPTS")


if __name__ == "__main__":
    main()
