"""Executive Command Center composer — assembles all 15 sections."""
from __future__ import annotations

from typing import Any

from auto_client_acquisition.executive_command_center.panels import (
    _approval_center_panel,
    _delivery_operations_panel,
    _executive_summary_panel,
    _finance_state_panel,
    _full_ops_score_panel,
    _growth_radar_panel,
    _partnership_radar_panel,
    _proof_ledger_panel,
    _revenue_radar_panel,
    _risks_compliance_panel,
    _sales_pipeline_panel,
    _support_inbox_panel,
    _today_3_decisions_panel,
    _whatsapp_decision_preview_panel,
)
from auto_client_acquisition.executive_command_center.schemas import (
    Cadence,
    CommandCenterView,
)


def build_command_center(
    *,
    customer_handle: str,
    cadence: Cadence = "snapshot",
) -> CommandCenterView:
    """Build the full 15-section view. Never raises."""
    degraded: list[dict[str, Any]] = []

    def _maybe_degrade(name: str, panel: Any) -> Any:
        if isinstance(panel, dict) and panel.get("degraded"):
            degraded.append(panel)
            return {}
        return panel

    sections = {
        "executive_summary": _maybe_degrade(
            "executive_summary", _executive_summary_panel(customer_handle)
        ),
        "full_ops_score": _maybe_degrade(
            "full_ops_score", _full_ops_score_panel()
        ),
        "today_3_decisions": _today_3_decisions_panel(customer_handle),
        "revenue_radar": _maybe_degrade(
            "revenue_radar", _revenue_radar_panel(customer_handle)
        ),
        "sales_pipeline": _maybe_degrade(
            "sales_pipeline", _sales_pipeline_panel(customer_handle)
        ),
        "growth_radar": _maybe_degrade(
            "growth_radar", _growth_radar_panel(customer_handle)
        ),
        "partnership_radar": _maybe_degrade(
            "partnership_radar", _partnership_radar_panel()
        ),
        "support_inbox": _maybe_degrade(
            "support_inbox", _support_inbox_panel(customer_handle)
        ),
        "delivery_operations": _maybe_degrade(
            "delivery_operations", _delivery_operations_panel(customer_handle)
        ),
        "finance_state": _maybe_degrade(
            "finance_state", _finance_state_panel(customer_handle)
        ),
        "proof_ledger": _maybe_degrade(
            "proof_ledger", _proof_ledger_panel(customer_handle)
        ),
        "risks_compliance": _maybe_degrade(
            "risks_compliance", _risks_compliance_panel()
        ),
        "approval_center": _maybe_degrade(
            "approval_center", _approval_center_panel()
        ),
        "whatsapp_decision_preview": _whatsapp_decision_preview_panel(customer_handle),
    }

    return CommandCenterView(
        customer_handle=customer_handle,
        cadence=cadence,
        executive_summary=sections["executive_summary"],
        full_ops_score=sections["full_ops_score"],
        today_3_decisions=sections["today_3_decisions"],
        revenue_radar=sections["revenue_radar"],
        sales_pipeline=sections["sales_pipeline"],
        growth_radar=sections["growth_radar"],
        partnership_radar=sections["partnership_radar"],
        support_inbox=sections["support_inbox"],
        delivery_operations=sections["delivery_operations"],
        finance_state=sections["finance_state"],
        proof_ledger=sections["proof_ledger"],
        risks_compliance=sections["risks_compliance"],
        approval_center=sections["approval_center"],
        whatsapp_decision_preview=sections["whatsapp_decision_preview"],
        degraded_sections=degraded,
    )


def build_daily(*, customer_handle: str) -> CommandCenterView:
    return build_command_center(customer_handle=customer_handle, cadence="daily")


def build_weekly(*, customer_handle: str) -> CommandCenterView:
    return build_command_center(customer_handle=customer_handle, cadence="weekly")
