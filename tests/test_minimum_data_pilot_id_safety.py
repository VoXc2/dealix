"""Pseudonymous ID fields must not double as contact or credential storage."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from dealix.privacy.minimum_data import MinimumDataPilotDataset


def _valid() -> dict:
    return {
        "profile_id": "revenue_command_minimum_data_v1",
        "tenant_id": "tenant_demo_001",
        "company_id": "company_demo_001",
        "company_context_source_ref": "company_context_demo_001",
        "icp_id": "icp_demo_001",
        "workflow_id": "lead_to_cash_001",
        "acceptance_criteria_ref": "acceptance_demo_001",
        "approval_policy_ref": "policy_demo_001",
        "proof_target_id": "proof_demo_001",
        "accountable_owner_role": "founder",
        "baseline_metrics": [
            {
                "metric_id": "metric_001",
                "metric_definition_ref": "metric_definition_001",
                "value": 62.0,
                "unit": "percent",
                "source_ref": "source_aggregate_001",
                "measurement_window_ref": "window_previous_30_days",
            }
        ],
        "opportunities": [
            {
                "opportunity_id": "OPP-001",
                "stage": "proposal",
                "age_days": 10,
                "value_band": "medium",
                "next_action_status": "ready",
                "owner_role": "sales_manager",
                "source_ref": "source_aggregate_001",
            }
        ],
    }


@pytest.mark.parametrize(
    "path,value,error",
    [
        (("company_id",), "0501234567", "Saudi mobile number"),
        (("company_context_source_ref",), "0501234567", "Saudi mobile number"),
        (("icp_id",), "sk-abcdefghijklmnop1234", "credential/token pattern"),
        (("acceptance_criteria_ref",), "0501234567", "Saudi mobile number"),
        (("proof_target_id",), "sk-abcdefghijklmnop1234", "credential/token pattern"),
        (("baseline_metrics", 0, "source_ref"), "0501234567", "Saudi mobile number"),
        (
            ("baseline_metrics", 0, "metric_definition_ref"),
            "sk-abcdefghijklmnop1234",
            "credential/token pattern",
        ),
        (("opportunities", 0, "opportunity_id"), "0501234567", "Saudi mobile number"),
        (("opportunities", 0, "source_ref"), "sk-abcdefghijklmnop1234", "credential/token pattern"),
    ],
)
def test_contact_or_secret_patterns_cannot_be_used_as_opaque_ids(
    path: tuple[object, ...], value: str, error: str
) -> None:
    payload = _valid()
    target = payload
    for key in path[:-1]:
        target = target[key]  # type: ignore[index]
    target[path[-1]] = value  # type: ignore[index]

    with pytest.raises(ValidationError, match=error):
        MinimumDataPilotDataset.model_validate(payload)
