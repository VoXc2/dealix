"""Tool Guardrail Gateway HTTP surface (Phase 8 Wave 5).

  GET  /api/v1/tool-guardrails/status
  POST /api/v1/tool-guardrails/check
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Body, HTTPException

from auto_client_acquisition.tool_guardrail_gateway import (
    audit_decision,
    check_cost_budget,
    check_input,
    check_output,
    check_tool_permission,
)

router = APIRouter(
    prefix="/api/v1/tool-guardrails",
    tags=["tool-guardrail-gateway"],
)

_HARD_GATES: dict[str, bool] = {
    "no_live_send": True,
    "no_live_charge": True,
    "no_cold_whatsapp": True,
    "no_linkedin_auto": True,
    "no_scraping": True,
    "no_blast": True,
    "input_output_guarded": True,
    "cost_budget_enforced": True,
    "audit_logged_to_radar_events": True,
}


@router.get("/status")
async def status() -> dict[str, Any]:
    return {
        "service": "tool_guardrail_gateway",
        "version": "1.0.0",
        "guardrail_layers": [
            "input_guardrails (prompt injection + PII overexposure)",
            "tool_guardrails (per-tool permission)",
            "output_guardrails (forbidden tokens + ROI claims)",
            "cost_budget (token + USD cap)",
            "audit (radar_events log)",
        ],
        "hard_gates": _HARD_GATES,
    }


@router.post("/check")
async def check(payload: dict[str, Any] = Body(default_factory=dict)) -> dict[str, Any]:
    """Run all 4 guardrail layers + audit. Returns combined decision."""
    tool_name = payload.get("tool_name")
    if not tool_name:
        raise HTTPException(status_code=422, detail="tool_name required")

    input_text = payload.get("input_text", "")
    output_text = payload.get("output_text", "")
    estimated_tokens = int(payload.get("estimated_tokens", 0))
    estimated_usd = float(payload.get("estimated_usd", 0.0))
    has_human_approval = bool(payload.get("has_human_approval", False))
    customer_handle = payload.get("customer_handle")

    input_check = check_input(text=input_text) if input_text else {"passed": True, "reasons": []}
    tool_check = check_tool_permission(
        tool_name=tool_name, has_human_approval=has_human_approval,
    )
    output_check = check_output(text=output_text) if output_text else {"passed": True, "reasons": [], "scrubbed_text": ""}
    cost_check = check_cost_budget(
        estimated_tokens=estimated_tokens, estimated_usd=estimated_usd,
    )

    overall_passed = all([
        input_check.get("passed", True),
        tool_check.get("permitted", False),
        output_check.get("passed", True),
        cost_check.get("passed", True),
    ])

    decision = {
        "passed": overall_passed,
        "tool_name": tool_name,
        "input_check": input_check,
        "tool_check": tool_check,
        "output_check": output_check,
        "cost_check": cost_check,
        "action_mode": tool_check.get("action_mode", "blocked"),
        "reasons": (
            input_check.get("reasons", [])
            + ([tool_check["reason"]] if not tool_check.get("permitted") else [])
            + output_check.get("reasons", [])
            + cost_check.get("reasons", [])
        ),
    }

    # Audit (never raises)
    audit_decision(
        tool_name=tool_name,
        decision={"passed": overall_passed, "reasons": decision["reasons"], "severity": "high" if not overall_passed else "info"},
        customer_handle=customer_handle,
    )

    return {"decision": decision, "hard_gates": _HARD_GATES}
