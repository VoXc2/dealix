"""
Lead Qualification — the enterprise-grade vertical slice.

This is the *one* workflow the blueprint says to build end-to-end before
anything else. It deliberately exercises the whole runtime:

    governance · approvals · audit · observability · rollback ·
    evals · ROI · operational memory · typed integrations

Steps:
    1. crm.fetch_lead          (A0/R0/S2)  read the lead from CRM
    2. memory.retrieve_history (A0/R0/S1)  permission-aware prior-run lookup
    3. evaluate_lead           (A0/R0/S1)  deterministic scoring
    4. crm.update_lead_status  (A0/R1/S2)  reversible write — has compensation
    5. response.generate_draft (A0/R0/S1)  draft the qualification reply
    6. whatsapp.send_message   (A1/R2/S2)  outbound — REQUIRES human approval

Step 6 is the governed boundary: it always escalates to a human. Step 4 is
reversible, so a failure in step 5/6 rolls it back automatically.
"""

from __future__ import annotations

import uuid
from typing import Any

from dealix.classifications import ApprovalClass, ReversibilityClass, SensitivityClass
from dealix.execution.memory import get_memory
from dealix.execution.roi import ROIBaseline, get_roi_ledger
from dealix.execution.tool_registry import Tool, ToolRegistry
from dealix.execution.workflow import WorkflowContext, WorkflowDefinition, WorkflowStep

# ── Mock CRM — an in-process stand-in for HubSpot/Salesforce ────────
# Phase 2 swaps this for the real connector behind the same tool surface.
_CRM: dict[str, dict[str, Any]] = {}
_CORRECTIONS: list[dict[str, Any]] = []

_TARGET_SECTORS = {"real_estate", "b2b_services", "healthcare", "fintech", "logistics"}
_INTENT_KEYWORDS = ("pricing", "demo", "buy", "subscribe", "quote", "سعر", "عرض", "اشتراك")


def _crm_key(tenant_id: str, lead_id: str) -> str:
    return f"{tenant_id}:{lead_id}"


def seed_lead(tenant_id: str, lead_id: str, record: dict[str, Any]) -> None:
    """Test/ops helper — pre-populate the mock CRM."""
    _CRM[_crm_key(tenant_id, lead_id)] = {"lead_id": lead_id, "status": "new", **record}


def crm_record(tenant_id: str, lead_id: str) -> dict[str, Any] | None:
    rec = _CRM.get(_crm_key(tenant_id, lead_id))
    return dict(rec) if rec else None


def reset_crm() -> None:
    """Test helper — clear mock CRM + correction log."""
    _CRM.clear()
    _CORRECTIONS.clear()


# ── Tool handlers ───────────────────────────────────────────────────


async def _fetch_lead(inp: dict[str, Any]) -> dict[str, Any]:
    tenant_id, lead_id = inp["tenant_id"], inp["lead_id"]
    key = _crm_key(tenant_id, lead_id)
    if key not in _CRM:
        # First contact — materialise the lead from the trigger payload.
        _CRM[key] = {
            "lead_id": lead_id,
            "status": "new",
            "company": inp.get("company", ""),
            "sector": inp.get("sector", ""),
            "region": inp.get("region", ""),
            "phone": inp.get("phone", ""),
            "budget_sar": inp.get("budget_sar", 0),
            "message": inp.get("message", ""),
        }
    return {"lead": dict(_CRM[key]), "found": True}


async def _retrieve_history(inp: dict[str, Any]) -> dict[str, Any]:
    history = get_memory().history_for_entity(
        inp["entity_id"], tenant_id=inp["tenant_id"], limit=10
    )
    return {
        "prior_runs": len(history),
        "returning_lead": len(history) > 0,
        "last_status": history[-1]["status"] if history else None,
    }


