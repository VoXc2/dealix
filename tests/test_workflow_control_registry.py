"""Governance workflow_control_registry expansion."""

from __future__ import annotations

from auto_client_acquisition.governance_os.workflow_control_registry import (
    control_classes_for,
    workflow_domain_is_governed,
)


def test_revenue_intake_outreach_is_governed() -> None:
    assert workflow_domain_is_governed("revenue_intake_outreach")
    assert "external_action" in control_classes_for("revenue_intake_outreach")


def test_partner_channel_is_governed() -> None:
    assert workflow_domain_is_governed("partner_channel")
    assert "contract_commitment" in control_classes_for("partner_channel")


def test_support_desk_resolution_is_governed() -> None:
    assert workflow_domain_is_governed("support_desk_resolution")
    assert "data_export" in control_classes_for("support_desk_resolution")


def test_procurement_intake_is_governed() -> None:
    assert workflow_domain_is_governed("procurement_intake")
    assert "contract_commitment" in control_classes_for("procurement_intake")


def test_back_office_automation_is_governed() -> None:
    assert workflow_domain_is_governed("back_office_automation")
    assert "irreversible_action" in control_classes_for("back_office_automation")
