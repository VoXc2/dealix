"""Registry of governance control classes by workflow domain."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ControlRule:
    control_class: str
    approval_required: bool
    rollback_plan_required: bool


_WORKFLOW_CONTROL_RULES: dict[str, tuple[ControlRule, ...]] = {
    "revenue_outreach": (
        ControlRule("external_action", True, False),
        ControlRule("pricing_commitment", True, False),
    ),
    "revenue_intake_outreach": (
        ControlRule("external_action", True, False),
        ControlRule("data_export", True, False),
        ControlRule("pricing_commitment", True, False),
    ),
    "delivery_execution": (
        ControlRule("data_export", True, False),
        ControlRule("irreversible_action", True, True),
    ),
    "customer_success": (
        ControlRule("external_action", True, False),
        ControlRule("contract_commitment", True, False),
    ),
    "support_desk_resolution": (
        ControlRule("external_action", True, False),
        ControlRule("data_export", True, False),
    ),
    "partner_channel": (
        ControlRule("external_action", True, False),
        ControlRule("contract_commitment", True, False),
        ControlRule("pricing_commitment", True, False),
    ),
    "back_office_automation": (
        ControlRule("data_export", True, False),
        ControlRule("irreversible_action", True, True),
    ),
    "procurement_intake": (
        ControlRule("data_export", True, False),
        ControlRule("contract_commitment", True, False),
        ControlRule("external_action", True, False),
    ),
    "finance_reporting": (
        ControlRule("data_export", True, False),
        ControlRule("pricing_commitment", True, False),
    ),
    "product_release": (
        ControlRule("irreversible_action", True, True),
        ControlRule("autonomy_change", True, False),
    ),
    "executive_reporting": (
        ControlRule("data_export", True, False),
        ControlRule("external_action", True, False),
    ),
    "self_evolving": (
        ControlRule("self_evolving_apply", True, True),
        ControlRule("autonomy_change", True, True),
    ),
    "compliance_pdpl": (
        ControlRule("data_export", True, False),
        ControlRule("external_action", True, False),
        ControlRule("irreversible_action", True, True),
    ),
    "billing_collections": (
        ControlRule("pricing_commitment", True, False),
        ControlRule("contract_commitment", True, False),
        ControlRule("external_action", True, False),
    ),
    "ai_model_routing": (
        ControlRule("autonomy_change", True, False),
        ControlRule("pricing_commitment", True, False),
        ControlRule("data_export", True, False),
    ),
    "capital_allocation": (
        ControlRule("pricing_commitment", True, False),
        ControlRule("contract_commitment", True, False),
        ControlRule("data_export", True, False),
    ),
}

_GOVERNED_DOMAIN_COUNT = len(_WORKFLOW_CONTROL_RULES)


def workflow_controls(workflow_domain: str) -> tuple[ControlRule, ...]:
    """Return the controls for a workflow domain."""
    return _WORKFLOW_CONTROL_RULES.get(workflow_domain, ())


def workflow_domain_is_governed(workflow_domain: str) -> bool:
    return len(workflow_controls(workflow_domain)) > 0


def control_classes_for(workflow_domain: str) -> tuple[str, ...]:
    return tuple(rule.control_class for rule in workflow_controls(workflow_domain))


def governed_workflow_domains() -> tuple[str, ...]:
    return tuple(sorted(_WORKFLOW_CONTROL_RULES.keys()))


def governed_domain_count() -> int:
    return _GOVERNED_DOMAIN_COUNT


__all__ = [
    "ControlRule",
    "control_classes_for",
    "governed_domain_count",
    "governed_workflow_domains",
    "workflow_controls",
    "workflow_domain_is_governed",
]