async def _evaluate_lead(inp: dict[str, Any]) -> dict[str, Any]:
    """Deterministic lead score — no LLM, fully reproducible."""
    lead = inp["lead"]
    score = 0
    reasons: list[str] = []
    if lead.get("company"):
        score += 20
        reasons.append("named company")
    if str(lead.get("sector", "")).lower() in _TARGET_SECTORS:
        score += 25
        reasons.append("target sector")
    budget = float(lead.get("budget_sar") or 0)
    if budget >= 50_000:
        score += 30
        reasons.append("budget >= 50k SAR")
    elif budget >= 10_000:
        score += 15
        reasons.append("budget >= 10k SAR")
    message = str(lead.get("message", "")).lower()
    if any(k in message for k in _INTENT_KEYWORDS):
        score += 25
        reasons.append("explicit buying intent")
    if inp.get("returning_lead"):
        score += 10
        reasons.append("returning lead")

    score = min(100, score)
    tier = "hot" if score >= 70 else "warm" if score >= 40 else "cold"
    return {
        "score": score,
        "normalized_score": round(score / 100.0, 3),
        "tier": tier,
        "qualified": score >= 40,
        "reasons": reasons,
    }


async def _update_lead_status(inp: dict[str, Any]) -> dict[str, Any]:
    key = _crm_key(inp["tenant_id"], inp["lead_id"])
    record = _CRM.get(key)
    if record is None:
        raise RuntimeError(f"lead {inp['lead_id']} not in CRM")
    previous = record.get("status", "new")
    record["status"] = inp["new_status"]
    return {"lead_id": inp["lead_id"], "previous_status": previous,
            "new_status": inp["new_status"]}


async def _revert_lead_status(
    original_input: dict[str, Any], output: dict[str, Any]
) -> dict[str, Any]:
    """Compensation for crm.update_lead_status — restore the prior status."""
    key = _crm_key(original_input["tenant_id"], original_input["lead_id"])
    record = _CRM.get(key)
    if record is not None and "previous_status" in output:
        record["status"] = output["previous_status"]
    return {"reverted_to": output.get("previous_status")}


async def _generate_draft(inp: dict[str, Any]) -> dict[str, Any]:
    lead = inp["lead"]
    tier = inp["tier"]
    company = lead.get("company") or "your team"
    if tier == "hot":
        body = (
            f"مرحباً {company} — يسعدنا اهتمامكم. حجزنا لكم أولوية مع فريق المبيعات "
            f"لمناقشة العرض المناسب. متى يناسبكم اتصال قصير؟"
        )
    elif tier == "warm":
        body = (
            f"مرحباً {company} — شكراً لتواصلكم. أرسلنا لكم ملخصاً للخدمة "
            f"وسنسعد بالإجابة على أي استفسار."
        )
    else:
        body = (
            f"مرحباً {company} — شكراً لتواصلكم. سنبقيكم على اطلاع بكل جديد "
            f"يناسب احتياجكم."
        )
    return {"draft": body, "channel": "whatsapp", "locale": "ar", "tier": tier}


async def _send_whatsapp(inp: dict[str, Any]) -> dict[str, Any]:
    if inp.get("simulate_failure"):
        raise RuntimeError("whatsapp gateway timeout (simulated)")
    if not inp.get("phone"):
        raise RuntimeError("no phone number on lead — cannot send")
    return {
        "message_id": f"wamid_{uuid.uuid4().hex[:18]}",
        "to": inp["phone"],
        "delivered": True,
    }


async def _retract_whatsapp(
    original_input: dict[str, Any], output: dict[str, Any]
) -> dict[str, Any]:
    """Compensation for whatsapp.send_message — a sent message cannot be
    un-sent, so we log a correction obligation against the lead instead."""
    correction = {
        "lead_phone": original_input.get("phone"),
        "original_message_id": output.get("message_id"),
        "action": "send_correction_required",
    }
    _CORRECTIONS.append(correction)
    return correction


def corrections_log() -> list[dict[str, Any]]:
    return list(_CORRECTIONS)


# ── Tool registry builder ───────────────────────────────────────────


