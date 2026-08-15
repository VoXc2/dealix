"""PostgreSQL persistence for governed workflow runs and agent tasks.

The adapter is deliberately synchronous because ``Orchestrator`` is a
synchronous execution surface. Every query is tenant-bound, idempotency is
enforced by a database unique constraint, and task/run leases are acquired by
conditional updates so multiple API/worker nodes cannot execute the same unit
of work concurrently.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import asdict
from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Engine,
    Integer,
    String,
    Text,
    UniqueConstraint,
    and_,
    create_engine,
    func,
    or_,
    select,
    update,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from auto_client_acquisition.orchestrator.queue import (
    ALL_STATUSES,
    AgentTask,
    TaskStatus,
    task_id_for,
)
from auto_client_acquisition.orchestrator.runtime import (
    WorkflowRunState,
    WorkflowRunStatus,
)
from auto_client_acquisition.persistence.db_sync_url import sync_sqlalchemy_url


class _Base(DeclarativeBase):
    pass


class WorkflowRunORM(_Base):
    """Mapping for the existing enterprise ``workflow_runs`` table."""

    __tablename__ = "workflow_runs"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "customer_id",
            "workflow_id",
            "idempotency_key",
            name="uq_workflow_runs_tenant_idempotency",
        ),
    )

    run_id: Mapped[str] = mapped_column(Text, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    workflow_id: Mapped[str] = mapped_column(Text, nullable=False)
    customer_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    state: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    correlation_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_run_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    current_step: Mapped[str | None] = mapped_column(Text, nullable=True)
    attached_policy_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False, default=list)
    metadata_json: Mapped[dict[str, Any]] = mapped_column(
        "metadata", JSON, nullable=False, default=dict
    )
    idempotency_key: Mapped[str] = mapped_column(Text, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    lease_owner: Mapped[str | None] = mapped_column(Text, nullable=True)
    lease_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    registered_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class OrchestratorTaskORM(_Base):
    __tablename__ = "orchestrator_tasks"
    __table_args__ = (
        UniqueConstraint(
            "tenant_id",
            "correlation_id",
            "step_id",
            name="uq_orchestrator_tasks_tenant_run_step",
        ),
    )

    task_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    tenant_id: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    customer_id: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    agent_id: Mapped[str] = mapped_column(Text, nullable=False)
    action_type: Mapped[str] = mapped_column(Text, nullable=False)
    step_id: Mapped[str] = mapped_column(Text, nullable=False)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(Text, nullable=False, index=True)
    requires_approval: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    approval_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    correlation_id: Mapped[str | None] = mapped_column(Text, nullable=True, index=True)
    causation_task_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    parent_workflow_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    approved_by: Mapped[str | None] = mapped_column(Text, nullable=True)
    executed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    result: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    retries: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    max_retries: Mapped[int] = mapped_column(Integer, nullable=False, default=2)
    version: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    claim_owner: Mapped[str | None] = mapped_column(Text, nullable=True)
    claim_expires_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


def _now() -> datetime:
    return datetime.now(UTC)


def _state_metadata(state: WorkflowRunState) -> dict[str, Any]:
    payload = asdict(state)
    for key in ("run_id", "tenant_id", "workflow_id", "customer_id", "idempotency_key"):
        payload.pop(key, None)
    payload.pop("version", None)
    return payload


def _state_from_row(row: WorkflowRunORM) -> WorkflowRunState:
    metadata = dict(row.metadata_json or {})
    return WorkflowRunState(
        run_id=row.run_id,
        tenant_id=row.tenant_id,
        workflow_id=row.workflow_id,
        customer_id=str(row.customer_id or ""),
        idempotency_key=row.idempotency_key,
        initial_inputs=dict(metadata.get("initial_inputs") or {}),
        outputs=dict(metadata.get("outputs") or {}),
        task_ids=list(metadata.get("task_ids") or []),
        completed_steps=list(metadata.get("completed_steps") or []),
        next_step_index=int(metadata.get("next_step_index") or 0),
        status=row.state,
        awaiting_task_id=metadata.get("awaiting_task_id"),
        failure_reason=metadata.get("failure_reason"),
        finalized=bool(metadata.get("finalized", False)),
        version=row.version,
    )


def _task_from_row(row: OrchestratorTaskORM) -> AgentTask:
    return AgentTask(
        task_id=row.task_id,
        tenant_id=row.tenant_id,
        customer_id=row.customer_id,
        agent_id=row.agent_id,
        action_type=row.action_type,
        payload=dict(row.payload or {}),
        status=row.status,
        requires_approval=row.requires_approval,
        approval_reason=row.approval_reason,
        correlation_id=row.correlation_id,
        causation_task_id=row.causation_task_id,
        parent_workflow_id=row.parent_workflow_id,
        created_at=row.created_at,
        approved_at=row.approved_at,
        approved_by=row.approved_by,
        executed_at=row.executed_at,
        completed_at=row.completed_at,
        error=row.error,
        result=dict(row.result) if isinstance(row.result, dict) else None,
        retries=row.retries,
        max_retries=row.max_retries,
    )


class ConcurrentWorkflowUpdate(RuntimeError):
    """Raised when a stale workflow snapshot attempts to overwrite a newer one."""


class PostgresWorkflowRunStore:
    backend_name = "postgres"

    def __init__(self, engine: Engine, *, tenant_id: str) -> None:
        if not tenant_id.strip():
            raise ValueError("tenant_id is required for PostgreSQL workflow state")
        self._tenant_id = tenant_id.strip()
        self._sessionmaker = sessionmaker(engine, expire_on_commit=False, future=True)

    def reserve(self, state: WorkflowRunState) -> tuple[WorkflowRunState, bool]:
        self._assert_tenant(state.tenant_id)
        now = _now()
        row = WorkflowRunORM(
            run_id=state.run_id,
            tenant_id=state.tenant_id,
            workflow_id=state.workflow_id,
            customer_id=state.customer_id,
            state=state.status,
            correlation_id=state.run_id,
            parent_run_id=None,
            current_step=None,
            attached_policy_ids=[],
            metadata_json=_state_metadata(state),
            idempotency_key=state.idempotency_key,
            version=state.version,
            registered_at=now,
            updated_at=now,
        )
        with self._sessionmaker() as session:
            session.add(row)
            try:
                session.commit()
                return state, True
            except IntegrityError:
                session.rollback()
        existing = self.find_idempotent(
            tenant_id=state.tenant_id,
            customer_id=state.customer_id,
            workflow_id=state.workflow_id,
            idempotency_key=state.idempotency_key,
        )
        if existing is None:
            raise ConcurrentWorkflowUpdate("idempotency reservation conflicted without a row")
        return existing, False

    def save(self, state: WorkflowRunState) -> WorkflowRunState:
        self._assert_tenant(state.tenant_id)
        stmt = (
            update(WorkflowRunORM)
            .where(
                WorkflowRunORM.run_id == state.run_id,
                WorkflowRunORM.tenant_id == self._tenant_id,
                WorkflowRunORM.version == state.version,
            )
            .values(
                state=state.status,
                current_step=state.awaiting_task_id,
                metadata_json=_state_metadata(state),
                version=state.version + 1,
                updated_at=_now(),
            )
        )
        with self._sessionmaker() as session:
            result = session.execute(stmt)
            if result.rowcount != 1:
                session.rollback()
                raise ConcurrentWorkflowUpdate(f"stale workflow state: {state.run_id}")
            session.commit()
        state.version += 1
        return state

    def get(
        self,
        run_id: str,
        *,
        tenant_id: str | None = None,
    ) -> WorkflowRunState | None:
        self._assert_tenant(tenant_id or self._tenant_id)
        with self._sessionmaker() as session:
            row = session.scalar(
                select(WorkflowRunORM).where(
                    WorkflowRunORM.run_id == run_id,
                    WorkflowRunORM.tenant_id == self._tenant_id,
                )
            )
            return _state_from_row(row) if row is not None else None

    def find_idempotent(
        self,
        *,
        tenant_id: str = "default",
        customer_id: str,
        workflow_id: str,
        idempotency_key: str,
    ) -> WorkflowRunState | None:
        self._assert_tenant(tenant_id)
        with self._sessionmaker() as session:
            row = session.scalar(
                select(WorkflowRunORM).where(
                    WorkflowRunORM.tenant_id == self._tenant_id,
                    WorkflowRunORM.customer_id == customer_id,
                    WorkflowRunORM.workflow_id == workflow_id,
                    WorkflowRunORM.idempotency_key == idempotency_key,
                )
            )
            return _state_from_row(row) if row is not None else None

    def claim(
        self,
        run_id: str,
        *,
        tenant_id: str,
        worker_id: str,
        lease_seconds: int = 60,
    ) -> WorkflowRunState | None:
        self._assert_tenant(tenant_id)
        now = _now()
        terminal = (
            WorkflowRunStatus.COMPLETED,
            WorkflowRunStatus.FAILED,
            WorkflowRunStatus.REJECTED,
        )
        stmt = (
            update(WorkflowRunORM)
            .where(
                WorkflowRunORM.run_id == run_id,
                WorkflowRunORM.tenant_id == self._tenant_id,
                WorkflowRunORM.state.not_in(terminal),
                or_(
                    WorkflowRunORM.lease_owner.is_(None),
                    WorkflowRunORM.lease_owner == worker_id,
                    WorkflowRunORM.lease_expires_at < now,
                ),
            )
            .values(
                lease_owner=worker_id,
                lease_expires_at=now + timedelta(seconds=max(1, lease_seconds)),
                updated_at=now,
            )
        )
        with self._sessionmaker() as session:
            result = session.execute(stmt)
            session.commit()
        return self.get(run_id, tenant_id=tenant_id) if result.rowcount == 1 else None

    def release(self, run_id: str, *, tenant_id: str, worker_id: str) -> None:
        self._assert_tenant(tenant_id)
        with self._sessionmaker() as session:
            session.execute(
                update(WorkflowRunORM)
                .where(
                    WorkflowRunORM.run_id == run_id,
                    WorkflowRunORM.tenant_id == self._tenant_id,
                    WorkflowRunORM.lease_owner == worker_id,
                )
                .values(lease_owner=None, lease_expires_at=None, updated_at=_now())
            )
            session.commit()

    def _assert_tenant(self, tenant_id: str) -> None:
        if tenant_id != self._tenant_id:
            raise ValueError("cross-tenant workflow state access denied")


class PostgresTaskQueue:
    backend_name = "postgres"

    def __init__(self, engine: Engine, *, tenant_id: str) -> None:
        if not tenant_id.strip():
            raise ValueError("tenant_id is required for PostgreSQL task state")
        self._tenant_id = tenant_id.strip()
        self._sessionmaker = sessionmaker(engine, expire_on_commit=False, future=True)

    def enqueue(
        self,
        *,
        tenant_id: str = "default",
        customer_id: str,
        agent_id: str,
        action_type: str,
        payload: dict[str, Any] | None = None,
        requires_approval: bool = False,
        approval_reason: str | None = None,
        correlation_id: str | None = None,
        causation_task_id: str | None = None,
        parent_workflow_id: str | None = None,
    ) -> AgentTask:
        self._assert_tenant(tenant_id)
        data = dict(payload or {})
        raw_step_id = str(data.get("step_id") or "") or None
        task_id = task_id_for(
            tenant_id=self._tenant_id,
            correlation_id=correlation_id,
            step_id=raw_step_id,
        )
        step_id = raw_step_id or task_id
        row = OrchestratorTaskORM(
            task_id=task_id,
            tenant_id=self._tenant_id,
            customer_id=customer_id,
            agent_id=agent_id,
            action_type=action_type,
            step_id=step_id,
            payload=data,
            status=(TaskStatus.AWAITING_APPROVAL if requires_approval else TaskStatus.PENDING),
            requires_approval=requires_approval,
            approval_reason=approval_reason,
            correlation_id=correlation_id,
            causation_task_id=causation_task_id,
            parent_workflow_id=parent_workflow_id,
            created_at=_now(),
            retries=0,
            max_retries=2,
            version=0,
        )
        with self._sessionmaker() as session:
            session.add(row)
            try:
                session.commit()
                return _task_from_row(row)
            except IntegrityError:
                session.rollback()
                existing = session.scalar(
                    select(OrchestratorTaskORM).where(
                        OrchestratorTaskORM.tenant_id == self._tenant_id,
                        OrchestratorTaskORM.correlation_id == correlation_id,
                        OrchestratorTaskORM.step_id == step_id,
                    )
                )
                if existing is None:
                    raise
                return _task_from_row(existing)

    def approve(
        self,
        task_id: str,
        *,
        approved_by: str,
        tenant_id: str | None = None,
    ) -> AgentTask:
        self._assert_tenant(tenant_id or self._tenant_id)
        now = _now()
        with self._sessionmaker() as session:
            result = session.execute(
                update(OrchestratorTaskORM)
                .where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                    OrchestratorTaskORM.status == TaskStatus.AWAITING_APPROVAL,
                )
                .values(
                    status=TaskStatus.APPROVED,
                    approved_at=now,
                    approved_by=approved_by,
                    version=OrchestratorTaskORM.version + 1,
                )
            )
            session.commit()
        task = self._require(task_id)
        if result.rowcount != 1 and not (
            task.status == TaskStatus.APPROVED and task.approved_by == approved_by
        ):
            raise ValueError(f"task {task_id} is not awaiting approval (status={task.status})")
        return task

    def reject(
        self,
        task_id: str,
        *,
        rejected_by: str,
        reason: str = "",
        tenant_id: str | None = None,
    ) -> AgentTask:
        self._assert_tenant(tenant_id or self._tenant_id)
        with self._sessionmaker() as session:
            result = session.execute(
                update(OrchestratorTaskORM)
                .where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                    OrchestratorTaskORM.status == TaskStatus.AWAITING_APPROVAL,
                )
                .values(
                    status=TaskStatus.REJECTED,
                    approved_by=rejected_by,
                    completed_at=_now(),
                    error=f"rejected: {reason}" if reason else "rejected",
                    version=OrchestratorTaskORM.version + 1,
                )
            )
            session.commit()
        task = self._require(task_id)
        if result.rowcount != 1:
            raise ValueError(f"task {task_id} is not awaiting approval (status={task.status})")
        return task

    def cancel(self, task_id: str, *, tenant_id: str | None = None) -> AgentTask:
        self._assert_tenant(tenant_id or self._tenant_id)
        terminal = (TaskStatus.SUCCEEDED, TaskStatus.FAILED, TaskStatus.CANCELLED)
        with self._sessionmaker() as session:
            result = session.execute(
                update(OrchestratorTaskORM)
                .where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                    OrchestratorTaskORM.status.not_in(terminal),
                )
                .values(
                    status=TaskStatus.CANCELLED,
                    completed_at=_now(),
                    claim_owner=None,
                    claim_expires_at=None,
                    version=OrchestratorTaskORM.version + 1,
                )
            )
            session.commit()
        task = self._require(task_id)
        if result.rowcount != 1:
            raise ValueError(f"task {task_id} is already terminal (status={task.status})")
        return task

    def mark_executing(
        self,
        task_id: str,
        *,
        tenant_id: str | None = None,
        worker_id: str | None = None,
    ) -> AgentTask:
        self._assert_tenant(tenant_id or self._tenant_id)
        owner = worker_id or "sync-worker"
        now = _now()
        with self._sessionmaker() as session:
            result = session.execute(
                update(OrchestratorTaskORM)
                .where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                    or_(
                        OrchestratorTaskORM.status.in_(
                            (TaskStatus.PENDING, TaskStatus.APPROVED)
                        ),
                        and_(
                            OrchestratorTaskORM.status == TaskStatus.EXECUTING,
                            OrchestratorTaskORM.claim_expires_at < now,
                        ),
                    ),
                )
                .values(
                    status=TaskStatus.EXECUTING,
                    executed_at=now,
                    claim_owner=owner,
                    claim_expires_at=now + timedelta(seconds=120),
                    version=OrchestratorTaskORM.version + 1,
                )
            )
            session.commit()
        task = self._require(task_id)
        if result.rowcount != 1:
            raise ValueError(f"cannot execute task in status={task.status}")
        return task

    def succeed(
        self,
        task_id: str,
        *,
        result: dict[str, Any],
        tenant_id: str | None = None,
        worker_id: str | None = None,
    ) -> AgentTask:
        self._assert_tenant(tenant_id or self._tenant_id)
        owner = worker_id or "sync-worker"
        with self._sessionmaker() as session:
            changed = session.execute(
                update(OrchestratorTaskORM)
                .where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                    OrchestratorTaskORM.status == TaskStatus.EXECUTING,
                    OrchestratorTaskORM.claim_owner == owner,
                )
                .values(
                    status=TaskStatus.SUCCEEDED,
                    result=result,
                    completed_at=_now(),
                    claim_owner=None,
                    claim_expires_at=None,
                    version=OrchestratorTaskORM.version + 1,
                )
            )
            session.commit()
        task = self._require(task_id)
        if changed.rowcount != 1 and task.status != TaskStatus.SUCCEEDED:
            raise ValueError(f"worker does not own executing task {task_id}")
        return task

    def fail(
        self,
        task_id: str,
        *,
        error: str,
        retryable: bool = True,
        tenant_id: str | None = None,
        worker_id: str | None = None,
    ) -> AgentTask:
        self._assert_tenant(tenant_id or self._tenant_id)
        owner = worker_id or "sync-worker"
        with self._sessionmaker() as session:
            row = session.scalar(
                select(OrchestratorTaskORM)
                .where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                )
                .with_for_update()
            )
            if row is None:
                raise KeyError(f"unknown task: {task_id}")
            if row.status == TaskStatus.EXECUTING and row.claim_owner not in (None, owner):
                raise ValueError(f"worker does not own executing task {task_id}")
            if retryable and row.retries < row.max_retries:
                row.retries += 1
                row.status = TaskStatus.PENDING
                row.completed_at = None
            else:
                row.status = TaskStatus.FAILED
                row.completed_at = _now()
            row.error = error
            row.claim_owner = None
            row.claim_expires_at = None
            row.version += 1
            session.commit()
            return _task_from_row(row)

    def by_status(self, status: str, *, tenant_id: str | None = None) -> list[AgentTask]:
        self._assert_tenant(tenant_id or self._tenant_id)
        return self._query(OrchestratorTaskORM.status == status)

    def for_customer(
        self,
        customer_id: str,
        *,
        tenant_id: str | None = None,
    ) -> list[AgentTask]:
        self._assert_tenant(tenant_id or self._tenant_id)
        return self._query(OrchestratorTaskORM.customer_id == customer_id)

    def for_workflow(
        self,
        workflow_id: str,
        *,
        tenant_id: str | None = None,
    ) -> list[AgentTask]:
        self._assert_tenant(tenant_id or self._tenant_id)
        return self._query(OrchestratorTaskORM.parent_workflow_id == workflow_id)

    def get(self, task_id: str, *, tenant_id: str | None = None) -> AgentTask | None:
        self._assert_tenant(tenant_id or self._tenant_id)
        with self._sessionmaker() as session:
            row = session.scalar(
                select(OrchestratorTaskORM).where(
                    OrchestratorTaskORM.task_id == task_id,
                    OrchestratorTaskORM.tenant_id == self._tenant_id,
                )
            )
            return _task_from_row(row) if row is not None else None

    def summary(
        self,
        customer_id: str | None = None,
        *,
        tenant_id: str | None = None,
    ) -> dict[str, int]:
        self._assert_tenant(tenant_id or self._tenant_id)
        filters = [OrchestratorTaskORM.tenant_id == self._tenant_id]
        if customer_id:
            filters.append(OrchestratorTaskORM.customer_id == customer_id)
        with self._sessionmaker() as session:
            rows: Sequence[tuple[str, int]] = session.execute(
                select(OrchestratorTaskORM.status, func.count())
                .where(*filters)
                .group_by(OrchestratorTaskORM.status)
            ).all()
        out: dict[str, int] = dict.fromkeys(ALL_STATUSES, 0)
        out.update({status: int(count) for status, count in rows})
        return out

    def _query(self, *filters: Any) -> list[AgentTask]:
        with self._sessionmaker() as session:
            rows = session.scalars(
                select(OrchestratorTaskORM)
                .where(OrchestratorTaskORM.tenant_id == self._tenant_id, *filters)
                .order_by(OrchestratorTaskORM.created_at)
            ).all()
            return [_task_from_row(row) for row in rows]

    def _require(self, task_id: str) -> AgentTask:
        task = self.get(task_id, tenant_id=self._tenant_id)
        if task is None:
            raise KeyError(f"unknown task: {task_id}")
        return task

    def _assert_tenant(self, tenant_id: str) -> None:
        if tenant_id != self._tenant_id:
            raise ValueError("cross-tenant task access denied")


def create_postgres_orchestrator_stores(
    database_url: str,
    *,
    tenant_id: str,
    create_tables: bool = False,
) -> tuple[PostgresTaskQueue, PostgresWorkflowRunStore]:
    """Build tenant-bound stores from the application's async or sync URL."""
    engine = create_engine(
        sync_sqlalchemy_url(database_url),
        future=True,
        pool_pre_ping=True,
    )
    if create_tables:
        _Base.metadata.create_all(engine)
    return (
        PostgresTaskQueue(engine, tenant_id=tenant_id),
        PostgresWorkflowRunStore(engine, tenant_id=tenant_id),
    )


__all__ = [
    "ConcurrentWorkflowUpdate",
    "OrchestratorTaskORM",
    "PostgresTaskQueue",
    "PostgresWorkflowRunStore",
    "WorkflowRunORM",
    "create_postgres_orchestrator_stores",
]
