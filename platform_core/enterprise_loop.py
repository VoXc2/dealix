"""The enterprise loop — one governed end-to-end run that proves the foundation.

The loop is the AI Revenue OS lead pipeline wrapped in the full governance
stack. It runs eleven steps; each step appends one append-only ``AuditEvent``
to the run record:

    1  provision tenant            7  CRM update (draft-only)
    2  create 3 users             8  executive report
    3  create 2 roles             9  eval report
    4  register 1 agent          10  rollback drill
    5  run workflow              11  audit-chain verification
    6  apply 1 approval rule

Each step is also a standalone async function so the proof API router can
drive the loop one HTTP call at a time. All steps share a ``LoopContext``
held in ``RUN_STORE``.

Doctrine honored in-loop:
  * Step 4 — agent gated by identity + card validity (identity, owner,
    autonomy_level all mandatory).
  * Step 6 — approval flow left ``pending_human``; no external action runs.
  * Step 7 — CRM is draft-only, never a live send.
  * No PII in audit/log fields — IDs and structural data only.
"""

from __future__ import annotations

import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone

from platform_core import stores
from platform_core.agent_runtime import (
    AgentCard,
    agent_card_valid,
    get_agent,
    register_agent,
)
from platform_core.governance import (
    approval_for_action,
    enforce_doctrine_non_negotiables,
)
from platform_core.identity import AgentIdentity, agent_identity_valid
from platform_core.observability import AuditEvent, audit_event_valid
from platform_core.rbac import AutonomyLevel
from platform_core.workflow_engine import (
    WORKFLOW_STAGE_ORDER,
    approval_flow_complete,
)

from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
from auto_client_acquisition.sales_os.qualification import (
    QualificationVerdict,
    qualify_opportunity,
)
from auto_client_acquisition.value_os.value_ledger import (
    ValueLedgerEvent,
    value_ledger_event_valid,
)


# ── Run state ───────────────────────────────────────────────────────

@dataclass
class LoopStepResult:
    step: str
    ok: bool
    detail: dict
    audit: AuditEvent

    def as_dict(self) -> dict:
        return {
            "step": self.step,
            "ok": self.ok,
            "decision": self.audit.decision,
            "detail": self.detail,
            "audit": asdict(self.audit),
        }


@dataclass
class LoopContext:
    run_id: str
    actor: str = "founder"
    tenant_id: str = ""
    tenant_handle: str = ""
    created: dict = field(
        default_factory=lambda: {"tenant": None, "users": [], "roles": [], "agent": None},
    )
    steps: list[LoopStepResult] = field(default_factory=list)
    # Artifacts (draft text, reports) live here — never in audit/log fields.
    artifacts: dict = field(default_factory=dict)
    rolled_back: bool = False

    def as_dict(self) -> dict:
        return {
            "run_id": self.run_id,
            "actor": self.actor,
            "tenant_id": self.tenant_id,
            "tenant_handle": self.tenant_handle,
            "created": self.created,
            "rolled_back": self.rolled_back,
            "steps": [s.as_dict() for s in self.steps],
            "artifacts": self.artifacts,
            "audit_chain_valid": all(audit_event_valid(s.audit) for s in self.steps),
        }


# Module-global run store — holds LoopContext per run_id.
RUN_STORE: dict[str, LoopContext] = {}


def new_run(actor: str = "founder") -> LoopContext:
    ctx = LoopContext(run_id=f"run_{uuid.uuid4().hex[:16]}", actor=actor)
    RUN_STORE[ctx.run_id] = ctx
    return ctx


def get_run(run_id: str) -> LoopContext | None:
    return RUN_STORE.get(run_id)


def reset_runs_for_tests() -> None:
    RUN_STORE.clear()


# ── Audit helper ────────────────────────────────────────────────────

def _audit(
    ctx: LoopContext,
    *,
    source: str,
    decision: str,
    policy_checked: str,
    matched_rule: str = "",
    approval_status: str = "n/a",
    output_id: str = "",
) -> AuditEvent:
    return AuditEvent(
        event_id=f"ae_{uuid.uuid4().hex[:16]}",
        actor=ctx.actor,
        source=source,
        policy_checked=policy_checked,
        matched_rule=matched_rule,
        decision=decision,
        approval_status=approval_status,
        output_id=output_id,
        timestamp_iso=datetime.now(timezone.utc).isoformat(),
    )


async def _record(
    ctx: LoopContext,
    *,
    step: str,
    ok: bool,
    detail: dict,
    event: AuditEvent,
) -> LoopStepResult:
    result = LoopStepResult(step=step, ok=ok, detail=detail, audit=event)
    ctx.steps.append(result)
    await stores.persist_audit(ctx.tenant_id, event)
    return result