def build_registry() -> ToolRegistry:
    """A fresh registry with the lead-qualification tools."""
    reg = ToolRegistry()
    reg.register(Tool(
        name="crm.fetch_lead",
        description="Fetch the lead record from the CRM of record",
        handler=_fetch_lead,
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S2,
        action_type="enrichment_query",
        max_attempts=3,
    ))
    reg.register(Tool(
        name="memory.retrieve_history",
        description="Permission-aware retrieval of this lead's prior workflow runs",
        handler=_retrieve_history,
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S1,
        action_type="market_research_query",
        max_attempts=2,
    ))
    reg.register(Tool(
        name="lead.evaluate",
        description="Deterministic lead scoring + qualification tier",
        handler=_evaluate_lead,
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S1,
        action_type="icp_match",
        max_attempts=1,
    ))
    reg.register(Tool(
        name="crm.update_lead_status",
        description="Write the qualification status back to the CRM (reversible)",
        handler=_update_lead_status,
        compensation=_revert_lead_status,
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R1,
        sensitivity_class=SensitivityClass.S2,
        action_type="crm_contact_upsert",
        max_attempts=3,
    ))
    reg.register(Tool(
        name="response.generate_draft",
        description="Draft the bilingual qualification reply",
        handler=_generate_draft,
        approval_class=ApprovalClass.A0,
        reversibility_class=ReversibilityClass.R0,
        sensitivity_class=SensitivityClass.S1,
        action_type="content_generate_draft",
        max_attempts=1,
    ))
    reg.register(Tool(
        name="whatsapp.send_message",
        description="Send the qualification reply to the lead via WhatsApp",
        handler=_send_whatsapp,
        compensation=_retract_whatsapp,
        approval_class=ApprovalClass.A1,  # outbound — always human-approved
        reversibility_class=ReversibilityClass.R2,
        sensitivity_class=SensitivityClass.S2,
        action_type="outreach_send",
        max_attempts=3,
    ))
    return reg


# ── Workflow definition ─────────────────────────────────────────────


def _in_fetch(ctx: WorkflowContext) -> dict[str, Any]:
    return {"tenant_id": ctx.tenant_id, "lead_id": ctx.entity_id, **ctx.trigger_payload}


def _in_history(ctx: WorkflowContext) -> dict[str, Any]:
    return {"tenant_id": ctx.tenant_id, "entity_id": ctx.entity_id}


def _in_evaluate(ctx: WorkflowContext) -> dict[str, Any]:
    return {
        "lead": ctx.output("fetch_lead").get("lead", {}),
        "returning_lead": ctx.output("retrieve_history").get("returning_lead", False),
    }


def _in_update_status(ctx: WorkflowContext) -> dict[str, Any]:
    ev = ctx.output("evaluate_lead")
    new_status = "qualified" if ev.get("qualified") else "nurture"
    return {"tenant_id": ctx.tenant_id, "lead_id": ctx.entity_id, "new_status": new_status}


def _in_draft(ctx: WorkflowContext) -> dict[str, Any]:
    return {
        "lead": ctx.output("fetch_lead").get("lead", {}),
        "tier": ctx.output("evaluate_lead").get("tier", "cold"),
    }


def _in_send(ctx: WorkflowContext) -> dict[str, Any]:
    lead = ctx.output("fetch_lead").get("lead", {})
    return {
        "phone": lead.get("phone", ""),
        "message": ctx.output("generate_draft").get("draft", ""),
        "simulate_failure": bool(ctx.trigger_payload.get("simulate_send_failure", False)),
    }


def lead_qualification_workflow() -> WorkflowDefinition:
    """The canonical Lead Qualification workflow definition."""
    return WorkflowDefinition(
        name="lead_qualification",
        version="1.0.0",
        description="Qualify an inbound lead and send a governed first reply",
        trigger="webhook",
        steps=[
            WorkflowStep("fetch_lead", "crm.fetch_lead", _in_fetch,
                         "Load the lead from CRM"),
            WorkflowStep("retrieve_history", "memory.retrieve_history", _in_history,
                         "Look up prior runs for this lead"),
            WorkflowStep("evaluate_lead", "lead.evaluate", _in_evaluate,
                         "Score and tier the lead"),
            WorkflowStep("update_status", "crm.update_lead_status", _in_update_status,
                         "Write qualification status back (reversible)"),
            WorkflowStep("generate_draft", "response.generate_draft", _in_draft,
                         "Draft the qualification reply"),
            WorkflowStep("send_message", "whatsapp.send_message", _in_send,
                         "Send the reply — requires human approval"),
        ],
    )


def register_roi_baseline() -> None:
    """Declare what a manual lead-qualification costs (for the ROI ledger)."""
    get_roi_ledger().register_baseline(
        ROIBaseline(
            workflow_name="lead_qualification",
            manual_minutes=22.0,
            cost_per_minute_sar=2.5,
        )
    )


__all__ = [
    "build_registry",
    "corrections_log",
    "crm_record",
    "lead_qualification_workflow",
    "register_roi_baseline",
    "reset_crm",
    "seed_lead",
]
