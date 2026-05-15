"""The 13 governed steps of the lead_qualification workflow.

Each step is a pure function ``(run, lead, deps) -> StepResult``. Steps
reuse existing canonical modules — they do not reimplement governance,
scoring, approval, or observability. Steps write their artifact into
``run.checkpoint`` so later steps can read it; the orchestrator owns
tracing, audit, state transitions, and rollback.
"""

from __future__ import annotations

import time
from typing import Any

from auto_client_acquisition.agent_observability.cost import estimate_cost
from auto_client_acquisition.agent_observability.quality import quality_summary
from auto_client_acquisition.agent_observability.trace import list_recent_traces
from auto_client_acquisition.approval_center.schemas import ApprovalRequest
from auto_client_acquisition.compliance_trust_os.approval_engine import GovernanceDecision
from auto_client_acquisition.crm_v10.lead_scoring import score_lead
from auto_client_acquisition.crm_v10.schemas import Account, Lead
from auto_client_acquisition.governance_os.claim_safety import audit_claim_safety
from auto_client_acquisition.governance_os.draft_gate import intake_violations_for_source
from auto_client_acquisition.governance_os.policy_check import run_policy_check
from auto_client_acquisition.governance_os.runtime_decision import (
    governance_decision_from_policy_check,
)
from auto_client_acquisition.knowledge_os.answer_with_citations import answer_with_citations
from auto_client_acquisition.sales_os.client_risk_score import ClientRiskSignals, client_risk_score
from auto_client_acquisition.sales_os.icp_score import ICPDimensions, icp_score
from auto_client_acquisition.sales_os.lead_qualification.sales_agent import (
    DRAFT_LABEL,
    draft_response,
)
from auto_client_acquisition.sales_os.lead_qualification.schemas import (
    REQUIRED_PERMISSION,
    LeadInput,
    StepResult,
    worst_governance,
)
from auto_client_acquisition.sales_os.qualification import QualificationVerdict, qualify_opportunity

WORKFLOW_NAME = "lead_qualification"

_ALLOW = str(GovernanceDecision.ALLOW)
_ALLOW_WITH_REVIEW = str(GovernanceDecision.ALLOW_WITH_REVIEW)
_DRAFT_ONLY = str(GovernanceDecision.DRAFT_ONLY)
_REQUIRE_APPROVAL = str(GovernanceDecision.REQUIRE_APPROVAL)
_BLOCK = str(GovernanceDecision.BLOCK)

_CRM_SOURCE_MAP = {
    "warm_intro": "warm_intro",
    "founder_observation": "founder_network",
    "manual_linkedin_research": "manual",
}


def has_permission(permissions: list[str], required: str) -> bool:
    """RBAC check supporting exact, domain wildcard, and admin wildcard."""
    if required in permissions:
        return True
    domain = required.split(":", 1)[0]
    wildcards = {f"{domain}:*", "admin:*", "*"}
    return any(p in wildcards for p in permissions)


def _icp_of(lead: LeadInput) -> ICPDimensions:
    return ICPDimensions(
        b2b_service_fit=lead.icp_b2b_service_fit,
        data_maturity=lead.icp_data_maturity,
        governance_posture=lead.icp_governance_posture,
        budget_signal=lead.icp_budget_signal,
        decision_velocity=lead.icp_decision_velocity,
    )


def _risk_of(lead: LeadInput) -> ClientRiskSignals:
    return ClientRiskSignals(
        wants_scraping_or_spam=lead.wants_scraping_or_spam,
        wants_guaranteed_sales=lead.wants_guaranteed_sales,
        unclear_pain=lead.unclear_pain,
        no_owner=lead.no_owner,
        data_not_ready=lead.data_not_ready,
        budget_unknown=lead.budget_unknown,
    )


# ─── Step 1: Lead enters ─────────────────────────────────────────────