# ── Step 1 — provision tenant ───────────────────────────────────────

async def step_provision_tenant(
    ctx: LoopContext,
    *,
    tenant_handle: str,
    tenant_name: str,
) -> LoopStepResult:
    tenant = await stores.create_tenant(tenant_handle, tenant_name)
    ctx.tenant_id = tenant.id
    ctx.tenant_handle = tenant.handle
    ctx.created["tenant"] = tenant.id
    event = _audit(
        ctx,
        source="platform.enterprise_loop.tenant",
        decision="tenant_provisioned",
        policy_checked="multi_tenant_isolation",
        matched_rule="tenant_id_scoped",
        output_id=tenant.id,
    )
    return await _record(
        ctx,
        step="provision_tenant",
        ok=True,
        detail={"tenant_id": tenant.id, "handle": tenant.handle},
        event=event,
    )


# ── Step 2 — create 3 users ─────────────────────────────────────────

_DEFAULT_USERS: tuple[dict[str, str], ...] = (
    {"email": "founder@loop.local", "name": "Loop Founder", "role": "founder"},
    {"email": "csm@loop.local", "name": "Loop CSM", "role": "csm"},
    {"email": "rep@loop.local", "name": "Loop Sales Rep", "role": "sales_rep"},
)


async def step_create_users(
    ctx: LoopContext,
    *,
    users: list[dict[str, str]] | None = None,
) -> LoopStepResult:
    chosen = users or list(_DEFAULT_USERS)
    user_ids: list[str] = []
    for u in chosen:
        record = await stores.create_user(
            ctx.tenant_id,
            email=u["email"],
            name=u.get("name", ""),
            role_name=u.get("role", "sales_rep"),
        )
        user_ids.append(record.id)
    ctx.created["users"] = user_ids
    event = _audit(
        ctx,
        source="platform.enterprise_loop.users",
        decision="users_created",
        policy_checked="identity",
        matched_rule=f"count={len(user_ids)}",
        output_id=ctx.tenant_id,
    )
    return await _record(
        ctx,
        step="create_users",
        ok=len(user_ids) == 3,
        detail={"user_ids": user_ids, "count": len(user_ids)},
        event=event,
    )


# ── Step 3 — create 2 roles ─────────────────────────────────────────

_DEFAULT_ROLES: tuple[dict, ...] = (
    {"name": "sales_rep", "permissions": ["leads:read", "leads:write", "agents:run"]},
    {"name": "viewer", "permissions": ["leads:read"]},
)


async def step_create_roles(
    ctx: LoopContext,
    *,
    roles: list[dict] | None = None,
) -> LoopStepResult:
    chosen = roles or [dict(r) for r in _DEFAULT_ROLES]
    role_ids: list[str] = []
    for r in chosen:
        record = await stores.create_role(
            ctx.tenant_id,
            name=r["name"],
            permissions=list(r.get("permissions", [])),
        )
        role_ids.append(record.id)
    ctx.created["roles"] = role_ids
    event = _audit(
        ctx,
        source="platform.enterprise_loop.roles",
        decision="roles_created",
        policy_checked="rbac",
        matched_rule=f"count={len(role_ids)}",
        output_id=ctx.tenant_id,
    )
    return await _record(
        ctx,
        step="create_roles",
        ok=len(role_ids) == 2,
        detail={"role_ids": role_ids, "count": len(role_ids)},
        event=event,
    )


# ── Step 4 — register 1 agent ───────────────────────────────────────

async def step_register_agent(
    ctx: LoopContext,
    *,
    name: str = "revenue_intelligence_agent",
    purpose: str = "Qualify inbound Saudi B2B leads and draft responses under approval.",
    owner: str | None = None,
) -> LoopStepResult:
    owner = ctx.actor if owner is None else owner
    agent_id = f"agt_{uuid.uuid4().hex[:16]}"
    identity = AgentIdentity(
        agent_id=agent_id,
        tenant_id=ctx.tenant_id,
        owner_principal=owner,
    )
    card = AgentCard(
        agent_id=agent_id,
        name=name,
        owner=owner,
        purpose=purpose,
        autonomy_level=int(AutonomyLevel.QUEUE_FOR_APPROVAL),
        status="active",
    )
    identity_ok = agent_identity_valid(identity)
    card_ok = agent_card_valid(card)

    if not (identity_ok and card_ok):
        event = _audit(
            ctx,
            source="platform.enterprise_loop.agent",
            decision="agent_rejected",
            policy_checked="agent_identity",
            matched_rule="identity_or_card_invalid",
            output_id=agent_id,
        )
        return await _record(
            ctx,
            step="register_agent",
            ok=False,
            detail={
                "agent_id": agent_id,
                "identity_valid": identity_ok,
                "card_valid": card_ok,
                "reason": "agent requires identity, owner, and autonomy_level",
            },
            event=event,
        )

    register_agent(card)
    ctx.created["agent"] = agent_id
    event = _audit(
        ctx,
        source="platform.enterprise_loop.agent",
        decision="agent_registered",
        policy_checked="agent_identity",
        matched_rule=f"autonomy_level={card.autonomy_level}",
        output_id=agent_id,
    )
    return await _record(
        ctx,
        step="register_agent",
        ok=True,
        detail={
            "agent_id": agent_id,
            "identity_valid": True,
            "card_valid": True,
            "autonomy_level": card.autonomy_level,
        },
        event=event,
    )


