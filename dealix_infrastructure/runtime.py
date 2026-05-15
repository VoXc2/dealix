"""Operational infrastructure runtime for governed workflows.

The runtime is intentionally deterministic and in-process so it can be used in
tests, drills, and local development without external dependencies.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from time import perf_counter
from typing import Any, Callable
from uuid import uuid4


def _utcnow() -> datetime:
    return datetime.now(UTC)


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:18]}"


class WorkflowStatus(StrEnum):
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"
    WAITING_APPROVAL = "waiting_approval"


@dataclass(slots=True, frozen=True)
class IdentityPrincipal:
    """Identity for a user, agent, workflow, or tool caller."""

    principal_id: str
    principal_type: str
    tenant_id: str
    role: str
    scope: tuple[str, ...] = ()


@dataclass(slots=True, frozen=True)
class ActionEnvelope:
    """Mandatory action envelope for auditable enterprise operations."""

    tenant_id: str
    who: str
    what: str
    when: datetime
    why: str
    policy_id: str
    trace_id: str
    rollback_id: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class WorkflowStep:
    """Single workflow step specification."""

    step_id: str
    tool: str
    risk_level: str = "medium"
    max_retries: int = 2
    requires_approval: bool = False
    external_action: bool = False


@dataclass(slots=True, frozen=True)
class WorkflowDefinition:
    """Workflow definition that can be executed by WorkflowEngine."""

    workflow_id: str
    name: str
    trigger: str
    steps: tuple[WorkflowStep, ...]


@dataclass(slots=True)
class WorkflowRun:
    """Result and telemetry for one workflow execution."""

    run_id: str
    tenant_id: str
    workflow_id: str
    started_at: datetime
    finished_at: datetime | None = None
    status: WorkflowStatus = WorkflowStatus.COMPLETED
    completed_steps: list[str] = field(default_factory=list)
    failed_step: str | None = None
    trace_id: str = ""
    approval_events: list[str] = field(default_factory=list)
    retries: dict[str, int] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class AuditRecord:
    action: ActionEnvelope
    outcome: str
    details: dict[str, Any] = field(default_factory=dict)
    recorded_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class MemoryRecord:
    tenant_id: str
    namespace: str
    content: str
    citations: tuple[str, ...]
    lineage: tuple[str, ...]
    created_at: datetime = field(default_factory=_utcnow)


@dataclass(slots=True, frozen=True)
class TraceSpan:
    trace_id: str
    span_id: str
    name: str
    started_at: datetime
    ended_at: datetime | None
    status: str
    attributes: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, frozen=True)
class MetricPoint:
    name: str
    value: float
    labels: dict[str, str]
    observed_at: datetime = field(default_factory=_utcnow)


class TenantIsolationError(PermissionError):
    """Raised when one tenant attempts to touch another tenant's data."""


class PermissionDenied(PermissionError):
    """Raised when caller lacks required permission."""


class WorkflowExecutionError(RuntimeError):
    """Raised when a workflow step fails after retry budget."""


class TenantBoundary:
    """Minimal tenant registry and hard access assertions."""

    def __init__(self) -> None:
        self._tenants: set[str] = set()

    def register(self, tenant_id: str) -> None:
        if not tenant_id:
            raise ValueError("tenant_id is required")
        self._tenants.add(tenant_id)

    def assert_known(self, tenant_id: str) -> None:
        if tenant_id not in self._tenants:
            raise TenantIsolationError(f"Unknown tenant: {tenant_id!r}")

    def assert_same_tenant(self, request_tenant: str, object_tenant: str) -> None:
        self.assert_known(request_tenant)
        self.assert_known(object_tenant)
        if request_tenant != object_tenant:
            raise TenantIsolationError(
                f"Cross-tenant access blocked: {request_tenant!r} -> {object_tenant!r}"
            )


