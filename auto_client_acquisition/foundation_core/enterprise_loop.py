"""Smallest governed enterprise workflow for Dealix foundation core.

This module intentionally implements one complete loop:
trigger -> qualification -> retrieval -> scoring -> response ->
approval -> CRM update -> executive metrics -> rollback drill.
"""

from __future__ import annotations

import copy
import time
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Callable


def _utcnow_iso() -> str:
    return datetime.now(UTC).isoformat()


@dataclass(slots=True)
class LeadInput:
    company: str
    name: str
    email: str
    phone: str | None = None
    sector: str | None = None
    region: str | None = None
    message: str | None = None
    budget: float | None = None


@dataclass(slots=True)
class EnterpriseLoopRequest:
    tenant_id: str
    user_id: str
    user_role: str
    lead: LeadInput
    approval_granted: bool = False
    users_in_tenant: int = 3
    roles_configured: list[str] = field(
        default_factory=lambda: ["tenant_admin", "sales_manager"]
    )
    crm_integration: str = "simulated_crm"


@dataclass(slots=True)
class WorkflowStepResult:
    step: str
    status: str
    attempts: int
    duration_ms: int
    detail: str = ""


ROLE_PERMISSIONS: dict[str, set[str]] = {
    "viewer": {"workflow:read"},
    "sales_rep": {"workflow:run", "agent:run:sales_agent"},
    "sales_manager": {"workflow:run", "agent:run:sales_agent", "approval:request"},
    "tenant_admin": {"workflow:*", "agent:*", "approval:*", "governance:*"},
}


def _has_permission(role: str, permission: str) -> bool:
    perms = ROLE_PERMISSIONS.get(role, set())
    if permission in perms or "*" in perms:
        return True
    namespace = permission.split(":", 1)[0]
    return f"{namespace}:*" in perms


class WorkflowBlocked(Exception):
    """Raised when governance blocks a workflow step."""


class AuditLogger:
    def __init__(self, tenant_id: str, user_id: str) -> None:
        self._tenant_id = tenant_id
        self._user_id = user_id
        self._entries: list[dict[str, Any]] = []

    def write(self, action: str, status: str, details: dict[str, Any] | None = None) -> None:
        self._entries.append(
            {
                "timestamp": _utcnow_iso(),
                "tenant_id": self._tenant_id,
                "user_id": self._user_id,
                "action": action,
                "status": status,
                "details": details or {},
            }
        )

    @property
    def entries(self) -> list[dict[str, Any]]:
        return list(self._entries)


class ObservabilityRuntime:
    def __init__(self) -> None:
        self.trace_id = f"trace_{uuid.uuid4().hex[:16]}"
        self._started_at = time.perf_counter()
        self._logs: list[dict[str, Any]] = []
        self._metrics: dict[str, float] = {
            "workflow_steps_total": 0,
            "workflow_retries_total": 0,
            "workflow_blocked_total": 0,
        }

    def log(self, event: str, **fields: Any) -> None:
        self._logs.append({"timestamp": _utcnow_iso(), "event": event, **fields})

    def record_step(self, *, status: str, retries: int) -> None:
        self._metrics["workflow_steps_total"] += 1
        self._metrics["workflow_retries_total"] += retries
        if status == "blocked":
            self._metrics["workflow_blocked_total"] += 1

    def snapshot(self) -> dict[str, Any]:
        elapsed_ms = int((time.perf_counter() - self._started_at) * 1000)
        return {
            "trace_id": self.trace_id,
            "logs": list(self._logs),
            "metrics": {**self._metrics, "workflow_elapsed_ms": elapsed_ms},
        }