# ── Step 5 — run workflow (intake -> qualify -> score -> draft) ─────

_DEFAULT_LEAD: dict[str, str] = {
    "company": "Najd Logistics Co.",
    "sector": "logistics",
    "contact_name": "Operations Lead",
}

_DEFAULT_ICP: dict[str, int] = {
    "b2b_service_fit": 78,
    "data_maturity": 65,
    "governance_posture": 72,
    "budget_signal": 70,
    "decision_velocity": 68,
}


def _suggested_response_draft(lead: dict[str, str], verdict: QualificationVerdict) -> str:
    """Bilingual suggested-response draft — Proof Pack artifact. Never sent."""
    company = lead.get("company", "the account")
    return (
        f"[AR] مسودة رد مقترحة لـ {company}: شكرًا لتواصلكم. بناءً على تقييم الملاءمة "
        f"({verdict.value})، نقترح جلسة تشخيص قصيرة لتأكيد الأولويات قبل أي عرض. "
        "هذه مسودة — لا تُرسَل إلا بعد موافقة بشرية.\n"
        f"[EN] Suggested reply draft for {company}: thank you for reaching out. "
        f"Given the fit assessment ({verdict.value}), we propose a short diagnostic "
        "session to confirm priorities before any proposal. "
        "This is a draft — it is not sent without human approval."
    )


async def step_run_workflow(
    ctx: LoopContext,
    *,
    lead: dict[str, str] | None = None,
    icp: dict[str, int] | None = None,
    risk: dict[str, bool] | None = None,
) -> LoopStepResult:
    lead = lead or dict(_DEFAULT_LEAD)
    icp_in = icp or dict(_DEFAULT_ICP)
    risk_in = risk or {}

    icp_dims = ICPDimensions(
        b2b_service_fit=int(icp_in.get("b2b_service_fit", 0)),
        data_maturity=int(icp_in.get("data_maturity", 0)),
        governance_posture=int(icp_in.get("governance_posture", 0)),
        budget_signal=int(icp_in.get("budget_signal", 0)),
        decision_velocity=int(icp_in.get("decision_velocity", 0)),
    )
    risk_signals = ClientRiskSignals(
        wants_scraping_or_spam=bool(risk_in.get("wants_scraping_or_spam", False)),
        wants_guaranteed_sales=bool(risk_in.get("wants_guaranteed_sales", False)),
        unclear_pain=bool(risk_in.get("unclear_pain", False)),
        no_owner=bool(risk_in.get("no_owner", False)),
        data_not_ready=bool(risk_in.get("data_not_ready", False)),
        budget_unknown=bool(risk_in.get("budget_unknown", False)),
    )

    score = icp_score(icp_dims)
    verdict, reasons = qualify_opportunity(
        icp=icp_dims,
        risk=risk_signals,
        accepts_governance=True,
        proof_path_possible=True,
    )
    stages = [stage.value for stage in WORKFLOW_STAGE_ORDER]
    draft = _suggested_response_draft(lead, verdict)
    draft_id = f"draft_{uuid.uuid4().hex[:12]}"
    ctx.artifacts["workflow_draft"] = {"draft_id": draft_id, "body": draft}

    event = _audit(
        ctx,
        source="platform.enterprise_loop.workflow",
        decision="workflow_qualified",
        policy_checked="workflow_stages",
        matched_rule=f"verdict={verdict.value}",
        output_id=draft_id,
    )
    return await _record(
        ctx,
        step="run_workflow",
        ok=True,
        detail={
            "verdict": verdict.value,
            "reasons": list(reasons),
            "icp_score": score,
            "stages_completed": stages,
            "draft_id": draft_id,
        },
        event=event,
    )