class PermissionEngine:
    """Simple RBAC with role and wildcard permission checks."""

    ROLE_PERMISSIONS: dict[str, set[str]] = {
        "viewer": {"memory:read", "workflow:read", "executive:read"},
        "operator": {"memory:read", "memory:write", "workflow:run", "executive:read"},
        "approver": {"approval:decide", "workflow:approve", "executive:read"},
        "tenant_admin": {"*"},
    }

    def __init__(self) -> None:
        self._principals: dict[str, IdentityPrincipal] = {}

    def register_principal(self, principal: IdentityPrincipal) -> None:
        self._principals[principal.principal_id] = principal

    def get(self, principal_id: str) -> IdentityPrincipal:
        if principal_id not in self._principals:
            raise PermissionDenied(f"Unknown principal: {principal_id!r}")
        return self._principals[principal_id]

    def has_permission(self, principal_id: str, permission: str) -> bool:
        principal = self.get(principal_id)
        grants = self.ROLE_PERMISSIONS.get(principal.role, set())
        if "*" in grants or permission in grants:
            return True
        namespace = permission.split(":", 1)[0]
        return f"{namespace}:*" in grants

    def require(self, principal_id: str, permission: str) -> None:
        if not self.has_permission(principal_id, permission):
            raise PermissionDenied(
                f"Principal {principal_id!r} lacks permission {permission!r}"
            )


class AuditLogStore:
    """Append-only action log."""

    def __init__(self) -> None:
        self._records: list[AuditRecord] = []

    def append(self, record: AuditRecord) -> None:
        self._records.append(record)

    def all(self) -> list[AuditRecord]:
        return list(self._records)

    def for_tenant(self, tenant_id: str) -> list[AuditRecord]:
        return [r for r in self._records if r.action.tenant_id == tenant_id]


class RecoveryEngine:
    """Tracks reversible operations and can execute rollback drills."""

    def __init__(self) -> None:
        self._callbacks: dict[str, Callable[[], None]] = {}
        self._rolled_back: set[str] = set()

    def register(self, rollback_id: str, callback: Callable[[], None]) -> None:
        self._callbacks[rollback_id] = callback

    def rollback(self, rollback_id: str) -> bool:
        callback = self._callbacks.get(rollback_id)
        if callback is None:
            return False
        callback()
        self._rolled_back.add(rollback_id)
        return True

    def was_rolled_back(self, rollback_id: str) -> bool:
        return rollback_id in self._rolled_back


class ApprovalRegistry:
    """Approval decisions for high-risk or externally impactful actions."""

    def __init__(self) -> None:
        self._approved_keys: set[str] = set()

    def approve(self, approval_key: str) -> None:
        self._approved_keys.add(approval_key)

    def is_approved(self, approval_key: str) -> bool:
        return approval_key in self._approved_keys


@dataclass(slots=True, frozen=True)
class GovernanceDecision:
    status: str
    policy_id: str
    risk_score: float
    reasons: tuple[str, ...]


class GovernanceRuntime:
    """Risk + policy + approval checks before execution."""

    def __init__(self, approvals: ApprovalRegistry) -> None:
        self._approvals = approvals

    def evaluate(
        self,
        *,
        step: WorkflowStep,
        has_decision_passport: bool,
        approval_key: str,
    ) -> GovernanceDecision:
        risk_map = {"low": 0.2, "medium": 0.5, "high": 0.75, "critical": 0.95}
        risk_score = risk_map.get(step.risk_level, 0.5)
        reasons: list[str] = []
        policy_id = "policy.default"

        if step.external_action and not has_decision_passport:
            reasons.append("No Decision Passport for external action")
            return GovernanceDecision(
                status="blocked",
                policy_id="policy.no_passport_no_external_action",
                risk_score=risk_score,
                reasons=tuple(reasons),
            )

        if step.requires_approval or risk_score >= 0.75:
            policy_id = "policy.approval_required"
            if not self._approvals.is_approved(approval_key):
                reasons.append("Approval required before execution")
                return GovernanceDecision(
                    status="pending_approval",
                    policy_id=policy_id,
                    risk_score=risk_score,
                    reasons=tuple(reasons),
                )

        reasons.append("Governance checks passed")
        return GovernanceDecision(
            status="approved",
            policy_id=policy_id,
            risk_score=risk_score,
            reasons=tuple(reasons),
        )