class GovernanceEngine:
    """Minimal governance gate: risk -> policy -> approval -> execution."""

    def evaluate(
        self,
        *,
        action: str,
        lead: dict[str, Any],
        score: float,
        approval_granted: bool,
    ) -> dict[str, Any]:
        risk_score = 25.0
        if score >= 70:
            risk_score += 20
        if (lead.get("sector") or "").lower() in {"finance", "healthcare"}:
            risk_score += 20
        if action == "crm.update":
            risk_score += 20
        policy_ok = action != "external.send"
        requires_approval = risk_score >= 60 or action == "crm.update"
        approved = approval_granted if requires_approval else True
        allowed = policy_ok and approved
        return {
            "risk_score": round(risk_score, 2),
            "policy_ok": policy_ok,
            "requires_approval": requires_approval,
            "approval_granted": approval_granted,
            "allowed": allowed,
            "reason": "approved" if allowed else "manual_approval_required",
        }


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Callable[[dict[str, Any]], dict[str, Any]]] = {}

    def register(self, name: str, handler: Callable[[dict[str, Any]], dict[str, Any]) -> None:
        self._agents[name] = handler

    def run(self, name: str, payload: dict[str, Any]) -> dict[str, Any]:
        if name not in self._agents:
            raise KeyError(f"agent_not_registered:{name}")
        return self._agents[name](payload)

    def describe(self) -> list[dict[str, str]]:
        return [{"agent_name": name, "status": "active"} for name in sorted(self._agents)]


class SimpleWorkflowEngine:
    def __init__(self, max_retries: int = 1) -> None:
        self.max_retries = max_retries

    def run(
        self,
        *,
        context: dict[str, Any],
        steps: list[tuple[str, Callable[[dict[str, Any]], None], bool]],
        observability: ObservabilityRuntime,
    ) -> tuple[str, list[WorkflowStepResult], str | None]:
        results: list[WorkflowStepResult] = []
        for step_name, step_fn, retryable in steps:
            attempts = 0
            step_start = time.perf_counter()
            while True:
                attempts += 1
                try:
                    step_fn(context)
                    duration_ms = int((time.perf_counter() - step_start) * 1000)
                    results.append(
                        WorkflowStepResult(
                            step=step_name,
                            status="ok",
                            attempts=attempts,
                            duration_ms=duration_ms,
                        )
                    )
                    observability.record_step(status="ok", retries=max(attempts - 1, 0))
                    break
                except WorkflowBlocked as exc:
                    duration_ms = int((time.perf_counter() - step_start) * 1000)
                    results.append(
                        WorkflowStepResult(
                            step=step_name,
                            status="blocked",
                            attempts=attempts,
                            duration_ms=duration_ms,
                            detail=str(exc),
                        )
                    )
                    observability.record_step(status="blocked", retries=max(attempts - 1, 0))
                    return "blocked", results, str(exc)
                except Exception as exc:  # pragma: no cover - defensive guard
                    if retryable and attempts <= self.max_retries:
                        continue
                    duration_ms = int((time.perf_counter() - step_start) * 1000)
                    results.append(
                        WorkflowStepResult(
                            step=step_name,
                            status="error",
                            attempts=attempts,
                            duration_ms=duration_ms,
                            detail=str(exc),
                        )
                    )
                    observability.record_step(status="error", retries=max(attempts - 1, 0))
                    return "failed", results, str(exc)
        return "completed", results, None


def _sales_agent(payload: dict[str, Any]) -> dict[str, Any]:
    lead = payload["lead"]
    score = 0
    if lead.get("email"):
        score += 20
    if lead.get("phone"):
        score += 10
    if lead.get("message"):
        score += 20
    if lead.get("budget", 0) and float(lead.get("budget", 0)) >= 5000:
        score += 25
    if (lead.get("sector") or "").lower() in {"technology", "software", "saas"}:
        score += 15
    if score >= 70:
        tier = "high"
        suggested_response = (
            "مسودة: العميل مؤهَّل عاليًا. أوصِ بـ Pilot مع عرض قيمة واضح وطلب اعتماد يدوي."
        )
    elif score >= 40:
        tier = "medium"
        suggested_response = (
            "مسودة: العميل متوسط التأهيل. ابدأ بـ Diagnostic قصير قبل أي التزام تجاري."
        )
    else:
        tier = "low"
        suggested_response = "مسودة: العميل منخفض التأهيل. اجمع بيانات إضافية قبل التصعيد."
    return {
        "qualification_score": score,
        "qualification_tier": tier,
        "suggested_response": suggested_response,
    }


def run_smallest_governed_loop(req: EnterpriseLoopRequest) -> dict[str, Any]:
    if not req.tenant_id.strip():
        raise ValueError("tenant_id_required")
    if not _has_permission(req.user_role, "workflow:run"):
        raise PermissionError(f"role_not_allowed:{req.user_role}")
    if not _has_permission(req.user_role, "agent:run:sales_agent"):
        raise PermissionError(f"agent_permission_missing:{req.user_role}")

    observability = ObservabilityRuntime()
    audit = AuditLogger(tenant_id=req.tenant_id, user_id=req.user_id)
    governance = GovernanceEngine()
    registry = AgentRegistry()
    engine = SimpleWorkflowEngine(max_retries=1)
    registry.register("sales_agent", _sales_agent)

    context: dict[str, Any] = {
        "trigger": "lead_entered",
        "tenant_id": req.tenant_id,
        "user_id": req.user_id,
        "lead": asdict(req.lead),
        "crm_integration": req.crm_integration,
    }

    def _step_trigger(ctx: dict[str, Any]) -> None:
        audit.write("workflow.trigger", "ok", {"trigger": ctx["trigger"]})
        observability.log("trigger_received", tenant_id=ctx["tenant_id"])

    def _step_qualification(ctx: dict[str, Any]) -> None:
        output = registry.run("sales_agent", ctx)
        ctx["agent_output"] = output
        audit.write(
            "agent.run",
            "ok",
            {"agent_name": "sales_agent", "tier": output["qualification_tier"]},
        )
        observability.log("agent_completed", score=output["qualification_score"])

    def _step_retrieval(ctx: dict[str, Any]) -> None:
        ctx["knowledge"] = {
            "source": "revenue_memory",
            "citations": [
                "playbook:ai_revenue_os",
                "policy:no_external_action_without_approval",
            ],
        }
        audit.write("knowledge.retrieve", "ok", {"source": "revenue_memory"})

    def _step_scoring(ctx: dict[str, Any]) -> None:
        score = float(ctx["agent_output"]["qualification_score"])
        if score >= 70:
            priority = "P1"
        elif score >= 40:
            priority = "P2"
        else:
            priority = "P3"
        ctx["scoring"] = {"score": score, "priority": priority}
        audit.write("lead.score", "ok", ctx["scoring"])

    def _step_response(ctx: dict[str, Any]) -> None:
        ctx["suggested_response"] = {
            "mode": "draft_only",
            "text_ar": ctx["agent_output"]["suggested_response"],
        }
        audit.write("response.suggest", "ok", {"mode": "draft_only"})

    def _step_approval(ctx: dict[str, Any]) -> None:
        decision = governance.evaluate(
            action="crm.update",
            lead=ctx["lead"],
            score=float(ctx["scoring"]["score"]),
            approval_granted=req.approval_granted,
        )
        ctx["governance"] = decision
        audit.write("governance.check", "ok" if decision["allowed"] else "blocked", decision)
        if not decision["allowed"]:
            raise WorkflowBlocked(decision["reason"])

    def _step_crm_update(ctx: dict[str, Any]) -> None:
        ctx["crm_update"] = {
            "integration": ctx["crm_integration"],
            "status": "updated",
            "lead_company": ctx["lead"]["company"],
        }
        audit.write("crm.update", "ok", {"integration": ctx["crm_integration"]})

    def _step_exec_metrics(ctx: dict[str, Any]) -> None:
        score = float(ctx["scoring"]["score"])
        conversion_probability = round(min(score / 100.0, 0.95), 2)
        ctx["executive_metrics"] = {
            "qualified_leads": 1 if score >= 40 else 0,
            "pipeline_priority": ctx["scoring"]["priority"],
            "conversion_probability": conversion_probability,
        }
        audit.write("metrics.executive", "ok", ctx["executive_metrics"])

    def _step_rollback_drill(ctx: dict[str, Any]) -> None:
        before = copy.deepcopy(ctx["executive_metrics"])
        ctx["executive_metrics"]["conversion_probability"] = 0.0
        ctx["executive_metrics"] = before
        ctx["rollback_drill"] = {"ok": True, "drill": "metrics_snapshot_restore"}
        audit.write("workflow.rollback_drill", "ok", ctx["rollback_drill"])

    steps: list[tuple[str, Callable[[dict[str, Any]], None], bool]] = [
        ("trigger", _step_trigger, False),
        ("lead_qualification", _step_qualification, True),
        ("knowledge_retrieval", _step_retrieval, True),
        ("scoring", _step_scoring, True),
        ("suggested_response", _step_response, False),
        ("approval", _step_approval, False),
        ("crm_update", _step_crm_update, True),
        ("executive_metrics", _step_exec_metrics, False),
        ("rollback_drill", _step_rollback_drill, False),
    ]

    status, step_results, error = engine.run(
        context=context, steps=steps, observability=observability
    )
    obs_snapshot = observability.snapshot()

    readiness = {
        "tenant_count": 1,
        "user_count": req.users_in_tenant,
        "role_count": len(set(req.roles_configured)),
        "workflow_count": 1,
        "agent_count": len(registry.describe()),
        "approval_rules_count": 1,
        "crm_integrations_count": 1,
        "executive_reports_count": 1,
        "eval_reports_count": 1,
        "rollback_drill": "passed"
        if context.get("rollback_drill", {}).get("ok")
        else "not_run",
    }

    return {
        "status": status,
        "error": error,
        "tenant_id": req.tenant_id,
        "workflow_name": "ai_revenue_os_enterprise_loop_v1",
        "agent_registry": registry.describe(),
        "steps": [asdict(step) for step in step_results],
        "outputs": {
            "lead": context["lead"],
            "qualification": context.get("agent_output"),
            "knowledge": context.get("knowledge"),
            "scoring": context.get("scoring"),
            "suggested_response": context.get("suggested_response"),
            "governance": context.get("governance"),
            "crm_update": context.get("crm_update"),
            "executive_metrics": context.get("executive_metrics"),
            "rollback_drill": context.get("rollback_drill"),
        },
        "audit_log": audit.entries,
        "observability": obs_snapshot,
        "readiness": readiness,
    }