# ── Step 6 — apply 1 approval rule ──────────────────────────────────

async def step_apply_approval(
    ctx: LoopContext,
    *,
    action: str = "send_email",
    request_external_send_without_approval: bool = False,
) -> LoopStepResult:
    risk, route = approval_for_action(action)

    try:
        enforce_doctrine_non_negotiables(
            request_external_send_without_approval=request_external_send_without_approval,
        )
    except ValueError:
        event = _audit(
            ctx,
            source="platform.enterprise_loop.approval",
            decision="doctrine_violation",
            policy_checked="doctrine_non_negotiables",
            matched_rule="external_action_requires_approval",
            approval_status="blocked",
        )
        await _record(
            ctx,
            step="apply_approval",
            ok=False,
            detail={
                "action": action,
                "risk": risk,
                "route": route,
                "reason": "external send without approval is forbidden",
            },
            event=event,
        )
        raise

    # Approval flow is deliberately incomplete: human steps are still pending.
    done = frozenset({"draft_created", "internal_review"})
    complete, missing = approval_flow_complete(done)
    approval_status = "complete" if complete else "pending_human"

    event = _audit(
        ctx,
        source="platform.enterprise_loop.approval",
        decision="approval_required",
        policy_checked="approval_matrix",
        matched_rule=route,
        approval_status=approval_status,
        output_id=ctx.artifacts.get("workflow_draft", {}).get("draft_id", ""),
    )
    return await _record(
        ctx,
        step="apply_approval",
        ok=True,
        detail={
            "action": action,
            "risk": risk,
            "route": route,
            "approval_flow_complete": complete,
            "approval_flow_missing": list(missing),
            "approval_status": approval_status,
            "doctrine_ok": True,
        },
        event=event,
    )


# ── Step 7 — CRM update (draft-only) ────────────────────────────────

async def step_crm_update(ctx: LoopContext) -> LoopStepResult:
    """Stage the intended CRM mutation as a draft — no live HubSpot call.

    Doctrine: no external action without approval. The CRM integration is
    wired here only to produce a reviewable draft.
    """
    draft = ctx.artifacts.get("workflow_draft", {})
    crm_draft = {
        "provider": "hubspot",
        "mode": "draft_only",
        "synced": False,
        "intended_contact": {"lifecyclestage": "lead", "hs_lead_status": "OPEN"},
        "intended_deal": {"dealstage": "qualifiedtobuy", "pipeline": "default"},
        "linked_draft_id": draft.get("draft_id", ""),
        "note": "Staged for human approval; not pushed to the live CRM.",
    }
    ctx.artifacts["crm_draft"] = crm_draft
    event = _audit(
        ctx,
        source="platform.enterprise_loop.crm",
        decision="crm_draft_staged",
        policy_checked="doctrine_non_negotiables",
        matched_rule="no_external_action_without_approval",
        approval_status="pending_human",
        output_id=draft.get("draft_id", ""),
    )
    return await _record(
        ctx,
        step="crm_update",
        ok=True,
        detail=crm_draft,
        event=event,
    )


# ── Step 8 — executive report ───────────────────────────────────────

async def step_executive_report(ctx: LoopContext) -> LoopStepResult:
    workflow_step = next((s for s in ctx.steps if s.step == "run_workflow"), None)
    qualified = 1 if workflow_step and workflow_step.ok else 0

    value_event = ValueLedgerEvent(
        value_event_id=f"val_{uuid.uuid4().hex[:12]}",
        project_id=ctx.run_id,
        client_id=ctx.tenant_id or "unknown",
        value_type="revenue_intelligence_pipeline",
        metric="qualified_accounts",
        before=0,
        after=qualified,
        evidence=f"enterprise_loop run {ctx.run_id}: {len(ctx.steps)} governed steps",
        confidence="estimated",
        limitations="Single synthetic loop run; not client-confirmed value.",
    )
    value_ok = value_ledger_event_valid(value_event)

    report = {
        "run_id": ctx.run_id,
        "tenant_id": ctx.tenant_id,
        "steps_executed": len(ctx.steps),
        "steps_ok": sum(1 for s in ctx.steps if s.ok),
        "qualified_accounts": qualified,
        "value_event": asdict(value_event),
        "value_event_valid": value_ok,
        "headline": (
            f"{qualified} account qualified through the governed loop; "
            "0 external messages sent (all drafts pending human approval)."
        ),
    }
    ctx.artifacts["executive_report"] = report
    event = _audit(
        ctx,
        source="platform.enterprise_loop.executive_report",
        decision="executive_report_emitted",
        policy_checked="value_ledger",
        matched_rule="confidence=estimated",
        output_id=value_event.value_event_id,
    )
    return await _record(
        ctx,
        step="executive_report",
        ok=value_ok,
        detail=report,
        event=event,
    )


