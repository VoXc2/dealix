"""
Workflow Engine — the deterministic runtime.

This is the layer the blueprint insists on building *before* agents. It walks
a `WorkflowDefinition` step by step and, for every step, enforces the full
governance loop:

    classify → policy evaluate → (approval if escalated) → execute (retry) →
    audit → on failure: compensate (saga rollback)

It is deliberately not a Temporal clone. It is in-process, deterministic, and
small enough to read in one sitting. Durability (Postgres-backed runs) is a
Phase-2 swap behind the same interface.

Agents execute *inside* steps. They never replace the engine.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from dealix.classifications import classify
from dealix.contracts.audit_log import AuditAction, AuditEntry
from dealix.contracts.decision import (
    DecisionOutput,
    Evidence,
    NextAction,
    PolicyRequirement,
)
from dealix.execution.evals import WorkflowEvalResult, evaluate_run
from dealix.execution.memory import OperationalMemory, get_memory
from dealix.execution.roi import ROILedger, get_roi_ledger
from dealix.execution.tool_registry import Tool, ToolRegistry
from dealix.execution.workflow import (
    RunStatus,
    StepRecord,
    StepStatus,
    WorkflowContext,
    WorkflowDefinition,
    WorkflowStep,
)
from dealix.observability.otel import tool_span
from dealix.reliability.dlq import DLQ
from dealix.reliability.retry import retry_with_backoff
from dealix.trust.approval import ApprovalCenter, ApprovalStatus
from dealix.trust.audit import AuditSink, InMemoryAuditSink
from dealix.trust.policy import PolicyDecision, PolicyEvaluator

log = logging.getLogger(__name__)


class StepFailed(Exception):
    """Raised internally when a tool step fails after retries."""


class WorkflowEngine:
    """Deterministic, governed workflow runtime."""

    def __init__(
        self,
        registry: ToolRegistry,
        *,
        policy: PolicyEvaluator | None = None,
        approvals: ApprovalCenter | None = None,
        audit: AuditSink | None = None,
        memory: OperationalMemory | None = None,
        roi: ROILedger | None = None,
        dlq: DLQ | None = None,
    ) -> None:
        self.registry = registry
        self.policy = policy or PolicyEvaluator()
        self.approvals = approvals or ApprovalCenter()
        self.audit = audit or InMemoryAuditSink()
        self.memory = memory or get_memory()
        self.roi = roi or get_roi_ledger()
        self.dlq = dlq

    # ── Public API ──────────────────────────────────────────────

    async def start(
        self,
        workflow: WorkflowDefinition,
        *,
        tenant_id: str,
        entity_id: str,
        trigger_payload: dict[str, Any],
        actor_id: str = "system",
        correlation_id: str | None = None,
    ) -> WorkflowContext:
        """Begin a new run and drive it as far as policy allows."""
        ctx = WorkflowContext.new(
            workflow,
            tenant_id=tenant_id,
            entity_id=entity_id,
            trigger_payload=trigger_payload,
            actor_id=actor_id,
            correlation_id=correlation_id,
        )
        self._audit(ctx, AuditAction.WORKFLOW_STARTED, outcome="ok")
        self.memory.record(ctx)
        await self._drive(workflow, ctx)
        return ctx

    async def resume(
        self, workflow: WorkflowDefinition, ctx: WorkflowContext
    ) -> WorkflowContext:
        """Resume a run that was paused awaiting approval."""
        if ctx.status != RunStatus.AWAITING_APPROVAL:
            return ctx
        # Reflect any approval TTL expiries before re-checking status.
        self.approvals.check_timeouts()
        await self._drive(workflow, ctx)
        return ctx

    def evaluate(self, ctx: WorkflowContext) -> WorkflowEvalResult:
        """Run operational evals over a finished (or paused) run."""
        return evaluate_run(ctx.to_dict())

    # ── Core driver ─────────────────────────────────────────────

    async def _drive(self, workflow: WorkflowDefinition, ctx: WorkflowContext) -> None:
        ctx.status = RunStatus.RUNNING
        ctx.pending_approval_id = None

        while ctx.current_step_index < len(workflow.steps):
            i = ctx.current_step_index
            step = workflow.steps[i]
            tool = self.registry.get(step.tool_name)
            record = self._record_for(ctx, i, step, tool)

            outcome = await self._run_step(workflow, ctx, step, tool, record)
            if outcome == "pause":
                self.memory.record(ctx)
                return
            if outcome == "fail":
                await self._fail_and_compensate(workflow, ctx)
                return
            # "advance"
            ctx.current_step_index = i + 1

        self._finish(ctx, RunStatus.COMPLETED)

    async def _run_step(
        self,
        workflow: WorkflowDefinition,
        ctx: WorkflowContext,
        step: WorkflowStep,
        tool: Tool,
        record: StepRecord,
    ) -> str:
        """Process one step. Returns 'advance' | 'pause' | 'fail'."""
        # ── Resuming an escalated step: check the approval verdict ──
        if record.approval_request_id:
            verdict = self._check_approval(ctx, record)
            if verdict == "pending":
                ctx.status = RunStatus.AWAITING_APPROVAL
                ctx.pending_approval_id = record.approval_request_id
                return "pause"
            if verdict == "rejected":
                record.status = StepStatus.DENIED
                record.error = "approval rejected or timed out"
                ctx.error = f"step '{step.name}' blocked: {record.error}"
                return "fail"
            # verdict == "granted" → fall through to execution.

        else:
            # ── Fresh step: classify + policy evaluate ──
            resolved = self._resolve_input(ctx, step)
            record.resolved_input = resolved
            decision, action = self._build_decision(ctx, step, tool, resolved)
            result = self.policy.evaluate(action, decision)
            record.policy_decision = result.decision.value
            record.policy_rule = result.rule_name
            self._audit(
                ctx,
                AuditAction.POLICY_EVALUATED,
                tool=tool,
                outcome=result.decision.value,
                reason=result.reason,
                decision_id=decision.decision_id,
            )

            if result.decision == PolicyDecision.DENY:
                record.status = StepStatus.DENIED
                record.error = f"policy denied: {result.reason}"
                ctx.error = f"step '{step.name}' denied by policy: {result.reason}"
                self._audit(ctx, AuditAction.POLICY_DENIED, tool=tool, reason=result.reason)
                return "fail"

            if result.decision == PolicyDecision.ESCALATE:
                req = self.approvals.submit(
                    decision,
                    action,
                    required_approvers=max(1, result.required_approvers),
                )
                record.approval_request_id = req.request_id
                record.status = StepStatus.AWAITING_APPROVAL
                ctx.status = RunStatus.AWAITING_APPROVAL
                ctx.pending_approval_id = req.request_id
                self._audit(
                    ctx,
                    AuditAction.APPROVAL_REQUESTED,
                    tool=tool,
                    reason=result.reason,
                    details={"approval_request_id": req.request_id,
                             "required_approvers": req.required_approvers},
                )
                return "pause"
            # PolicyDecision.ALLOW → fall through to execution.

        # ── Execute the tool (with retry, timeout, span) ──
        return await self._execute_step(ctx, step, tool, record)

    async def _execute_step(
        self,
        ctx: WorkflowContext,
        step: WorkflowStep,
        tool: Tool,
        record: StepRecord,
    ) -> str:
        from datetime import UTC, datetime

        record.status = StepStatus.RUNNING
        record.started_at = datetime.now(UTC)
        resolved = record.resolved_input
        attempts = 0

        async def _invoke() -> dict[str, Any]:
            nonlocal attempts
            attempts += 1
            return await asyncio.wait_for(
                tool.handler(resolved), timeout=tool.timeout_seconds
            )

        self._audit(ctx, AuditAction.TOOL_INVOKED, tool=tool, outcome="ok")
        try:
            with tool_span(tool.name, workflow=ctx.workflow_name, run_id=ctx.run_id):
                output = await retry_with_backoff(
                    _invoke,
                    max_attempts=tool.max_attempts,
                    base_delay=0.1,
                    dlq=self.dlq,
                    dlq_source=f"workflow:{ctx.workflow_name}:{step.name}",
                    dlq_payload={"run_id": ctx.run_id, "step": step.name},
                )
        except Exception as exc:  # tool failed after all retries
            record.attempts = attempts
            record.status = StepStatus.FAILED
            record.error = f"{type(exc).__name__}: {exc}"
            record.finished_at = datetime.now(UTC)
            record.duration_ms = self._elapsed_ms(record)
            ctx.error = f"step '{step.name}' failed: {record.error}"
            self._audit(ctx, AuditAction.WORKFLOW_FAILED, tool=tool, reason=record.error)
            return "fail"

        record.attempts = attempts
        record.output = output if isinstance(output, dict) else {"result": output}
        record.status = StepStatus.COMPLETED
        record.finished_at = datetime.now(UTC)
        record.duration_ms = self._elapsed_ms(record)
        ctx.step_outputs[step.name] = record.output
        if record.policy_decision == PolicyDecision.ESCALATE.value:
            self._audit(ctx, AuditAction.APPROVAL_GRANTED, tool=tool, outcome="ok")
        return "advance"

    # ── Failure / rollback ──────────────────────────────────────

    async def _fail_and_compensate(
        self, workflow: WorkflowDefinition, ctx: WorkflowContext
    ) -> None:
        """Saga rollback: compensate completed steps in reverse order."""
        compensated_any = False
        for record in reversed(ctx.step_records):
            if record.status != StepStatus.COMPLETED:
                continue
            tool = self.registry.get(record.tool_name)
            if tool.compensation is None:
                continue
            try:
                await tool.compensation(record.resolved_input, record.output)
                record.compensated = True
                record.status = StepStatus.COMPENSATED
                compensated_any = True
                self._audit(
                    ctx,
                    AuditAction.WORKFLOW_COMPENSATED,
                    tool=tool,
                    outcome="ok",
                    reason=f"rolled back after failure of run {ctx.run_id}",
                )
            except Exception as exc:  # compensation must not raise — log + continue
                log.error(
                    "compensation_failed run=%s step=%s err=%s",
                    ctx.run_id,
                    record.name,
                    exc,
                )
                self._audit(
                    ctx,
                    AuditAction.WORKFLOW_COMPENSATED,
                    tool=tool,
                    outcome="failed",
                    reason=str(exc)[:200],
                )
        final = RunStatus.COMPENSATED if compensated_any else RunStatus.FAILED
        self._finish(ctx, final)

    # ── Helpers ─────────────────────────────────────────────────

    def _finish(self, ctx: WorkflowContext, status: RunStatus) -> None:
        from datetime import UTC, datetime

        ctx.status = status
        ctx.finished_at = datetime.now(UTC)
        ctx.pending_approval_id = None
        action = (
            AuditAction.WORKFLOW_COMPLETED
            if status == RunStatus.COMPLETED
            else AuditAction.WORKFLOW_FAILED
        )
        self._audit(ctx, action, outcome=status.value, reason=ctx.error)
        self.memory.record(ctx)
        self.roi.book(
            run_id=ctx.run_id,
            workflow_name=ctx.workflow_name,
            tenant_id=ctx.tenant_id,
            status=status.value,
            automated_ms=ctx.duration_ms,
        )

    def _record_for(
        self, ctx: WorkflowContext, index: int, step: WorkflowStep, tool: Tool
    ) -> StepRecord:
        if index < len(ctx.step_records):
            return ctx.step_records[index]
        record = StepRecord(name=step.name, tool_name=tool.name)
        ctx.step_records.append(record)
        return record

    def _resolve_input(self, ctx: WorkflowContext, step: WorkflowStep) -> dict[str, Any]:
        try:
            resolved = step.inputs(ctx)
        except Exception as exc:  # a bad mapper is a definition error
            raise StepFailed(f"input mapper for '{step.name}' raised: {exc}") from exc
        return dict(resolved) if isinstance(resolved, dict) else {}

    def _build_decision(
        self,
        ctx: WorkflowContext,
        step: WorkflowStep,
        tool: Tool,
        resolved: dict[str, Any],
    ) -> tuple[DecisionOutput, NextAction]:
        """Wrap a step into the canonical DecisionOutput the policy engine expects."""
        # Evidence = the upstream context that justifies this step.
        upstream = {k: ctx.step_outputs.get(k, {}) for k in list(ctx.step_outputs)[-3:]}
        excerpt = str({"trigger": ctx.trigger_payload, "upstream": upstream})[:1900]
        evidence = [
            Evidence(
                source=f"workflow:{ctx.workflow_name}",
                uri=f"run:{ctx.run_id}",
                excerpt=excerpt,
            )
        ]
        confidence = float(
            ctx.step_outputs.get("evaluate_lead", {}).get("normalized_score", 1.0)
        )
        policy_reqs: list[PolicyRequirement] = []
        if tool.sensitivity_class.is_pdpl_scope:
            policy_reqs.append(
                PolicyRequirement(
                    policy_name="pdpl_lawful_basis",
                    description="Personal-data action — lawful basis must be on file",
                )
            )
        action = NextAction(
            action_type=tool.action_type,
            description=tool.description,
            approval_class=tool.approval_class,
            reversibility_class=tool.reversibility_class,
            sensitivity_class=tool.sensitivity_class,
            payload={"step": step.name},
            policy_requirements=policy_reqs,
        )
        decision = DecisionOutput(
            tenant_id=ctx.tenant_id,
            entity_id=ctx.entity_id,
            objective=f"{ctx.workflow_name}:{step.name}",
            agent_name="workflow_engine",
            recommendation={"execute_tool": tool.name},
            confidence=max(0.0, min(1.0, confidence)),
            rationale=f"Step '{step.name}' of workflow '{ctx.workflow_name}' executes tool '{tool.name}'.",
            evidence=evidence,
            approval_class=tool.approval_class,
            reversibility_class=tool.reversibility_class,
            sensitivity_class=tool.sensitivity_class,
            next_actions=[action],
            trace_id=ctx.trace_id,
            correlation_id=ctx.correlation_id,
        )
        return decision, action

    def _check_approval(self, ctx: WorkflowContext, record: StepRecord) -> str:
        """Returns 'granted' | 'rejected' | 'pending'."""
        req = self.approvals.get(record.approval_request_id or "")
        if req is None:
            return "rejected"
        if req.status == ApprovalStatus.GRANTED:
            return "granted"
        if req.status in (ApprovalStatus.REJECTED, ApprovalStatus.TIMED_OUT,
                          ApprovalStatus.WITHDRAWN):
            self._audit(
                ctx,
                AuditAction.APPROVAL_REJECTED,
                outcome=req.status.value,
                reason=req.reject_reason or req.status.value,
            )
            return "rejected"
        return "pending"

    @staticmethod
    def _elapsed_ms(record: StepRecord) -> float:
        if record.started_at and record.finished_at:
            return (record.finished_at - record.started_at).total_seconds() * 1000.0
        return 0.0

    def _audit(
        self,
        ctx: WorkflowContext,
        action: AuditAction,
        *,
        tool: Tool | None = None,
        outcome: str = "ok",
        reason: str | None = None,
        decision_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        from dealix.classifications import (
            ApprovalClass,
            ReversibilityClass,
            SensitivityClass,
        )

        self.audit.append(
            AuditEntry(
                tenant_id=ctx.tenant_id,
                action=action,
                actor_type="workflow",
                actor_id=ctx.actor_id,
                decision_id=decision_id,
                entity_id=ctx.entity_id,
                workflow_id=ctx.run_id,
                approval_class=tool.approval_class if tool else ApprovalClass.A0,
                reversibility_class=tool.reversibility_class if tool else ReversibilityClass.R0,
                sensitivity_class=tool.sensitivity_class if tool else SensitivityClass.S1,
                outcome=outcome,
                reason=reason,
                details=details or {},
                trace_id=ctx.trace_id,
                correlation_id=ctx.correlation_id,
            )
        )


__all__ = ["StepFailed", "WorkflowEngine"]
