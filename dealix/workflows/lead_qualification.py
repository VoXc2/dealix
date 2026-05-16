"""Governed lead-qualification workflow for the Revenue OS."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Any
from uuid import uuid4

import yaml

from dealix.contracts.audit_log import AuditAction, AuditEntry
from dealix.trust.audit import AuditSink, InMemoryAuditSink

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_WORKFLOW_PATH = REPO_ROOT / "workflows" / "lead_qualification.workflow.yaml"

WORKFLOW_STEP_SEQUENCE: tuple[str, ...] = (
    "lead_enters",
    "detect_tenant",
    "check_rbac",
    "retrieve_company_context",
    "qualify_lead",
    "score_lead",
    "draft_response",
    "risk_check",
    "approval",
    "crm_update",
    "emit_metrics",
)

PERMISSION_WORKFLOW_RUN = "workflow.lead_qualification.run"
PERMISSION_COMPANY_CONTEXT_READ = "memory.company_context.read"
PERMISSION_CRM_WRITE = "crm.lead.write"
PERMISSION_APPROVAL_REQUEST = "governance.approval.request"

DEFAULT_ROLE_PERMISSIONS: dict[str, frozenset[str]] = {
    "tenant_admin": frozenset(
        {
            PERMISSION_WORKFLOW_RUN,
            PERMISSION_COMPANY_CONTEXT_READ,
            PERMISSION_CRM_WRITE,
            PERMISSION_APPROVAL_REQUEST,
        }
    ),
    "revenue_operator": frozenset(
        {
            PERMISSION_WORKFLOW_RUN,
            PERMISSION_COMPANY_CONTEXT_READ,
            PERMISSION_CRM_WRITE,
        }
    ),
    "risk_officer": frozenset(
        {
            PERMISSION_WORKFLOW_RUN,
            PERMISSION_COMPANY_CONTEXT_READ,
            PERMISSION_APPROVAL_REQUEST,
        }
    ),
    "viewer": frozenset(),
}


class WorkflowDefinitionError(ValueError):
    """Raised when the workflow definition is missing required fields."""


@dataclass(frozen=True, slots=True)
class LeadInput:
    """Input payload used by the lead-qualification workflow."""

    lead_id: str
    tenant_id: str
    company: str
    name: str
    email: str
    message: str
    budget_sar: float = 0.0
    source: str = "web"


@dataclass(frozen=True, slots=True)
class ActorContext:
    """Current caller identity."""

    actor_id: str
    tenant_id: str
    roles: tuple[str, ...] = ("revenue_operator",)


@dataclass(frozen=True, slots=True)
class CompanyContext:
    """Permission-aware company context."""

    company: str
    summary: str
    signals: tuple[str, ...] = ()
    region: str = "Saudi Arabia"


@dataclass(slots=True)
class WorkflowExecutionResult:
    """Outcome + observability payload."""

    run_id: str
    status: str
    reason: str
    tenant_id: str
    lead_id: str
    qualification: str
    lead_score: float
    risk_score: float
    approval_required: bool
    draft_response_ar: str
    metrics: dict[str, float]
    rollback_token: str | None
    steps_executed: tuple[str, ...]
    audit_entries: tuple[AuditEntry, ...]


class RoleMatrix:
    """Simple deterministic RBAC map."""

    def __init__(self, permissions_by_role: dict[str, frozenset[str]] | None = None) -> None:
        self._permissions_by_role = permissions_by_role or DEFAULT_ROLE_PERMISSIONS

    def has_permission(self, actor: ActorContext, permission: str) -> bool:
        return any(
            permission in self._permissions_by_role.get(role, frozenset()) for role in actor.roles
        )


class InMemoryTenantContextStore:
    """Tenant-scoped company context store."""

    def __init__(self) -> None:
        self._store: dict[str, dict[str, CompanyContext]] = {}

    def upsert(self, tenant_id: str, context: CompanyContext) -> None:
        self._store.setdefault(tenant_id, {})[context.company.lower()] = context

    def get(self, tenant_id: str, company: str) -> CompanyContext | None:
        return self._store.get(tenant_id, {}).get(company.lower())


class InMemoryCRMStore:
    """Very small tenant-aware CRM projection store."""

    def __init__(self) -> None:
        self._leads: dict[str, dict[str, dict[str, Any]]] = {}

    def get(self, tenant_id: str, lead_id: str) -> dict[str, Any] | None:
        tenant_leads = self._leads.get(tenant_id, {})
        existing = tenant_leads.get(lead_id)
        if existing is None:
            return None
        return dict(existing)

    def upsert(self, tenant_id: str, lead_id: str, payload: dict[str, Any]) -> None:
        self._leads.setdefault(tenant_id, {})[lead_id] = dict(payload)

    def delete(self, tenant_id: str, lead_id: str) -> None:
        tenant_leads = self._leads.get(tenant_id)
        if tenant_leads is None:
            return
        tenant_leads.pop(lead_id, None)


class InMemoryRollbackJournal:
    """Records CRM snapshots so a workflow run can be compensated."""

    def __init__(self) -> None:
        self._snapshots: dict[str, tuple[str, str, dict[str, Any] | None]] = {}

    def record_crm_upsert(
        self, token: str, tenant_id: str, lead_id: str, previous: dict[str, Any] | None
    ) -> None:
        self._snapshots[token] = (tenant_id, lead_id, previous)

    def rollback(self, token: str, crm_store: InMemoryCRMStore) -> bool:
        snapshot = self._snapshots.get(token)
        if snapshot is None:
            return False
        tenant_id, lead_id, previous = snapshot
        if previous is None:
            crm_store.delete(tenant_id, lead_id)
        else:
            crm_store.upsert(tenant_id, lead_id, previous)
        return True


def load_lead_qualification_workflow_definition(
    workflow_path: Path | None = None,
) -> dict[str, Any]:
    """Load and validate the lead-qualification workflow YAML."""
    path = workflow_path or DEFAULT_WORKFLOW_PATH
    if not path.exists():
        raise WorkflowDefinitionError(f"workflow definition missing: {path}")

    with path.open("r", encoding="utf-8") as handle:
        raw = yaml.safe_load(handle)
    if not isinstance(raw, dict):
        raise WorkflowDefinitionError("workflow definition must be a mapping")

    for key in ("name", "version", "steps"):
        if key not in raw:
            raise WorkflowDefinitionError(f"workflow definition missing key: {key}")

    step_rows = raw.get("steps")
    if not isinstance(step_rows, list):
        raise WorkflowDefinitionError("workflow steps must be a list")

    ids = tuple(str(step.get("step_id", "")) for step in step_rows if isinstance(step, dict))
    if ids != WORKFLOW_STEP_SEQUENCE:
        raise WorkflowDefinitionError(
            f"workflow step sequence mismatch: expected {WORKFLOW_STEP_SEQUENCE}, got {ids}"
        )

    return raw


class LeadQualificationWorkflow:
    """Executes the first unavoidable governed workflow end-to-end."""

    def __init__(
        self,
        *,
        audit_sink: AuditSink | None = None,
        role_matrix: RoleMatrix | None = None,
        context_store: InMemoryTenantContextStore | None = None,
        crm_store: InMemoryCRMStore | None = None,
        rollback_journal: InMemoryRollbackJournal | None = None,
        risk_threshold: float = 0.7,
        workflow_path: Path | None = None,
    ) -> None:
        self.audit = audit_sink or InMemoryAuditSink()
        self.roles = role_matrix or RoleMatrix()
        self.context_store = context_store or InMemoryTenantContextStore()
        self.crm_store = crm_store or InMemoryCRMStore()
        self.rollback_journal = rollback_journal or InMemoryRollbackJournal()
        self.risk_threshold = risk_threshold
        self.definition = load_lead_qualification_workflow_definition(workflow_path)

    def run(self, lead: LeadInput, actor: ActorContext) -> WorkflowExecutionResult:
        """Run the workflow deterministically with governance checks."""
        run_id = f"run_{uuid4().hex[:16]}"
        started_at = perf_counter()
        step_metrics: dict[str, float] = {}
        audit_entries: list[AuditEntry] = []
        rollback_token: str | None = None
        steps_executed: list[str] = []

        def step(step_id: str, action: AuditAction, *, details: dict[str, Any] | None = None) -> None:
            step_start = perf_counter()
            steps_executed.append(step_id)
            entry = AuditEntry(
                tenant_id=lead.tenant_id,
                action=action,
                actor_type="workflow",
                actor_id=actor.actor_id,
                entity_id=lead.lead_id,
                workflow_id=self.definition["name"],
                trace_id=run_id,
                details=details or {"step_id": step_id},
            )
            self.audit.append(entry)
            audit_entries.append(entry)
            step_metrics[f"step_{step_id}_ms"] = round((perf_counter() - step_start) * 1000, 3)

        step("lead_enters", AuditAction.WORKFLOW_STARTED, details={"source": lead.source})
        step("detect_tenant", AuditAction.ACCESS_GRANTED, details={"tenant_id": lead.tenant_id})

        if lead.tenant_id != actor.tenant_id:
            step(
                "check_rbac",
                AuditAction.ACCESS_DENIED,
                details={"reason": "tenant isolation violation", "actor_tenant_id": actor.tenant_id},
            )
            return self._finalize(
                run_id=run_id,
                started_at=started_at,
                step_metrics=step_metrics,
                steps_executed=steps_executed,
                audit_entries=audit_entries,
                lead=lead,
                status="denied",
                reason="tenant isolation violation",
                qualification="blocked",
                lead_score=0.0,
                risk_score=1.0,
                approval_required=False,
                draft_response_ar="تم رفض التنفيذ بسبب عزل المستأجر.",
                rollback_token=None,
                failed=True,
            )

        required_permissions = (
            PERMISSION_WORKFLOW_RUN,
            PERMISSION_COMPANY_CONTEXT_READ,
        )
        for permission in required_permissions:
            if not self.roles.has_permission(actor, permission):
                step(
                    "check_rbac",
                    AuditAction.ACCESS_DENIED,
                    details={"reason": "rbac denied", "missing_permission": permission},
                )
                return self._finalize(
                    run_id=run_id,
                    started_at=started_at,
                    step_metrics=step_metrics,
                    steps_executed=steps_executed,
                    audit_entries=audit_entries,
                    lead=lead,
                    status="denied",
                    reason=f"rbac denied: {permission}",
                    qualification="blocked",
                    lead_score=0.0,
                    risk_score=1.0,
                    approval_required=False,
                    draft_response_ar="تم رفض التنفيذ بسبب صلاحيات غير كافية.",
                    rollback_token=None,
                    failed=True,
                )
        step("check_rbac", AuditAction.ACCESS_GRANTED, details={"roles": list(actor.roles)})

        context = self.context_store.get(lead.tenant_id, lead.company)
        step(
            "retrieve_company_context",
            AuditAction.TOOL_INVOKED,
            details={"context_found": context is not None, "company": lead.company},
        )

        qualification = self._qualify_lead(lead, context)
        step("qualify_lead", AuditAction.DECISION_EMITTED, details={"qualification": qualification})

        lead_score = self._score_lead(lead, context)
        step("score_lead", AuditAction.DECISION_EMITTED, details={"lead_score": lead_score})

        draft_response_ar = self._draft_response(lead, lead_score, context)
        step("draft_response", AuditAction.TOOL_VERIFIED, details={"draft_ready": True})

        risk_score = self._risk_score(lead, lead_score)
        step("risk_check", AuditAction.POLICY_EVALUATED, details={"risk_score": risk_score})

        approval_required = risk_score >= self.risk_threshold
        if approval_required:
            if not self.roles.has_permission(actor, PERMISSION_APPROVAL_REQUEST):
                step(
                    "approval",
                    AuditAction.ACCESS_DENIED,
                    details={"reason": "missing approval permission"},
                )
                return self._finalize(
                    run_id=run_id,
                    started_at=started_at,
                    step_metrics=step_metrics,
                    steps_executed=steps_executed,
                    audit_entries=audit_entries,
                    lead=lead,
                    status="denied",
                    reason="rbac denied: governance.approval.request",
                    qualification=qualification,
                    lead_score=lead_score,
                    risk_score=risk_score,
                    approval_required=True,
                    draft_response_ar=draft_response_ar,
                    rollback_token=None,
                    failed=True,
                )

            step(
                "approval",
                AuditAction.APPROVAL_REQUESTED,
                details={"risk_score": risk_score, "threshold": self.risk_threshold},
            )
            step(
                "crm_update",
                AuditAction.POLICY_ESCALATED,
                details={"crm_updated": False, "reason": "awaiting approval"},
            )
            return self._finalize(
                run_id=run_id,
                started_at=started_at,
                step_metrics=step_metrics,
                steps_executed=steps_executed,
                audit_entries=audit_entries,
                lead=lead,
                status="pending_approval",
                reason="risk threshold exceeded",
                qualification=qualification,
                lead_score=lead_score,
                risk_score=risk_score,
                approval_required=True,
                draft_response_ar=draft_response_ar,
                rollback_token=None,
            )

        if not self.roles.has_permission(actor, PERMISSION_CRM_WRITE):
            step("crm_update", AuditAction.ACCESS_DENIED, details={"reason": "missing crm.write.lead"})
            return self._finalize(
                run_id=run_id,
                started_at=started_at,
                step_metrics=step_metrics,
                steps_executed=steps_executed,
                audit_entries=audit_entries,
                lead=lead,
                status="denied",
                reason="rbac denied: crm.lead.write",
                qualification=qualification,
                lead_score=lead_score,
                risk_score=risk_score,
                approval_required=False,
                draft_response_ar=draft_response_ar,
                rollback_token=None,
                failed=True,
            )

        previous = self.crm_store.get(lead.tenant_id, lead.lead_id)
        rollback_token = f"rbk_{uuid4().hex[:16]}"
        self.rollback_journal.record_crm_upsert(rollback_token, lead.tenant_id, lead.lead_id, previous)
        self.crm_store.upsert(
            lead.tenant_id,
            lead.lead_id,
            {
                "tenant_id": lead.tenant_id,
                "lead_id": lead.lead_id,
                "company": lead.company,
                "name": lead.name,
                "email": lead.email,
                "qualification": qualification,
                "lead_score": lead_score,
                "risk_score": risk_score,
                "draft_response_ar": draft_response_ar,
                "trace_id": run_id,
            },
        )
        step("approval", AuditAction.POLICY_ALLOWED, details={"risk_score": risk_score})
        step(
            "crm_update",
            AuditAction.TOOL_VERIFIED,
            details={"crm_updated": True, "rollback_token": rollback_token},
        )

        return self._finalize(
            run_id=run_id,
            started_at=started_at,
            step_metrics=step_metrics,
            steps_executed=steps_executed,
            audit_entries=audit_entries,
            lead=lead,
            status="completed",
            reason="ok",
            qualification=qualification,
            lead_score=lead_score,
            risk_score=risk_score,
            approval_required=False,
            draft_response_ar=draft_response_ar,
            rollback_token=rollback_token,
        )

    def _finalize(
        self,
        *,
        run_id: str,
        started_at: float,
        step_metrics: dict[str, float],
        steps_executed: list[str],
        audit_entries: list[AuditEntry],
        lead: LeadInput,
        status: str,
        reason: str,
        qualification: str,
        lead_score: float,
        risk_score: float,
        approval_required: bool,
        draft_response_ar: str,
        rollback_token: str | None,
        failed: bool = False,
    ) -> WorkflowExecutionResult:
        completed_action = AuditAction.WORKFLOW_FAILED if failed else AuditAction.WORKFLOW_COMPLETED
        done_entry = AuditEntry(
            tenant_id=lead.tenant_id,
            action=completed_action,
            actor_type="workflow",
            entity_id=lead.lead_id,
            workflow_id=self.definition["name"],
            trace_id=run_id,
            outcome=status,
            reason=reason,
            details={"lead_score": lead_score, "risk_score": risk_score},
        )
        self.audit.append(done_entry)
        audit_entries.append(done_entry)

        metrics = dict(step_metrics)
        metrics["workflow_total_ms"] = round((perf_counter() - started_at) * 1000, 3)
        metrics["lead_score"] = float(round(lead_score, 3))
        metrics["risk_score"] = float(round(risk_score, 3))
        metrics["approval_required"] = 1.0 if approval_required else 0.0
        metrics["status_completed"] = 1.0 if status == "completed" else 0.0
        metrics["status_pending_approval"] = 1.0 if status == "pending_approval" else 0.0

        emit_entry = AuditEntry(
            tenant_id=lead.tenant_id,
            action=AuditAction.TOOL_VERIFIED,
            actor_type="workflow",
            entity_id=lead.lead_id,
            workflow_id=self.definition["name"],
            trace_id=run_id,
            details={"step_id": "emit_metrics", "workflow_total_ms": metrics["workflow_total_ms"]},
        )
        self.audit.append(emit_entry)
        audit_entries.append(emit_entry)
        steps_executed.append("emit_metrics")
        metrics["step_emit_metrics_ms"] = 0.0

        return WorkflowExecutionResult(
            run_id=run_id,
            status=status,
            reason=reason,
            tenant_id=lead.tenant_id,
            lead_id=lead.lead_id,
            qualification=qualification,
            lead_score=lead_score,
            risk_score=risk_score,
            approval_required=approval_required,
            draft_response_ar=draft_response_ar,
            metrics=metrics,
            rollback_token=rollback_token,
            steps_executed=tuple(steps_executed),
            audit_entries=tuple(audit_entries),
        )

    def _qualify_lead(self, lead: LeadInput, context: CompanyContext | None) -> str:
        text = lead.message.lower()
        priority_terms = ("pricing", "pilot", "contract", "meeting", "demo", "migration")
        signal_hits = sum(term in text for term in priority_terms)
        if context and any("high_intent" in signal for signal in context.signals):
            signal_hits += 1
        if lead.budget_sar >= 50_000 or signal_hits >= 3:
            return "hot"
        if lead.budget_sar >= 10_000 or signal_hits >= 1:
            return "warm"
        return "cold"

    def _score_lead(self, lead: LeadInput, context: CompanyContext | None) -> float:
        score = 25.0
        if lead.budget_sar >= 100_000:
            score += 35.0
        elif lead.budget_sar >= 50_000:
            score += 25.0
        elif lead.budget_sar >= 10_000:
            score += 15.0

        text = lead.message.lower()
        for term in ("urgent", "ready", "contract", "demo", "integration", "roi"):
            if term in text:
                score += 6.0

        if context and any("existing_customer" in signal for signal in context.signals):
            score += 12.0
        if context and any("high_intent" in signal for signal in context.signals):
            score += 10.0
        return float(max(0.0, min(score, 100.0)))

    def _risk_score(self, lead: LeadInput, lead_score: float) -> float:
        risk = 0.15
        if lead_score < 40:
            risk += 0.35
        elif lead_score < 60:
            risk += 0.2

        text = lead.message.lower()
        for term in ("refund", "legal", "complaint", "breach", "bulk send"):
            if term in text:
                risk += 0.15
        if "personal data" in text:
            risk += 0.1
        return float(max(0.0, min(risk, 1.0)))

    def _draft_response(
        self, lead: LeadInput, lead_score: float, context: CompanyContext | None
    ) -> str:
        context_hint = ""
        if context is not None and context.summary:
            context_hint = f" بناءً على سياق {context.company}: {context.summary}."

        if lead_score >= 75:
            return (
                "شكرًا للتواصل. نوصي بجدولة اجتماع تشخيصي خلال 24 ساعة لتأكيد "
                f"الأثر التجاري وخطة التنفيذ.{context_hint}"
            )
        if lead_score >= 50:
            return (
                "شكرًا للتواصل. جهّزنا لك مسودة عرض مبدئي ونحتاج بعض التفاصيل "
                f"الإضافية قبل التفعيل النهائي.{context_hint}"
            )
        return (
            "شكرًا لتواصلكم. سنحتاج معلومات إضافية عن الحالة الحالية والأهداف "
            f"التجارية قبل إرسال التوصية المناسبة.{context_hint}"
        )