# ── Step 9 — eval report ────────────────────────────────────────────

async def step_eval_report(ctx: LoopContext) -> LoopStepResult:
    prior = ctx.steps  # steps 1..8 recorded before this one
    checks = {
        "all_prior_steps_ok": all(s.ok for s in prior),
        "doctrine_clean": all(s.audit.decision != "doctrine_violation" for s in prior),
        "audit_chain_valid": all(audit_event_valid(s.audit) for s in prior),
        "workflow_draft_present": "workflow_draft" in ctx.artifacts,
        "agent_has_identity": ctx.created.get("agent") is not None,
        "executive_report_present": "executive_report" in ctx.artifacts,
    }
    passed = all(checks.values())
    eval_report = {
        "run_id": ctx.run_id,
        "checks": checks,
        "passed": passed,
        "steps_evaluated": len(prior),
    }
    ctx.artifacts["eval_report"] = eval_report
    event = _audit(
        ctx,
        source="platform.enterprise_loop.eval_report",
        decision="eval_report_emitted",
        policy_checked="evals",
        matched_rule=f"passed={passed}",
    )
    return await _record(
        ctx,
        step="eval_report",
        ok=passed,
        detail=eval_report,
        event=event,
    )


# ── Step 10 — rollback drill ────────────────────────────────────────

async def step_rollback_drill(ctx: LoopContext) -> LoopStepResult:
    rolled = await stores.rollback_run(
        tenant_id=ctx.created.get("tenant"),
        user_ids=list(ctx.created.get("users", [])),
        role_ids=list(ctx.created.get("roles", [])),
        agent_id=ctx.created.get("agent"),
    )
    ctx.rolled_back = True
    agent_id = ctx.created.get("agent")
    agent_cleared = agent_id is None or get_agent(agent_id) is None
    event = _audit(
        ctx,
        source="platform.enterprise_loop.rollback",
        decision="rollback_drill_completed",
        policy_checked="reversibility",
        matched_rule="soft_delete_and_deregister",
        output_id=ctx.tenant_id,
    )
    return await _record(
        ctx,
        step="rollback_drill",
        ok=agent_cleared,
        detail={"rolled_back": rolled, "agent_deregistered": agent_cleared},
        event=event,
    )


# ── Step 11 — audit-chain verification ──────────────────────────────

async def step_verify_audit(ctx: LoopContext) -> LoopStepResult:
    prior_events = [s.audit for s in ctx.steps]
    all_valid = all(audit_event_valid(e) for e in prior_events)
    enough = len(prior_events) >= 10  # steps 1..10 must each have logged

    event = _audit(
        ctx,
        source="platform.enterprise_loop.audit",
        decision="audit_chain_verified",
        policy_checked="auditability",
        matched_rule=f"events={len(prior_events) + 1}",
    )
    return await _record(
        ctx,
        step="verify_audit",
        ok=all_valid and enough,
        detail={
            "events_before": len(prior_events),
            "events_total": len(prior_events) + 1,
            "all_valid": all_valid,
        },
        event=event,
    )


# ── Full loop ───────────────────────────────────────────────────────

async def run_enterprise_loop(
    *,
    tenant_handle: str,
    tenant_name: str,
    actor: str = "founder",
) -> LoopContext:
    """Run all eleven steps in sequence and return the completed run record."""
    ctx = new_run(actor=actor)
    await step_provision_tenant(ctx, tenant_handle=tenant_handle, tenant_name=tenant_name)
    await step_create_users(ctx)
    await step_create_roles(ctx)
    await step_register_agent(ctx)
    await step_run_workflow(ctx)
    await step_apply_approval(ctx)
    await step_crm_update(ctx)
    await step_executive_report(ctx)
    await step_eval_report(ctx)
    await step_rollback_drill(ctx)
    await step_verify_audit(ctx)
    return ctx


__all__ = [
    "RUN_STORE",
    "LoopContext",
    "LoopStepResult",
    "get_run",
    "new_run",
    "reset_runs_for_tests",
    "run_enterprise_loop",
    "step_apply_approval",
    "step_create_roles",
    "step_create_users",
    "step_crm_update",
    "step_eval_report",
    "step_executive_report",
    "step_provision_tenant",
    "step_register_agent",
    "step_rollback_drill",
    "step_run_workflow",
    "step_verify_audit",
]