class OperationalMemory:
    """Permission-aware memory with citations and lineage."""

    def __init__(self, tenant_boundary: TenantBoundary, permissions: PermissionEngine) -> None:
        self._tenant_boundary = tenant_boundary
        self._permissions = permissions
        self._records: list[MemoryRecord] = []

    def write(
        self,
        *,
        tenant_id: str,
        principal_id: str,
        namespace: str,
        content: str,
        citations: tuple[str, ...] = (),
        lineage: tuple[str, ...] = (),
    ) -> None:
        self._tenant_boundary.assert_known(tenant_id)
        self._permissions.require(principal_id, "memory:write")
        principal = self._permissions.get(principal_id)
        self._tenant_boundary.assert_same_tenant(principal.tenant_id, tenant_id)
        self._records.append(
            MemoryRecord(
                tenant_id=tenant_id,
                namespace=namespace,
                content=content,
                citations=citations,
                lineage=lineage,
            )
        )

    def retrieve(
        self,
        *,
        tenant_id: str,
        principal_id: str,
        query: str,
        namespace: str | None = None,
    ) -> list[MemoryRecord]:
        self._tenant_boundary.assert_known(tenant_id)
        self._permissions.require(principal_id, "memory:read")
        principal = self._permissions.get(principal_id)
        self._tenant_boundary.assert_same_tenant(principal.tenant_id, tenant_id)

        q = query.lower().strip()
        out: list[MemoryRecord] = []
        for record in self._records:
            if record.tenant_id != tenant_id:
                continue
            if namespace and record.namespace != namespace:
                continue
            if q and q not in record.content.lower():
                continue
            out.append(record)
        return out


class ObservabilityRuntime:
    """Collects traces, logs, metrics, and alerts for replayability."""

    def __init__(self) -> None:
        self._spans: list[TraceSpan] = []
        self._metrics: list[MetricPoint] = []
        self._logs: list[dict[str, Any]] = []
        self._alerts: list[dict[str, Any]] = []

    def start_span(self, trace_id: str, name: str, attributes: dict[str, Any]) -> str:
        span_id = _new_id("span")
        self._spans.append(
            TraceSpan(
                trace_id=trace_id,
                span_id=span_id,
                name=name,
                started_at=_utcnow(),
                ended_at=None,
                status="running",
                attributes=dict(attributes),
            )
        )
        return span_id

    def end_span(self, span_id: str, *, status: str) -> None:
        for idx, span in enumerate(self._spans):
            if span.span_id != span_id:
                continue
            self._spans[idx] = TraceSpan(
                trace_id=span.trace_id,
                span_id=span.span_id,
                name=span.name,
                started_at=span.started_at,
                ended_at=_utcnow(),
                status=status,
                attributes=span.attributes,
            )
            return

    def log(self, event: str, **fields: Any) -> None:
        self._logs.append({"event": event, "when": _utcnow(), **fields})

    def metric(self, name: str, value: float, labels: dict[str, str]) -> None:
        self._metrics.append(MetricPoint(name=name, value=value, labels=dict(labels)))

    def alert(self, name: str, severity: str, detail: str) -> None:
        self._alerts.append(
            {"name": name, "severity": severity, "detail": detail, "when": _utcnow()}
        )

    def replay_trace(self, trace_id: str) -> list[TraceSpan]:
        return [span for span in self._spans if span.trace_id == trace_id]

    @property
    def metrics(self) -> list[MetricPoint]:
        return list(self._metrics)

    @property
    def alerts(self) -> list[dict[str, Any]]:
        return list(self._alerts)


