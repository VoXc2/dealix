"""Regression contracts for the first real-customer minimum-data Pilot profile."""

from __future__ import annotations

from pathlib import Path

import yaml

from scripts.verify_minimum_data_pilot_profile import validate

ROOT = Path(__file__).resolve().parents[1]
PROFILE_PATH = ROOT / "dealix" / "config" / "minimum_data_pilot_profile.yaml"


def _profile() -> dict:
    value = yaml.safe_load(PROFILE_PATH.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def test_profile_passes_fail_closed_verifier() -> None:
    assert validate(_profile()) == []


def test_profile_never_authorizes_personal_data_or_external_effects() -> None:
    blocks = _profile()["hard_blocks"]
    for key in (
        "personal_data_allowed",
        "sensitive_personal_data_allowed",
        "raw_contact_data_allowed",
        "raw_message_bodies_allowed",
        "meeting_transcripts_allowed",
        "customer_file_uploads_allowed",
        "crm_raw_export_allowed",
        "payment_or_bank_data_allowed",
        "credentials_or_secrets_allowed",
        "external_send_allowed",
        "live_checkout_or_charge_allowed",
        "production_mutation_allowed",
        "legal_or_compliance_conclusion_allowed",
    ):
        assert blocks[key] is False, key


def test_profile_requires_pseudonymous_and_aggregate_business_evidence() -> None:
    profile = _profile()
    allowed = {item["id"]: item for item in profile["allowed_data_classes"]}
    assert "pseudonymous_opportunity" in allowed
    assert "aggregate_baseline_metric" in allowed
    assert "non_personal_proof_event" in allowed
    assert all(item["provenance_required"] is True for item in allowed.values())


def test_profile_rejects_contact_content_payment_and_secrets() -> None:
    prohibited = set(_profile()["prohibited_fields"])
    for field in (
        "work_email",
        "phone",
        "whatsapp_number",
        "linkedin_profile",
        "message_body",
        "transcript",
        "bank_account",
        "iban",
        "card_data",
        "api_key",
        "password",
        "access_token",
        "refresh_token",
    ):
        assert field in prohibited


def test_profile_has_no_legal_effect_claim() -> None:
    profile = _profile()
    assert profile["status"] == "technical_profile_only"
    assert profile["legal_effect"] == "none"
    assert profile["hard_blocks"]["legal_or_compliance_conclusion_allowed"] is False


def test_customer_proof_stays_same_company_and_source_bound() -> None:
    labels = _profile()["proof_labels"]
    assert labels["synthetic"] == "never_customer_proof"
    assert labels["internal_dealix"] == "internal_only"
    assert (
        labels["minimum_data_customer_pilot"]
        == "customer_evidence_only_if_same_company_and_source_bound"
    )
    assert labels["publication"] == "separate_written_permission_required"


def test_pilot_cannot_start_from_profile_alone() -> None:
    conditions = set(_profile()["exit_conditions"]["pilot_can_start_only_if"])
    assert "named_customer_scope_approved" in conditions
    assert "this_profile_is_accepted_for_the_exact_dataset" in conditions
    assert "no_personal_or_sensitive_data_is_required_for_the_scoped_workflow" in conditions
    assert "baseline_and_proof_path_are_defined" in conditions
    assert "approval_owner_and_delivery_owner_are_defined" in conditions
    assert "production_and_tenant_controls_required_by_the_workflow_are_green" in conditions
