"""Typed dataset gate for the no-personal-data first Pilot."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dealix.privacy.minimum_data import MinimumDataPilotDataset


def _valid() -> dict:
    return {
        "profile_id": "revenue_command_minimum_data_v1",
        "tenant_id": "tenant_demo_001",
        "company_id": "company_001",
        "company_context_source_ref": "company_context_001",
        "icp_id": "icp_001",
        "workflow_id": "lead_to_cash_001",
        "acceptance_criteria_ref": "acceptance_001",
        "approval_policy_ref": "policy_001",
        "proof_target_id": "proof_target_001",
        "accountable_owner_role": "founder",
        "baseline_metrics": [
            {
                "metric_id": "metric_followup_coverage",
                "metric_definition_ref": "metric_definition_followup_coverage",
                "value": 62.0,
                "unit": "percent",
                "source_ref": "source_customer_aggregate_001",
                "measurement_window_ref": "window_previous_30_days",
            }
        ],
        "opportunities": [
            {
                "opportunity_id": "OPP-017",
                "stage": "proposal",
                "age_days": 19,
                "value_band": "medium",
                "next_action_status": "missing",
                "owner_role": "sales_manager",
                "source_ref": "source_customer_aggregate_001",
            }
        ],
    }


def test_valid_pseudonymous_aggregate_dataset_passes() -> None:
    dataset = MinimumDataPilotDataset.model_validate(_valid())
    assert dataset.company_id == "company_001"
    assert dataset.icp_id == "icp_001"
    assert dataset.company_context_source_ref == "company_context_001"
    assert dataset.opportunities[0].opportunity_id == "OPP-017"


@pytest.mark.parametrize(
    "field,value",
    [
        ("email", "person@example.com"),
        ("phone", "+966500000000"),
        ("message_body", "customer asked for discount"),
        ("linkedin_profile", "https://linkedin.example/person"),
        ("iban", "SA0000000000000000000000"),
        ("api_key", "sk-secret-example-value-123456"),
        ("company_offer_summary", "free text is not part of the typed minimum dataset"),
    ],
)
def test_unknown_personal_secret_or_free_text_field_is_rejected(
    field: str, value: str
) -> None:
    payload = _valid()
    payload[field] = value
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        MinimumDataPilotDataset.model_validate(payload)


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("company_context_source_ref", "0501234567", "Saudi mobile number"),
        ("icp_id", "sk-abcdefghijklmnop1234", "credential/token pattern"),
        ("acceptance_criteria_ref", "0501234567", "Saudi mobile number"),
    ],
)
def test_required_context_refs_cannot_smuggle_contact_or_secret_patterns(
    field: str, value: str, error: str
) -> None:
    payload = _valid()
    payload[field] = value
    with pytest.raises(ValidationError, match=error):
        MinimumDataPilotDataset.model_validate(payload)


def test_arbitrary_metric_text_fields_are_not_part_of_schema() -> None:
    payload = _valid()
    payload["baseline_metrics"][0]["metric_name"] = "Ahmed pipeline metric"
    payload["baseline_metrics"][0]["measurement_window"] = "previous 30 days"
    with pytest.raises(ValidationError, match="Extra inputs are not permitted"):
        MinimumDataPilotDataset.model_validate(payload)


def test_duplicate_opportunity_ids_are_rejected() -> None:
    payload = _valid()
    payload["opportunities"].append(dict(payload["opportunities"][0]))
    with pytest.raises(ValidationError, match="opportunity_id values must be unique"):
        MinimumDataPilotDataset.model_validate(payload)


def test_duplicate_metric_ids_are_rejected() -> None:
    payload = _valid()
    payload["baseline_metrics"].append(dict(payload["baseline_metrics"][0]))
    with pytest.raises(ValidationError, match="metric_id values must be unique"):
        MinimumDataPilotDataset.model_validate(payload)


def test_profile_id_cannot_be_switched_to_broader_data_mode() -> None:
    payload = _valid()
    payload["profile_id"] = "full_crm_import"
    with pytest.raises(ValidationError):
        MinimumDataPilotDataset.model_validate(payload)