class WorkflowEngine:
    """Governed workflow execution engine."""

    def __init__(
        self,
        *,
        tenant_boundary: TenantBoundary,
        permissions: PermissionEngine,
        governance: GovernanceRuntime,
        audit_logs: AuditLogStore,
        recovery: RecoveryEngine,
        observability: ObservabilityRuntime,
        memory: OperationalMemory,
    ) -> None:
        self._tenant_boundary = tenant_boundary
        self._permissions = permissions
        self._governance = governance
        self._audit_logs = audit_logs
        self._recovery = recovery
        self._observability = observability
        self._memory = memory

    def run(
        self,
        *,
        definition: WorkflowDefinition,
        tenant_id: str,
        principal_id: str,
        tool_registry: dict[str, Callable[[dict[str, Any]], dict[str, Any]]],
        payload: dict[str, Any],
        has_decision_passport: bool,
    ) -> WorkflowRun:
        self._tenant_boundary.assert_known(tenant_id)
        self._permissions.require(principal_id, "workflow:run")
        principal = self._permissions.get(principal_id)
        self._tenant_boundary.assert_same_tenant(principal.tenant_id, tenant_id)

        run = WorkflowRun(
            run_id=_new_id("run"),
            tenant_id=tenant_id,
            workflow_id=definition.workflow_id,
            started_at=_utcnow(),
            trace_id=_new_id("trace"),
        )

        for step in definition.steps:
            approval_key = f"{definition.workflow_id}:{step.step_id}"
            decision = self._governance.evaluate(
                step=step,
                has_decision_passport=has_decision_passport,
                approval_key=approval_key,
            )
            run.approval_events.append(decision.status)
            if decision.status == "blocked":
                run.status = WorkflowStatus.BLOCKED
                run.failed_step = step.step_id
                self._observability.alert(
                    "workflow_blocked",
                    "high",
                    f"{definition.workflow_id}:{step.step_id}:{decision.policy_id}",
                )
                self._audit_logs.append(
                    AuditRecord(
                        action=ActionEnvelope(
                            tenant_id=tenant_id,
                            who=principal_id,
                            what=f"{definition.workflow_id}.{step.step_id}",
                            when=_utcnow(),
                            why=payload.get("why", "workflow_execution"),
                            policy_id=decision.policy_id,
                            trace_id=run.trace_id,
                            rollback_id=_new_id("rb"),
                            metadata={"decision": decision.status, "reasons": decision.reasons},
                        ),
                        outcome="blocked",
                    )
                )
                run.finished_at = _utcnow()
                return run

            if decision.status == "pending_approval":
                run.status = WorkflowStatus.WAITING_APPROVAL
                run.failed_step = step.step_id
                run.finished_at = _utcnow()
                return run

            if step.tool not in tool_registry:
                raise WorkflowExecutionError(f"Tool {step.tool!r} is not registered")

            span_id = self._observability.start_span(
                run.trace_id,
                f"{definition.workflow_id}.{step.step_id}",
                {"tenant_id": tenant_id, "tool": step.tool},
            )
            rollback_id = _new_id("rb")
            envelope = ActionEnvelope(
                tenant_id=tenant_id,
                who=principal_id,
                what=f"{definition.workflow_id}.{step.step_id}",
                when=_utcnow(),
                why=payload.get("why", "workflow_execution"),
                policy_id=decision.policy_id,
                trace_id=run.trace_id,
                rollback_id=rollback_id,
                metadata={"risk": step.risk_level},
            )

            started = perf_counter()
            attempt = 0
            step_result: dict[str, Any] | None = None
            while attempt < max(1, step.max_retries):
                attempt += 1
                run.retries[step.step_id] = attempt - 1
                try:
                    step_result = tool_registry[step.tool](dict(payload))
                    break
                except Exception as exc:  # pragma: no cover - exercised via tests
                    if attempt >= max(1, step.max_retries):
                        run.status = WorkflowStatus.FAILED
                        run.failed_step = step.step_id
                        self._audit_logs.append(
                            AuditRecord(
                                action=envelope,
                                outcome="failed",
                                details={"error": str(exc), "attempts": attempt},
                            )
                        )
                        self._observability.end_span(span_id, status="error")
                        self._observability.metric(
                            "workflow_step_latency_ms",
                            (perf_counter() - started) * 1000.0,
                            {
                                "workflow_id": definition.workflow_id,
                                "step_id": step.step_id,
                                "status": "failed",
                            },
                        )
                        run.finished_at = _utcnow()
                        return run

            assert step_result is not None
            self._audit_logs.append(AuditRecord(action=envelope, outcome="completed", details=step_result))
            self._memory.write(
                tenant_id=tenant_id,
                principal_id=principal_id,
                namespace="workflow_execution",
                content=f"{definition.workflow_id}:{step.step_id}:{step_result.get('summary', 'ok')}",
                citations=tuple(step_result.get("citations", ())),
                lineage=(run.run_id, step.step_id),
            )
            if step_result.get("rollback_callable"):
                callback = step_result["rollback_callable"]
                if callable(callback):
                    self._recovery.register(rollback_id, callback)

            run.completed_steps.append(step.step_id)
            self._observability.end_span(span_id, status="ok")
            self._observability.metric(
                "workflow_step_latency_ms",
                (perf_counter() - started) * 1000.0,
                {"workflow_id": definition.workflow_id, "step_id": step.step_id, "status": "ok"},
            )

        run.status = WorkflowStatus.COMPLETED
        run.finished_at = _utcnow()
        return run


