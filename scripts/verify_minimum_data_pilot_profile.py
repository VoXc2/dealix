#!/usr/bin/env python3
"""Fail-closed verifier for Dealix's minimum-data first-pilot profile.

This is a repository contract only. It never reads customer data, connects to a
provider, or makes a legal conclusion. It proves that the checked-in profile
cannot silently authorize personal data, free-text customer notes, external
send, payment, production mutation, or public customer claims while the broader
privacy gate is open.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from dealix.privacy.minimum_data import MinimumDataPilotDataset

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "dealix" / "config" / "minimum_data_pilot_profile.yaml"

REQUIRED_BLOCKS = (
    "personal_data_allowed",
    "sensitive_personal_data_allowed",
    "raw_contact_data_allowed",
    "raw_message_bodies_allowed",
    "meeting_transcripts_allowed",
    "customer_file_uploads_allowed",
    "crm_raw_export_allowed",
    "payment_or_bank_data_allowed",
    "identity_documents_allowed",
    "employee_hr_data_allowed",
    "health_data_allowed",
    "credentials_or_secrets_allowed",
    "external_send_allowed",
    "live_checkout_or_charge_allowed",
    "production_mutation_allowed",
    "legal_or_compliance_conclusion_allowed",
)

REQUIRED_ALLOWED_CLASSES = {
    "company_public_facts",
    "company_operating_context",
    "pseudonymous_opportunity",
    "aggregate_baseline_metric",
    "approval_metadata",
    "non_personal_proof_event",
    "technical_run_metadata",
}

REQUIRED_PROHIBITED_FIELDS = {
    "personal_email",
    "work_email",
    "phone",
    "whatsapp_number",
    "linkedin_profile",
    "national_id",
    "iqama",
    "passport",
    "bank_account",
    "iban",
    "card_data",
    "health_record",
    "employee_record",
    "message_body",
    "transcript",
    "recording",
    "api_key",
    "password",
    "access_token",
    "refresh_token",
}

REQUIRED_OUTPUT_BLOCKS = {
    "customer_facing_send",
    "invoice_or_payment_request",
    "legal_compliance_opinion",
    "public_customer_claim",
}

REQUIRED_MINIMUM_INPUTS = {
    "tenant_id",
    "company_id",
    "company_context_source_ref",
    "icp_id",
    "workflow_id",
    "acceptance_criteria_ref",
    "accountable_owner_role",
    "approval_policy_ref",
    "proof_target_id",
    "baseline_metrics",
}


def _load() -> dict[str, Any]:
    data = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise AssertionError("minimum-data pilot profile must be a mapping")
    return data


def validate(profile: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    if profile.get("status") != "technical_profile_only":
        errors.append("status must remain technical_profile_only")
    if profile.get("legal_effect") != "none":
        errors.append("legal_effect must remain none")

    product = profile.get("product") or {}
    if product.get("motion") != "revenue_command_pilot_30d":
        errors.append("profile must remain bound to revenue_command_pilot_30d")
    if product.get("one_icp") is not True or product.get("one_revenue_workflow") is not True:
        errors.append("profile must remain one-ICP / one-workflow")

    hard_blocks = profile.get("hard_blocks") or {}
    for key in REQUIRED_BLOCKS:
        if hard_blocks.get(key) is not False:
            errors.append(f"hard_blocks.{key} must be false")

    allowed = profile.get("allowed_data_classes") or []
    allowed_ids = {
        item.get("id")
        for item in allowed
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    missing_allowed = REQUIRED_ALLOWED_CLASSES - allowed_ids
    if missing_allowed:
        errors.append(f"missing allowed data classes: {sorted(missing_allowed)}")
    for item in allowed:
        if not isinstance(item, dict):
            errors.append("allowed_data_classes entries must be mappings")
            continue
        if item.get("provenance_required") is not True:
            errors.append(f"provenance must be required for {item.get('id')!r}")

    prohibited_fields = set(profile.get("prohibited_fields") or [])
    missing_prohibited = REQUIRED_PROHIBITED_FIELDS - prohibited_fields
    if missing_prohibited:
        errors.append(f"missing prohibited fields: {sorted(missing_prohibited)}")

    free_text = profile.get("free_text_policy") or {}
    if free_text.get("default_allowed") is not False:
        errors.append("free_text_policy.default_allowed must be false")
    if free_text.get("allowed_fields") not in ([], None):
        errors.append("minimum-data typed dataset must not authorize arbitrary free-text fields")
    rule = str(free_text.get("rule") or "").casefold()
    if "reject/quarantine" not in rule:
        errors.append("free-text rule must reject/quarantine suspected personal content")

    minimum_inputs = set(profile.get("minimum_required_inputs") or [])
    missing_inputs = REQUIRED_MINIMUM_INPUTS - minimum_inputs
    if missing_inputs:
        errors.append(f"minimum required inputs missing: {sorted(missing_inputs)}")
    schema_fields = set(MinimumDataPilotDataset.model_fields)
    unsupported_inputs = minimum_inputs - schema_fields
    if unsupported_inputs:
        errors.append(
            "minimum required inputs are not represented by typed dataset: "
            f"{sorted(unsupported_inputs)}"
        )

    outputs = profile.get("outputs") or {}
    output_blocks = set(outputs.get("prohibited") or [])
    missing_output_blocks = REQUIRED_OUTPUT_BLOCKS - output_blocks
    if missing_output_blocks:
        errors.append(f"missing prohibited outputs: {sorted(missing_output_blocks)}")

    fail_closed = profile.get("fail_closed") or {}
    expected_fail_closed = {
        "missing_profile_or_dataset_approval": "reject",
        "unknown_data_class": "reject",
        "prohibited_field_present": "reject",
        "personal_data_detected_or_suspected": "quarantine",
        "sensitive_data_detected_or_suspected": "quarantine",
        "external_effect_requested": "approval_block_and_product_block",
        "legal_or_compliance_conclusion_requested": "human_only",
    }
    for key, value in expected_fail_closed.items():
        if fail_closed.get(key) != value:
            errors.append(f"fail_closed.{key} must be {value}")

    exit_conditions = profile.get("exit_conditions") or {}
    start_conditions = set(exit_conditions.get("pilot_can_start_only_if") or [])
    for condition in (
        "named_customer_scope_approved",
        "this_profile_is_accepted_for_the_exact_dataset",
        "no_personal_or_sensitive_data_is_required_for_the_scoped_workflow",
        "baseline_and_proof_path_are_defined",
        "approval_owner_and_delivery_owner_are_defined",
        "production_and_tenant_controls_required_by_the_workflow_are_green",
    ):
        if condition not in start_conditions:
            errors.append(f"pilot start condition missing: {condition}")

    return errors


def main() -> int:
    errors = validate(_load())
    if errors:
        print("MINIMUM_DATA_PILOT_PROFILE=FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("MINIMUM_DATA_PILOT_PROFILE=PASS")
    print(
        "personal_data=false free_text=false external_send=false "
        "live_charge=false production_mutation=false"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