def step_lead_intake(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    violations = intake_violations_for_source(lead.source)
    blocked_source = [v for v in violations if v.startswith("blocked_source")]
    unknown_source = [v for v in violations if v.startswith("unknown_tier1_source")]
    artifact = {
        "lead_id": lead.lead_id,
        "company_name": lead.company_name,
        "source": lead.source,
        "sector": lead.sector,
        "region": lead.region,
        "source_warnings": violations,
    }
    if blocked_source:
        return StepResult(
            "lq_lead_intake", "lead_intake_record", _BLOCK,
            ok=False, blocked=True, reason=blocked_source[0], artifact=artifact,
        )
    decision = _ALLOW_WITH_REVIEW if unknown_source else _ALLOW
    run.checkpoint["intake"] = artifact
    return StepResult("lq_lead_intake", "lead_intake_record", decision, artifact=artifact)


# ─── Step 2: Tenant detection ────────────────────────────────────────


def step_tenant_detection(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    tenant = deps.tenant_resolver(lead.tenant_slug)
    if not tenant:
        return StepResult(
            "lq_tenant_detection", "tenant_context", _BLOCK,
            ok=False, blocked=True, reason=f"tenant_not_found:{lead.tenant_slug}",
        )
    if tenant.get("status", "active") != "active":
        return StepResult(
            "lq_tenant_detection", "tenant_context", _BLOCK,
            ok=False, blocked=True, reason=f"tenant_not_active:{lead.tenant_slug}",
            artifact=dict(tenant),
        )
    run.checkpoint["tenant"] = tenant
    return StepResult("lq_tenant_detection", "tenant_context", _ALLOW, artifact=dict(tenant))


# ─── Step 3: RBAC check ──────────────────────────────────────────────


def step_rbac_check(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    permissions = list(deps.rbac_resolver(lead.tenant_slug, lead.actor_role))
    granted = has_permission(permissions, REQUIRED_PERMISSION)
    artifact = {
        "role": lead.actor_role,
        "permissions": permissions,
        "required": REQUIRED_PERMISSION,
        "granted": granted,
    }
    if not granted:
        return StepResult(
            "lq_rbac_check", "rbac_decision", _BLOCK,
            ok=False, blocked=True,
            reason=f"rbac_denied:{lead.actor_role}:{REQUIRED_PERMISSION}",
            artifact=artifact,
        )
    run.checkpoint["rbac"] = artifact
    return StepResult("lq_rbac_check", "rbac_decision", _ALLOW, artifact=artifact)


# ─── Step 4: Knowledge retrieval ─────────────────────────────────────


def step_knowledge_retrieval(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    sources = list(deps.knowledge_retriever(lead))
    question = f"Qualification context for {lead.company_name} in sector {lead.sector}"
    result = answer_with_citations(question, sources=sources)
    insufficient = bool(result.get("insufficient_evidence"))
    artifact = {
        "question": question,
        "citations": result.get("citations", []),
        "insufficient_evidence": insufficient,
    }
    run.checkpoint["cited_context"] = result
    decision = _ALLOW_WITH_REVIEW if insufficient else _ALLOW
    return StepResult("lq_knowledge_retrieval", "cited_context", decision, artifact=artifact)


# ─── Step 5: Lead qualification ──────────────────────────────────────


def step_qualification(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    verdict, reasons = qualify_opportunity(
        icp=_icp_of(lead),
        risk=_risk_of(lead),
        accepts_governance=lead.accepts_governance,
        proof_path_possible=lead.proof_path_possible,
    )
    artifact = {"verdict": str(verdict), "reasons": list(reasons)}
    run.checkpoint["qualification"] = artifact
    if verdict == QualificationVerdict.REJECT:
        return StepResult(
            "lq_qualification", "qualification_verdict", _BLOCK,
            ok=False, blocked=True,
            reason=f"qualification_rejected:{reasons[0] if reasons else 'rejected'}",
            artifact=artifact,
        )
    soft = {QualificationVerdict.REFRAME, QualificationVerdict.DIAGNOSTIC_ONLY,
            QualificationVerdict.REFER_OUT}
    decision = _ALLOW_WITH_REVIEW if verdict in soft else _ALLOW
    return StepResult("lq_qualification", "qualification_verdict", decision, artifact=artifact)


# ─── Step 6: Lead scoring ────────────────────────────────────────────


def step_lead_scoring(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    icp_s = icp_score(_icp_of(lead))
    risk_s = client_risk_score(_risk_of(lead))
    artifact = {"icp_score": icp_s, "risk_score": risk_s}
    run.checkpoint["score"] = artifact
    return StepResult("lq_lead_scoring", "lead_score", _ALLOW, artifact=artifact)


# ─── Step 7: Draft response ──────────────────────────────────────────


def step_draft_response(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    verdict = run.checkpoint["qualification"]["verdict"]
    cited = run.checkpoint.get("cited_context", {})
    draft = draft_response(lead, verdict, cited, llm=deps.llm)
    run.checkpoint["draft"] = draft
    artifact = {
        "is_draft": True,
        "label": DRAFT_LABEL,
        "draft_preview": draft[:280],
        "draft_length": len(draft),
    }
    return StepResult("lq_draft_response", "response_draft", _DRAFT_ONLY, artifact=artifact)


# ─── Step 8: Risk check ──────────────────────────────────────────────


def step_risk_check(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    draft = run.checkpoint["draft"]
    policy = run_policy_check(draft_text=draft)
    policy_decision = str(governance_decision_from_policy_check(policy))
    claim = audit_claim_safety(draft)
    claim_decision = str(claim.suggested_decision)
    decision = worst_governance([policy_decision, claim_decision])
    artifact = {
        "policy_issues": list(policy.issues),
        "claim_issues": list(claim.issues),
        "decision": decision,
    }
    run.checkpoint["risk"] = artifact
    if decision == _BLOCK:
        return StepResult(
            "lq_risk_check", "governance_decision", _BLOCK,
            ok=False, blocked=True,
            reason=f"risk_blocked:{(list(policy.issues) + list(claim.issues))[:1]}",
            artifact=artifact,
        )
    return StepResult("lq_risk_check", "governance_decision", decision, artifact=artifact)


# ─── Step 9: Approval ────────────────────────────────────────────────


def step_approval(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    tenant = run.checkpoint.get("tenant", {})
    verdict = run.checkpoint["qualification"]["verdict"]
    request = ApprovalRequest(
        object_type="lead_response",
        object_id=lead.lead_id,
        action_type="draft_email",
        action_mode="approval_required",
        summary_ar=f"رد مسودة على العميل {lead.company_name} — نتيجة التأهيل {verdict}",
        summary_en=f"Draft response to lead {lead.company_name} — qualification {verdict}",
        risk_level="medium",
        proof_impact="lead_qualified",
        lead_id=lead.lead_id,
        customer_id=tenant.get("tenant_id"),
        audit_ref=run.run_id,
        proof_target="lead_qualified",
    )
    deps.approval_store.create(request)
    artifact = {
        "approval_id": request.approval_id,
        "status": str(request.status),
        "action_mode": request.action_mode,
    }
    run.checkpoint["approval_id"] = request.approval_id
    run.checkpoint["approval"] = artifact
    return StepResult("lq_approval", "approval_request", _REQUIRE_APPROVAL, artifact=artifact)


# ─── Step 10: CRM update ─────────────────────────────────────────────


def step_crm_update(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    account = Account(
        id=f"acc_{lead.lead_id}",
        name=lead.company_name,
        sector=lead.sector,
        region=lead.region,
        tier="pilot",
    )
    crm_source = _CRM_SOURCE_MAP.get(lead.source, "inbound")
    crm_lead = Lead(
        id=lead.lead_id,
        account_id=account.id,
        source=crm_source,
        stage="qualified",
        notes=lead.notes,
    )
    scored = score_lead(crm_lead, account)
    crm_lead = crm_lead.model_copy(update={
        "fit_score": scored["fit_score"],
        "urgency_score": scored["urgency_score"],
    })
    artifact = {
        "account_id": account.id,
        "lead_id": crm_lead.id,
        "stage": crm_lead.stage,
        "fit_score": crm_lead.fit_score,
        "urgency_score": crm_lead.urgency_score,
        "approval_id": run.checkpoint.get("approval_id", ""),
    }
    run.checkpoint["crm"] = artifact
    return StepResult("lq_crm_update", "crm_record_update", _ALLOW, artifact=artifact)


# ─── Step 11: Metrics emission ───────────────────────────────────────


def step_metrics_emission(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    traces = [
        t for t in list_recent_traces(limit=200)
        if t.workflow == WORKFLOW_NAME and t.customer_handle == lead.company_name
    ]
    draft = run.checkpoint.get("draft", "")
    tokens = max(1, len(draft) // 4)
    cost = estimate_cost(input_tokens=tokens, output_tokens=tokens)
    quality = quality_summary(traces)
    artifact = {
        "trace_count": len(traces),
        "cost_estimate_usd": cost,
        "quality": quality,
        "score": run.checkpoint.get("score", {}),
    }
    run.checkpoint["metrics"] = artifact
    return StepResult("lq_metrics_emission", "metrics_snapshot", _ALLOW, artifact=artifact)


# ─── Step 12: Eval report ────────────────────────────────────────────


def step_eval_report(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    from auto_client_acquisition.sales_os.lead_qualification.eval_report import build_eval_report

    report = build_eval_report(run)
    run.checkpoint["eval"] = report
    decision = _ALLOW if report.get("overall_pass") else _ALLOW_WITH_REVIEW
    return StepResult("lq_eval_report", "eval_report", decision, artifact=report)


# ─── Step 13: Executive dashboard ────────────────────────────────────


def step_executive_dashboard(run: Any, lead: LeadInput, deps: Any) -> StepResult:
    from auto_client_acquisition.executive_command_center.card_schema import to_card_dict

    qualification = run.checkpoint.get("qualification", {})
    score = run.checkpoint.get("score", {})
    eval_report = run.checkpoint.get("eval", {})
    verdict = qualification.get("verdict", "unknown")
    card = to_card_dict(
        signal=(
            f"Lead {lead.company_name} qualified — verdict {verdict}, "
            f"ICP {score.get('icp_score', 0)}/100"
        ),
        why_now=f"Qualification workflow completed for tenant {lead.tenant_slug}.",
        recommended_action="Review the governed draft response and approve or revise.",
        risk=f"Client risk score {score.get('risk_score', 0)}/100.",
        impact="Faster, governed lead response with a full audit trail.",
        owner="founder",
        action_mode="approval_required",
        proof_link=run.checkpoint.get("approval_id") or None,
    )
    card["eval_overall_pass"] = bool(eval_report.get("overall_pass"))
    run.checkpoint["dashboard_card"] = card
    return StepResult("lq_executive_dashboard", "dashboard_card", _ALLOW, artifact=card)


def timed(fn, run: Any, lead: LeadInput, deps: Any) -> StepResult:
    """Run a step function and stamp its latency."""
    started = time.monotonic()
    result = fn(run, lead, deps)
    result.latency_ms = int((time.monotonic() - started) * 1000)
    return result


__all__ = ["WORKFLOW_NAME", "has_permission", "timed"]