class ExecutiveReporter:
    """Builds outcome-oriented executive metrics."""

    def build_report(
        self,
        *,
        run: WorkflowRun,
        audit_logs: AuditLogStore,
        observability: ObservabilityRuntime,
    ) -> dict[str, Any]:
        tenant_logs = audit_logs.for_tenant(run.tenant_id)
        completed = [r for r in tenant_logs if r.outcome == "completed"]
        blocked = [r for r in tenant_logs if r.outcome == "blocked"]
        failures = [r for r in tenant_logs if r.outcome == "failed"]
        workflow_metrics = [m for m in observability.metrics if m.name == "workflow_step_latency_ms"]

        avg_latency = 0.0
        if workflow_metrics:
            avg_latency = sum(m.value for m in workflow_metrics) / len(workflow_metrics)
        efficiency = float(len(completed)) / max(len(tenant_logs), 1)
        roi_score = round((efficiency * 100.0) - (len(blocked) * 3.0) - (len(failures) * 5.0), 2)
        return {
            "tenant_id": run.tenant_id,
            "workflow_id": run.workflow_id,
            "run_id": run.run_id,
            "status": run.status.value,
            "workflow_efficiency": round(efficiency, 3),
            "operational_latency_ms_avg": round(avg_latency, 2),
            "conversion_lift_proxy": max(len(completed) - len(blocked), 0),
            "revenue_impact_proxy": len(completed) * 1000,
            "roi_score": max(roi_score, 0.0),
        }


class DeliveryPlaybooks:
    """Canonical customer delivery machine playbooks."""

    PLAYBOOKS: dict[str, tuple[str, ...]] = {
        "discovery": (
            "Collect current workflow baseline and ownership map",
            "Confirm legal basis and contactability rules",
        ),
        "onboarding": (
            "Provision tenant, users, and role scopes",
            "Configure governed workflow and approval matrix",
        ),
        "delivery": (
            "Run workflow with monitored execution",
            "Publish executive report and action log summary",
        ),
        "qa": (
            "Run readiness drill",
            "Verify rollback and cross-tenant isolation checks",
        ),
        "monthly_review": (
            "Review ROI and latency trends",
            "Tune policy and retry thresholds",
        ),
    }

    def list_playbooks(self) -> dict[str, tuple[str, ...]]:
        return dict(self.PLAYBOOKS)
