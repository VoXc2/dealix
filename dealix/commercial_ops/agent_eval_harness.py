"""Deterministic agent policy eval harness (CLEARS-lite) — offline regression."""

from __future__ import annotations

from typing import Any

from auto_client_acquisition.agent_governance.policy import evaluate_action
from auto_client_acquisition.agent_governance.schemas import (
    AutonomyLevel,
    ToolCategory,
    ToolPermission,
)
from auto_client_acquisition.revenue_os.anti_waste import validate_pipeline_step

_GOLDEN_CASES: list[dict[str, Any]] = [
    {
        "id": "forbid_whatsapp_live",
        "kind": "governance",
        "tool": ToolCategory.SEND_WHATSAPP_LIVE,
        "level": AutonomyLevel.L3_APPROVED_EXECUTE,
        "expect_permission": ToolPermission.FORBIDDEN,
    },
    {
        "id": "draft_email_requires_approval",
        "kind": "governance",
        "tool": ToolCategory.DRAFT_EMAIL,
        "level": AutonomyLevel.L3_APPROVED_EXECUTE,
        "allowed_tools": [ToolCategory.DRAFT_EMAIL],
        "expect_permission": ToolPermission.REQUIRES_APPROVAL,
    },
    {
        "id": "anti_waste_no_passport",
        "kind": "anti_waste",
        "kwargs": {
            "has_decision_passport": False,
            "lead_source": "inbound",
            "action_external": True,
            "upsell_attempt": False,
            "proof_event_count": 0,
        },
        "expect_violations_min": 1,
    },
]


def run_agent_eval_harness() -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    failures = 0
    for case in _GOLDEN_CASES:
        cid = case["id"]
        if case["kind"] == "governance":
            verdict = evaluate_action(
                agent_id="eval-harness",
                tool=case["tool"],
                autonomy_level=case["level"],
                allowed_tools=case.get("allowed_tools"),
            )
            ok = verdict.permission == case["expect_permission"]
            perm = verdict.permission
            perm_str = perm.value if hasattr(perm, "value") else str(perm)
            results.append({"id": cid, "ok": ok, "permission": perm_str})
        else:
            violations = validate_pipeline_step(**case["kwargs"])
            ok = len(violations) >= int(case["expect_violations_min"])
            results.append({"id": cid, "ok": ok, "violations": [v.code for v in violations]})
        if not results[-1]["ok"]:
            failures += 1

    return {
        "cases": len(_GOLDEN_CASES),
        "failures": failures,
        "results": results,
        "verdict": "PASS" if failures == 0 else "FAIL",
    }
